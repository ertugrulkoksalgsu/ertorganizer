import os
import shutil
import subprocess
import tempfile
from typing import Optional


_LIBREOFFICE_CANDIDATES = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice",
    "/usr/local/bin/soffice",
    "/opt/homebrew/bin/soffice",
]


def find_libreoffice() -> Optional[str]:
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    for path in _LIBREOFFICE_CANDIDATES:
        if os.path.isfile(path):
            return path
    return None


def convert_via_libreoffice(input_path: str, output_path: str, target_format: str):
    """
    target_format examples: 'pdf', 'docx', 'html', 'txt', 'csv', 'xlsx'.
    Returns (success: bool, message: str).
    """
    binary = find_libreoffice()
    if not binary:
        return False, (
            "LibreOffice bulunamadı. Bu dönüşüm LibreOffice gerektirir.\n"
            "macOS:   brew install --cask libreoffice\n"
            "Linux:   sudo apt install libreoffice  (veya dnf/pacman)\n"
            "Windows: https://www.libreoffice.org/download/"
        )

    out_dir = tempfile.mkdtemp(prefix="ertorganizer-lo-")
    try:
        result = subprocess.run(
            [binary, "--headless", "--convert-to", target_format,
             "--outdir", out_dir, input_path],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode != 0:
            stderr = (result.stderr or result.stdout or "").strip()[:300]
            return False, f"LibreOffice hata kodu {result.returncode}: {stderr}"

        base = os.path.splitext(os.path.basename(input_path))[0]
        produced = os.path.join(out_dir, f"{base}.{target_format}")
        if not os.path.isfile(produced):
            return False, f"LibreOffice çıktı dosyası bulunamadı: {produced}"

        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        shutil.move(produced, output_path)
        return True, "OK"
    except subprocess.TimeoutExpired:
        return False, "LibreOffice dönüşümü zaman aşımına uğradı (180s)."
    except Exception as e:
        return False, f"LibreOffice çalıştırılırken hata: {e}"
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)
