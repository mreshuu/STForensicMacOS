"""
Zaman Çizelgesi Analizi Modülü
"""

import os
import stat
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base_module import BaseModule
from ..utils.helpers import run_command


class TimelineModule(BaseModule):
    """Zaman çizelgesi analizi modülü"""
    
    description = "Zaman çizelgesi analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Zaman çizelgesi bilgilerini analiz et"""
        data = {}
        
        try:
            # Dosya zaman çizelgesi
            data["file_timeline"] = self._get_file_timeline()
            
            # Sistem olayları
            data["system_events"] = self._get_system_events()
            
            # Kullanıcı aktiviteleri
            data["user_activities"] = self._get_user_activities()
            
            # Zaman çizelgesi özeti
            data["timeline_summary"] = self._get_timeline_summary()
            
        except Exception as e:
            self.add_error(f"Zaman çizelgesi analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_file_timeline(self) -> List[Dict[str, Any]]:
        """Dosya zaman çizelgesi"""
        timeline = []
        
        try:
            # Son 24 saatte değişen dosyalar
            code, stdout, stderr = run_command("find / -type f -mtime -1 2>/dev/null | head -200")
            if code == 0:
                files = stdout.strip().split('\n')
                for file_path in files:
                    if file_path and os.path.exists(file_path):
                        try:
                            stat_info = os.stat(file_path)
                            timeline.append({
                                "type": "file_modified",
                                "path": file_path,
                                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                                "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                                "size": stat_info.st_size,
                                "permissions": oct(stat_info.st_mode)[-3:]
                            })
                        except (OSError, PermissionError):
                            continue
            
            # Son 7 günde değişen önemli dosyalar
            important_paths = [
                "/etc/passwd", "/etc/group", "/etc/hosts", "/etc/sudoers",
                os.path.expanduser("~/.bash_history"), os.path.expanduser("~/.zsh_history"),
                "/var/log/system.log", "/var/log/auth.log"
            ]
            
            for file_path in important_paths:
                if os.path.exists(file_path):
                    try:
                        stat_info = os.stat(file_path)
                        timeline.append({
                            "type": "important_file",
                            "path": file_path,
                            "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                            "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                            "size": stat_info.st_size
                        })
                    except (OSError, PermissionError):
                        continue
                        
        except Exception as e:
            self.add_error(f"Dosya zaman çizelgesi alınırken hata: {str(e)}")
        
        return timeline
    
    def _get_system_events(self) -> List[Dict[str, Any]]:
        """Sistem olayları"""
        events = []
        
        try:
            # Son sistem olayları
            code, stdout, stderr = run_command("log show --last 24h --predicate 'eventType == logEvent' | head -100")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        events.append({
                            "type": "system_event",
                            "timestamp": datetime.now().isoformat(),
                            "message": line.strip(),
                            "source": "unified_log"
                        })
            
            # Boot olayları
            code, stdout, stderr = run_command("log show --predicate 'process == \"kernel\"' --last 24h | head -30")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        events.append({
                            "type": "boot_event",
                            "timestamp": datetime.now().isoformat(),
                            "message": line.strip(),
                            "source": "kernel_log"
                        })
            
            # Güvenlik olayları
            code, stdout, stderr = run_command("log show --predicate 'category == \"security\"' --last 24h | head -30")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        events.append({
                            "type": "security_event",
                            "timestamp": datetime.now().isoformat(),
                            "message": line.strip(),
                            "source": "security_log"
                        })
                        
        except Exception as e:
            self.add_error(f"Sistem olayları alınırken hata: {str(e)}")
        
        return events
    
    def _get_user_activities(self) -> List[Dict[str, Any]]:
        """Kullanıcı aktiviteleri"""
        activities = []
        
        try:
            # Son kullanıcı aktiviteleri
            code, stdout, stderr = run_command("log show --predicate 'eventType == logEvent' --last 1h | head -50")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        activities.append({
                            "type": "user_activity",
                            "timestamp": datetime.now().isoformat(),
                            "activity": line.strip(),
                            "source": "unified_log"
                        })
            
            # Login aktiviteleri
            code, stdout, stderr = run_command("log show --predicate 'eventMessage CONTAINS \"login\"' --last 24h | head -20")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        activities.append({
                            "type": "login_activity",
                            "timestamp": datetime.now().isoformat(),
                            "activity": line.strip(),
                            "source": "auth_log"
                        })
            
            # Uygulama başlatma aktiviteleri
            code, stdout, stderr = run_command("log show --predicate 'eventMessage CONTAINS \"launched\"' --last 24h | head -20")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        activities.append({
                            "type": "app_launch",
                            "timestamp": datetime.now().isoformat(),
                            "activity": line.strip(),
                            "source": "app_log"
                        })
                        
        except Exception as e:
            self.add_error(f"Kullanıcı aktiviteleri alınırken hata: {str(e)}")
        
        return activities
    
    def _get_timeline_summary(self) -> Dict[str, Any]:
        """Zaman çizelgesi özeti"""
        summary = {
            "total_events": 0,
            "file_events": 0,
            "system_events": 0,
            "user_events": 0,
            "time_range": {
                "start": (datetime.now() - timedelta(days=1)).isoformat(),
                "end": datetime.now().isoformat()
            },
            "event_distribution": {}
        }
        
        try:
            # Olay dağılımı
            summary["event_distribution"] = {
                "last_hour": 0,
                "last_6_hours": 0,
                "last_12_hours": 0,
                "last_24_hours": 0
            }
            
            # Dosya değişiklik sayısı
            code, stdout, stderr = run_command("find / -type f -mtime -1 2>/dev/null | wc -l")
            if code == 0:
                summary["file_events"] = int(stdout.strip()) if stdout.strip().isdigit() else 0
            
            # Sistem olay sayısı
            code, stdout, stderr = run_command("log show --last 24h --predicate 'eventType == logEvent' | wc -l")
            if code == 0:
                summary["system_events"] = int(stdout.strip()) if stdout.strip().isdigit() else 0
            
            summary["total_events"] = summary["file_events"] + summary["system_events"]
            
        except Exception as e:
            self.add_error(f"Zaman çizelgesi özeti alınırken hata: {str(e)}")
        
        return summary 