from .base import Converter, ConversionResult, register

try:
    import markdown as md_lib
except ImportError:
    md_lib = None


class MarkdownConverter(Converter):
    name = "markdown"

    def supports(self, in_ext, out_ext):
        return in_ext == '.md' and out_ext == '.html'

    def convert(self, input_path, output_path):
        if md_lib is None:
            return ConversionResult(
                False,
                "markdown kütüphanesi kurulu değil. Kurmak için: pipx inject ertorganizer markdown",
            )
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()
            html = md_lib.markdown(text, extensions=['fenced_code', 'tables', 'toc'])
            full_html = (
                "<!DOCTYPE html>\n<html>\n<head>\n"
                "<meta charset='utf-8'>\n"
                "<title>Converted</title>\n"
                "<style>body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.6}"
                "pre{background:#f5f5f5;padding:1rem;overflow:auto;border-radius:6px}"
                "code{background:#f5f5f5;padding:0.1rem 0.3rem;border-radius:3px}"
                "table{border-collapse:collapse}th,td{border:1px solid #ddd;padding:0.4rem 0.6rem}</style>"
                f"\n</head>\n<body>\n{html}\n</body>\n</html>"
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"Markdown dönüştürme hatası: {e}")

    def pairs(self):
        return [('.md', '.html')]


register(MarkdownConverter())
