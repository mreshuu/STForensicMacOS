"""
Temel modül sınıfı
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class BaseModule(ABC):
    """Tüm forensic modülleri için temel sınıf"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.name = self.__class__.__name__
        self.description = getattr(self, 'description', 'No description')
        self.version = getattr(self, 'version', '1.0.0')
        self.start_time = None
        self.end_time = None
        self.data = {}
        self.errors = []
        self.warnings = []
    
    def run(self, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Modülü çalıştır"""
        self.start_time = datetime.now()
        self.logger.info(f"Modül başlatılıyor: {self.name}")
        
        try:
            # Ön kontroller
            if not self._pre_check():
                raise Exception("Ön kontroller başarısız")
            
            # Ana analiz
            self.data = self._analyze(args or {})
            
            # Son kontroller
            self._post_check()
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            self.logger.info(f"Modül tamamlandı: {self.name} - {duration:.2f}s")
            
            return {
                "module": self.name,
                "description": self.description,
                "version": self.version,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
                "duration": duration,
                "data": self.data,
                "errors": self.errors,
                "warnings": self.warnings,
                "status": "success" if not self.errors else "error"
            }
            
        except Exception as e:
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds() if self.start_time else 0
            
            self.logger.error(f"Modül hatası {self.name}: {str(e)}")
            self.errors.append(str(e))
            
            return {
                "module": self.name,
                "description": self.description,
                "version": self.version,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration": duration,
                "data": self.data,
                "errors": self.errors,
                "warnings": self.warnings,
                "status": "error"
            }
    
    def _pre_check(self) -> bool:
        """Çalıştırma öncesi kontroller"""
        try:
            # Sistem kontrolü
            if not self._check_system_requirements():
                return False
            
            # Yetki kontrolü
            if not self._check_permissions():
                return False
            
            # Kaynak kontrolü
            if not self._check_resources():
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Ön kontrol hatası: {str(e)}")
            return False
    
    def _post_check(self):
        """Çalıştırma sonrası kontroller"""
        try:
            # Veri bütünlüğü kontrolü
            if not self._verify_data_integrity():
                self.warnings.append("Veri bütünlüğü doğrulanamadı")
            
            # Sonuç kontrolü
            if not self._validate_results():
                self.warnings.append("Sonuçlar doğrulanamadı")
                
        except Exception as e:
            self.logger.warning(f"Son kontrol hatası: {str(e)}")
    
    def _check_system_requirements(self) -> bool:
        """Sistem gereksinimlerini kontrol et"""
        # Alt sınıflar override edebilir
        return True
    
    def _check_permissions(self) -> bool:
        """Gerekli yetkileri kontrol et"""
        # Alt sınıflar override edebilir
        return True
    
    def _check_resources(self) -> bool:
        """Kaynak yeterliliğini kontrol et"""
        # Alt sınıflar override edebilir
        return True
    
    def _verify_data_integrity(self) -> bool:
        """Veri bütünlüğünü doğrula"""
        # Alt sınıflar override edebilir
        return True
    
    def _validate_results(self) -> bool:
        """Sonuçları doğrula"""
        # Alt sınıflar override edebilir
        return True
    
    @abstractmethod
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Ana analiz fonksiyonu - alt sınıflar implement etmeli"""
        pass
    
    def add_error(self, error: str):
        """Hata ekle"""
        self.errors.append(error)
        self.logger.error(f"{self.name} hatası: {error}")
    
    def add_warning(self, warning: str):
        """Uyarı ekle"""
        self.warnings.append(warning)
        self.logger.warning(f"{self.name} uyarısı: {warning}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Modül özeti"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "status": "success" if not self.errors else "error",
            "data_count": len(self.data),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "duration": (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
        }
    
    def cleanup(self):
        """Temizlik işlemleri"""
        try:
            # Geçici dosyaları temizle
            self._cleanup_temp_files()
            
            # Belleği temizle
            self.data.clear()
            self.errors.clear()
            self.warnings.clear()
            
        except Exception as e:
            self.logger.warning(f"Temizlik hatası: {str(e)}")
    
    def _cleanup_temp_files(self):
        """Geçici dosyaları temizle"""
        # Alt sınıflar override edebilir
        pass 