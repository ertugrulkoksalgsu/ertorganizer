import os
import shutil

EXTENSION_MAP = {
    'Resimler': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'Belgeler': ['.pdf', '.doc', '.docx', '.txt', '.md', '.xlsx', '.xls', '.ppt', '.pptx'],
    'Videolar': ['.mp4', '.mkv', '.avi', '.mov'],
    'Sesler': ['.mp3', '.wav', '.flac', '.aac'],
    'Arsivler': ['.zip', '.rar', '.tar', '.gz', '.7z']
}

def organize_folder(target_folder):
    if not os.path.isdir(target_folder):
        print(f"Hata: {target_folder} bir klasör değil veya bulunamadı.")
        return

    moved_count = 0
    
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        
        # Sadece dosyaları taşı (klasörleri atla)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Uzantının hangi kategoriye ait olduğunu bul
            category = "Diger"
            for cat, exts in EXTENSION_MAP.items():
                if file_ext in exts:
                    category = cat
                    break
                    
            # Kategori klasörünü oluştur
            category_path = os.path.join(target_folder, category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)
                
            # Dosyayı taşı
            new_file_path = os.path.join(category_path, filename)
            # Eğer aynı isimde dosya varsa üzerine yazmamak için basitçe atlıyoruz veya taşıyoruz
            if not os.path.exists(new_file_path):
                shutil.move(file_path, new_file_path)
                moved_count += 1
                print(f"Taşındı: {filename} -> {category}/")
            else:
                print(f"Atlandı (Zaten var): {filename}")
            
    print(f"Toplam {moved_count} dosya organize edildi.")
