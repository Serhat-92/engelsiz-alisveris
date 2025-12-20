# Engelsiz Alışveriş Asistanı

Görme engelli bireyler için sesli asistan destekli alışveriş uygulaması.

## Proje Yapısı

- **backend/**: FastAPI (Python) ile yazılmış sunucu tarafı.
- **mobile/**: Flutter (Dart) ile yazılmış mobil uygulama.

## Kurulum

### Backend
`backend` klasörüne gidin ve `run_backend.bat` dosyasını çalıştırın.

### Mobile
`mobile` klasöründe `flutter run` komutunu kullanın.

## 📱 Uygulamayı Telefonda Açma (Ekstra)
Eğer uygulamayı bilgisayarınızdan yayınlayıp telefondan girmek isterseniz (En sağlıklı yöntem):
1. `mobile` klasöründe şu komutu çalıştırın (Tek seferlik derleme yapar):
   `flutter build web --release --web-renderer html`
2. Derleme bitince şu komutu çalıştırın (Sunucuyu başlatır):
   `cd build/web && python -m http.server 8080`
3. Yeni bir terminal açıp proje ana dizininde şu komutu yazın:
   `npx localtunnel --port 8080`
4. Size verilen linki (`https://....loca.lt`) telefondan açın.
