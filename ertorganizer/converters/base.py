from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, List, Optional


@dataclass
class ConversionResult:
    success: bool
    message: str
    output_path: Optional[str] = None
    missing: List[str] = field(default_factory=list)


class Converter(ABC):
    name: str = "converter"

    @abstractmethod
    def supports(self, in_ext: str, out_ext: str) -> bool: ...

    @abstractmethod
    def convert(self, input_path: str, output_path: str) -> ConversionResult: ...

    def pairs(self) -> Iterable[tuple]:
        """Optional: (in_ext, out_ext) pairs for help/docs output."""
        return ()

    def required_for(self, in_ext: str, out_ext: str) -> List[str]:
        """Bu dönüşüm için gerekli `Requirement` anahtarları.

        Alternatif kabul eden gereksinimler için 'a|b' biçimi kullanılabilir
        (en az biri yeterlidir).
        """
        return []


_REGISTRY: list = []


def register(converter: Converter) -> Converter:
    _REGISTRY.append(converter)
    return converter


def find_converter(in_ext: str, out_ext: str) -> Optional[Converter]:
    for c in _REGISTRY:
        if c.supports(in_ext, out_ext):
            return c
    return None


def supported_pairs() -> list:
    """Return list of (in_ext, out_ext, converter_name) for documentation."""
    return [(i, o, c.name) for c in _REGISTRY for i, o in c.pairs()]
