"""
Forensic Engine - Ana analiz motoru
"""

import os
import sys
import time
import logging
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Modülleri import et
from ..modules.system_info import SystemInfoModule
from ..modules.processes import ProcessesModule
from ..modules.network import NetworkModule
from ..modules.users import UsersModule
from ..modules.filesystem import FilesystemModule
from ..modules.memory import MemoryModule
from ..modules.logs import LogsModule
from ..modules.timeline import TimelineModule

# Raporlayıcıları import et
from ..reporters.json_reporter import JSONReporter
from ..reporters.html_reporter import HTMLReporter
# from ..reporters.pdf_reporter import PDFReporter
# from ..reporters.csv_reporter import CSVReporter


class ForensicEngine:
    """Forensic analiz motoru"""
    
    def __init__(self, config, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.modules = {}
        self.reporters = {}
        self.results = {}
        
        # Modülleri kaydet
        self._register_modules()
        
        # Raporlayıcıları kaydet
        self._register_reporters()
    
    def _register_modules(self):
        """Modülleri kaydet"""
        try:
            # Sistem bilgileri modülü
            self.modules["system_info"] = SystemInfoModule(
                self.config.get_module_config("system_info"),
                self.logger
            )
            
            # Process analizi modülü
            self.modules["processes"] = ProcessesModule(
                self.config.get_module_config("processes"),
                self.logger
            )
            
            # Network analizi modülü
            self.modules["network"] = NetworkModule(
                self.config.get_module_config("network"),
                self.logger
            )
            
            # Kullanıcı analizi modülü
            self.modules["users"] = UsersModule(
                self.config.get_module_config("users"),
                self.logger
            )
            
            # Gelişmiş modüller
            self.modules["filesystem"] = FilesystemModule(
                self.config.get_module_config("filesystem"),
                self.logger
            )
            self.modules["memory"] = MemoryModule(
                self.config.get_module_config("memory"),
                self.logger
            )
            self.modules["logs"] = LogsModule(
                self.config.get_module_config("logs"),
                self.logger
            )
            self.modules["timeline"] = TimelineModule(
                self.config.get_module_config("timeline"),
                self.logger
            )
            
        except Exception as e:
            self.logger.error(f"Modül kayıt hatası: {str(e)}")
    
    def _register_reporters(self):
        """Raporlayıcıları kaydet"""
        try:
            self.reporters["json"] = JSONReporter(self.config, self.logger)
            self.reporters["html"] = HTMLReporter(self.config, self.logger)
            # self.reporters["pdf"] = PDFReporter(self.config, self.logger)
            # self.reporters["csv"] = CSVReporter(self.config, self.logger)
            
        except Exception as e:
            self.logger.error(f"Raporlayıcı kayıt hatası: {str(e)}")
    
    def run_mode(self, mode: str, args) -> Dict[str, Any]:
        """Belirli bir modda analiz çalıştır"""
        self.logger.info(f"Mod analizi başlatılıyor: {mode}")
        
        # Mod konfigürasyonunu al
        mode_config = self.config.get_mode_config(mode)
        if not mode_config:
            raise ValueError(f"Geçersiz mod: {mode}")
        
        # Modül listesini al
        module_list = mode_config.get("modules", [])
        
        # Mod bilgilerini göster
        description = mode_config.get("description", "Açıklama yok")
        estimated_time = mode_config.get("estimated_time", "Bilinmiyor")
        
        print(f"\n🎯 Mod: {mode.upper()}")
        print(f"📝 Açıklama: {description}")
        print(f"⏱️  Tahmini süre: {estimated_time}")
        print(f"🔧 Modüller: {', '.join(module_list)}")
        
        # Modülleri çalıştır
        return self.run_modules(module_list, args)
    
    def run_modules(self, module_list: List[str], args) -> Dict[str, Any]:
        """Belirli modülleri çalıştır"""
        self.logger.info(f"Modül analizi başlatılıyor: {', '.join(module_list)}")
        
        # Modül tahmini süreleri (saniye) - Gerçek sürelere göre güncellendi
        module_estimates = {
            "system_info": 1,
            "processes": 40,  # 35.79s gerçek
            "network": 12,    # 11.45s gerçek
            "users": 8,       # 7.42s gerçek
            "filesystem": 300,  # 5 dakika
            "memory": 5,
            "logs": 20,
            "timeline": 400  # 6-7 dakika
        }
        
        results = {
            "analysis_info": {
                "start_time": datetime.now().isoformat(),
                "modules": module_list,
                "args": vars(args) if hasattr(args, '__dict__') else str(args)
            },
            "modules": {},
            "summary": {
                "total_modules": len(module_list),
                "successful_modules": 0,
                "failed_modules": 0,
                "total_duration": 0,
                "total_data_count": 0
            }
        }
        
        start_time = time.time()
        total_estimated_time = sum(module_estimates.get(m, 10) for m in module_list)
        
        print(f"\n🚀 Analiz başlatılıyor...")
        print(f"📊 {len(module_list)} modül çalıştırılacak")
        print(f"⏱️  Tahmini toplam süre: {total_estimated_time} saniye")
        print("=" * 60)
        print()
        
        for i, module_name in enumerate(module_list, 1):
            try:
                # Modülün mevcut olup olmadığını kontrol et
                if module_name not in self.modules:
                    self.logger.warning(f"Modül bulunamadı: {module_name}")
                    print(f"❌ [{i}/{len(module_list)}] Modül bulunamadı: {module_name}")
                    continue
                
                # Modülün etkin olup olmadığını kontrol et
                if not self.config.is_module_enabled(module_name):
                    self.logger.info(f"Modül devre dışı: {module_name}")
                    print(f"⚠️  [{i}/{len(module_list)}] Modül devre dışı: {module_name}")
                    continue
                
                # Modülü çalıştır
                estimated_time = module_estimates.get(module_name, 10)
                print(f"🔄 [{i}/{len(module_list)}] {module_name} çalıştırılıyor... (Tahmini: {estimated_time}s)")
                print(f"   {'─' * 40}")
                
                # Progress göstergesi başlat
                progress_stop = threading.Event()
                progress_thread = None
                
                def show_progress():
                    dots = 0
                    while not progress_stop.is_set():
                        dots = (dots + 1) % 4
                        print(f"\r🔄 [{i}/{len(module_list)}] {module_name} çalışıyor{'.' * dots}   ", end='', flush=True)
                        time.sleep(0.5)
                
                # Progress thread'ini başlat
                progress_thread = threading.Thread(target=show_progress)
                progress_thread.daemon = True
                progress_thread.start()
                
                self.logger.info(f"Modül çalıştırılıyor: {module_name}")
                module_result = self.modules[module_name].run(args)
                
                # Progress'i durdur
                progress_stop.set()
                if progress_thread:
                    progress_thread.join(timeout=1)
                
                # Sonucu kaydet
                results["modules"][module_name] = module_result
                
                # Özet bilgilerini güncelle
                if module_result["status"] == "success":
                    results["summary"]["successful_modules"] += 1
                    duration = module_result.get("duration", 0)
                    print(f"\r✅ [{i}/{len(module_list)}] {module_name} tamamlandı ({duration:.1f}s)")
                    print(f"   {'─' * 40}")
                else:
                    results["summary"]["failed_modules"] += 1
                    print(f"\r❌ [{i}/{len(module_list)}] {module_name} başarısız")
                    print(f"   {'─' * 40}")
                
                # Modüller arası boşluk (son modül değilse)
                if i < len(module_list):
                    print()
                
                results["summary"]["total_duration"] += module_result.get("duration", 0)
                results["summary"]["total_data_count"] += len(module_result.get("data", {}))
                
            except Exception as e:
                self.logger.error(f"Modül çalıştırma hatası {module_name}: {str(e)}")
                print(f"💥 [{i}/{len(module_list)}] {module_name} hatası: {str(e)}")
                print(f"   {'─' * 40}")
                
                # Modüller arası boşluk (son modül değilse)
                if i < len(module_list):
                    print()
                    
                results["modules"][module_name] = {
                    "module": module_name,
                    "status": "error",
                    "error": str(e),
                    "start_time": datetime.now().isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "duration": 0,
                    "data": {},
                    "errors": [str(e)],
                    "warnings": []
                }
                results["summary"]["failed_modules"] += 1
        
        end_time = time.time()
        total_duration = end_time - start_time
        results["analysis_info"]["end_time"] = datetime.now().isoformat()
        results["analysis_info"]["total_duration"] = total_duration
        
        self.results = results
        
        print("=" * 60)
        print(f"🎉 Analiz tamamlandı!")
        print(f"✅ Başarılı: {results['summary']['successful_modules']}")
        print(f"❌ Başarısız: {results['summary']['failed_modules']}")
        print(f"⏱️  Toplam süre: {total_duration:.1f}s")
        print(f"📊 Toplam veri: {results['summary']['total_data_count']} öğe")
        
        self.logger.info(f"Analiz tamamlandı: {results['summary']['successful_modules']} başarılı, {results['summary']['failed_modules']} başarısız")
        
        return results
    
    def generate_reports(self, results: Dict[str, Any], output_dir: str, format: str = "json"):
        """Raporları oluştur"""
        self.logger.info(f"Raporlar oluşturuluyor: {format} formatında")
        
        try:
            # Çıktı dizinini oluştur
            output_path = Path(output_dir)
            reports_dir = output_path / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Zaman damgası
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Raporlayıcıyı seç
            if format in self.reporters:
                reporter = self.reporters[format]
                
                # Rapor dosya adı
                filename = f"forensic_report_{timestamp}.{format}"
                report_path = reports_dir / filename
                
                # Raporu oluştur
                reporter.generate_report(results, str(report_path))
                
                self.logger.info(f"Rapor oluşturuldu: {report_path}")
                
                # Hash hesapla (opsiyonel)
                if self.config.get("security.hash_verification", True):
                    from ..utils.helpers import calculate_hash
                    report_hash = calculate_hash(str(report_path))
                    if report_hash:
                        hash_file = report_path.with_suffix(f".{format}.sha256")
                        with open(hash_file, 'w') as f:
                            f.write(f"{report_hash}  {filename}\n")
                        self.logger.info(f"Rapor hash'i oluşturuldu: {hash_file}")
                
            else:
                self.logger.error(f"Desteklenmeyen rapor formatı: {format}")
                
        except Exception as e:
            self.logger.error(f"Rapor oluşturma hatası: {str(e)}")
    
    def generate_all_reports(self, results: Dict[str, Any], output_dir: str):
        """Tüm formatlarda rapor oluştur"""
        self.logger.info("Tüm formatlarda raporlar oluşturuluyor")
        
        for format in self.reporters.keys():
            try:
                self.generate_reports(results, output_dir, format)
            except Exception as e:
                self.logger.error(f"{format} raporu oluşturma hatası: {str(e)}")
    
    def get_available_modules(self) -> List[str]:
        """Mevcut modülleri listele"""
        return list(self.modules.keys())
    
    def get_module_info(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Modül bilgilerini al"""
        if module_name in self.modules:
            module = self.modules[module_name]
            return {
                "name": module.name,
                "description": module.description,
                "version": module.version,
                "enabled": self.config.is_module_enabled(module_name)
            }
        return None
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Analiz özetini al"""
        if not self.results:
            return {}
        
        summary = self.results.get("summary", {})
        analysis_info = self.results.get("analysis_info", {})
        
        return {
            "total_modules": summary.get("total_modules", 0),
            "successful_modules": summary.get("successful_modules", 0),
            "failed_modules": summary.get("failed_modules", 0),
            "total_duration": summary.get("total_duration", 0),
            "total_data_count": summary.get("total_data_count", 0),
            "start_time": analysis_info.get("start_time"),
            "end_time": analysis_info.get("end_time"),
            "modules": list(self.results.get("modules", {}).keys())
        }
    
    def cleanup(self):
        """Temizlik işlemleri"""
        self.logger.info("Forensic engine temizleniyor")
        
        # Modülleri temizle
        for module in self.modules.values():
            try:
                module.cleanup()
            except Exception as e:
                self.logger.warning(f"Modül temizlik hatası: {str(e)}")
        
        # Sonuçları temizle
        self.results.clear()
        
        self.logger.info("Forensic engine temizlendi") 