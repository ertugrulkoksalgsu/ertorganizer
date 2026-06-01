"""Geriye dönük uyumluluk katmanı.

Organize mantığı `ertorganizer.organizers` paketine (strategy pattern) taşındı.
Bu modül eski import yolunu korur; yeni kod doğrudan `organizers`'tan içe
aktarmalıdır.
"""
from .organizers import (
    OrganizeResult,
    all_strategies,
    find_strategy,
    organize_folder,
)

__all__ = [
    "OrganizeResult",
    "all_strategies",
    "find_strategy",
    "organize_folder",
]
