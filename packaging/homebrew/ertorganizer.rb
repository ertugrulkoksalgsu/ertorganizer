class Ertorganizer < Formula
  desc "Akilli dosya organizasyonu ve format donusturme araci (terminal CLI)"
  homepage "https://github.com/ertugrulkoksalgsu/ertorganizer"
  version "0.3.0"
  license "MIT"

  # Yalnizca Apple Silicon (arm64). Intel Mac kullanicilari pipx ile kurar.
  depends_on arch: :arm64
  depends_on :macos

  url "https://github.com/ertugrulkoksalgsu/ertorganizer/releases/download/v0.3.0/ertorganizer-macos-arm64.tar.gz"
  sha256 "PLACEHOLDER_ARM64_SHA256"

  # Hafif sistem araclari otomatik kurulur. LibreOffice bilerek zorunlu
  # tutulmadi (~700 MB); Office->PDF gerektiginde ErtOrganizer kullaniciya
  # "brew install --cask libreoffice" onerir (graceful error).
  depends_on "poppler"
  depends_on "pandoc"

  def install
    bin.install "ertorganizer"
  end

  test do
    assert_match "ErtOrganizer", pipe_output("#{bin}/ertorganizer", "/exit\n")
  end
end
