# Dağıtım (Packaging)

ErtOrganizer iki ana paket yöneticisi üzerinden dağıtılır. Her ikisi de
GitHub Releases'taki standalone binary'leri kullanır.

| Platform | Kurulum komutu |
|----------|----------------|
| macOS | `brew install ertugrulkoksalgsu/ertorganizer/ertorganizer` |
| Windows | `winget install ErtugrulKoksal.ErtOrganizer` |

Binary'ler `v*` tag'i push'landığında `.github/workflows/release.yml`
tarafından otomatik derlenip Release'e eklenir.

## Homebrew (`homebrew/ertorganizer.rb`)

1. GitHub'da `homebrew-ertorganizer` adında bir repo oluştur (tap reposu).
2. `ertorganizer.rb` dosyasını o reponun `Formula/` klasörüne koy.
3. Formüldeki `PLACEHOLDER_*_SHA256` değerlerini Release'teki
   `SHA256SUMS.txt`'ten al ve doldur.
4. Kullanıcı `brew install ertugrulkoksalgsu/ertorganizer/ertorganizer`
   ile kurar; `poppler` ve `pandoc` otomatik gelir.

## winget (`winget/`)

3 dosyalı manifest, `microsoft/winget-pkgs` reposuna PR ile gönderilir:

1. `microsoft/winget-pkgs` reposunu fork'la.
2. Manifest dosyalarını
   `manifests/e/ErtugrulKoksal/ErtOrganizer/0.3.0/` altına kopyala.
3. `installer.yaml` içindeki `PLACEHOLDER_WINDOWS_SHA256` değerini doldur.
4. PR aç; Microsoft otomatik doğrulama + moderasyondan geçirir.

> **Not:** Windows binary'si imzalanmamıştır; ilk çalıştırmada Defender
> SmartScreen uyarı verebilir. Kod imzalama sertifikası ileride eklenebilir.
