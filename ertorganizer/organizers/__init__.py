from .base import (
    OrganizeResult,
    OrganizeStrategy,
    all_strategies,
    find_strategy,
    organize_folder,
    register,
)

# Stratejileri import ederek registry'ye kaydet.
from . import category, detailed, extension  # noqa: F401,E402

__all__ = [
    "OrganizeResult",
    "OrganizeStrategy",
    "all_strategies",
    "find_strategy",
    "organize_folder",
    "register",
]
