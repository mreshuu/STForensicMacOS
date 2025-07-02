"""
Sistem Bilgileri Modülü
"""

import os
import platform
import subprocess
from typing import Dict, Any, List
from .base_module import BaseModule
from ..utils.helpers import run_command, get_system_info


class SystemInfoModule(BaseModule):
    """Sistem bilgileri toplama modülü"""
    
    description = "Sistem bilgileri toplama"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Sistem bilgilerini analiz et"""
        data = {}
        
        try:
            # Temel sistem bilgileri
            data["basic_info"] = self._get_basic_system_info()
            
            # Donanım bilgileri
            data["hardware_info"] = self._get_hardware_info()
            
            # İşletim sistemi bilgileri
            data["os_info"] = self._get_os_info()
            
            # Sistem yapılandırması
            data["system_config"] = self._get_system_config()
            
            # Çevre değişkenleri
            data["environment"] = self._get_environment_info()
            
            # Sistem durumu
            data["system_status"] = self._get_system_status()
            
        except Exception as e:
            self.add_error(f"Sistem bilgileri alınırken hata: {str(e)}")
        
        return data
    
    def _get_basic_system_info(self) -> Dict[str, Any]:
        """Temel sistem bilgileri"""
        info = get_system_info()
        
        # Ek bilgiler
        info["uptime"] = self._get_uptime()
        info["load_average"] = self._get_load_average()
        info["timezone"] = self._get_timezone()
        
        return info
    
    def _get_hardware_info(self) -> Dict[str, Any]:
        """Donanım bilgileri"""
        hardware = {}
        
        try:
            # CPU bilgileri
            hardware["cpu"] = self._get_cpu_info()
            
            # Bellek bilgileri
            hardware["memory"] = self._get_memory_info()
            
            # Disk bilgileri
            hardware["disks"] = self._get_disk_info()
            
            # Ağ adaptörleri
            hardware["network_adapters"] = self._get_network_adapters()
            
            # USB cihazları
            hardware["usb_devices"] = self._get_usb_devices()
            
            # PCI cihazları
            hardware["pci_devices"] = self._get_pci_devices()
            
        except Exception as e:
            self.add_error(f"Donanım bilgileri alınırken hata: {str(e)}")
        
        return hardware
    
    def _get_os_info(self) -> Dict[str, Any]:
        """İşletim sistemi bilgileri"""
        os_info = {}
        
        try:
            # macOS özel bilgiler
            if platform.system() == "Darwin":
                # macOS versiyonu
                code, stdout, stderr = run_command("sw_vers")
                if code == 0:
                    lines = stdout.strip().split('\n')
                    for line in lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            os_info[key.strip()] = value.strip()
                
                # Kernel bilgileri
                code, stdout, stderr = run_command("uname -a")
                if code == 0:
                    os_info["kernel_info"] = stdout.strip()
                
                # Boot bilgileri
                code, stdout, stderr = run_command("system_profiler SPBootVolumeDataType")
                if code == 0:
                    os_info["boot_volume"] = self._parse_system_profiler(stdout)
                
                # Güvenlik ayarları
                os_info["security_settings"] = self._get_security_settings()
                
        except Exception as e:
            self.add_error(f"OS bilgileri alınırken hata: {str(e)}")
        
        return os_info
    
    def _get_system_config(self) -> Dict[str, Any]:
        """Sistem yapılandırması"""
        config = {}
        
        try:
            # Sistem ayarları
            code, stdout, stderr = run_command("defaults read com.apple.dock")
            if code == 0:
                config["dock_settings"] = "Available"
            
            # Kullanıcı ayarları
            config["user_preferences"] = self._get_user_preferences()
            
            # Sistem servisleri
            config["system_services"] = self._get_system_services()
            
        except Exception as e:
            self.add_error(f"Sistem yapılandırması alınırken hata: {str(e)}")
        
        return config
    
    def _get_cpu_info(self) -> Dict[str, Any]:
        """CPU bilgileri"""
        cpu_info = {}
        
        try:
            # CPU modeli
            code, stdout, stderr = run_command("sysctl -n machdep.cpu.brand_string")
            if code == 0 and stdout.strip():
                cpu_info["model"] = stdout.strip()
            
            # CPU çekirdek sayısı
            code, stdout, stderr = run_command("sysctl -n hw.ncpu")
            if code == 0 and stdout.strip():
                try:
                    cpu_info["cores"] = int(stdout.strip())
                except ValueError:
                    self.add_warning("CPU çekirdek sayısı alınamadı")
            
            # CPU hızı
            code, stdout, stderr = run_command("sysctl -n hw.cpufrequency")
            if code == 0 and stdout.strip():
                try:
                    freq = int(stdout.strip())
                    cpu_info["frequency_mhz"] = freq // 1000000
                except ValueError:
                    self.add_warning("CPU hızı alınamadı")
            
            # CPU mimarisi
            code, stdout, stderr = run_command("sysctl -n hw.machine")
            if code == 0 and stdout.strip():
                cpu_info["architecture"] = stdout.strip()
            
            # Alternatif CPU bilgileri
            if not cpu_info:
                code, stdout, stderr = run_command("system_profiler SPHardwareDataType")
                if code == 0:
                    cpu_info["hardware_info"] = self._parse_system_profiler(stdout)
            
        except Exception as e:
            self.add_error(f"CPU bilgileri alınırken hata: {str(e)}")
        
        return cpu_info
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Bellek bilgileri"""
        memory_info = {}
        
        try:
            # Toplam bellek
            code, stdout, stderr = run_command("sysctl -n hw.memsize")
            if code == 0:
                total_mem = int(stdout.strip())
                memory_info["total_bytes"] = total_mem
                memory_info["total_gb"] = total_mem // (1024**3)
            
            # Bellek kullanımı
            code, stdout, stderr = run_command("vm_stat")
            if code == 0:
                memory_info["vm_stat"] = self._parse_vm_stat(stdout)
            
        except Exception as e:
            self.add_error(f"Bellek bilgileri alınırken hata: {str(e)}")
        
        return memory_info
    
    def _get_disk_info(self) -> List[Dict[str, Any]]:
        """Disk bilgileri"""
        disks = []
        
        try:
            # Disk listesi
            code, stdout, stderr = run_command("diskutil list")
            if code == 0:
                disks = self._parse_diskutil_list(stdout)
            
        except Exception as e:
            self.add_error(f"Disk bilgileri alınırken hata: {str(e)}")
        
        return disks
    
    def _get_network_adapters(self) -> List[Dict[str, Any]]:
        """Ağ adaptörleri"""
        adapters = []
        
        try:
            # Ağ adaptörleri
            code, stdout, stderr = run_command("ifconfig")
            if code == 0:
                adapters = self._parse_ifconfig(stdout)
            
        except Exception as e:
            self.add_error(f"Ağ adaptörleri alınırken hata: {str(e)}")
        
        return adapters
    
    def _get_usb_devices(self) -> List[Dict[str, Any]]:
        """USB cihazları"""
        devices = []
        
        try:
            # USB cihazları
            code, stdout, stderr = run_command("system_profiler SPUSBDataType")
            if code == 0:
                parsed = self._parse_system_profiler(stdout)
                if isinstance(parsed, list):
                    devices = parsed
                else:
                    devices = [parsed]
            
        except Exception as e:
            self.add_error(f"USB cihazları alınırken hata: {str(e)}")
        
        return devices
    
    def _get_pci_devices(self) -> List[Dict[str, Any]]:
        """PCI cihazları"""
        devices = []
        
        try:
            # PCI cihazları
            code, stdout, stderr = run_command("system_profiler SPPCIDataType")
            if code == 0:
                parsed = self._parse_system_profiler(stdout)
                if isinstance(parsed, list):
                    devices = parsed
                else:
                    devices = [parsed]
            
        except Exception as e:
            self.add_error(f"PCI cihazları alınırken hata: {str(e)}")
        
        return devices
    
    def _get_uptime(self) -> str:
        """Sistem çalışma süresi"""
        try:
            code, stdout, stderr = run_command("uptime")
            if code == 0:
                return stdout.strip()
        except Exception:
            pass
        return "Unknown"
    
    def _get_load_average(self) -> List[float]:
        """Sistem yükü"""
        try:
            code, stdout, stderr = run_command("sysctl -n vm.loadavg")
            if code == 0:
                load_str = stdout.strip()
                return [float(x) for x in load_str.split()]
        except Exception:
            pass
        return [0.0, 0.0, 0.0]
    
    def _get_timezone(self) -> str:
        """Zaman dilimi"""
        try:
            return os.environ.get('TZ', 'Unknown')
        except Exception:
            return "Unknown"
    
    def _get_security_settings(self) -> Dict[str, Any]:
        """Güvenlik ayarları"""
        security = {}
        
        try:
            # FileVault durumu
            code, stdout, stderr = run_command("fdesetup status")
            if code == 0:
                security["filevault"] = stdout.strip()
            
            # SIP durumu
            code, stdout, stderr = run_command("csrutil status")
            if code == 0:
                security["sip"] = stdout.strip()
            
            # Gatekeeper durumu
            code, stdout, stderr = run_command("spctl --status")
            if code == 0:
                security["gatekeeper"] = stdout.strip()
            
        except Exception as e:
            self.add_error(f"Güvenlik ayarları alınırken hata: {str(e)}")
        
        return security
    
    def _get_user_preferences(self) -> Dict[str, Any]:
        """Kullanıcı ayarları"""
        preferences = {}
        
        try:
            # Dock ayarları
            code, stdout, stderr = run_command("defaults read com.apple.dock")
            if code == 0:
                preferences["dock"] = "Available"
            
            # Finder ayarları
            code, stdout, stderr = run_command("defaults read com.apple.finder")
            if code == 0:
                preferences["finder"] = "Available"
            
        except Exception as e:
            self.add_error(f"Kullanıcı ayarları alınırken hata: {str(e)}")
        
        return preferences
    
    def _get_system_services(self) -> List[str]:
        """Sistem servisleri"""
        services = []
        
        try:
            # Launch daemons
            code, stdout, stderr = run_command("launchctl list")
            if code == 0:
                services = stdout.strip().split('\n')
            
        except Exception as e:
            self.add_error(f"Sistem servisleri alınırken hata: {str(e)}")
        
        return services
    
    def _get_environment_info(self) -> Dict[str, Any]:
        """Çevre değişkenleri"""
        env = {}
        
        try:
            # Önemli çevre değişkenleri
            important_vars = ['PATH', 'HOME', 'USER', 'SHELL', 'TERM', 'LANG', 'TZ']
            
            for var in important_vars:
                if var in os.environ:
                    env[var] = os.environ[var]
            
        except Exception as e:
            self.add_error(f"Çevre değişkenleri alınırken hata: {str(e)}")
        
        return env
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Sistem durumu"""
        status = {}
        
        try:
            # CPU kullanımı
            code, stdout, stderr = run_command("top -l 1 -n 0")
            if code == 0:
                status["cpu_usage"] = self._parse_top_output(stdout)
            
            # Bellek kullanımı
            code, stdout, stderr = run_command("vm_stat")
            if code == 0:
                status["memory_usage"] = self._parse_vm_stat(stdout)
            
        except Exception as e:
            self.add_error(f"Sistem durumu alınırken hata: {str(e)}")
        
        return status
    
    def _parse_system_profiler(self, output: str) -> Dict[str, Any]:
        """system_profiler çıktısını parse et"""
        # Basit parse - gerçek uygulamada daha gelişmiş olabilir
        return {"raw_output": output[:1000] + "..." if len(output) > 1000 else output}
    
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
    
    def _parse_diskutil_list(self, output: str) -> List[Dict[str, Any]]:
        """diskutil list çıktısını parse et"""
        disks = []
        
        try:
            lines = output.strip().split('\n')
            current_disk = {}
            
            for line in lines:
                if line.strip().startswith('/dev/'):
                    if current_disk:
                        disks.append(current_disk)
                    current_disk = {"device": line.strip()}
                elif current_disk and line.strip():
                    current_disk["info"] = line.strip()
            
            if current_disk:
                disks.append(current_disk)
                
        except Exception:
            pass
        
        return disks
    
    def _parse_ifconfig(self, output: str) -> List[Dict[str, Any]]:
        """ifconfig çıktısını parse et"""
        adapters = []
        
        try:
            lines = output.strip().split('\n')
            current_adapter = {}
            
            for line in lines:
                if line and not line.startswith('\t'):
                    if current_adapter:
                        adapters.append(current_adapter)
                    current_adapter = {"name": line.split(':')[0]}
                elif current_adapter and line.strip():
                    current_adapter["details"] = line.strip()
            
            if current_adapter:
                adapters.append(current_adapter)
                
        except Exception:
            pass
        
        return adapters
    
    def _parse_top_output(self, output: str) -> Dict[str, Any]:
        """top çıktısını parse et"""
        # Basit parse - gerçek uygulamada daha gelişmiş olabilir
        return {"raw_output": output[:500] + "..." if len(output) > 500 else output} 