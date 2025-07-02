# STForensicMacOS - MacOS Forensic Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

MacOS sistemleri için geliştirilmiş modüler forensic analiz aracı. Olay anında hızlı kurulum ve sistem imajı alma özellikleri ile donatılmıştır.

## 🚀 Özellikler

- **🔧 Modüler Yapı**: Her analiz türü için ayrı modüller
- **⚡ Hızlı Kurulum**: Tek komutla kurulum ve çalıştırma
- **📊 İki Analiz Modu**: Lite (hızlı analiz) ve Full (tam imaj)
- **📄 Otomatik Raporlama**: HTML, JSON formatlarında detaylı raporlar
- **🔍 Gerçek Zamanlı Analiz**: Sistem durumu ve değişikliklerin takibi
- **🔒 Güvenlik Odaklı**: Sadece okuma işlemleri, veri bütünlüğü korunur

## 📋 Modüller

### 🔍 Sistem Bilgileri
- Donanım bilgileri (CPU, RAM, Disk)
- İşletim sistemi detayları
- Sistem yapılandırması
- Çevre değişkenleri

### 📁 Dosya Sistemi Analizi
- Dosya sistemi yapısı
- Dosya hash'leri (MD5, SHA256)
- Zaman damgaları
- Silinmiş dosya kurtarma (temel)

### 🧠 Bellek Analizi
- RAM durumu ve kullanımı
- Kernel modülleri
- Bellek haritası
- Swap durumu

### 🌐 Ağ Analizi
- Aktif bağlantılar (IPv4/IPv6)
- Routing tablosu
- DNS bilgileri
- Firewall kuralları

### 📝 Log Analizi
- Sistem logları
- Uygulama logları
- Güvenlik logları
- Crash logları

### ⚙️ Process Analizi
- Çalışan processler
- Process detayları
- Sistem servisleri
- Açık dosyalar

### 👥 Kullanıcı Analizi
- Kullanıcı hesapları
- Grup bilgileri
- Yetki seviyeleri
- Oturum bilgileri

### ⏰ Zaman Çizelgesi Analizi
- Dosya zaman çizelgesi
- Sistem olayları
- Kullanıcı aktiviteleri

## 🛠️ Kurulum

### Gereksinimler
- macOS 10.15 veya üzeri
- Python 3.8+
- Root/Administrator yetkisi

### Adımlar

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/silexi/stforensicmacos.git
cd stforensicmacos
```

2. **Gereksinimleri yükleyin:**
```bash
pip3 install -r requirements.txt
```

3. **Çalıştırın:**
```bash
sudo python3 main.py --mode lite
```

## 📖 Kullanım

### Temel Kullanım

```bash
# Hızlı analiz (Lite mode)
sudo python3 main.py --mode lite --output ./reports

# Tam analiz (Full mode)
sudo python3 main.py --mode full --output ./reports

# Belirli modülleri çalıştır
sudo python3 main.py --modules system_info,filesystem,network --output ./reports

# HTML raporu oluştur
sudo python3 main.py --mode lite --output ./reports --format html
```

### Komut Satırı Seçenekleri

```bash
python3 main.py [OPTIONS]

Options:
  --mode TEXT           Analiz modu: lite veya full [default: lite]
  --modules TEXT        Çalıştırılacak modüller (virgülle ayrılmış)
  --output TEXT         Rapor çıktı dizini [default: ./reports]
  --format TEXT         Rapor formatı: json, html [default: json]
  --verbose, -v         Detaylı çıktı
  --no-hash             Hash hesaplamalarını atla
  --config TEXT         Konfigürasyon dosyası yolu
  --help                Bu mesajı göster
```

### Örnekler

```bash
# Hızlı sistem analizi
sudo python3 main.py --mode lite --output ./forensic_reports

# Sadece ağ analizi
sudo python3 main.py --modules network --output ./network_analysis

# Tam analiz + HTML raporu
sudo python3 main.py --mode full --output ./full_analysis --format html

# Detaylı çıktı ile belirli modüller
sudo python3 main.py --modules system_info,processes,users --verbose --output ./detailed_analysis
```

## 📊 Raporlar

### JSON Raporu
Yapılandırılmış veri formatında tüm analiz sonuçları.

### HTML Raporu
Modern, interaktif web tabanlı rapor:
- Modül bazlı tablolar
- Arama ve filtreleme
- Responsive tasarım
- Detaylı veri görüntüleme

## 🔒 Güvenlik

- **Root Yetkisi**: Bu araç root/administrator yetkisi gerektirir
- **Sadece Okuma**: Orijinal veriler değiştirilmez
- **Hash Doğrulama**: Rapor dosyaları için SHA256 hash'leri
- **Veri Bütünlüğü**: Tüm işlemler salt okuma modunda

## 🏗️ Proje Yapısı

```
stforensicmacos/
├── main.py                 # Ana uygulama
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Bu dosya
├── LICENSE                # MIT License
├── .gitignore            # Git ignore kuralları
├── project_details.json   # Proje detayları
├── roadmap.md            # Geliştirme yol haritası
├── src/                  # Kaynak kod
│   ├── core/             # Çekirdek modüller
│   │   ├── config.py     # Konfigürasyon yönetimi
│   │   ├── forensic_engine.py  # Ana analiz motoru
│   │   └── logger.py     # Logging sistemi
│   ├── modules/          # Forensic modüller
│   │   ├── base_module.py
│   │   ├── system_info.py
│   │   ├── filesystem.py
│   │   ├── memory.py
│   │   ├── network.py
│   │   ├── logs.py
│   │   ├── processes.py
│   │   ├── users.py
│   │   └── timeline.py
│   ├── reporters/        # Raporlayıcılar
│   │   ├── json_reporter.py
│   │   └── html_reporter.py
│   └── utils/            # Yardımcı fonksiyonlar
│       └── helpers.py
├── static/               # Statik dosyalar
├── templates/            # HTML şablonları
└── test_reports/         # Test raporları
```

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT License altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## ⚠️ Uyarı

Bu araç sadece eğitim ve yasal forensic analiz amaçları için tasarlanmıştır. Kullanıcılar, bu aracı kullanırken yerel yasaları ve düzenlemeleri takip etmekten sorumludur.

## 📞 İletişim

- **Proje Linki**: [https://github.com/silexi/stforensicmacos](https://github.com/silexi/stforensicmacos)
- **Sorunlar**: [GitHub Issues](https://github.com/silexi/stforensicmacos/issues)

## 🙏 Teşekkürler

Bu proje aşağıdaki açık kaynak projelerden ilham almıştır:
- [Volatility](https://github.com/volatilityfoundation/volatility)
- [Autopsy](https://github.com/sleuthkit/autopsy)
- [The Sleuth Kit](https://github.com/sleuthkit/sleuthkit)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 