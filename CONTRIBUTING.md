# Contributing to STForensicMacOS

STForensicMacOS projesine katkıda bulunmak istediğiniz için teşekkürler! Bu belge, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 🚀 Başlarken

### Geliştirme Ortamı Kurulumu

1. **Repository'yi fork edin ve klonlayın:**
```bash
git clone https://github.com/silexi/stforensicmacos.git
cd stforensicmacos
```

2. **Sanal ortam oluşturun:**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Geliştirme bağımlılıklarını yükleyin:**
```bash
pip install -r requirements-dev.txt  # Eğer varsa
```

## 📝 Katkı Türleri

### 🐛 Bug Reports
- GitHub Issues kullanın
- Açıklayıcı başlık kullanın
- Adım adım yeniden üretim talimatları ekleyin
- Beklenen ve gerçek davranışı açıklayın
- Sistem bilgilerini ekleyin (macOS versiyonu, Python versiyonu)

### 💡 Feature Requests
- Özelliğin amacını açıklayın
- Kullanım senaryolarını belirtin
- Varsa örnek implementasyon önerin

### 🔧 Code Contributions
- Fork ve pull request workflow kullanın
- Feature branch'ler oluşturun
- Kod standartlarına uyun
- Test ekleyin (mümkünse)

## 🏗️ Kod Standartları

### Python Kod Stili
- PEP 8 standartlarına uyun
- 4 boşluk girinti kullanın
- 79 karakter satır uzunluğu
- Docstring'ler ekleyin
- Type hints kullanın

### Commit Mesajları
- Açıklayıcı ve kısa olun
- İngilizce kullanın
- Conventional commits formatını takip edin:
  - `feat:` Yeni özellik
  - `fix:` Bug düzeltmesi
  - `docs:` Dokümantasyon
  - `style:` Kod stili
  - `refactor:` Refactoring
  - `test:` Test ekleme/düzenleme
  - `chore:` Bakım işleri

### Örnek Commit Mesajları
```
feat: Add memory dump functionality
fix: Resolve IPv6 address parsing issue
docs: Update README with installation instructions
style: Format code according to PEP 8
```

## 🧪 Test Etme

### Manuel Test
```bash
# Lite mode test
sudo python3 main.py --mode lite --output ./test_reports

# Belirli modül testi
sudo python3 main.py --modules network --output ./test_reports

# HTML rapor testi
sudo python3 main.py --mode lite --output ./test_reports --format html
```

### Otomatik Test (Gelecekte)
```bash
# Unit testler
python -m pytest tests/

# Coverage raporu
python -m pytest --cov=src tests/
```

## 📋 Pull Request Süreci

1. **Issue oluşturun** (eğer yoksa)
2. **Feature branch oluşturun:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Değişikliklerinizi yapın**
4. **Test edin**
5. **Commit edin:**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```
6. **Push edin:**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Pull Request oluşturun**

### Pull Request Checklist
- [ ] Kod standartlarına uygun
- [ ] Test edilmiş
- [ ] Dokümantasyon güncellenmiş
- [ ] Commit mesajları açıklayıcı
- [ ] Issue referansı eklenmiş

## 🔒 Güvenlik

### Güvenlik Açıkları
- Güvenlik açıklarını doğrudan maintainer'a bildirin
- Public issue oluşturmayın
- Detaylı bilgi sağlayın

### Güvenlik Prensipleri
- Sadece okuma işlemleri yapın
- Kullanıcı verilerini koruyun
- Root yetkisi kontrolü yapın
- Hash doğrulama kullanın

## 📚 Dokümantasyon

### Kod Dokümantasyonu
- Tüm fonksiyonlar için docstring ekleyin
- Karmaşık algoritmalar için açıklama ekleyin
- Örnek kullanım ekleyin

### README Güncellemeleri
- Yeni özellikler için dokümantasyon ekleyin
- Örnekler güncelleyin
- Screenshot'lar ekleyin (gerekirse)

## 🎯 Katkı Alanları

### Öncelikli Alanlar
- [ ] PDF raporlama
- [ ] CSV export
- [ ] GUI arayüzü
- [ ] Docker desteği
- [ ] Test coverage artırma
- [ ] Performans optimizasyonu

### Modül Geliştirme
- Yeni forensic modülleri ekleyin
- Mevcut modülleri geliştirin
- Hata yönetimini iyileştirin

### Raporlama
- Yeni rapor formatları ekleyin
- HTML raporlarını geliştirin
- Grafik ve görselleştirme ekleyin

## 🤝 İletişim

- **GitHub Issues:** [Issues](https://github.com/silexi/stforensicmacos/issues)
- **Discussions:** [Discussions](https://github.com/silexi/stforensicmacos/discussions)

## 📄 Lisans

Bu projeye katkıda bulunarak, katkılarınızın MIT License altında lisanslanacağını kabul etmiş olursunuz.

---

Katkıda bulunduğunuz için teşekkürler! 🎉 