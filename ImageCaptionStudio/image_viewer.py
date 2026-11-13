
from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem
)


class ImageViewer(QGraphicsView):
    imageContextMenuRequested = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene_obj = QGraphicsScene(self)
        self.setScene(self.scene_obj)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene_obj.addItem(self.pixmap_item)

        self.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform
        )

        self.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.has_image = False

    def load_image(self, path):
        pixmap = QPixmap(str(path))

        if pixmap.isNull():
            self.clear_image()
            return False

        self.pixmap_item.setPixmap(pixmap)
        self.scene_obj.setSceneRect(
            self.pixmap_item.boundingRect()
        )

        self.has_image = True
        self.fit_image()
        return True

    def clear_image(self):
        self.pixmap_item.setPixmap(QPixmap())
        self.scene_obj.setSceneRect(
            self.pixmap_item.boundingRect()
        )
        self.has_image = False

    def fit_image(self):
        if not self.has_image:
            return

        self.resetTransform()

        self.fitInView(
            self.pixmap_item,
            Qt.AspectRatioMode.KeepAspectRatio
        )

    def zoom_in(self):
        if self.has_image:
            self.scale(1.25, 1.25)

    def zoom_out(self):
        if self.has_image:
            self.scale(0.8, 0.8)

    def wheelEvent(self, event):
        if not self.has_image:
            return super().wheelEvent(event)

        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

        event.accept()

    def contextMenuEvent(self, event):
        viewport_position = self.viewport().mapFromGlobal(
            event.globalPos()
        )
        if (
            self.has_image
            and self.itemAt(viewport_position) is not None
        ):
            self.imageContextMenuRequested.emit(
                event.globalPos()
            )
            event.accept()
            return

        super().contextMenuEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
