"""Bağımlılık tespiti ve otomatik kurulum.

Hem Python paketleri (pipx inject / pip install) hem de sistem paketleri
(brew, apt-get, dnf, pacman, winget) için tek noktadan yönetim sağlar.
Konsept: her `Requirement` kendi tespit ve kurulum komutunu taşır;
`required_for(in_ext, out_ext)` çıktısı 'a|b' formatında alternatifler
içerebilir — en az biri yeterlidir.
"""
import importlib
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple


@dataclass
class Requirement:
    key: str
    display: str
    purpose: str
    kind: str  # 'system' veya 'python'
    detect: Callable[[], bool]
    install_cmd: Dict[str, str] = field(default_factory=dict)
    pipx_pkg: Optional[str] = None
    notes: str = ""


def os_kind() -> str:
    """Çalışılan platformu ve mevcut paket yöneticisini belirler."""
    s = platform.system()
    if s == 'Darwin':
        return 'mac'
    if s == 'Linux':
        if shutil.which('apt-get'):
            return 'linux-apt'
        if shutil.which('dnf'):
            return 'linux-dnf'
        if shutil.which('pacman'):
            return 'linux-pacman'
        return 'linux'
    if s == 'Windows':
        return 'win'
    return 'unknown'


def _detect_libreoffice():
    from .converters._libreoffice import find_libreoffice
    return find_libreoffice() is not None


def _detect_binary(name: str) -> Callable[[], bool]:
    return lambda: shutil.which(name) is not None


def _detect_python(import_name: str) -> Callable[[], bool]:
    def check():
        try:
            importlib.import_module(import_name)
            return True
        except ImportError:
            return False
    return check


REQUIREMENTS: List[Requirement] = [
    Requirement(
        key='libreoffice', display='LibreOffice',
        purpose='Word/Excel/PowerPoint → PDF dönüşümleri',
        kind='system', detect=_detect_libreoffice,
        install_cmd={
            'mac': 'brew install --cask libreoffice',
            'linux-apt': 'sudo apt-get install -y libreoffice',
            'linux-dnf': 'sudo dnf install -y libreoffice',
            'linux-pacman': 'sudo pacman -S --noconfirm libreoffice-fresh',
            'win': 'winget install -e --id TheDocumentFoundation.LibreOffice',
        },
        notes='~700 MB indirme; headless modda çalışır, pencere açılmaz.',
    ),
    Requirement(
        key='poppler', display='Poppler',
        purpose='PDF → Resim dönüşümü için',
        kind='system', detect=_detect_binary('pdftoppm'),
        install_cmd={
            'mac': 'brew install poppler',
            'linux-apt': 'sudo apt-get install -y poppler-utils',
            'linux-dnf': 'sudo dnf install -y poppler-utils',
            'linux-pacman': 'sudo pacman -S --noconfirm poppler',
            'win': 'choco install -y poppler',
        },
    ),
    Requirement(
        key='pandoc', display='Pandoc',
        purpose='Word ↔ Markdown/HTML/LaTeX dönüşümleri',
        kind='system', detect=_detect_binary('pandoc'),
        install_cmd={
            'mac': 'brew install pandoc',
            'linux-apt': 'sudo apt-get install -y pandoc',
            'linux-dnf': 'sudo dnf install -y pandoc',
            'linux-pacman': 'sudo pacman -S --noconfirm pandoc',
            'win': 'winget install -e --id JohnMacFarlane.Pandoc',
        },
    ),
    Requirement(
        key='pdf2image', display='pdf2image (Python)',
        purpose='PDF → PNG/JPG', kind='python',
        detect=_detect_python('pdf2image'), pipx_pkg='pdf2image',
        notes='Ayrıca Poppler sistem paketi gerekir.',
    ),
    Requirement(
        key='pypdf', display='pypdf (Python)',
        purpose='PDF → metin', kind='python',
        detect=_detect_python('pypdf'), pipx_pkg='pypdf',
    ),
    Requirement(
        key='pdf2docx', display='pdf2docx (Python)',
        purpose='PDF → Word', kind='python',
        detect=_detect_python('pdf2docx'), pipx_pkg='pdf2docx',
    ),
    Requirement(
        key='docx2pdf', display='docx2pdf (Python)',
        purpose='Word → PDF (MS Word ile)', kind='python',
        detect=_detect_python('docx2pdf'), pipx_pkg='docx2pdf',
        notes='MS Word kurulu olmalı; LibreOffice de aynı işi görür.',
    ),
    Requirement(
        key='pypandoc', display='pypandoc (Python)',
        purpose='Pandoc Python sarmalayıcısı', kind='python',
        detect=_detect_python('pypandoc'), pipx_pkg='pypandoc',
    ),
    Requirement(
        key='python-docx', display='python-docx (Python)',
        purpose='DOCX → düz metin', kind='python',
        detect=_detect_python('docx'), pipx_pkg='python-docx',
    ),
    Requirement(
        key='openpyxl', display='openpyxl (Python)',
        purpose='Excel I/O (CSV/JSON)', kind='python',
        detect=_detect_python('openpyxl'), pipx_pkg='openpyxl',
    ),
]


def find(key: str) -> Optional[Requirement]:
    for r in REQUIREMENTS:
        if r.key == key:
            return r
    return None


def status() -> List[Tuple[Requirement, bool]]:
    return [(r, r.detect()) for r in REQUIREMENTS]


def check_missing(specs: List[str]) -> List[str]:
    """Verilen gereksinim listesinden eksik olanları döndürür.

    `specs` içindeki öğe 'a|b|c' biçiminde olabilir; en az biri varsa
    o spec karşılanmış sayılır.
    """
    missing = []
    for spec in specs:
        alternatives = spec.split('|')
        satisfied = False
        for alt in alternatives:
            req = find(alt.strip())
            if req and req.detect():
                satisfied = True
                break
        if not satisfied:
            missing.append(spec)
    return missing


def describe_spec(spec: str) -> str:
    alts = [a.strip() for a in spec.split('|')]
    names = []
    for alt in alts:
        r = find(alt)
        names.append(r.display if r else alt)
    return " veya ".join(names)


def _is_pipx_install() -> bool:
    return '/pipx/venvs/' in sys.executable


def install_python_pkg(pkg: str) -> Tuple[bool, str]:
    """Python paketini pipx inject ile (mümkünse) veya pip ile kurar."""
    if _is_pipx_install() and shutil.which('pipx'):
        cmd = ['pipx', 'inject', 'ertorganizer', pkg]
    else:
        cmd = [sys.executable, '-m', 'pip', 'install', pkg]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            return True, f"{pkg} başarıyla kuruldu."
        err = (result.stderr or result.stdout or "")[-500:]
        return False, f"Kurulum başarısız (kod {result.returncode}): {err.strip()}"
    except subprocess.TimeoutExpired:
        return False, "Kurulum zaman aşımına uğradı (10 dakika)."
    except Exception as e:
        return False, f"Kurulum hatası: {e}"


def install_system_pkg(req: Requirement) -> Tuple[bool, str]:
    """Sistem paketini platforma uygun paket yöneticisiyle kurar."""
    os_k = os_kind()
    cmd = req.install_cmd.get(os_k)
    if not cmd:
        return False, (
            f"Bu platform için otomatik kurulum tanımlı değil ({os_k}). "
            f"Manuel kurulum gerekli: {req.display}"
        )
    parts = cmd.split()
    pm = parts[1] if parts[0] == 'sudo' else parts[0]
    if not shutil.which(pm):
        return False, (
            f"Paket yöneticisi '{pm}' sistemde yok. "
            f"Kurulum komutu: {cmd}"
        )
    print(f"→ Çalıştırılıyor: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, timeout=1800)
        if result.returncode == 0:
            return True, f"{req.display} başarıyla kuruldu."
        return False, f"Kurulum komutu {result.returncode} koduyla bitti."
    except subprocess.TimeoutExpired:
        return False, "Kurulum 30 dakikayı aştı, iptal edildi."
    except Exception as e:
        return False, f"Kurulum hatası: {e}"


def install_requirement(req: Requirement) -> Tuple[bool, str]:
    if req.kind == 'python':
        return install_python_pkg(req.pipx_pkg or req.key)
    return install_system_pkg(req)


def install_spec(spec: str, prefer_first: bool = True) -> Tuple[bool, str]:
    """'a|b' biçimindeki bir spec'i kurar. prefer_first=True ise ilk alternatifi seçer."""
    alts = [a.strip() for a in spec.split('|')]
    target_key = alts[0] if prefer_first else alts[-1]
    req = find(target_key)
    if not req:
        return False, f"Bilinmeyen bağımlılık: {target_key}"
    return install_requirement(req)
