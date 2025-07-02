"""
Yardımcı fonksiyonlar
"""

import os
import sys
import subprocess
import hashlib
import time
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


def check_root_permissions() -> bool:
    """Root/administrator yetkisi kontrolü"""
    try:
        # macOS için root kontrolü
        if platform.system() == "Darwin":
            # Eğer EUID 0 ise root yetkisi var
            return os.geteuid() == 0
        else:
            # Diğer sistemler için basit kontrol
            return os.name == 'posix' and os.geteuid() == 0
    except Exception:
        return False


def create_output_directory(output_path: str) -> Path:
    """Çıktı dizinini oluştur"""
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Alt dizinleri oluştur
    (output_dir / "logs").mkdir(exist_ok=True)
    (output_dir / "reports").mkdir(exist_ok=True)
    (output_dir / "images").mkdir(exist_ok=True)
    (output_dir / "temp").mkdir(exist_ok=True)
    
    return output_dir


def run_command(command: str, timeout: int = 300) -> Tuple[int, str, str]:
    """Sistem komutunu çalıştır"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Komut zaman aşımına uğradı: {command}"
    except Exception as e:
        return -1, "", f"Komut çalıştırma hatası: {str(e)}"


def calculate_hash(file_path: str, algorithm: str = "sha256") -> Optional[str]:
    """Dosya hash'ini hesapla"""
    try:
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    except Exception:
        return None


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Dosya bilgilerini al"""
    try:
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:],
            "owner": stat.st_uid,
            "group": stat.st_gid
        }
    except Exception:
        return {}


def format_size(size_bytes: int) -> str:
    """Byte boyutunu okunabilir formata çevir"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes = int(size_bytes / 1024)
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def parse_size_string(size_str: str) -> int:
    """Boyut string'ini byte'a çevir"""
    size_str = size_str.upper().strip()
    
    try:
        if size_str.endswith('KB'):
            return int(float(size_str[:-2]) * 1024)
        elif size_str.endswith('MB'):
            return int(float(size_str[:-2]) * 1024 * 1024)
        elif size_str.endswith('GB'):
            return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
        elif size_str.endswith('TB'):
            return int(float(size_str[:-2]) * 1024 * 1024 * 1024 * 1024)
        else:
            return int(float(size_str))
    except (ValueError, TypeError):
        return 0


def get_system_info() -> Dict[str, Any]:
    """Sistem bilgilerini al"""
    info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "username": os.getenv("USER", "unknown"),
        "home_directory": os.path.expanduser("~"),
        "current_directory": os.getcwd()
    }
    
    # macOS özel bilgiler
    if platform.system() == "Darwin":
        try:
            # macOS versiyonu
            code, stdout, stderr = run_command("sw_vers -productVersion")
            if code == 0:
                info["macos_version"] = stdout.strip()
            
            # Build numarası
            code, stdout, stderr = run_command("sw_vers -buildVersion")
            if code == 0:
                info["macos_build"] = stdout.strip()
                
        except Exception:
            pass
    
    return info


def sanitize_filename(filename: str) -> str:
    """Dosya adını güvenli hale getir"""
    # Geçersiz karakterleri kaldır
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Başındaki ve sonundaki boşlukları kaldır
    filename = filename.strip()
    
    # Çok uzun dosya adlarını kısalt
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename


def create_timestamp() -> str:
    """Zaman damgası oluştur"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def is_macos() -> bool:
    """macOS sisteminde olup olmadığını kontrol et"""
    return platform.system() == "Darwin"


def get_available_disk_space(path: str = "/") -> int:
    """Kullanılabilir disk alanını al"""
    try:
        statvfs = os.statvfs(path)
        return statvfs.f_frsize * statvfs.f_bavail
    except Exception:
        return 0


def check_disk_space(required_size: int, path: str = "/") -> bool:
    """Disk alanı yeterliliğini kontrol et"""
    available = get_available_disk_space(path)
    return available >= required_size


def get_process_info(pid: int) -> Dict[str, Any]:
    """Process bilgilerini al"""
    try:
        import psutil
        process = psutil.Process(pid)
        
        return {
            "pid": pid,
            "name": process.name(),
            "cmdline": process.cmdline(),
            "status": process.status(),
            "cpu_percent": process.cpu_percent(),
            "memory_percent": process.memory_percent(),
            "memory_info": process.memory_info()._asdict(),
            "create_time": datetime.fromtimestamp(process.create_time()).isoformat(),
            "num_threads": process.num_threads(),
            "connections": [conn._asdict() for conn in process.connections()],
            "open_files": [f.path for f in process.open_files()]
        }
    except Exception:
        return {"pid": pid, "error": "Process bilgileri alınamadı"}


def list_directory_contents(path: str, max_depth: int = 3) -> List[Dict[str, Any]]:
    """Dizin içeriğini listele"""
    contents = []
    
    try:
        for root, dirs, files in os.walk(path):
            depth = root[len(path):].count(os.sep)
            if depth > max_depth:
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_info = get_file_info(file_path)
                    contents.append(file_info)
                except Exception:
                    continue
                    
    except Exception:
        pass
    
    return contents


def compress_data(data: bytes, algorithm: str = "gzip") -> bytes:
    """Veriyi sıkıştır"""
    import gzip
    import zlib
    
    try:
        if algorithm == "gzip":
            return gzip.compress(data)
        elif algorithm == "zlib":
            return zlib.compress(data)
        else:
            return data
    except Exception:
        return data


def decompress_data(data: bytes, algorithm: str = "gzip") -> bytes:
    """Sıkıştırılmış veriyi aç"""
    import gzip
    import zlib
    
    try:
        if algorithm == "gzip":
            return gzip.decompress(data)
        elif algorithm == "zlib":
            return zlib.decompress(data)
        else:
            return data
    except Exception:
        return data


def validate_file_integrity(file_path: str, expected_hash: str, algorithm: str = "sha256") -> bool:
    """Dosya bütünlüğünü doğrula"""
    actual_hash = calculate_hash(file_path, algorithm)
    return actual_hash == expected_hash if actual_hash else False


def create_backup(file_path: str, backup_dir: str = "./backups") -> Optional[str]:
    """Dosya yedeği oluştur"""
    try:
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        filename = Path(file_path).name
        timestamp = create_timestamp()
        backup_file = backup_path / f"{filename}.{timestamp}.bak"
        
        import shutil
        shutil.copy2(file_path, backup_file)
        
        return str(backup_file)
    except Exception:
        return None 