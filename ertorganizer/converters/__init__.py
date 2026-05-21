import os

from .base import (
    Converter,
    ConversionResult,
    find_converter,
    register,
    supported_pairs,
)

# Register all built-in converters by importing the modules.
from . import image, markdown, pdf, office, spreadsheet  # noqa: F401,E402


def convert_file(input_path: str, output_path: str, *, skip_dep_check: bool = False) -> ConversionResult:
    if not os.path.isfile(input_path):
        msg = f"Hata: Girdi dosyası bulunamadı ({input_path})"
        return ConversionResult(False, msg)

    in_ext = os.path.splitext(input_path)[1].lower()
    out_ext = os.path.splitext(output_path)[1].lower()

    converter = find_converter(in_ext, out_ext)
    if converter is None:
        msg = (f"Desteklenmeyen dönüştürme: {in_ext} -> {out_ext}\n"
               "Desteklenen formatlar için: /formats")
        return ConversionResult(False, msg)

    if not skip_dep_check:
        from .. import system as _sys
        specs = converter.required_for(in_ext, out_ext)
        missing = _sys.check_missing(specs) if specs else []
        if missing:
            names = ", ".join(_sys.describe_spec(s) for s in missing)
            msg = f"Eksik bağımlılık(lar): {names}"
            return ConversionResult(False, msg, missing=missing)

    return converter.convert(input_path, output_path)


__all__ = [
    "Converter",
    "ConversionResult",
    "convert_file",
    "find_converter",
    "register",
    "supported_pairs",
]


__all__ = [
    "Converter",
    "ConversionResult",
    "convert_file",
    "find_converter",
    "register",
    "supported_pairs",
]
