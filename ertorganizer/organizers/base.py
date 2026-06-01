"""Organize stratejileri için ortak altyapı.

`converters` paketiyle simetrik tasarlandı: bir ABC (`OrganizeStrategy`),
bir registry (`register` / `find_strategy` / `all_strategies`) ve dosyaları
fiilen taşıyan paylaşılan bir döngü (`organize_folder`).

Stratejiler yalnızca "bu dosya hangi (göreli) klasöre gitmeli?" sorusunu
yanıtlar; tarama, klasör oluşturma ve taşıma mantığı tek yerde durur.
"""
import os
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class OrganizeResult:
    moved: int
    skipped: int
    strategy: str


class OrganizeStrategy(ABC):
    key: str = ""          # /organize --by <key>
    label: str = ""        # menüde gösterilen ad
    description: str = ""   # menüde gösterilen açıklama

    @abstractmethod
    def category_for(self, filename: str) -> str:
        """Dosyanın gideceği göreli klasör yolu.

        Çok seviyeli olabilir, örn. 'Belgeler/PDF'. os.path.join'e güvenli
        biçimde verilebilecek '/' ayraçlı bir yol döndürür.
        """
        ...


_REGISTRY: "dict[str, OrganizeStrategy]" = {}


def register(strategy):
    """Bir stratejiyi registry'ye kaydeder.

    Sınıf-decorator olarak (`@register`) ya da instance ile
    (`register(ByCategory())`) kullanılabilir; sınıf verilirse örneklenir.
    Sınıf-decorator kullanımında dönüş değeri sınıfın kendisidir.
    """
    instance = strategy() if isinstance(strategy, type) else strategy
    _REGISTRY[instance.key] = instance
    return strategy


def find_strategy(key: str) -> Optional[OrganizeStrategy]:
    return _REGISTRY.get(key)


def all_strategies() -> List[OrganizeStrategy]:
    return list(_REGISTRY.values())


def organize_folder(target_folder: str, strategy: Optional[OrganizeStrategy] = None,
                    *, verbose: bool = True) -> Optional[OrganizeResult]:
    """`target_folder` içindeki üst seviye dosyaları stratejiye göre taşır.

    Yalnızca üst seviyedeki dosyalara dokunur; alt klasörlerdeki dosyalar
    (önceki organize çıktıları dahil) olduğu gibi bırakılır.
    """
    if strategy is None:
        strategy = find_strategy("kategori")

    if not os.path.isdir(target_folder):
        if verbose:
            print(f"Hata: {target_folder} bir klasör değil veya bulunamadı.")
        return None

    moved = 0
    skipped = 0

    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        if not os.path.isfile(file_path):
            continue

        category = strategy.category_for(filename)
        category_path = os.path.join(target_folder, *category.split("/"))
        os.makedirs(category_path, exist_ok=True)

        new_file_path = os.path.join(category_path, filename)
        if os.path.exists(new_file_path):
            skipped += 1
            if verbose:
                print(f"Atlandı (Zaten var): {filename}")
            continue

        shutil.move(file_path, new_file_path)
        moved += 1
        if verbose:
            print(f"Taşındı: {filename} -> {category}/")

    if verbose:
        print(f"Toplam {moved} dosya organize edildi.")
    return OrganizeResult(moved=moved, skipped=skipped, strategy=strategy.key)
