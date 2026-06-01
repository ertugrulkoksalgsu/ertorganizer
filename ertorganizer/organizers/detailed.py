"""Detaylı organize — iki seviyeli hiyerarşi.

Üst seviyede kategori bazlı ile aynıdır; ancak en kalabalık kova olan
'Belgeler' kendi içinde alt türlere ayrılır (Belgeler/PDF, Belgeler/Word,
Belgeler/Excel, Belgeler/Sunum, Belgeler/Metin). Böylece "her şey tek
Belgeler klasöründe yığılıyor" sorunu çözülür, üst seviye temiz kalır.
"""
import os

from .base import OrganizeStrategy, register
from .category import CATEGORY_MAP

# 'Belgeler' kovasının alt türlere kırılımı.
DOCUMENT_SUBMAP = {
    'PDF': ['.pdf'],
    'Word': ['.doc', '.docx', '.odt', '.rtf'],
    'Excel': ['.xls', '.xlsx', '.csv'],
    'Sunum': ['.ppt', '.pptx'],
    'Metin': ['.txt', '.md', '.json', '.html'],
}


@register
class ByDetailed(OrganizeStrategy):
    key = "detay"
    label = "Detaylı"
    description = "İki seviyeli: Belgeler kendi içinde PDF / Word / Excel / Sunum / Metin olarak ayrılır"

    def category_for(self, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        for category, exts in CATEGORY_MAP.items():
            if ext not in exts:
                continue
            if category == "Belgeler":
                for sub, sub_exts in DOCUMENT_SUBMAP.items():
                    if ext in sub_exts:
                        return f"Belgeler/{sub}"
                return "Belgeler/Diger"
            return category
        return "Diger"
