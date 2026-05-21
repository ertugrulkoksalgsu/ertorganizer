import os

from .base import Converter, ConversionResult, register
from ._libreoffice import find_libreoffice, convert_via_libreoffice


_PANDOC_FORMATS = {
    '.html': 'html',
    '.md': 'markdown',
    '.rst': 'rst',
    '.tex': 'latex',
    '.epub': 'epub',
}


class OfficeConverter(Converter):
    """Word documents (.docx) ↔ PDF / HTML / Markdown / plain text."""
    name = "office"

    def supports(self, in_ext, out_ext):
        if in_ext == '.docx':
            return out_ext in {'.pdf', '.html', '.md', '.txt', '.rst'}
        if out_ext == '.docx':
            return in_ext in {'.md', '.html', '.rst', '.txt'}
        return False

    def convert(self, input_path, output_path):
        in_ext = os.path.splitext(input_path)[1].lower()
        out_ext = os.path.splitext(output_path)[1].lower()

        if in_ext == '.docx' and out_ext == '.pdf':
            return self._docx_to_pdf(input_path, output_path)
        if in_ext == '.docx' and out_ext == '.txt':
            return self._docx_to_text(input_path, output_path)
        # Everything else routed through pypandoc
        return self._via_pandoc(input_path, output_path, in_ext, out_ext)

    def _docx_to_pdf(self, input_path, output_path):
        # Try docx2pdf first (uses Word on macOS/Windows for best fidelity)
        try:
            from docx2pdf import convert as docx2pdf_convert
            try:
                docx2pdf_convert(input_path, output_path)
                if os.path.isfile(output_path):
                    return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
            except Exception as e:
                # Fall through to LibreOffice
                docx2pdf_error = str(e)
        except ImportError:
            docx2pdf_error = None

        ok, msg = convert_via_libreoffice(input_path, output_path, "pdf")
        if ok:
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)

        hint = ""
        if docx2pdf_error:
            hint = f"\ndocx2pdf denendi ama başarısız: {docx2pdf_error}"
        return ConversionResult(False, (
            f"DOCX→PDF için Microsoft Word (docx2pdf) veya LibreOffice gerekir.\n{msg}{hint}\n"
            "Alternatif olarak: pipx inject ertorganizer docx2pdf"
        ))

    def _docx_to_text(self, input_path, output_path):
        # python-docx (lightweight) — fallback to pypandoc if missing
        try:
            from docx import Document
        except ImportError:
            return self._via_pandoc(input_path, output_path, '.docx', '.txt')
        try:
            doc = Document(input_path)
            text = "\n".join(p.text for p in doc.paragraphs)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"DOCX→TXT hatası: {e}")

    def _via_pandoc(self, input_path, output_path, in_ext, out_ext):
        try:
            import pypandoc
        except ImportError:
            return ConversionResult(False, (
                "Eksik bağımlılık: pypandoc. Kurmak için:\n"
                "  pipx inject ertorganizer pypandoc\n"
                "Ayrıca pandoc binary gerekir:\n"
                "  macOS: brew install pandoc\n"
                "  Linux: sudo apt install pandoc"
            ))
        try:
            in_fmt = 'docx' if in_ext == '.docx' else _PANDOC_FORMATS.get(in_ext, in_ext.lstrip('.'))
            out_fmt = 'docx' if out_ext == '.docx' else _PANDOC_FORMATS.get(out_ext, out_ext.lstrip('.'))
            pypandoc.convert_file(
                input_path,
                out_fmt,
                format=in_fmt,
                outputfile=output_path,
                extra_args=['--standalone'] if out_ext in {'.html', '.tex', '.epub'} else [],
            )
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except OSError as e:
            if "pandoc" in str(e).lower():
                return ConversionResult(False, (
                    "pandoc binary bulunamadı.\n"
                    "macOS: brew install pandoc\n"
                    "Linux: sudo apt install pandoc"
                ))
            return ConversionResult(False, f"Pandoc dönüşüm hatası: {e}")
        except Exception as e:
            return ConversionResult(False, f"Pandoc dönüşüm hatası: {e}")

    def pairs(self):
        return [
            ('.docx', '.pdf'),
            ('.docx', '.html'),
            ('.docx', '.md'),
            ('.docx', '.txt'),
            ('.md', '.docx'),
            ('.html', '.docx'),
        ]

    def required_for(self, in_ext, out_ext):
        if in_ext == '.docx' and out_ext == '.pdf':
            return ['libreoffice|docx2pdf']
        if in_ext == '.docx' and out_ext == '.txt':
            return ['python-docx']
        # Diğer tüm yollar pypandoc + pandoc binary üzerinden gider.
        if (in_ext == '.docx' or out_ext == '.docx'):
            return ['pypandoc', 'pandoc']
        return []


register(OfficeConverter())
