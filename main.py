#!/usr/bin/env python3
"""
STForensicMacOS - MacOS Forensic Analysis Tool
Ana uygulama dosyası
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Proje modüllerini import et
from src.core.config import Config
from src.core.logger import setup_logger
from src.core.forensic_engine import ForensicEngine
from src.utils.helpers import check_root_permissions, create_output_directory


def parse_arguments():
    """Komut satırı argümanlarını parse et"""
    parser = argparse.ArgumentParser(
        description="STForensicMacOS - MacOS Forensic Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python main.py --mode lite --output ./reports
  python main.py --mode full --output ./reports --image-size 50GB
  python main.py --modules system,filesystem,network --output ./reports
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["lite", "full"],
        default="lite",
        help="Analiz modu: lite (hızlı) veya full (tam imaj)"
    )
    
    parser.add_argument(
        "--modules",
        type=str,
        help="Çalıştırılacak modüller (virgülle ayrılmış)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./reports",
        help="Rapor çıktı dizini"
    )
    
    parser.add_argument(
        "--image-size",
        type=str,
        help="İmaj boyutu (örn: 50GB, 100GB)"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "html", "pdf", "csv"],
        default="json",
        help="Rapor formatı"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Detaylı çıktı"
    )
    
    parser.add_argument(
        "--no-hash",
        action="store_true",
        help="Hash hesaplamalarını atla"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Konfigürasyon dosyası yolu"
    )
    
    return parser.parse_args()


def main():
    """Ana uygulama fonksiyonu"""
    print("=" * 60)
    print("STForensicMacOS - MacOS Forensic Analysis Tool")
    print("=" * 60)
    
    # Argümanları parse et
    args = parse_arguments()
    
    # Root yetkisi kontrolü
    if not check_root_permissions():
        print("❌ Hata: Bu uygulama root/administrator yetkisi gerektirir!")
        print("   Lütfen 'sudo python main.py' ile çalıştırın.")
        sys.exit(1)
    
    # Konfigürasyon yükle
    config = Config(args.config)
    
    # Logger kurulumu
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_level, args.output)
    
    logger.info("STForensicMacOS başlatılıyor...")
    logger.info(f"Analiz modu: {args.mode}")
    logger.info(f"Çıktı dizini: {args.output}")
    
    try:
        # Çıktı dizinini oluştur
        create_output_directory(args.output)
        
        # Forensic engine'i başlat
        engine = ForensicEngine(config, logger)
        
        # Analizi başlat
        start_time = datetime.now()
        logger.info(f"Analiz başlatılıyor: {start_time}")
        
        if args.modules:
            # Belirli modülleri çalıştır
            module_list = [m.strip() for m in args.modules.split(",")]
            print(f"\n🎯 Belirli modüller çalıştırılıyor: {', '.join(module_list)}")
            results = engine.run_modules(module_list, args)
        else:
            # Mod bazlı çalıştır
            results = engine.run_mode(args.mode, args)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"Analiz tamamlandı: {end_time}")
        logger.info(f"Toplam süre: {duration}")
        
        # Raporları oluştur
        print(f"\n📄 Raporlar oluşturuluyor...")
        engine.generate_reports(results, args.output, args.format)
        
        print(f"\n🎉 Analiz başarıyla tamamlandı!")
        print(f"📊 Raporlar: {args.output}")
        print(f"⏱️  Toplam süre: {duration}")
        
    except KeyboardInterrupt:
        logger.warning("Kullanıcı tarafından durduruldu")
        print("\n⚠️  Analiz kullanıcı tarafından durduruldu")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Kritik hata: {str(e)}")
        print(f"\n❌ Kritik hata: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 