"""
Dosya Sistemi Analizi Modülü
"""

import os
import hashlib
import stat
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_module import BaseModule
from ..utils.helpers import run_command, calculate_hash, get_file_info, format_size


class FilesystemModule(BaseModule):
    """Dosya sistemi analizi modülü"""
    
    description = "Dosya sistemi analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Dosya sistemi bilgilerini analiz et"""
        data = {}
        
        try:
            # Dosya sistemi yapısı
            data["filesystem_structure"] = self._get_filesystem_structure()
            
            # Önemli dizinler
            data["important_directories"] = self._get_important_directories()
            
            # Dosya hash'leri
            data["file_hashes"] = self._get_file_hashes()
            
            # Zaman damgaları
            data["timestamps"] = self._get_file_timestamps()
            
            # Silinmiş dosyalar
            data["deleted_files"] = self._get_deleted_files()
            
            # Dosya izinleri
            data["file_permissions"] = self._get_file_permissions()
            
            # Disk kullanımı
            data["disk_usage"] = self._get_disk_usage()
            
        except Exception as e:
            self.add_error(f"Dosya sistemi analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_filesystem_structure(self) -> Dict[str, Any]:
        """Dosya sistemi yapısı"""
        structure = {}
        
        try:
            # Ana dizinler
            root_dirs = ['/', '/Applications', '/System', '/Users', '/var', '/etc', '/tmp']
            
            for root_dir in root_dirs:
                if os.path.exists(root_dir):
                    structure[root_dir] = self._scan_directory(root_dir, max_depth=3)
            
        except Exception as e:
            self.add_error(f"Dosya sistemi yapısı alınırken hata: {str(e)}")
        
        return structure
    
    def _scan_directory(self, path: str, max_depth: int = 3, current_depth: int = 0) -> Dict[str, Any]:
        """Dizini tara"""
        if current_depth > max_depth:
            return {"type": "max_depth_reached"}
        
        try:
            result = {
                "type": "directory",
                "path": path,
                "exists": os.path.exists(path),
                "items": {}
            }
            
            if not os.path.exists(path):
                return result
            
            try:
                items = os.listdir(path)
                for item in items[:50]:  # İlk 50 öğe
                    item_path = os.path.join(path, item)
                    try:
                        if os.path.isdir(item_path):
                            result["items"][item] = self._scan_directory(
                                item_path, max_depth, current_depth + 1
                            )
                        else:
                            result["items"][item] = {
                                "type": "file",
                                "size": os.path.getsize(item_path) if os.path.exists(item_path) else 0
                            }
                    except (OSError, PermissionError):
                        result["items"][item] = {"type": "access_denied"}
                        
            except (OSError, PermissionError):
                result["error"] = "access_denied"
                
        except Exception as e:
            result = {"error": str(e)}
        
        return result
    
    def _get_important_directories(self) -> Dict[str, Any]:
        """Önemli dizinler"""
        directories = {}
        
        try:
            important_paths = {
                "home": os.path.expanduser("~"),
                "desktop": os.path.expanduser("~/Desktop"),
                "documents": os.path.expanduser("~/Documents"),
                "downloads": os.path.expanduser("~/Downloads"),
                "applications": "/Applications",
                "system_applications": "/System/Applications",
                "system_library": "/System/Library",
                "library": "/Library",
                "user_library": os.path.expanduser("~/Library"),
                "etc": "/etc",
                "var": "/var",
                "tmp": "/tmp",
                "usr": "/usr"
            }
            
            for name, path in important_paths.items():
                if os.path.exists(path):
                    try:
                        stat_info = os.stat(path)
                        directories[name] = {
                            "path": path,
                            "exists": True,
                            "size": stat_info.st_size,
                            "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                            "permissions": oct(stat_info.st_mode)[-3:],
                            "owner": stat_info.st_uid,
                            "group": stat_info.st_gid
                        }
                    except (OSError, PermissionError):
                        directories[name] = {
                            "path": path,
                            "exists": True,
                            "error": "access_denied"
                        }
                else:
                    directories[name] = {
                        "path": path,
                        "exists": False
                    }
                    
        except Exception as e:
            self.add_error(f"Önemli dizinler alınırken hata: {str(e)}")
        
        return directories
    
    def _get_file_hashes(self) -> Dict[str, Any]:
        """Dosya hash'leri"""
        hashes = {}
        
        try:
            # Önemli sistem dosyaları
            important_files = [
                "/etc/hosts",
                "/etc/passwd",
                "/etc/group",
                "/etc/sudoers",
                "/System/Library/CoreServices/SystemVersion.plist",
                "/var/log/system.log"
            ]
            
            for file_path in important_files:
                if os.path.exists(file_path):
                    try:
                        file_hash = calculate_hash(file_path, "sha256")
                        if file_hash:
                            hashes[file_path] = {
                                "sha256": file_hash,
                                "size": os.path.getsize(file_path),
                                "modified": datetime.fromtimestamp(
                                    os.path.getmtime(file_path)
                                ).isoformat()
                            }
                    except (OSError, PermissionError):
                        hashes[file_path] = {"error": "access_denied"}
                        
        except Exception as e:
            self.add_error(f"Dosya hash'leri alınırken hata: {str(e)}")
        
        return hashes
    
    def _get_file_timestamps(self) -> List[Dict[str, Any]]:
        """Dosya zaman damgaları"""
        timestamps = []
        
        try:
            # Son 24 saatte değişen dosyalar
            code, stdout, stderr = run_command("find / -type f -mtime -1 2>/dev/null | head -100")
            if code == 0:
                files = stdout.strip().split('\n')
                for file_path in files:
                    if file_path and os.path.exists(file_path):
                        try:
                            stat_info = os.stat(file_path)
                            timestamps.append({
                                "path": file_path,
                                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                                "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                                "size": stat_info.st_size
                            })
                        except (OSError, PermissionError):
                            continue
            
            # Son 7 günde değişen dosyalar (özet)
            code, stdout, stderr = run_command("find / -type f -mtime -7 2>/dev/null | wc -l")
            if code == 0:
                timestamps.append({
                    "summary": "files_modified_last_7_days",
                    "count": int(stdout.strip()) if stdout.strip().isdigit() else 0
                })
                
        except Exception as e:
            self.add_error(f"Zaman damgaları alınırken hata: {str(e)}")
        
        return timestamps
    
    def _get_deleted_files(self) -> List[Dict[str, Any]]:
        """Silinmiş dosyalar (kurtarma için)"""
        deleted_files = []
        
        try:
            # Trash/Recycle Bin
            trash_paths = [
                os.path.expanduser("~/.Trash"),
                "/.Trashes"
            ]
            
            for trash_path in trash_paths:
                if os.path.exists(trash_path):
                    try:
                        for root, dirs, files in os.walk(trash_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    stat_info = os.stat(file_path)
                                    deleted_files.append({
                                        "path": file_path,
                                        "original_name": file,
                                        "size": stat_info.st_size,
                                        "deleted_date": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                                        "location": "trash"
                                    })
                                except (OSError, PermissionError):
                                    continue
                    except (OSError, PermissionError):
                        continue
            
            # Disk üzerinde silinmiş dosyalar (basit analiz)
            # Not: Gerçek kurtarma için özel araçlar gerekir
            deleted_files.append({
                "note": "For complete deleted file recovery, use specialized tools like PhotoRec, TestDisk, or forensic software"
            })
            
        except Exception as e:
            self.add_error(f"Silinmiş dosyalar alınırken hata: {str(e)}")
        
        return deleted_files
    
    def _get_file_permissions(self) -> Dict[str, Any]:
        """Dosya izinleri analizi"""
        permissions = {}
        
        try:
            # SUID/SGID dosyalar
            code, stdout, stderr = run_command("find / -type f -perm -4000 2>/dev/null | head -50")
            if code == 0:
                suid_files = stdout.strip().split('\n')
                permissions["suid_files"] = [
                    {"path": f, "permission": "SUID"} 
                    for f in suid_files if f
                ]
            
            # SGID dosyalar
            code, stdout, stderr = run_command("find / -type f -perm -2000 2>/dev/null | head -50")
            if code == 0:
                sgid_files = stdout.strip().split('\n')
                permissions["sgid_files"] = [
                    {"path": f, "permission": "SGID"} 
                    for f in sgid_files if f
                ]
            
            # Yürütülebilir dosyalar
            code, stdout, stderr = run_command("find / -type f -executable 2>/dev/null | head -100")
            if code == 0:
                executable_files = stdout.strip().split('\n')
                permissions["executable_files_count"] = len([f for f in executable_files if f])
            
        except Exception as e:
            self.add_error(f"Dosya izinleri alınırken hata: {str(e)}")
        
        return permissions
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """Disk kullanımı"""
        disk_usage = {}
        
        try:
            # Disk kullanımı
            code, stdout, stderr = run_command("df -h")
            if code == 0:
                lines = stdout.strip().split('\n')
                disk_usage["partitions"] = []
                
                for line in lines[1:]:  # İlk satırı atla
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 6:
                            disk_usage["partitions"].append({
                                "filesystem": parts[0],
                                "size": parts[1],
                                "used": parts[2],
                                "available": parts[3],
                                "use_percent": parts[4],
                                "mounted_on": parts[5]
                            })
            
            # İnodu kullanımı
            code, stdout, stderr = run_command("df -i")
            if code == 0:
                lines = stdout.strip().split('\n')
                disk_usage["inodes"] = []
                
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 6:
                            disk_usage["inodes"].append({
                                "filesystem": parts[0],
                                "inodes": parts[1],
                                "used": parts[2],
                                "available": parts[3],
                                "use_percent": parts[4],
                                "mounted_on": parts[5]
                            })
            
            # En büyük dizinler
            code, stdout, stderr = run_command("du -h / 2>/dev/null | sort -hr | head -20")
            if code == 0:
                lines = stdout.strip().split('\n')
                disk_usage["largest_directories"] = []
                
                for line in lines:
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            disk_usage["largest_directories"].append({
                                "size": parts[0],
                                "path": parts[1]
                            })
            
        except Exception as e:
            self.add_error(f"Disk kullanımı alınırken hata: {str(e)}")
        
        return disk_usage 