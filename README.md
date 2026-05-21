# ✨ ErtOrganizer CLI

ErtOrganizer, dosyalarınızı otomatik olarak türlerine göre klasörlere ayıran ve saniyeler içinde farklı formatlara dönüştürmenizi sağlayan şık, modern ve etkileşimli bir terminal aracıdır.

![ErtOrganizer Ekran Görüntüsü](https://i.imgur.com/K3L2rVq.png) *(Temsili Görsel)*

## 🌟 Neler Mümkün?
- **Akıllı Organizasyon (`/organize`)**: Dağınık duran İndirilenler, Masaüstü veya herhangi bir klasördeki dosyaları tek bir komutla türlerine (Resimler, Videolar, Belgeler, Sesler, Arşivler vb.) göre düzenli alt klasörlere yerleştirir.
- **Hızlı Dönüştürme (`/convert`)**: Dosya formatlarını ek bir program kurmanıza gerek kalmadan terminal üzerinden anında birbirine dönüştürür.
- **Etkileşimli Arayüz (REPL)**: Modern tasarımı, açılış animasyonu ve komutlar arası geçişte yardımcı olan **otomatik tamamlama (auto-complete)** desteğiyle premium bir kullanıcı deneyimi sunar.

## 🔄 Desteklenen Dönüşüm Formatları
Şu anda aşağıdaki dosya formatları arasında sorunsuz dönüşüm yapabilirsiniz:

| İşlem Türü | Kaynak Formatlar | Hedef Formatlar |
| :--- | :--- | :--- |
| **Görsel Dönüşümleri** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp` | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp` |
| **Belge Dönüşümleri** | `.md` (Markdown) | `.html` |

*(Not: Yakın zamanda PDF, Video ve Ses dönüştürme özellikleri de sisteme entegre edilecektir.)*

## 📥 İndirme ve Kurulum

Sistemi kullanmaya başlamak için aşağıdaki adımları sırasıyla uygulayın.

### 1. Projeyi Bilgisayarınıza İndirin
Terminalinizi açın ve projeyi klonlayın:
```bash
git clone https://github.com/ertugrulkoksalgsu/ertorganizer.git
cd ertorganizer
```

### 2. Gerekli Kütüphaneleri Kurun
ErtOrganizer'ın arayüzü ve dönüştürme araçları için gereken Python kütüphanelerini yükleyin:
```bash
python3 -m pip install -r requirements.txt
```
*(Eğer bir yetki hatası alırsanız komutun sonuna `--user` ekleyebilirsiniz.)*

### 3. Global Kısayol Ekleyin (İsteğe Bağlı)
ErtOrganizer'ı herhangi bir klasörde sadece `ertorganizer` yazarak çalıştırabilmek için terminal profilinize (`~/.zshrc` veya `~/.bashrc`) kısayol ekleyin:
```bash
echo "alias ertorganizer='python3 \"$(pwd)/main.py\"'" >> ~/.zshrc
source ~/.zshrc
```

## 🚀 Nasıl Kullanılır?

Terminali açın ve `ertorganizer` yazarak sisteme giriş yapın.

Karşılama ekranını gördükten sonra kullanabileceğiniz yetenekleri (skilleri) listelemek için klavyeden **`/`** tuşuna basmanız yeterlidir.

- `/organize`: Bulunduğunuz dizindeki dosyaları organize eder.
- `/convert <kaynak_dosya> <hedef_dosya>`: Dosya formatını dönüştürür. (Örn: `/convert logo.png logo.jpg`)
- `/pwd`: Mevcut konumu gösterir.
- `/cd <hedef_klasör>`: Terminalden çıkmadan işlem yapılan klasörü değiştirir.
- `/help`: Tüm komut detaylarını görüntüler.
- `/exit`: Sistemden çıkış yapar.

---
**Geliştirici:** Ertuğrul Köksal
