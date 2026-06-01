"""Uzantı bazlı organize — her uzantı kendi klasörüne.

Her dosya, uzantısının büyük harfli adıyla bir klasöre gider (.pdf -> PDF/,
.png -> PNG/). Yalnızca mevcut dosyalar için klasör oluşur; uzantısız
dosyalar 'Diger' klasörüne gider. Az çeşitli, net ayrım isteyen kullanıcı
için idealdir.
"""
import os

from .base import OrganizeStrategy, register


@register
class ByExtension(OrganizeStrategy):
    key = "uzanti"
    label = "Uzantı"
    description = "Her uzantı kendi klasöründe (PDF/, PNG/, DOCX/ …); sadece dolu olanlar oluşur"

    def category_for(self, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return ext.upper() if ext else "Diger"
