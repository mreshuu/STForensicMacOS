"""
Konfigürasyon yönetimi
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Uygulama konfigürasyonu yönetimi"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.yaml"
        self.config = self._load_default_config()
        
        if os.path.exists(self.config_path):
            self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Varsayılan konfigürasyonu yükle"""
        return {
            "app": {
                "name": "STForensicMacOS",
                "version": "1.0.0",
                "description": "MacOS Forensic Analysis Tool"
            },
            "modes": {
                "lite": {
                    "modules": ["system_info", "processes", "network", "users"],
                    "description": "Hızlı analiz - Temel bilgiler",
                    "estimated_time": "1-2 dakika"
                },
                "full": {
                    "modules": ["system_info", "filesystem", "memory", "network", 
                               "logs", "processes", "users", "timeline"],
                    "description": "Tam imaj - Kapsamlı analiz",
                    "estimated_time": "12-15 dakika"
                }
            },
            "modules": {
                "system_info": {
                    "enabled": True,
                    "description": "Sistem bilgileri toplama",
                    "commands": ["system_profiler", "ioreg", "sysctl"]
                },
                "filesystem": {
                    "enabled": True,
                    "description": "Dosya sistemi analizi",
                    "commands": ["find", "md5", "sha256", "ls"]
                },
                "memory": {
                    "enabled": True,
                    "description": "Bellek analizi",
                    "commands": ["vm_stat", "top", "lsof"]
                },
                "network": {
                    "enabled": True,
                    "description": "Ağ analizi",
                    "commands": ["netstat", "ifconfig", "arp", "route"]
                },
                "logs": {
                    "enabled": True,
                    "description": "Log analizi",
                    "commands": ["log", "system.log", "auth.log"]
                },
                "processes": {
                    "enabled": True,
                    "description": "Process analizi",
                    "commands": ["ps", "lsof", "launchctl"]
                },
                "users": {
                    "enabled": True,
                    "description": "Kullanıcı analizi",
                    "commands": ["dscl", "id", "who"]
                },
                "timeline": {
                    "enabled": True,
                    "description": "Zaman çizelgesi analizi",
                    "commands": ["find", "stat", "mdls"]
                }
            },
            "output": {
                "formats": ["json", "html", "pdf", "csv"],
                "default_format": "json",
                "compression": True,
                "encryption": False
            },
            "security": {
                "hash_verification": True,
                "read_only": True,
                "preserve_timestamps": True,
                "verify_integrity": True
            },
            "performance": {
                "max_threads": 4,
                "chunk_size": 1024 * 1024,  # 1MB
                "timeout": 300,  # 5 dakika
                "memory_limit": "2GB"
            },
            "logging": {
                "level": "INFO",
                "file": "stforensic.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
    
    def _load_config(self):
        """Konfigürasyon dosyasını yükle"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    user_config = yaml.safe_load(f)
                elif self.config_path.endswith('.json'):
                    user_config = json.load(f)
                else:
                    raise ValueError(f"Desteklenmeyen konfigürasyon formatı: {self.config_path}")
                
                # Kullanıcı konfigürasyonunu varsayılan ile birleştir
                self._merge_config(self.config, user_config)
                
        except Exception as e:
            print(f"Konfigürasyon yüklenirken hata: {e}")
            print("Varsayılan konfigürasyon kullanılıyor...")
    
    def _merge_config(self, default: Dict, user: Dict):
        """İki konfigürasyonu birleştir"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_config(default[key], value)
            else:
                default[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Konfigürasyon değerini al"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Konfigürasyon değerini ayarla"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """Konfigürasyonu dosyaya kaydet"""
        save_path = path or self.config_path
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if save_path.endswith('.yaml') or save_path.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
                elif save_path.endswith('.json'):
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                else:
                    raise ValueError(f"Desteklenmeyen format: {save_path}")
                    
        except Exception as e:
            print(f"Konfigürasyon kaydedilirken hata: {e}")
    
    def get_mode_config(self, mode: str) -> Dict[str, Any]:
        """Belirli bir mod için konfigürasyonu al"""
        return self.get(f"modes.{mode}", {})
    
    def get_module_config(self, module: str) -> Dict[str, Any]:
        """Belirli bir modül için konfigürasyonu al"""
        return self.get(f"modules.{module}", {})
    
    def is_module_enabled(self, module: str) -> bool:
        """Modülün etkin olup olmadığını kontrol et"""
        return self.get(f"modules.{module}.enabled", True)
    
    def get_enabled_modules(self) -> list:
        """Etkin modülleri listele"""
        enabled = []
        for module, config in self.config.get("modules", {}).items():
            if config.get("enabled", True):
                enabled.append(module)
        return enabled 