
# Image Classifier with FastAPI

Bu proje, eğitilmiş bir resim sınıflandırma modelinin FastAPI web çerçevesi kullanılarak bir API üzerinden servis edilmesini sağlar. Sistem, POST metodu aracılığıyla gönderilen görselleri analiz ederek sınıflandırma sonuçlarını döndürür.

## Kurulum ve Çalıştırma

### 1. Bağımlılıkların Yüklenmesi
Gerekli kütüphaneleri yüklemek için aşağıdaki komutu çalıştırın:
`pip install -r requirements.txt`

### 2. Model Dosyalarının Hazırlanması
[Buradan indirebileceğiniz hazır modelleri](https://drive.google.com/drive/folders/1cnbq-2SmnofCMNLb7uC5zOd1Ob344hSR?usp=sharing) projenin içindeki `src/prediction/models` klasörüne kopyalayın.

### 3. Uygulamanın Başlatılması
Sunucuyu ayağa kaldırmak için ana dizinde şu komutu yürütün:
`python main.py`, docker üzerinden çalıştırmak için `docker compose up` 

## API Uç Noktaları

| Endpoint | Açıklama |
| :--- | :--- |
| `http://localhost:7001/` | Sistem durumunu kontrol etmek için kullanılır (Health Check). |
| `http://localhost:7001/UI` | Tarayıcı üzerinden dosya yüklemeyi sağlayan basit kullanıcı arayüzü. |
| `http://localhost:7001/predict` | Resim sınıflandırma işleminin yapıldığı ana tahmin noktası. |
```