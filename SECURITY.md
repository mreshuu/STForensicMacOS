# Security Policy

## Supported Versions

Bu proje aşağıdaki versiyonlar için güvenlik güncellemeleri alır:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

Güvenlik açıklarını bildirmek için:

1. **Doğrudan iletişim:** Güvenlik açığını doğrudan maintainer'a bildirin
2. **Public issue oluşturmayın:** Güvenlik açıklarını public GitHub issue olarak paylaşmayın
3. **Detaylı bilgi sağlayın:**
   - Açığın açıklaması
   - Yeniden üretim adımları
   - Etkilenen sistem bilgileri
   - Potansiyel etki

### İletişim Bilgileri

- **Email:** [Güvenlik email adresi]
- **GitHub:** [GitHub Security](https://github.com/silexi/stforensicmacos/security)

## Security Features

### Mevcut Güvenlik Özellikleri

- **Root Yetkisi Kontrolü:** Araç sadece root yetkisi ile çalışır
- **Salt Okuma Modu:** Orijinal veriler değiştirilmez
- **Hash Doğrulama:** Rapor dosyaları için SHA256 hash'leri
- **Veri Bütünlüğü:** Tüm işlemler güvenli modda
- **Hata Yönetimi:** Güvenli hata yakalama ve loglama

### Güvenlik Prensipleri

1. **En Az Yetki Prensibi:** Sadece gerekli yetkiler kullanılır
2. **Veri Koruma:** Kullanıcı verileri korunur
3. **Şeffaflık:** Tüm işlemler loglanır
4. **Doğrulama:** Tüm girdiler doğrulanır

## Best Practices

### Kullanıcılar İçin

- Araç sadece kendi sistemlerinizde kullanın
- Root yetkisi gerektiğini unutmayın
- Raporları güvenli şekilde saklayın
- Hash değerlerini doğrulayın

### Geliştiriciler İçin

- Güvenlik açıklarını hemen bildirin
- Kod incelemesi yapın
- Test coverage'ı artırın
- Güvenlik testleri ekleyin

## Disclosure Policy

1. **Keşif:** Güvenlik açığı keşfedilir
2. **Doğrulama:** Açık doğrulanır ve değerlendirilir
3. **Düzeltme:** Güvenlik açığı düzeltilir
4. **Test:** Düzeltme test edilir
5. **Yayınlama:** Güvenlik güncellemesi yayınlanır
6. **Bildirim:** Kullanıcılar bilgilendirilir

## Security Updates

Güvenlik güncellemeleri:

- Kritik açıklar için: 24-48 saat içinde
- Yüksek öncelikli açıklar için: 1 hafta içinde
- Orta öncelikli açıklar için: 2 hafta içinde
- Düşük öncelikli açıklar için: 1 ay içinde

## Responsible Disclosure

Güvenlik araştırmacıları için:

- Açıkları sorumlu şekilde bildirin
- Proof-of-concept kodları paylaşın
- Açık yayınlanmadan önce düzeltme için zaman tanıyın
- İşbirliği yapın

---

Güvenlik konularında işbirliğiniz için teşekkürler! 🔒 