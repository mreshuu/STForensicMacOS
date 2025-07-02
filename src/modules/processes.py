"""
Process Analizi Modülü
"""

import os
import psutil
from typing import Dict, Any, List
from .base_module import BaseModule
from ..utils.helpers import run_command, get_process_info


class ProcessesModule(BaseModule):
    """Process analizi modülü"""
    
    description = "Process analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Process bilgilerini analiz et"""
        data = {}
        
        try:
            # Çalışan processler
            data["running_processes"] = self._get_running_processes()
            
            # Process detayları
            data["process_details"] = self._get_process_details()
            
            # Process ağaç yapısı
            data["process_tree"] = self._get_process_tree()
            
            # Sistem servisleri
            data["system_services"] = self._get_system_services()
            
            # Açık dosyalar
            data["open_files"] = self._get_open_files()
            
            # Ağ bağlantıları
            data["network_connections"] = self._get_network_connections()
            
        except Exception as e:
            self.add_error(f"Process analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_running_processes(self) -> List[Dict[str, Any]]:
        """Çalışan processleri al"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    proc_info['create_time'] = proc.create_time()
                    proc_info['num_threads'] = proc.num_threads()
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.add_error(f"Çalışan processler alınırken hata: {str(e)}")
        
        return processes
    
    def _get_process_details(self) -> List[Dict[str, Any]]:
        """Detaylı process bilgileri"""
        details = []
        
        try:
            # En çok CPU kullanan processler
            top_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    # None değerleri kontrol et
                    cpu_percent = proc_info.get('cpu_percent', 0)
                    memory_percent = proc_info.get('memory_percent', 0)
                    
                    if cpu_percent is not None and cpu_percent > 0:
                        top_processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # CPU kullanımına göre sırala (None değerleri 0 olarak kabul et)
            top_processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
            details.append({
                "category": "top_cpu_processes",
                "processes": top_processes[:20]  # İlk 20
            })
            
            # En çok bellek kullanan processler
            memory_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    # None değerleri kontrol et
                    memory_percent = proc_info.get('memory_percent', 0)
                    
                    if memory_percent is not None and memory_percent > 0:
                        memory_processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            memory_processes.sort(key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)
            details.append({
                "category": "top_memory_processes",
                "processes": memory_processes[:20]  # İlk 20
            })
            
        except Exception as e:
            self.add_error(f"Process detayları alınırken hata: {str(e)}")
        
        return details
    
    def _get_process_tree(self) -> Dict[str, Any]:
        """Process ağaç yapısı"""
        tree = {}
        
        try:
            # PID 1'den başlayarak ağaç yapısını oluştur
            def build_tree(pid, depth=0):
                if depth > 10:  # Maksimum derinlik
                    return None
                
                try:
                    proc = psutil.Process(pid)
                    children = []
                    
                    for child in proc.children():
                        child_info = build_tree(child.pid, depth + 1)
                        if child_info:
                            children.append(child_info)
                    
                    return {
                        "pid": pid,
                        "name": proc.name(),
                        "status": proc.status(),
                        "children": children
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return None
            
            # PID 1 (launchd) ile başla
            result = build_tree(1)
            if result:
                tree = result
            
        except Exception as e:
            self.add_error(f"Process ağacı oluşturulurken hata: {str(e)}")
        
        return tree
    
    def _get_system_services(self) -> List[Dict[str, Any]]:
        """Sistem servisleri"""
        services = []
        
        try:
            # Launch daemons
            code, stdout, stderr = run_command("launchctl list")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines[1:]:  # İlk satırı atla (başlık)
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            services.append({
                                "pid": parts[0],
                                "status": parts[1],
                                "name": " ".join(parts[2:]) if len(parts) > 2 else "Unknown"
                            })
            
            # System daemons
            code, stdout, stderr = run_command("launchctl list | grep -E '^[0-9]+'")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            services.append({
                                "type": "system_daemon",
                                "pid": parts[0],
                                "status": parts[1],
                                "name": " ".join(parts[2:]) if len(parts) > 2 else "Unknown"
                            })
            
        except Exception as e:
            self.add_error(f"Sistem servisleri alınırken hata: {str(e)}")
        
        return services
    
    def _get_open_files(self) -> List[Dict[str, Any]]:
        """Açık dosyalar"""
        open_files = []
        
        try:
            # lsof komutu ile açık dosyaları al
            code, stdout, stderr = run_command("lsof")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines[1:]:  # İlk satırı atla (başlık)
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 9:
                            open_files.append({
                                "command": parts[0],
                                "pid": parts[1],
                                "user": parts[2],
                                "fd": parts[3],
                                "type": parts[4],
                                "device": parts[5],
                                "size": parts[6],
                                "node": parts[7],
                                "name": " ".join(parts[8:])
                            })
            
        except Exception as e:
            self.add_error(f"Açık dosyalar alınırken hata: {str(e)}")
        
        return open_files
    
    def _get_network_connections(self) -> List[Dict[str, Any]]:
        """Ağ bağlantıları"""
        connections = []
        
        try:
            # netstat ile aktif bağlantıları al
            code, stdout, stderr = run_command("netstat -an")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Proto'):
                        parts = line.split()
                        if len(parts) >= 4:
                            connections.append({
                                "protocol": parts[0],
                                "recv_q": parts[1],
                                "send_q": parts[2],
                                "local_address": parts[3],
                                "foreign_address": parts[4] if len(parts) > 4 else "",
                                "state": parts[5] if len(parts) > 5 else ""
                            })
            
            # lsof ile ağ bağlantılarını al
            code, stdout, stderr = run_command("lsof -i")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines[1:]:  # İlk satırı atla
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 9:
                            connections.append({
                                "command": parts[0],
                                "pid": parts[1],
                                "user": parts[2],
                                "fd": parts[3],
                                "type": parts[4],
                                "device": parts[5],
                                "size": parts[6],
                                "node": parts[7],
                                "name": parts[8]
                            })
            
        except Exception as e:
            self.add_error(f"Ağ bağlantıları alınırken hata: {str(e)}")
        
        return connections 