"""
Bellek Analizi Modülü
"""

import os
import psutil
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_module import BaseModule
from ..utils.helpers import run_command, format_size


class MemoryModule(BaseModule):
    """Bellek analizi modülü"""
    
    description = "Bellek analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Bellek bilgilerini analiz et"""
        data = {}
        
        try:
            # RAM durumu
            data["ram_status"] = self._get_ram_status()
            
            # Bellek kullanımı
            data["memory_usage"] = self._get_memory_usage()
            
            # Kernel modülleri
            data["kernel_modules"] = self._get_kernel_modules()
            
            # Bellek haritası
            data["memory_map"] = self._get_memory_map()
            
            # Swap durumu
            data["swap_status"] = self._get_swap_status()
            
            # Bellek istatistikleri
            data["memory_stats"] = self._get_memory_stats()
            
            # Bellek dump (opsiyonel)
            if isinstance(args, dict) and args.get('dump_memory'):
                data["memory_dump"] = self._create_memory_dump(args)
            
        except Exception as e:
            self.add_error(f"Bellek analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_ram_status(self) -> Dict[str, Any]:
        """RAM durumu"""
        ram_status = {}
        
        try:
            # Toplam RAM
            total_ram = psutil.virtual_memory().total
            ram_status["total_ram"] = {
                "bytes": total_ram,
                "formatted": format_size(total_ram)
            }
            
            # Kullanılabilir RAM
            available_ram = psutil.virtual_memory().available
            ram_status["available_ram"] = {
                "bytes": available_ram,
                "formatted": format_size(available_ram)
            }
            
            # Kullanılan RAM
            used_ram = psutil.virtual_memory().used
            ram_status["used_ram"] = {
                "bytes": used_ram,
                "formatted": format_size(used_ram)
            }
            
            # RAM kullanım yüzdesi
            ram_status["usage_percent"] = psutil.virtual_memory().percent
            
            # RAM türü ve hızı
            try:
                code, stdout, stderr = run_command("system_profiler SPHardwareDataType | grep -E 'Memory|RAM'")
                if code == 0:
                    ram_status["hardware_info"] = stdout.strip()
            except Exception:
                pass
            
        except Exception as e:
            self.add_error(f"RAM durumu alınırken hata: {str(e)}")
        
        return ram_status
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Bellek kullanımı"""
        memory_usage = {}
        
        try:
            # vm_stat çıktısı
            code, stdout, stderr = run_command("vm_stat")
            if code == 0:
                memory_usage["vm_stat"] = self._parse_vm_stat(stdout)
            
            # En çok bellek kullanan processler
            memory_usage["top_memory_processes"] = self._get_top_memory_processes()
            
            # Bellek kullanım grafiği
            memory_usage["usage_trend"] = self._get_memory_usage_trend()
            
        except Exception as e:
            self.add_error(f"Bellek kullanımı alınırken hata: {str(e)}")
        
        return memory_usage
    
    def _get_kernel_modules(self) -> List[Dict[str, Any]]:
        """Kernel modülleri"""
        modules = []
        
        try:
            # Yüklü kernel modülleri
            code, stdout, stderr = run_command("kextstat")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines[1:]:  # İlk satırı atla
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            modules.append({
                                "index": parts[0],
                                "refs": parts[1],
                                "size": parts[2],
                                "name": parts[3],
                                "version": parts[4] if len(parts) > 4 else "Unknown"
                            })
            
            # Kernel extension bilgileri
            code, stdout, stderr = run_command("system_profiler SPKernelExtensionsDataType")
            if code == 0:
                modules.append({
                    "type": "kernel_extensions_info",
                    "data": stdout.strip()[:1000] + "..." if len(stdout) > 1000 else stdout.strip()
                })
            
        except Exception as e:
            self.add_error(f"Kernel modülleri alınırken hata: {str(e)}")
        
        return modules
    
    def _get_memory_map(self) -> Dict[str, Any]:
        """Bellek haritası"""
        memory_map = {}
        
        try:
            # Process bellek haritası (PID 1 için örnek)
            code, stdout, stderr = run_command("vmmap 1")
            if code == 0:
                memory_map["process_1_map"] = stdout.strip()[:2000] + "..." if len(stdout) > 2000 else stdout.strip()
            
            # Sistem bellek haritası
            code, stdout, stderr = run_command("vm_stat -c 1 1")
            if code == 0:
                memory_map["system_memory_stats"] = stdout.strip()
            
            # Bellek bölgeleri
            memory_map["memory_regions"] = self._get_memory_regions()
            
        except Exception as e:
            self.add_error(f"Bellek haritası alınırken hata: {str(e)}")
        
        return memory_map
    
    def _get_swap_status(self) -> Dict[str, Any]:
        """Swap durumu"""
        swap_status = {}
        
        try:
            # Swap kullanımı
            swap = psutil.swap_memory()
            swap_status["total"] = {
                "bytes": swap.total,
                "formatted": format_size(swap.total)
            }
            swap_status["used"] = {
                "bytes": swap.used,
                "formatted": format_size(swap.used)
            }
            swap_status["free"] = {
                "bytes": swap.free,
                "formatted": format_size(swap.free)
            }
            swap_status["percent"] = swap.percent
            
            # Swap dosyaları
            code, stdout, stderr = run_command("sysctl vm.swapusage")
            if code == 0:
                swap_status["swap_usage_info"] = stdout.strip()
            
        except Exception as e:
            self.add_error(f"Swap durumu alınırken hata: {str(e)}")
        
        return swap_status
    
    def _get_memory_stats(self) -> Dict[str, Any]:
        """Bellek istatistikleri"""
        stats = {}
        
        try:
            # Bellek basıncı
            code, stdout, stderr = run_command("memory_pressure")
            if code == 0:
                stats["memory_pressure"] = stdout.strip()
            
            # Bellek kullanım istatistikleri
            vm = psutil.virtual_memory()
            stats["detailed_stats"] = {
                "total": format_size(vm.total),
                "available": format_size(vm.available),
                "used": format_size(vm.used),
                "free": format_size(vm.free),
                "percent": vm.percent,
                "cached": format_size(getattr(vm, 'cached', 0)),
                "buffers": format_size(getattr(vm, 'buffers', 0)),
                "shared": format_size(getattr(vm, 'shared', 0))
            }
            
            # Bellek performans metrikleri
            stats["performance_metrics"] = self._get_memory_performance_metrics()
            
        except Exception as e:
            self.add_error(f"Bellek istatistikleri alınırken hata: {str(e)}")
        
        return stats
    
    def _get_top_memory_processes(self) -> List[Dict[str, Any]]:
        """En çok bellek kullanan processler"""
        processes = []
        
        try:
            # En çok bellek kullanan 20 process
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
                try:
                    proc_info = proc.info
                    if proc_info['memory_percent'] and proc_info['memory_percent'] > 0:
                        processes.append({
                            "pid": proc_info['pid'],
                            "name": proc_info['name'],
                            "memory_percent": proc_info['memory_percent'],
                            "memory_rss": format_size(proc_info['memory_info'].rss),
                            "memory_vms": format_size(proc_info['memory_info'].vms)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Bellek kullanımına göre sırala
            processes.sort(key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)
            return processes[:20]
            
        except Exception as e:
            self.add_error(f"En çok bellek kullanan processler alınırken hata: {str(e)}")
            return []
    
    def _get_memory_usage_trend(self) -> List[Dict[str, Any]]:
        """Bellek kullanım trendi"""
        trend = []
        
        try:
            # Son 10 ölçüm
            for i in range(10):
                vm = psutil.virtual_memory()
                trend.append({
                    "timestamp": datetime.now().isoformat(),
                    "used_percent": vm.percent,
                    "used_bytes": vm.used,
                    "available_bytes": vm.available
                })
                import time
                time.sleep(0.1)  # Kısa bekleme
            
        except Exception as e:
            self.add_error(f"Bellek kullanım trendi alınırken hata: {str(e)}")
        
        return trend
    
    def _get_memory_regions(self) -> List[Dict[str, Any]]:
        """Bellek bölgeleri"""
        regions = []
        
        try:
            # Bellek bölgeleri (basit analiz)
            code, stdout, stderr = run_command("vm_stat")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        regions.append({
                            "region": key.strip(),
                            "value": value.strip()
                        })
            
        except Exception as e:
            self.add_error(f"Bellek bölgeleri alınırken hata: {str(e)}")
        
        return regions
    
    def _get_memory_performance_metrics(self) -> Dict[str, Any]:
        """Bellek performans metrikleri"""
        metrics = {}
        
        try:
            # Bellek performans bilgileri
            code, stdout, stderr = run_command("sysctl -a | grep vm.")
            if code == 0:
                vm_settings = {}
                lines = stdout.strip().split('\n')
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        vm_settings[key.strip()] = value.strip()
                
                metrics["vm_settings"] = vm_settings
            
            # Bellek kullanım oranları
            vm = psutil.virtual_memory()
            metrics["usage_ratios"] = {
                "used_to_total": vm.used / vm.total if vm.total > 0 else 0,
                "available_to_total": vm.available / vm.total if vm.total > 0 else 0,
                "free_to_total": vm.free / vm.total if vm.total > 0 else 0
            }
            
        except Exception as e:
            self.add_error(f"Bellek performans metrikleri alınırken hata: {str(e)}")
        
        return metrics
    
    def _create_memory_dump(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Bellek dump oluştur (opsiyonel)"""
        dump_info = {}
        
        try:
            # Dump boyutu kontrolü
            available_memory = psutil.virtual_memory().available
            max_dump_size = args.get("max_dump_size", 1024 * 1024 * 1024)  # 1GB default
            
            if available_memory < max_dump_size:
                dump_info["warning"] = f"Yetersiz bellek: {format_size(available_memory)} mevcut, {format_size(max_dump_size)} gerekli"
                return dump_info
            
            # Dump dosyası yolu
            dump_path = args.get("dump_path", "./memory_dump.bin")
            
            # Not: Gerçek bellek dump için özel araçlar gerekir
            # Bu sadece örnek bir implementasyon
            dump_info["note"] = "Memory dump requires specialized tools like volatility, rekall, or system-specific dump utilities"
            dump_info["recommended_tools"] = [
                "volatility",
                "rekall",
                "memoryze",
                "winpmem",
                "osxpmem"
            ]
            dump_info["dump_path"] = dump_path
            dump_info["estimated_size"] = format_size(psutil.virtual_memory().total)
            
        except Exception as e:
            self.add_error(f"Bellek dump oluşturulurken hata: {str(e)}")
        
        return dump_info
    
    def _parse_vm_stat(self, output: str) -> Dict[str, Any]:
        """vm_stat çıktısını parse et"""
        vm_stats = {}
        
        try:
            lines = output.strip().split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    vm_stats[key.strip()] = value.strip()
        except Exception:
            pass
        
        return vm_stats 