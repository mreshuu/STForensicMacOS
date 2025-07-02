"""
Logging sistemi
"""

import os
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(level: int = logging.INFO, output_dir: str = "./reports") -> logging.Logger:
    """Logger kurulumu"""
    
    # Logger oluştur
    logger = logging.getLogger("STForensicMacOS")
    logger.setLevel(level)
    
    # Eğer handler'lar zaten eklenmişse, tekrar ekleme
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Console format
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    log_dir = Path(output_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"stforensic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # File format (daha detaylı)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Rotating file handler (opsiyonel)
    rotating_handler = logging.handlers.RotatingFileHandler(
        log_dir / "stforensic.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(file_formatter)
    
    # Handler'ları ekle
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(rotating_handler)
    
    return logger


def get_logger(name: str = "STForensicMacOS") -> logging.Logger:
    """Mevcut logger'ı al"""
    return logging.getLogger(name)


class ForensicLogger:
    """Forensic analiz için özel logger sınıfı"""
    
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = Path(output_dir)
        self.logger = setup_logger(output_dir=output_dir)
        self.analysis_log = self.output_dir / "analysis.log"
        
        # Analiz log dosyası
        self.analysis_logger = logging.getLogger("Analysis")
        self.analysis_logger.setLevel(logging.INFO)
        
        if not self.analysis_logger.handlers:
            analysis_handler = logging.FileHandler(self.analysis_log, encoding='utf-8')
            analysis_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            analysis_handler.setFormatter(formatter)
            self.analysis_logger.addHandler(analysis_handler)
    
    def log_analysis_start(self, mode: str, modules: list):
        """Analiz başlangıcını logla"""
        self.analysis_logger.info(f"Analiz başlatılıyor - Mod: {mode}")
        self.analysis_logger.info(f"Modüller: {', '.join(modules)}")
        self.logger.info(f"Analiz başlatılıyor - Mod: {mode}")
    
    def log_analysis_end(self, duration: str, results: dict):
        """Analiz sonunu logla"""
        self.analysis_logger.info(f"Analiz tamamlandı - Süre: {duration}")
        self.analysis_logger.info(f"Sonuçlar: {len(results)} modül tamamlandı")
        self.logger.info(f"Analiz tamamlandı - Süre: {duration}")
    
    def log_module_start(self, module: str):
        """Modül başlangıcını logla"""
        self.analysis_logger.info(f"Modül başlatılıyor: {module}")
        self.logger.info(f"Modül başlatılıyor: {module}")
    
    def log_module_end(self, module: str, duration: str, data_count: int):
        """Modül sonunu logla"""
        self.analysis_logger.info(f"Modül tamamlandı: {module} - Süre: {duration} - Veri: {data_count}")
        self.logger.info(f"Modül tamamlandı: {module} - Süre: {duration} - Veri: {data_count}")
    
    def log_error(self, module: str, error: str):
        """Hata logla"""
        self.analysis_logger.error(f"Modül hatası {module}: {error}")
        self.logger.error(f"Modül hatası {module}: {error}")
    
    def log_warning(self, module: str, warning: str):
        """Uyarı logla"""
        self.analysis_logger.warning(f"Modül uyarısı {module}: {warning}")
        self.logger.warning(f"Modül uyarısı {module}: {warning}")
    
    def log_security_event(self, event: str, details: dict):
        """Güvenlik olayını logla"""
        self.analysis_logger.warning(f"Güvenlik olayı: {event} - {details}")
        self.logger.warning(f"Güvenlik olayı: {event} - {details}")
    
    def log_performance(self, operation: str, duration: float, size: Optional[int] = None):
        """Performans bilgisini logla"""
        if size:
            self.analysis_logger.info(f"Performans: {operation} - {duration:.2f}s - {size} bytes")
        else:
            self.analysis_logger.info(f"Performans: {operation} - {duration:.2f}s")
    
    def get_analysis_summary(self) -> dict:
        """Analiz özetini al"""
        summary = {
            "log_file": str(self.analysis_log),
            "total_entries": 0,
            "errors": 0,
            "warnings": 0,
            "modules": []
        }
        
        try:
            with open(self.analysis_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                summary["total_entries"] = len(lines)
                
                for line in lines:
                    if "ERROR" in line:
                        summary["errors"] += 1
                    elif "WARNING" in line:
                        summary["warnings"] += 1
                    elif "Modül tamamlandı" in line:
                        # Modül bilgilerini çıkar
                        parts = line.split(" - ")
                        if len(parts) >= 3:
                            module_info = parts[2].split(": ")[1]
                            summary["modules"].append(module_info)
                            
        except Exception as e:
            self.logger.error(f"Analiz özeti alınırken hata: {e}")
        
        return summary 