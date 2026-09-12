import json
import os
import datetime
import google.generativeai as genai

# Gemini API Anahtarını al
api_key = os.environ.get("GEMINI_API_KEY")

today_str = datetime.datetime.now().strftime("%d.%m.%Y")

# Eğer API key tanımlı değilse güvenli varsayılan değer yaz
if not api_key:
    print("API Anahtarı bulunamadı, varsayılan kaydediliyor.")
    data = {
        "cevap": "Hayır",
        "aciklama": "Henüz resmi bir açıklama veya anlaşma bulunmamaktadır.",
        "tarih": today_str
    }
else:
    try:
        genai.configure(api_key=api_key)
        # Güncel verilere erişim imkanı olan model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Bugünün tarihi: " + today_str + ". "
            "Son spor haberlerini tara ve İsmail Kartal'ın Fenerbahçe'ye veya başka bir kulübe "
            "teknik direktör olarak geri dönüp dönmediğini kontrol et. "
            "Sadece şu JSON formatında cevap ver, başka hiçbir ekstra yazı ekleme:\n"
            '{"cevap": "Evet" veya "Hayır", "aciklama": "Kısa 1 cümle açıklama"}'
        )
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # JSON temizleme
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        res_json = json.loads(text)
        data = {
            "cevap": res_json.get("cevap", "Hayır"),
            "aciklama": res_json.get("aciklama", "Henüz yeni bir imza atılmadı, beklemedeyiz."),
            "tarih": today_str
        }
    except Exception as e:
        print(f"Hata oluştu: {e}")
        data = {
            "cevap": "Hayır",
            "aciklama": "Haber kontrolü yapılırken bir güncelleme alınamadı.",
            "tarih": today_str
        }

# data.json dosyasını güncelle
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("data.json başarıyla güncellendi!")
