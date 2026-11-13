
import sys
import re
from pathlib import Path

from PySide6.QtCore import QFile, QMimeData, QSettings, Qt, QUrl
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QFont,
    QKeySequence,
    QShortcut
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QMenu,
    QInputDialog,
    QVBoxLayout,
    QFormLayout,
    QDialog,
    QDialogButtonBox,
    QKeySequenceEdit,
    QListWidgetItem,
    QWidget
)

from ui_form import Ui_MainWindow
from image_viewer import ImageViewer
from caption_manager import CaptionManager

try:
    import jieba
except ImportError:
    jieba = None


IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp"
}


def count_prompt_words(text):
    if jieba is not None:
        return sum(
            1
            for token in jieba.cut(text)
            if any(character.isalnum() for character in token)
        )

    return len(re.findall(r"\w+", text, flags=re.UNICODE))


class ShortcutSettingsDialog(QDialog):
    def __init__(self, parent, language, shortcuts):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(self.tr_text("\u5feb\u6377\u952e", "Keyboard Shortcuts"))
        self.editors = {}
        self.labels = {
            "save": ("\u4fdd\u5b58\u6807\u6ce8", "Save Caption"),
            "import": ("\u5bfc\u5165\u56fe\u7247\u76ee\u5f55", "Import Image Folder"),
            "next": ("\u4e0b\u4e00\u5f20", "Next Image"),
            "previous": ("\u4e0a\u4e00\u5f20", "Previous Image"),
            "fit": ("\u9002\u5e94\u7a97\u53e3", "Fit to Window"),
            "copy": ("\u590d\u5236\u56fe\u7247", "Copy Image"),
        }
        layout = QVBoxLayout(self)
        form = QFormLayout()
        for key, (chinese, english) in self.labels.items():
            editor = QKeySequenceEdit(self)
            editor.setKeySequence(QKeySequence(shortcuts[key]))
            self.editors[key] = editor
            form.addRow(self.tr_text(chinese, english), editor)
        layout.addLayout(form)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setText(
            self.tr_text("\u786e\u5b9a", "OK")
        )
        self.buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(
            self.tr_text("\u53d6\u6d88", "Cancel")
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def tr_text(self, chinese, english):
        return chinese if self.language == "zh_CN" else english

    def sequences(self):
        return {key: editor.keySequence() for key, editor in self.editors.items()}

    def accept(self):
        owners = {}
        for key, sequence in self.sequences().items():
            normalized = sequence.toString(QKeySequence.SequenceFormat.PortableText)
            if not normalized:
                continue
            if normalized in owners:
                first_name = self.tr_text(*self.labels[owners[normalized]])
                second_name = self.tr_text(*self.labels[key])
                QMessageBox.warning(
                    self,
                    self.tr_text("\u5feb\u6377\u952e\u51b2\u7a81", "Shortcut Conflict"),
                    self.tr_text(
                        f"{first_name} \u4e0e {second_name} \u4f7f\u7528\u4e86\u76f8\u540c\u5feb\u6377\u952e\u3002",
                        f"{first_name} and {second_name} use the same shortcut."
                    ),
                )
                return
            owners[normalized] = key
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.images = []
        self.current_index = -1
        self.dirty = False
        self.prompt_directory = None

        self.setup_viewer()
        self.setup_ui_font_setting()
        self.setup_language_setting()
        self.setup_prompt_font_controls()
        self.setup_signals()
        self.setup_shortcuts()

        self.ui.mainSplitter.setSizes(
            [260, 800, 340]
        )
        self.update_caption_status()

    def setup_viewer(self):
        self.viewer = ImageViewer(
            self.ui.viewerContainer
        )

        layout = QVBoxLayout(
            self.ui.viewerContainer
        )
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewer)

    def setup_ui_font_setting(self):
        default_size = self.font().pointSizeF()
        if default_size <= 0:
            default_size = 10
        default_size = max(8, min(48, round(default_size)))

        self.ui_font_settings = QSettings(
            "Textoimage",
            "ImageCaptionStudio"
        )
        stored_size = self.ui_font_settings.value(
            "uiFontSize",
            default_size
        )
        try:
            initial_size = int(stored_size)
        except (TypeError, ValueError):
            initial_size = default_size
        initial_size = max(8, min(48, initial_size))

        self.apply_ui_font_size(initial_size)
        self.ui.actionUiFontSize.triggered.connect(
            self.open_ui_font_size_dialog
        )
        self.ui.actionShortcutSettings.triggered.connect(
            self.open_shortcut_settings
        )

    def setup_language_setting(self):
        self.language_settings = QSettings("Textoimage", "ImageCaptionStudio")
        language = self.language_settings.value("language", "zh_CN")
        self.language = language if language in ("zh_CN", "en") else "zh_CN"
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)
        self.language_actions = {}
        for code, label in (("zh_CN", "简体中文"), ("en", "English")):
            action = QAction(label, self)
            action.setCheckable(True)
            action.setChecked(code == self.language)
            self.language_group.addAction(action)
            self.ui.menuLanguage.addAction(action)
            self.language_actions[code] = action
            action.triggered.connect(lambda checked=False, value=code: self.set_language(value))
        self.apply_language()

    def set_language(self, language):
        if language not in ("zh_CN", "en") or language == self.language:
            return
        self.language = language
        self.language_settings.setValue("language", language)
        self.apply_language()

    def tr_text(self, chinese, english):
        return chinese if self.language == "zh_CN" else english

    def apply_language(self):
        en = self.language == "en"
        self.setWindowTitle("Image Caption Studio v1.0")
        self.ui.menuSettings.setTitle(self.tr_text("设置", "Settings"))
        self.ui.menuLanguage.setTitle(self.tr_text("语言", "Language"))
        self.ui.actionUiFontSize.setText(self.tr_text("界面字号…", "UI Font Size…"))
        self.ui.actionShortcutSettings.setText(self.tr_text("快捷键…", "Keyboard Shortcuts…"))
        labels = [
            (self.ui.btnImport, "导入图片目录", "Import Image Folder"),
            (self.ui.btnImportPrompt, "导入Prompt目录", "Import Prompt Folder"),
            (self.ui.btnPrevious, "上一张", "Previous"),
            (self.ui.btnNext, "下一张", "Next"),
            (self.ui.btnZoomIn, "放大", "Zoom In"),
            (self.ui.btnZoomOut, "缩小", "Zoom Out"),
            (self.ui.btnFit, "适应窗口", "Fit to Window"),
            (self.ui.btnSave, "保存 Prompt", "Save Prompt"),
            (self.ui.labelImages, "图片列表", "Images"),
            (self.ui.labelPreview, "图片预览", "Image Preview"),
            (self.ui.labelPrompt, "Prompt 标注", "Prompt Caption"),
            (self.ui.labelPromptFontSize, "字号：", "Font Size:"),
        ]
        for widget, chinese, english in labels:
            widget.setText(self.tr_text(chinese, english))
        self.ui.captionEditor.setPlaceholderText(self.tr_text("请输入图片的文本描述…", "Enter an image description…"))
        self.ui.spinPromptFontSize.setSuffix(" pt")
        if self.current_index < 0:
            self.ui.labelImageInfo.setText(self.tr_text("尚未加载图片", "No image loaded"))
        self.refresh_status()
        self.update_caption_status()

    def apply_ui_font_size(self, size):
        editor = self.ui.captionEditor
        prompt_font = QFont(editor.font())
        prompt_document_font = QFont(
            editor.document().defaultFont()
        )

        window_font = QFont(self.font())
        window_font.setPointSize(size)
        self.setFont(window_font)

        for widget in self.findChildren(QWidget):
            if widget is editor or editor.isAncestorOf(widget):
                continue

            font = QFont(widget.font())
            font.setPointSize(size)
            widget.setFont(font)

        editor.setFont(prompt_font)
        editor.document().setDefaultFont(prompt_document_font)
        self.ui_font_size = size

    def setup_prompt_font_controls(self):
        default_size = self.ui.captionEditor.font().pointSizeF()
        if default_size <= 0:
            default_size = 10
        default_size = max(8, min(48, round(default_size)))

        self.prompt_font_settings = QSettings(
            "Textoimage",
            "ImageCaptionStudio"
        )
        stored_size = self.prompt_font_settings.value(
            "promptFontSize",
            default_size
        )
        try:
            initial_size = int(stored_size)
        except (TypeError, ValueError):
            initial_size = default_size
        initial_size = max(8, min(48, initial_size))

        self.ui.spinPromptFontSize.setValue(initial_size)
        self.apply_prompt_font_size(initial_size)
        self.ui.spinPromptFontSize.valueChanged.connect(
            self.on_prompt_font_size_changed
        )

    def apply_prompt_font_size(self, size):
        editor = self.ui.captionEditor
        font = QFont(editor.font())
        font.setPointSize(size)

        signals_were_blocked = editor.blockSignals(True)
        try:
            editor.setFont(font)
            editor.document().setDefaultFont(font)
        finally:
            editor.blockSignals(signals_were_blocked)
        self.prompt_font_size = size

    def on_prompt_font_size_changed(self, size):
        self.apply_prompt_font_size(size)
        self.prompt_font_settings.setValue(
            "promptFontSize",
            size
        )

    def open_ui_font_size_dialog(self):
        size, accepted = QInputDialog.getInt(
            self,
            self.tr_text("界面字体设置", "UI Font Size"),
            self.tr_text("界面字号（pt）：", "UI font size (pt):"),
            self.ui_font_size,
            8,
            48,
            1
        )
        if not accepted:
            return

        self.apply_ui_font_size(size)
        self.ui_font_settings.setValue(
            "uiFontSize",
            size
        )

    def setup_signals(self):
        self.ui.btnImport.clicked.connect(
            self.import_folder
        )

        self.ui.btnImportPrompt.clicked.connect(
            self.import_prompt_folder
        )

        self.ui.btnPrevious.clicked.connect(
            self.previous_image
        )

        self.ui.btnNext.clicked.connect(
            self.next_image
        )

        self.ui.btnSave.clicked.connect(
            self.save_caption
        )

        self.ui.btnZoomIn.clicked.connect(
            self.viewer.zoom_in
        )

        self.ui.btnZoomOut.clicked.connect(
            self.viewer.zoom_out
        )

        self.ui.btnFit.clicked.connect(
            self.viewer.fit_image
        )

        self.ui.imageList.currentRowChanged.connect(
            self.on_image_selected
        )
        self.ui.imageList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.imageList.customContextMenuRequested.connect(
            self.show_image_context_menu
        )

        self.viewer.imageContextMenuRequested.connect(
            self.show_preview_context_menu
        )

        self.ui.captionEditor.textChanged.connect(
            self.on_caption_changed
        )

    def setup_shortcuts(self):
        self.shortcut_defaults = {
            "save": "Ctrl+S",
            "import": "Ctrl+O",
            "next": "Ctrl+Right",
            "previous": "Ctrl+Left",
            "fit": "Ctrl+0",
            "copy": QKeySequence(QKeySequence.StandardKey.Copy).toString(
                QKeySequence.SequenceFormat.PortableText
            ),
        }
        self.shortcut_callbacks = {
            "save": self.save_caption,
            "import": self.import_folder,
            "next": self.next_image,
            "previous": self.previous_image,
            "fit": self.viewer.fit_image,
            "copy": self.copy_current_image,
        }
        self.shortcut_settings = QSettings("Textoimage", "ImageCaptionStudio")
        self.shortcuts = {}
        for key, default in self.shortcut_defaults.items():
            stored = self.shortcut_settings.value(f"shortcuts/{key}", default)
            sequence = QKeySequence(str(stored))
            parent = self.ui.imageList if key == "copy" else self
            shortcut = QShortcut(sequence, parent)
            if key == "copy":
                shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            shortcut.activated.connect(self.shortcut_callbacks[key])
            self.shortcuts[key] = shortcut

    def open_shortcut_settings(self):
        current = {
            key: shortcut.key().toString(QKeySequence.SequenceFormat.PortableText)
            for key, shortcut in self.shortcuts.items()
        }
        dialog = ShortcutSettingsDialog(self, self.language, current)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        for key, sequence in dialog.sequences().items():
            self.shortcuts[key].setKey(sequence)
            self.shortcut_settings.setValue(
                f"shortcuts/{key}",
                sequence.toString(QKeySequence.SequenceFormat.PortableText),
            )

    def show_image_context_menu(self, position):
        item = self.ui.imageList.itemAt(position)
        if item is None:
            return

        index = self.ui.imageList.row(item)
        if index < 0 or index >= len(self.images):
            return

        menu = QMenu(self.ui.imageList)
        copy_action = menu.addAction("复制")
        copy_action.triggered.connect(
            lambda: self.copy_image(index)
        )
        menu.addSeparator()
        delete_action = menu.addAction("删除图片")
        delete_action.triggered.connect(
            lambda: self.delete_image(index)
        )
        menu.exec(
            self.ui.imageList.mapToGlobal(position)
        )

    def show_preview_context_menu(self, global_position):
        if not self.viewer.has_image:
            return

        index = self.current_index
        if index < 0 or index >= len(self.images):
            return

        viewport_position = self.viewer.viewport().mapFromGlobal(
            global_position
        )
        if self.viewer.itemAt(viewport_position) is None:
            return

        menu = QMenu(self.viewer)
        copy_action = menu.addAction("复制")
        copy_action.triggered.connect(
            lambda: self.copy_image(index)
        )
        menu.addSeparator()
        delete_action = menu.addAction("删除图片")
        delete_action.triggered.connect(
            lambda: self.delete_image(index)
        )
        menu.exec(global_position)

    def copy_current_image(self):
        self.copy_image(self.ui.imageList.currentRow())

    def copy_image(self, index):
        if index < 0 or index >= len(self.images):
            return

        mime_data = QMimeData()
        mime_data.setUrls([
            QUrl.fromLocalFile(str(self.images[index]))
        ])
        QApplication.clipboard().setMimeData(mime_data)
        self.statusBar().showMessage("已复制图片文件", 3000)

    def delete_image(self, index):
        if index < 0 or index >= len(self.images):
            return

        image_path = self.images[index]
        deleting_current = index == self.current_index

        if deleting_current and not self.save_if_needed():
            return

        if not QFile.moveToTrash(str(image_path)):
            QMessageBox.warning(
                self,
                "删除失败",
                f"无法将图片移入回收站：\n{image_path}"
            )
            return

        caption_path = CaptionManager.get_caption_path(
            image_path,
            self.prompt_directory
        )
        caption_move_failed = (
            caption_path.is_file()
            and not QFile.moveToTrash(str(caption_path))
        )

        self.images.pop(index)

        image_list = self.ui.imageList
        image_list.blockSignals(True)
        image_list.takeItem(index)

        if not self.images:
            image_list.setCurrentRow(-1)
            self.current_index = -1
            self.dirty = False
        elif deleting_current:
            next_index = min(index, len(self.images) - 1)
            image_list.setCurrentRow(next_index)
        else:
            if index < self.current_index:
                self.current_index -= 1
            image_list.setCurrentRow(self.current_index)

        image_list.blockSignals(False)

        if not self.images:
            self.viewer.clear_image()
            self.ui.captionEditor.blockSignals(True)
            self.ui.captionEditor.clear()
            self.ui.captionEditor.blockSignals(False)
            self.ui.labelImageInfo.setText("目录中没有图片")
        elif deleting_current:
            self.load_image(image_list.currentRow())
        elif self.current_index >= 0:
            self.ui.labelImageInfo.setText(
                f"{self.images[self.current_index].name} "
                f"({self.current_index + 1}/{len(self.images)})"
            )
        else:
            self.ui.labelImageInfo.setText("未选择图片")

        self.update_caption_status()
        self.refresh_status()

        if caption_move_failed:
            QMessageBox.warning(
                self,
                "标注文件未删除",
                f"图片已移入回收站，但标注文件无法移入回收站：\n"
                f"{caption_path}"
            )
        else:
            self.statusBar().showMessage(
                "图片已移入回收站", 3000
            )

    def import_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择图片目录"
        )

        if not folder:
            return

        if not self.save_if_needed():
            return

        directory = Path(folder)

        self.images = sorted(
            [
                path
                for path in directory.iterdir()
                if path.is_file()
                and path.suffix.lower()
                in IMAGE_EXTENSIONS
            ],
            key=lambda p: p.name.lower()
        )

        self.current_index = -1
        self.dirty = False

        self.ui.imageList.blockSignals(True)
        self.ui.imageList.clear()

        for image_path in self.images:
            item = QListWidgetItem(
                image_path.name
            )
            self.ui.imageList.addItem(item)

        self.ui.imageList.blockSignals(False)

        if self.images:
            self.ui.imageList.setCurrentRow(0)
        else:
            self.viewer.clear_image()
            self.ui.captionEditor.blockSignals(True)
            self.ui.captionEditor.clear()
            self.ui.captionEditor.blockSignals(False)
            self.ui.labelImageInfo.setText(
                "目录中没有图片"
            )
            self.update_caption_status()

        self.refresh_status()

    def import_prompt_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择Prompt目录"
        )

        if not folder:
            return

        if not self.save_if_needed():
            return

        self.prompt_directory = Path(folder)
        if self.current_index >= 0:
            self.load_image(self.current_index)
        else:
            self.ui.captionEditor.blockSignals(True)
            self.ui.captionEditor.clear()
            self.ui.captionEditor.blockSignals(False)
            self.update_caption_status()

        self.refresh_status()

    def on_image_selected(self, index):
        if index < 0 or index >= len(self.images):
            return

        if index == self.current_index:
            return

        if not self.save_if_needed():
            self.ui.imageList.blockSignals(True)
            self.ui.imageList.setCurrentRow(
                self.current_index
            )
            self.ui.imageList.blockSignals(False)
            return

        self.load_image(index)

    def load_image(self, index):
        self.current_index = index
        image_path = self.images[index]

        success = self.viewer.load_image(
            image_path
        )

        if not success:
            QMessageBox.warning(
                self,
                "图片错误",
                f"无法加载图片：\n{image_path}"
            )

        try:
            caption = CaptionManager.read_caption(
                image_path,
                self.prompt_directory
            )
        except OSError as error:
            QMessageBox.warning(
                self,
                "读取错误",
                str(error)
            )
            caption = ""

        self.ui.captionEditor.blockSignals(True)
        self.ui.captionEditor.setPlainText(
            caption
        )
        self.ui.captionEditor.blockSignals(False)

        self.dirty = False

        self.ui.labelImageInfo.setText(
            f"{image_path.name} "
            f"({index + 1}/{len(self.images)})"
        )

        self.update_caption_status()

    def on_caption_changed(self):
        if self.current_index >= 0:
            self.dirty = True
        self.update_caption_status()

    def update_caption_status(self):
        word_count = count_prompt_words(
            self.ui.captionEditor.toPlainText()
        )

        if self.current_index < 0:
            status_text = self.tr_text("未选择图片", "No image selected")
            self.ui.labelCaptionStatus.setText(
                f"{status_text} · {self.tr_text('词数', 'Words')}: {word_count}"
            )
            return

        if self.dirty:
            status_text = self.tr_text("● 未保存", "● Unsaved")
        else:
            image_path = self.images[
                self.current_index
            ]

            try:
                annotated = CaptionManager.is_annotated(
                    image_path,
                    self.prompt_directory
                )
                status_text = (
                    self.tr_text("✓ 已标注", "✓ Annotated")
                    if annotated
                    else self.tr_text("○ 未标注", "○ Not annotated")
                )
            except OSError:
                status_text = self.tr_text("读取标注状态失败", "Failed to read annotation status")

        self.ui.labelCaptionStatus.setText(
            f"{status_text} · {self.tr_text('词数', 'Words')}: {word_count}"
        )

    def save_caption(self):
        if self.current_index < 0:
            return False

        image_path = self.images[
            self.current_index
        ]

        caption = self.ui.captionEditor.toPlainText()

        try:
            CaptionManager.save_caption(
                image_path,
                caption,
                self.prompt_directory
            )
        except OSError as error:
            QMessageBox.critical(
                self,
                "保存失败",
                str(error)
            )
            return False

        self.dirty = False

        self.update_caption_status()
        self.refresh_status()

        self.statusBar().showMessage(
            self.tr_text("\u6807\u6ce8\u5df2\u4fdd\u5b58", "Annotation saved"),
            3000
        )

        return True

    def save_if_needed(self):
        if not self.dirty:
            return True

        return self.save_caption()

    def previous_image(self):
        if self.current_index > 0:
            self.ui.imageList.setCurrentRow(
                self.current_index - 1
            )

    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.ui.imageList.setCurrentRow(
                self.current_index + 1
            )

    def refresh_status(self):
        annotated_count = 0

        for index, image_path in enumerate(
            self.images
        ):
            try:
                annotated = CaptionManager.is_annotated(
                    image_path,
                    self.prompt_directory
                )
            except OSError:
                annotated = False

            if annotated:
                annotated_count += 1

            item = self.ui.imageList.item(index)

            if item:
                prefix = (
                    "✓ " if annotated else "○ "
                )
                item.setText(
                    prefix + image_path.name
                )

        self.ui.labelStats.setText(self.tr_text(
            f"已标注：{annotated_count} / {len(self.images)}",
            f"Annotated: {annotated_count} / {len(self.images)}"
        ))

    def closeEvent(self, event):
        if self.save_if_needed():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
