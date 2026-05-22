"""PyInstaller giris betigi.

Paketlenmis binary'nin baslangic noktasi. `ertorganizer/__main__.py` relative
import kullandigi icin PyInstaller tarafindan dogrudan calistirilamiyor; bu
betik mutlak import ile main()'i cagirir.
"""

from ertorganizer.main import main

if __name__ == "__main__":
    main()
