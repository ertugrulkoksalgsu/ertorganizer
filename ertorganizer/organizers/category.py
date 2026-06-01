"""Kategori bazlı organize — varsayılan strateji.

Dosyaları 6 kaba kovaya ayırır (Resimler, Belgeler, Videolar, Sesler,
Arsivler, Kod). Tanınmayan uzantılar 'Diger' kovasına gider.
"""
import os

from .base import OrganizeStrategy, register

CATEGORY_MAP = {
    'Resimler': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.ico'],
    'Belgeler': ['.pdf', '.doc', '.docx', '.txt', '.md', '.xlsx', '.xls', '.ppt',
                 '.pptx', '.csv', '.json', '.html', '.rtf', '.odt'],
    'Videolar': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
    'Sesler': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Arsivler': ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2'],
    'Kod': ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.java',
            '.c', '.cpp', '.go', '.rs', '.rb', '.sh'],
}


@register
class ByCategory(OrganizeStrategy):
    key = "kategori"
    label = "Kategori"
    description = "Tür bazlı 6 kova: Resimler, Belgeler, Videolar, Sesler, Arsivler, Kod"

    def category_for(self, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        for category, exts in CATEGORY_MAP.items():
            if ext in exts:
                return category
        return "Diger"
