
from pathlib import Path


class CaptionManager:
    @staticmethod
    def get_caption_path(image_path, prompt_directory=None):
        image_path = Path(image_path)
        if prompt_directory is not None:
            return Path(prompt_directory) / f"{image_path.stem}.txt"
        return image_path.with_suffix(".txt")

    @staticmethod
    def read_caption(image_path, prompt_directory=None):
        txt_path = CaptionManager.get_caption_path(
            image_path,
            prompt_directory
        )

        if not txt_path.exists():
            return ""

        return txt_path.read_text(
            encoding="utf-8-sig"
        )

    @staticmethod
    def save_caption(image_path, caption, prompt_directory=None):
        txt_path = CaptionManager.get_caption_path(
            image_path,
            prompt_directory
        )

        caption = caption.strip()

        if caption:
            txt_path.write_text(
                caption + "\n",
                encoding="utf-8"
            )
        elif txt_path.exists():
            txt_path.unlink()

        return txt_path

    @staticmethod
    def is_annotated(image_path, prompt_directory=None):
        caption = CaptionManager.read_caption(
            image_path,
            prompt_directory
        )

        return bool(caption.strip())
