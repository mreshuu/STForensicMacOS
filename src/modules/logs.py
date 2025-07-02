"""
Log Analizi Modülü
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base_module import BaseModule
from ..utils.helpers import run_command


class LogsModule(BaseModule):
    """Log analizi modülü"""
    
    description = "Log analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Log bilgilerini analiz et"""
        data = {}
        
        try:
            # Sistem logları
            data["system_logs"] = self._get_system_logs()
            
            # Uygulama logları
            data["application_logs"] = self._get_application_logs()
            
            # Güvenlik logları
            data["security_logs"] = self._get_security_logs()
            
            # Kullanıcı aktiviteleri
            data["user_activities"] = self._get_user_activities()
            
            # Log dosyaları analizi
            data["log_files_analysis"] = self._get_log_files_analysis()
            
            # Hata logları
            data["error_logs"] = self._get_error_logs()
            
            # Log istatistikleri
            data["log_statistics"] = self._get_log_statistics()
            
        except Exception as e:
            self.add_error(f"Log analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_system_logs(self) -> Dict[str, Any]:
        """Sistem logları"""
        system_logs = {}
        
        try:
            # system.log
            system_log_path = "/var/log/system.log"
            if os.path.exists(system_log_path):
                system_logs["system_log"] = self._analyze_log_file(system_log_path, max_lines=500)
            
            # Unified log (macOS 10.12+)
            system_logs["unified_logs"] = self._get_unified_logs()
            
        except Exception as e:
            self.add_error(f"Sistem logları alınırken hata: {str(e)}")
        
        return system_logs
    
    def _get_application_logs(self) -> List[Dict[str, Any]]:
        """Uygulama logları"""
        app_logs = []
        
        try:
            # Console logları
            console_log_path = os.path.expanduser("~/Library/Logs/Console")
            if os.path.exists(console_log_path):
                for log_file in glob.glob(os.path.join(console_log_path, "*.log")):
                    try:
                        stat_info = os.stat(log_file)
                        app_logs.append({
                            "file": log_file,
                            "size": stat_info.st_size,
                            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                        })
                    except (OSError, PermissionError):
                        continue
                        
        except Exception as e:
            self.add_error(f"Uygulama logları alınırken hata: {str(e)}")
        
        return app_logs[:20]  # İlk 20
    
    def _get_security_logs(self) -> Dict[str, Any]:
        """Güvenlik logları"""
        security_logs = {}
        
        try:
            # auth.log
            auth_log_path = "/var/log/auth.log"
            if os.path.exists(auth_log_path):
                security_logs["auth_log"] = self._analyze_log_file(auth_log_path, max_lines=300)
            
            # SSH logları
            security_logs["ssh_logs"] = self._get_ssh_logs()
            
        except Exception as e:
            self.add_error(f"Güvenlik logları alınırken hata: {str(e)}")
        
        return security_logs
    
    def _get_user_activities(self) -> Dict[str, Any]:
        """Kullanıcı aktiviteleri"""
        user_activities = {}
        
        try:
            # Son kullanıcı aktiviteleri
            user_activities["recent_activities"] = self._get_recent_user_activities()
            
            # Shell geçmişi
            user_activities["shell_history"] = self._get_shell_history()
            
            # Uygulama kullanım geçmişi
            user_activities["app_usage"] = self._get_app_usage_history()
            
            # Dosya erişim geçmişi
            user_activities["file_access"] = self._get_file_access_history()
            
        except Exception as e:
            self.add_error(f"Kullanıcı aktiviteleri alınırken hata: {str(e)}")
        
        return user_activities
    
    def _get_log_files_analysis(self) -> Dict[str, Any]:
        """Log dosyaları analizi"""
        analysis = {}
        
        try:
            # Log dosyaları listesi
            log_dirs = ["/var/log", "/private/var/log", os.path.expanduser("~/Library/Logs")]
            log_files = []
            
            for log_dir in log_dirs:
                if os.path.exists(log_dir):
                    for root, dirs, files in os.walk(log_dir):
                        for file in files:
                            if file.endswith(('.log', '.out', '.err')):
                                file_path = os.path.join(root, file)
                                try:
                                    stat_info = os.stat(file_path)
                                    log_files.append({
                                        "path": file_path,
                                        "size": stat_info.st_size,
                                        "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                                    })
                                except (OSError, PermissionError):
                                    continue
            
            analysis["log_files"] = sorted(log_files, key=lambda x: x["size"], reverse=True)[:30]
            
        except Exception as e:
            self.add_error(f"Log dosyaları analizi sırasında hata: {str(e)}")
        
        return analysis
    
    def _get_error_logs(self) -> List[Dict[str, Any]]:
        """Hata logları"""
        error_logs = []
        
        try:
            # Son 24 saatteki hatalar
            code, stdout, stderr = run_command("log show --predicate 'eventType == logEvent' --last 24h | grep -i error | head -100")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        error_logs.append({
                            "timestamp": datetime.now().isoformat(),
                            "message": line.strip(),
                            "type": "system_error"
                        })
            
            # Crash logları
            crash_logs = self._get_crash_logs()
            error_logs.extend(crash_logs)
            
        except Exception as e:
            self.add_error(f"Hata logları alınırken hata: {str(e)}")
        
        return error_logs
    
    def _get_crash_logs(self) -> List[Dict[str, Any]]:
        """Crash logları"""
        crash_logs = []
        
        try:
            # Crash logları dizini
            crash_dirs = [
                "/Library/Logs/DiagnosticReports",
                os.path.expanduser("~/Library/Logs/DiagnosticReports"),
                "/var/log/DiagnosticReports"
            ]
            
            for crash_dir in crash_dirs:
                if os.path.exists(crash_dir):
                    try:
                        for file in os.listdir(crash_dir):
                            if file.endswith('.crash') or file.endswith('.ips'):
                                file_path = os.path.join(crash_dir, file)
                                try:
                                    stat_info = os.stat(file_path)
                                    crash_logs.append({
                                        "file": file,
                                        "path": file_path,
                                        "size": stat_info.st_size,
                                        "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                                        "type": "crash_log"
                                    })
                                except (OSError, PermissionError):
                                    continue
                    except (OSError, PermissionError):
                        continue
            
            # Son crash logları (en fazla 20 tane)
            crash_logs = sorted(crash_logs, key=lambda x: x['modified'], reverse=True)[:20]
            
        except Exception as e:
            self.add_error(f"Crash logları alınırken hata: {str(e)}")
        
        return crash_logs
    
    def _get_log_statistics(self) -> Dict[str, Any]:
        """Log istatistikleri"""
        stats = {}
        
        try:
            # Log dosyası sayıları
            log_dirs = ["/var/log", "/private/var/log", os.path.expanduser("~/Library/Logs")]
            total_files = 0
            total_size = 0
            
            for log_dir in log_dirs:
                if os.path.exists(log_dir):
                    for root, dirs, files in os.walk(log_dir):
                        for file in files:
                            if file.endswith(('.log', '.out', '.err')):
                                total_files += 1
                                try:
                                    file_path = os.path.join(root, file)
                                    total_size += os.path.getsize(file_path)
                                except (OSError, PermissionError):
                                    continue
            
            stats["total_log_files"] = total_files
            stats["total_size"] = total_size
            stats["total_size_formatted"] = self._format_file_size(total_size)
            
            # Log türleri dağılımı
            stats["log_types_distribution"] = self._get_log_types_distribution()
            
        except Exception as e:
            self.add_error(f"Log istatistikleri alınırken hata: {str(e)}")
        
        return stats
    
    def _get_unified_logs(self) -> List[Dict[str, Any]]:
        """Unified logları (macOS 10.12+)"""
        unified_logs = []
        
        try:
            # Son 100 log kaydı
            code, stdout, stderr = run_command("log show --last 1h --predicate 'eventType == logEvent' | head -50")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        unified_logs.append({
                            "timestamp": datetime.now().isoformat(),
                            "message": line.strip(),
                            "source": "unified_log"
                        })
            
        except Exception as e:
            self.add_error(f"Unified logları alınırken hata: {str(e)}")
        
        return unified_logs
    
    def _get_ssh_logs(self) -> List[Dict[str, Any]]:
        """SSH logları"""
        ssh_logs = []
        
        try:
            # SSH logları
            code, stdout, stderr = run_command("log show --predicate 'process == \"sshd\"' --last 24h | head -20")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        ssh_logs.append({
                            "timestamp": datetime.now().isoformat(),
                            "message": line.strip(),
                            "type": "ssh_log"
                        })
            
        except Exception as e:
            self.add_error(f"SSH logları alınırken hata: {str(e)}")
        
        return ssh_logs
    
    def _get_recent_user_activities(self) -> List[Dict[str, Any]]:
        """Son kullanıcı aktiviteleri"""
        activities = []
        
        try:
            # Son kullanıcı aktiviteleri
            code, stdout, stderr = run_command("log show --predicate 'eventType == logEvent' --last 1h | head -50")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        activities.append({
                            "timestamp": datetime.now().isoformat(),
                            "activity": line.strip(),
                            "type": "user_activity"
                        })
            
        except Exception as e:
            self.add_error(f"Son kullanıcı aktiviteleri alınırken hata: {str(e)}")
        
        return activities
    
    def _get_shell_history(self) -> List[Dict[str, Any]]:
        """Shell geçmişi"""
        shell_history = []
        
        try:
            # Bash geçmişi
            bash_history = os.path.expanduser("~/.bash_history")
            if os.path.exists(bash_history):
                with open(bash_history, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines[-50:]:  # Son 50 komut
                        if line.strip():
                            shell_history.append({
                                "command": line.strip(),
                                "shell": "bash"
                            })
            
            # Zsh geçmişi
            zsh_history = os.path.expanduser("~/.zsh_history")
            if os.path.exists(zsh_history):
                with open(zsh_history, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines[-50:]:  # Son 50 komut
                        if line.strip():
                            shell_history.append({
                                "command": line.strip(),
                                "shell": "zsh"
                            })
                            
        except Exception as e:
            self.add_error(f"Shell geçmişi alınırken hata: {str(e)}")
        
        return shell_history
    
    def _get_app_usage_history(self) -> List[Dict[str, Any]]:
        """Uygulama kullanım geçmişi"""
        app_usage = []
        
        try:
            # Son açılan uygulamalar
            code, stdout, stderr = run_command("log show --predicate 'eventMessage CONTAINS \"launched\"' --last 24h | head -30")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        app_usage.append({
                            "timestamp": datetime.now().isoformat(),
                            "app": line.strip(),
                            "type": "app_launch"
                        })
            
        except Exception as e:
            self.add_error(f"Uygulama kullanım geçmişi alınırken hata: {str(e)}")
        
        return app_usage
    
    def _get_file_access_history(self) -> List[Dict[str, Any]]:
        """Dosya erişim geçmişi"""
        file_access = []
        
        try:
            # Son dosya erişimleri (basit analiz)
            # Not: Detaylı dosya erişim geçmişi için farklı araçlar gerekir
            file_access.append({
                "note": "Detailed file access history requires specialized tools or system monitoring"
            })
            
        except Exception as e:
            self.add_error(f"Dosya erişim geçmişi alınırken hata: {str(e)}")
        
        return file_access
    
    def _analyze_log_file(self, log_path: str, max_lines: int = 500) -> Dict[str, Any]:
        """Log dosyasını analiz et"""
        analysis = {
            "file_path": log_path,
            "total_lines": 0,
            "recent_entries": [],
            "error_count": 0,
            "warning_count": 0
        }
        
        try:
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    analysis["total_lines"] = len(lines)
                    
                    # Son satırları al
                    recent_lines = lines[-max_lines:] if len(lines) > max_lines else lines
                    analysis["recent_entries"] = [
                        {
                            "line_number": i + 1,
                            "content": line.strip(),
                            "timestamp": self._extract_timestamp(line)
                        }
                        for i, line in enumerate(recent_lines)
                        if line.strip()
                    ]
                    
                    # Hata ve uyarı sayıları
                    for line in lines:
                        line_lower = line.lower()
                        if "error" in line_lower:
                            analysis["error_count"] += 1
                        if "warning" in line_lower:
                            analysis["warning_count"] += 1
                            
        except Exception as e:
            analysis["error"] = str(e)
        
        return analysis
    
    def _extract_timestamp(self, log_line: str) -> str:
        """Log satırından zaman damgası çıkar"""
        try:
            # Basit timestamp extraction
            timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
            match = re.search(timestamp_pattern, log_line)
            if match:
                return match.group()
        except Exception:
            pass
        
        return datetime.now().isoformat()
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Dosya boyutunu formatla"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes = int(size_bytes / 1024)
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def _categorize_log_files(self, log_files: List[Dict[str, Any]]) -> Dict[str, int]:
        """Log dosyalarını kategorilere ayır"""
        categories = {}
        
        try:
            for log_file in log_files:
                file_path = log_file["path"]
                if "system" in file_path.lower():
                    categories["system"] = categories.get("system", 0) + 1
                elif "auth" in file_path.lower() or "secure" in file_path.lower():
                    categories["security"] = categories.get("security", 0) + 1
                elif "crash" in file_path.lower():
                    categories["crash"] = categories.get("crash", 0) + 1
                elif "console" in file_path.lower():
                    categories["console"] = categories.get("console", 0) + 1
                else:
                    categories["other"] = categories.get("other", 0) + 1
                    
        except Exception as e:
            self.add_error(f"Log dosyaları kategorize edilirken hata: {str(e)}")
        
        return categories
    
    def _get_log_types_distribution(self) -> Dict[str, Any]:
        """Log türleri dağılımı"""
        distribution = {}
        
        try:
            # Log türleri analizi
            log_dirs = ["/var/log", "/private/var/log", os.path.expanduser("~/Library/Logs")]
            
            for log_dir in log_dirs:
                if os.path.exists(log_dir):
                    for root, dirs, files in os.walk(log_dir):
                        for file in files:
                            if file.endswith(('.log', '.out', '.err')):
                                file_ext = os.path.splitext(file)[1]
                                distribution[file_ext] = distribution.get(file_ext, 0) + 1
                                
        except Exception as e:
            self.add_error(f"Log türleri dağılımı alınırken hata: {str(e)}")
        
        return distribution 