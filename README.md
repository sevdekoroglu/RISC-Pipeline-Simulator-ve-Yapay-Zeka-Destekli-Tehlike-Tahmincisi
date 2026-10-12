Bu proje, RISC mimarisine uygun assembly kodlarını üç aşamalı (IF, EX, WB) bir boru hattında (pipeline) çalıştıran ve olası veri tehlikelerini (hazards) tespit eden web tabanlı bir CPU simülatörüdür. İçerisinde barındırdığı yapay zeka modülü sayesinde komut bağımlılıklarını analiz eder ve pipeline performansını (CPI, Stall Rate) tahmin eder.

✨ Öne Çıkan Özellikler

Üç Aşamalı Pipeline Mimarisi: Komutlar Instruction Fetch (IF), Execute (EX) ve Write Back (WB) aşamalarından geçerek gerçeğe yakın bir simülasyon sunar.

Akıllı Assembly Ayrıştırıcı (Parser): ADD, SUB, AND, OR, XOR gibi R-Tipi ve LOAD gibi I-Tipi komutları destekler. Satır içi yorumları (#) otomatik temizler.

Dinamik Tehlike (Hazard) Yönetimi: Read-After-Write (RAW) ve LOAD-USE tehlikelerini tespit eder. Veri bütünlüğünü sağlamak için gerektiğinde Stall (bekleme) uygular veya Forwarding (veri iletimi) yapar.

Yapay Zeka Destekli Tahmin Motoru: Komutlar çalışmadan önce örüntü tanıma ile olası duraksamaları (stall) hesaplar ve donanım metriklerini (CPI, Stall Rate) raporlar.

Web Tabanlı Görselleştirme: Flask tabanlı HTTP API sayesinde kodlar bir web arayüzünden yüklenebilir ve saat çevrimi (clock cycle) adım adım izlenebilir.

Gerçek Zamanlı Simülasyon Logları: Her oturum ve çevrim verisi simulation_db.txt dosyasına zaman damgasıyla kaydedilir.

🛠️ Kullanılan Teknolojiler

Arka Uç: Python 3.x, Flask

Mimari: Object-Oriented Programming (OOP), RISC Pipeline Konsepti

Veri Formatı: JSON (API Haberleşmesi), Düz Metin (Loglama)

📁 Proje Yapısı

Dosya Adı

Açıklama

app.py

Ana web sunucusu ve REST API uç noktalarını barındırır.

pipeline.py

CPU'nun IF, EX ve WB aşamalarını ve döngü mantığını koordine eder.

parser.py

Gelen Assembly kodunu işlenebilir makine komutlarına (opcode, rs1 vb.) çevirir.

hazard_unit.py

Veri tehlikelerini denetler; Stall veya Forwarding kararlarını verir.

ai_predictor.py

Çalışma zamanı hazard tahminleri ve performans istatistiklerini (CPI) tutar.

ai.engine.py

(Opsiyonel Modül) Önceden kod analizi yaparak beklenen Stall sayısını hesaplar.

simulation_db.txt

Simülasyon loglarının tutulduğu sistem veritabanı.

🚀 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1. Depoyu Klonlayın

git clone https://github.com/KULLANICI_ADINIZ/risc-pipeline-simulator.git
cd risc-pipeline-simulator


2. Gerekli Kütüphaneleri Yükleyin
Proje Flask framework'üne ihtiyaç duyar:

pip install Flask


3. Simülatörü Başlatın

python app.py


4. Arayüze Erişin
Uygulama, port çakışmalarını (ör. macOS AirPlay) önlemek için 5001 portunda çalışır. Tarayıcınızdan şu adrese gidin:
http://127.0.0.1:5001

🔌 API Kullanımı

POST /load_code: JSON formatında {"code": "ASSEMBLY_KODU"} göndererek işlemciye yeni program yükler.

GET /next: Simülasyonu 1 saat çevrimi (cycle) ilerletir ve güncel CPU durumunu (Registers, Pipeline State, AI Metrics) döndürür.

GET /reset: Mevcut programı silmeden işlemci saatini ve durumunu sıfırlar.

📝 Örnek Assembly Kodu

Simülatörde test edebileceğiniz basit bir örnek:

LOAD x1, 15        # x1 = 15
LOAD x2, 10        # x2 = 10
AND x3, x1, x2     # x3 = x1 & x2 (RAW ve Forwarding Testi)
OR  x4, x1, x2     # x4 = x1 | x2


