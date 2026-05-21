import os

from .base import Converter, ConversionResult, register


class PDFConverter(Converter):
    name = "pdf"
    IMAGE_OUT = {'.png', '.jpg', '.jpeg'}
    TEXT_OUT = {'.txt'}
    DOC_OUT = {'.docx'}

    def supports(self, in_ext, out_ext):
        if in_ext != '.pdf':
            return False
        return (out_ext in self.IMAGE_OUT
                or out_ext in self.TEXT_OUT
                or out_ext in self.DOC_OUT)

    def convert(self, input_path, output_path):
        out_ext = os.path.splitext(output_path)[1].lower()
        if out_ext in self.IMAGE_OUT:
            return self._to_image(input_path, output_path, out_ext)
        if out_ext in self.TEXT_OUT:
            return self._to_text(input_path, output_path)
        if out_ext in self.DOC_OUT:
            return self._to_docx(input_path, output_path)
        return ConversionResult(False, f"Desteklenmeyen PDF hedefi: {out_ext}")

    def _to_image(self, input_path, output_path, out_ext):
        try:
            from pdf2image import convert_from_path
        except ImportError:
            return ConversionResult(False, (
                "Eksik bağımlılık: pdf2image. Kurmak için:\n"
                "  pipx inject ertorganizer pdf2image\n"
                "Ek olarak poppler sistem paketi gerekir:\n"
                "  macOS: brew install poppler\n"
                "  Linux: sudo apt install poppler-utils"
            ))
        try:
            fmt = "JPEG" if out_ext in {'.jpg', '.jpeg'} else "PNG"
            pages = convert_from_path(input_path, dpi=200, fmt=fmt.lower())
            if not pages:
                return ConversionResult(False, "PDF'te sayfa bulunamadı.")
            if len(pages) == 1:
                pages[0].save(output_path, fmt)
                return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
            base, ext = os.path.splitext(output_path)
            saved = []
            for i, page in enumerate(pages, start=1):
                target = f"{base}_page{i}{ext}"
                page.save(target, fmt)
                saved.append(target)
            return ConversionResult(
                True,
                f"{len(pages)} sayfa dönüştürüldü:\n  - " + "\n  - ".join(saved),
                saved[0],
            )
        except Exception as e:
            hint = ""
            if "poppler" in str(e).lower() or "Unable to get page count" in str(e):
                hint = "\nİpucu: poppler kurulu mu? macOS: brew install poppler"
            return ConversionResult(False, f"PDF→Resim hatası: {e}{hint}")

    def _to_text(self, input_path, output_path):
        try:
            from pypdf import PdfReader
        except ImportError:
            return ConversionResult(False, (
                "Eksik bağımlılık: pypdf. Kurmak için:\n"
                "  pipx inject ertorganizer pypdf"
            ))
        try:
            reader = PdfReader(input_path)
            chunks = []
            for i, page in enumerate(reader.pages, start=1):
                txt = page.extract_text() or ""
                chunks.append(f"--- Sayfa {i} ---\n{txt}".rstrip())
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n\n".join(chunks))
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"PDF→Metin hatası: {e}")

    def _to_docx(self, input_path, output_path):
        try:
            from pdf2docx import Converter as Pdf2DocxConv
        except ImportError:
            return ConversionResult(False, (
                "Eksik bağımlılık: pdf2docx. Kurmak için:\n"
                "  pipx inject ertorganizer pdf2docx"
            ))
        try:
            cv = Pdf2DocxConv(input_path)
            try:
                cv.convert(output_path, start=0, end=None)
            finally:
                cv.close()
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"PDF→DOCX hatası: {e}")

    def pairs(self):
        return [
            ('.pdf', '.png'),
            ('.pdf', '.jpg'),
            ('.pdf', '.jpeg'),
            ('.pdf', '.txt'),
            ('.pdf', '.docx'),
        ]

    def required_for(self, in_ext, out_ext):
        if in_ext != '.pdf':
            return []
        if out_ext in self.IMAGE_OUT:
            return ['pdf2image', 'poppler']
        if out_ext == '.txt':
            return ['pypdf']
        if out_ext == '.docx':
            return ['pdf2docx']
        return []


register(PDFConverter())
