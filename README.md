# ✨ ErtOrganizer CLI

ErtOrganizer, dosyalarınızı otomatik olarak türlerine göre klasörlere ayıran ve PDF, Word, Excel, görsel, markdown gibi pek çok formatı saniyeler içinde birbirine dönüştürmenizi sağlayan şık ve interaktif bir terminal aracıdır.

## 🌟 Neler Mümkün?

- **Akıllı Organizasyon (`/organize`)** — Karışık duran İndirilenler / Masaüstü klasörünü tek komutla **Resimler, Belgeler, Videolar, Sesler, Arsivler, Kod** gibi alt klasörlere ayırır.
- **80+ Format Dönüşümü (`/convert`)** — PDF ↔ Word, Word ↔ HTML/MD/PDF, Excel ↔ CSV/JSON/PDF, görsel ↔ görsel/PDF dönüşümleri tek komutla.
- **Etkileşimli REPL** — Modern tasarım, açılış animasyonu, klavyeden `/` ile açılan **akıllı otomatik tamamlama** menüsü.
- **Tek Komutla Kurulum** — `pipx install ertorganizer` yazıp her terminalde `ertorganizer` komutunu çalıştırabilirsiniz.

## 📦 Kurulum

### 🚀 Önerilen: `pipx` ile (her yerde çalışan global komut)

`pipx` Python araçlarını izole sanal ortamlarda kuran ve PATH'inize bağlayan bir araçtır.

```bash
# pipx kurulumu (bir kereliktir)
brew install pipx          # macOS
# veya:  python3 -m pip install --user pipx && python3 -m pipx ensurepath

# ErtOrganizer'ı kur
pipx install ertorganizer

# Tüm opsiyonel dönüştürücülerle birlikte:
pipx install "ertorganizer[all]"
```

Kurulum biter bitmez **her terminalde** sadece şunu yazmanız yeterli:

```bash
ertorganizer
```

### Alternatif: doğrudan `pip` ile

```bash
pip install --user ertorganizer
ertorganizer
```

### Geliştirici kurulumu (kaynaktan)

```bash
git clone https://github.com/ertugrulkoksalgsu/ertorganizer.git
cd ertorganizer
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[all,dev]"
ertorganizer
```

## 🧩 Opsiyonel Dönüştürücüler

Temel kurulum hafiftir. PDF / Word / Excel dönüşümleri için ek paketleri ihtiyacınıza göre seçebilirsiniz:

```bash
pipx install "ertorganizer[pdf]"     # PDF → image/text/docx
pipx install "ertorganizer[office]"  # DOCX ↔ PDF/HTML/MD
pipx install "ertorganizer[excel]"   # XLSX ↔ CSV/JSON/PDF
pipx install "ertorganizer[all]"     # Hepsi
```

Mevcut kuruluma ek özellik enjekte etmek isterseniz:

```bash
pipx inject ertorganizer pdf2image pypdf pdf2docx
```

Bazı dönüşümler **sistem binary'lerine** ihtiyaç duyar:

| Dönüşüm | Gereken Sistem Paketi | Kurulum |
|---|---|---|
| PDF → Resim | poppler | `brew install poppler` |
| DOCX → MD/HTML | pandoc | `brew install pandoc` |
| DOCX → PDF / XLSX → PDF | LibreOffice (veya MS Word) | `brew install --cask libreoffice` |

ErtOrganizer eksik bağımlılık tespit ettiğinde **otomatik olarak** sizi kurulum komutuna yönlendirir:

- `/doctor` — tüm bağımlılıkların güncel durumunu tablo halinde gösterir
- `/install libreoffice` — tek komutla doğru paket yöneticisini (brew/apt/dnf/winget) bularak kurar
- `/install all` — eksik olan her şeyi sırayla kurar
- Üstelik bir dönüşüm sırasında eksik bağımlılık varsa REPL **anında "Şimdi kurmak ister misin?"** diye sorar, onaylarsanız kurar ve dönüşümü **otomatik tekrar dener**.

## 🔄 Desteklenen Dönüşümler

| Kategori | Girdi | Hedefler |
|---|---|---|
| **Görsel** | `.png` `.jpg` `.jpeg` `.webp` `.bmp` `.gif` `.tiff` `.ico` | Birbirine + `.pdf` |
| **Markdown** | `.md` | `.html` `.docx` |
| **HTML** | `.html` | `.docx` |
| **Word** | `.docx` | `.pdf` `.html` `.md` `.txt` |
| **PDF** | `.pdf` | `.png` `.jpg` `.jpeg` `.txt` `.docx` |
| **Excel** | `.xlsx` | `.csv` `.json` `.pdf` |
| **CSV** | `.csv` | `.xlsx` |

> Tam liste için sistem içinde `/formats` komutunu kullanabilirsiniz — gerçek zamanlı olarak kayıtlı tüm dönüştürücüleri listeler.

## 🚀 Nasıl Kullanılır?

Terminalde `ertorganizer` yazın. Karşılama panelini gördükten sonra:

| Komut | Açıklama |
|---|---|
| `/organize [klasör]` | Belirtilen (veya mevcut) klasörü türlere göre organize eder |
| `/convert <girdi> <hedef>` | Format dönüşümü (örn: `/convert rapor.docx rapor.pdf`) |
| `/formats` | Desteklenen tüm dönüşümlerin canlı listesi |
| `/doctor` | Sistem & Python bağımlılıklarını tarar, eksikleri tablo halinde gösterir |
| `/install <ad>` | Eksik bağımlılığı **otomatik kurar** (örn: `/install libreoffice`) |
| `/install all` | Tüm eksik bağımlılıkları sırayla kurar |
| `/cd <klasör>` | Çalışma dizinini değiştir |
| `/pwd` | Mevcut dizini göster |
| `/version` | Sürüm bilgisi |
| `/help` | Yardım menüsü |
| `/exit` veya `/quit` | Çıkış |

İpucu: Komut menüsünü açmak için klavyede sadece **`/`** tuşuna basın — otomatik tamamlama önerileri açılır.

## 🧪 Hızlı Örnekler

```text
[Desktop] ❯ /convert sunum.docx sunum.pdf
🔄 Dönüştürülüyor...
Başarıyla dönüştürüldü: sunum.pdf

[Desktop] ❯ /convert satislar.xlsx satislar.json
Başarıyla dönüştürüldü: satislar.json

[Desktop] ❯ /convert e-fatura.pdf e-fatura.txt
Başarıyla dönüştürüldü: e-fatura.txt

[Desktop] ❯ /organize ~/Downloads
✨ Organizasyon işlemi başlatıldı: /Users/.../Downloads
Taşındı: rapor.pdf -> Belgeler/
Taşındı: logo.png -> Resimler/
Toplam 42 dosya organize edildi.
```

## 🏗️ Mimari

```
ertorganizer/
├── __init__.py          # __version__
├── __main__.py          # python -m ertorganizer
├── main.py              # REPL, komut yönlendirme
├── organizer.py         # /organize (uzantıdan kategoriye)
└── converters/
    ├── base.py          # Converter ABC + registry
    ├── __init__.py      # convert_file dispatcher
    ├── image.py         # Pillow tabanlı görsel + PDF
    ├── markdown.py      # md → html
    ├── pdf.py           # PDF → image/text/docx
    ├── office.py        # DOCX ↔ PDF/HTML/MD (docx2pdf + pypandoc + LibreOffice)
    ├── spreadsheet.py   # XLSX ↔ CSV/JSON/PDF (openpyxl + LibreOffice)
    └── _libreoffice.py  # `soffice --headless` yardımcısı
```

Yeni dönüştürücü eklemek için `Converter` sınıfından türetip `register(MyConverter())` çağırmak yeterli — dispatcher otomatik olarak fark eder.

---

**Geliştirici:** Ertuğrul Köksal · **Lisans:** MIT
