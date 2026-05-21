import os

from .base import Converter, ConversionResult, register

try:
    from PIL import Image
except ImportError:
    Image = None


IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.ico'}


class ImageConverter(Converter):
    name = "image"

    def supports(self, in_ext, out_ext):
        if in_ext not in IMAGE_EXTS:
            return False
        return out_ext in IMAGE_EXTS or out_ext == '.pdf'

    def convert(self, input_path, output_path):
        if Image is None:
            return ConversionResult(
                False,
                "Pillow kurulu değil. Kurmak için: pipx inject ertorganizer Pillow",
            )
        try:
            with Image.open(input_path) as img:
                target_lower = output_path.lower()
                if img.mode in ("RGBA", "P", "LA") and target_lower.endswith(('.jpg', '.jpeg', '.pdf', '.bmp')):
                    img = img.convert("RGB")
                if target_lower.endswith('.pdf'):
                    img.save(output_path, "PDF", resolution=100.0)
                else:
                    img.save(output_path)
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"Resim dönüştürme hatası: {e}")

    def pairs(self):
        out = []
        for i in IMAGE_EXTS:
            for o in IMAGE_EXTS:
                if i != o:
                    out.append((i, o))
            out.append((i, '.pdf'))
        return out


register(ImageConverter())
