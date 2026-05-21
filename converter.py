import os
import markdown
try:
    from PIL import Image
except ImportError:
    print("Pillow kütüphanesi bulunamadı. Lütfen 'pip install Pillow' komutunu çalıştırın.")
    Image = None

def convert_image(input_path, output_path):
    if not Image:
        return False
        
    try:
        with Image.open(input_path) as img:
            # Sadece RGB'ye çevir eğer PNG/WEBP'den JPG'ye geçiyorsak ve alpha channel varsa
            if img.mode in ("RGBA", "P") and output_path.lower().endswith('.jpg'):
                img = img.convert("RGB")
            img.save(output_path)
            print(f"Başarıyla dönüştürüldü: {output_path}")
            return True
    except Exception as e:
        print(f"Resim dönüştürme hatası: {e}")
        return False

def convert_markdown(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        html = markdown.markdown(text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            full_html = f"<!DOCTYPE html>\\n<html>\\n<head>\\n<meta charset='utf-8'>\\n<title>Converted</title>\\n</head>\\n<body>\\n{html}\\n</body>\\n</html>"
            f.write(full_html)
            
        print(f"Başarıyla dönüştürüldü: {output_path}")
        return True
    except Exception as e:
        print(f"Markdown dönüştürme hatası: {e}")
        return False

def convert_file(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"Hata: Girdi dosyası bulunamadı ({input_path})")
        return

    in_ext = os.path.splitext(input_path)[1].lower()
    out_ext = os.path.splitext(output_path)[1].lower()

    image_exts = ['.jpg', '.jpeg', '.png', '.webp', '.bmp']
    
    if in_ext in image_exts and out_ext in image_exts:
        convert_image(input_path, output_path)
    elif in_ext == '.md' and out_ext == '.html':
        convert_markdown(input_path, output_path)
    else:
        print(f"Desteklenmeyen dönüştürme: {in_ext} -> {out_ext}")
        print("Desteklenenler: Resim formatları (jpg, png, webp) ve md -> html")
