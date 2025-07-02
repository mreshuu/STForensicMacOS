"""
Network Analizi Modülü
"""

import os
import socket
import psutil
from typing import Dict, Any, List
from .base_module import BaseModule
from ..utils.helpers import run_command


class NetworkModule(BaseModule):
    """Network analizi modülü"""
    
    description = "Network analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Network bilgilerini analiz et"""
        data = {}
        
        try:
            # Ağ arayüzleri
            data["network_interfaces"] = self._get_network_interfaces()
            
            # Aktif bağlantılar
            data["active_connections"] = self._get_active_connections()
            
            # Routing tablosu
            data["routing_table"] = self._get_routing_table()
            
            # DNS bilgileri
            data["dns_info"] = self._get_dns_info()
            
            # ARP tablosu
            data["arp_table"] = self._get_arp_table()
            
            # Firewall kuralları
            data["firewall_rules"] = self._get_firewall_rules()
            
            # Ağ istatistikleri
            data["network_stats"] = self._get_network_stats()
            
        except Exception as e:
            self.add_error(f"Network analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_network_interfaces(self) -> List[Dict[str, Any]]:
        """Ağ arayüzleri"""
        interfaces = []
        
        try:
            # ifconfig ile ağ arayüzlerini al
            code, stdout, stderr = run_command("ifconfig")
            if code == 0:
                current_interface = {}
                lines = stdout.strip().split('\n')
                
                for line in lines:
                    if line and not line.startswith('\t'):
                        if current_interface:
                            interfaces.append(current_interface)
                        current_interface = {"name": line.split(':')[0]}
                    elif current_interface and line.strip():
                        if 'inet ' in line:
                            parts = line.strip().split()
                            for i, part in enumerate(parts):
                                if part == 'inet':
                                    current_interface['ip_address'] = parts[i + 1]
                                elif part == 'netmask':
                                    current_interface['netmask'] = parts[i + 1]
                        elif 'ether' in line:
                            parts = line.strip().split()
                            for i, part in enumerate(parts):
                                if part == 'ether':
                                    current_interface['mac_address'] = parts[i + 1]
                
                if current_interface:
                    interfaces.append(current_interface)
            
            # psutil ile ek bilgiler
            for interface in interfaces:
                try:
                    if 'name' in interface:
                        if_stats = psutil.net_if_stats().get(interface['name'])
                        if if_stats:
                            interface['status'] = 'up' if if_stats.isup else 'down'
                            interface['speed'] = if_stats.speed
                            interface['mtu'] = if_stats.mtu
                except Exception:
                    pass
                    
        except Exception as e:
            self.add_error(f"Ağ arayüzleri alınırken hata: {str(e)}")
        
        return interfaces
    
    def _get_active_connections(self) -> List[Dict[str, Any]]:
        """Aktif ağ bağlantıları"""
        connections = []
        try:
            code, stdout, stderr = run_command("netstat -an")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not (line.startswith('tcp') or line.startswith('udp')):
                        continue
                    parts = line.split()
                    if len(parts) < 5:
                        continue
                    # Local ve foreign address parse
                    local_addr = self._parse_address(parts[3])
                    foreign_addr = self._parse_address(parts[4])
                    state = parts[5] if len(parts) > 5 else ""
                    connections.append({
                        "protocol": parts[0],
                        "recv_q": parts[1],
                        "send_q": parts[2],
                        "local_address": local_addr,
                        "foreign_address": foreign_addr,
                        "state": state
                    })
        except Exception as e:
            self.add_error(f"Aktif bağlantılar alınırken hata: {str(e)}")
        return connections
    
    def _parse_address(self, address_str: str) -> Dict[str, str]:
        """IP adresi ve port numarasını ayrıştır (IPv4/IPv6 uyumlu)"""
        try:
            # IPv6: 2a00:1880:a08a:8.59239 veya 2a00:1880:a08a:8:0:0:0:1.443
            if ':' in address_str and address_str.count('.') == 1:
                # IPv6 + port (son . sonrası port)
                ip, port = address_str.rsplit('.', 1)
                return {"ip": ip, "port": port}
            elif address_str.count('.') == 4:
                # IPv4 + port
                parts = address_str.split('.')
                ip = '.'.join(parts[:4])
                port = parts[4]
                return {"ip": ip, "port": port}
            elif address_str.count('.') == 1 and address_str.count(':') == 0:
                # 127.0.0.1.80 gibi
                ip, port = address_str.rsplit('.', 1)
                return {"ip": ip, "port": port}
            elif address_str == '*.*':
                return {"ip": "*", "port": "*"}
            else:
                return {"ip": address_str, "port": ""}
        except Exception:
            return {"ip": address_str, "port": ""}
    
    def _get_routing_table(self) -> List[Dict[str, Any]]:
        """Routing tablosu"""
        routes = []
        
        try:
            # netstat ile routing tablosunu al
            code, stdout, stderr = run_command("netstat -rn")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Routing'):
                        parts = line.split()
                        if len(parts) >= 4:
                            routes.append({
                                "destination": parts[0],
                                "gateway": parts[1],
                                "flags": parts[2],
                                "interface": parts[3]
                            })
            
        except Exception as e:
            self.add_error(f"Routing tablosu alınırken hata: {str(e)}")
        
        return routes
    
    def _get_dns_info(self) -> Dict[str, Any]:
        """DNS bilgileri"""
        dns_info = {}
        
        try:
            # DNS sunucuları
            code, stdout, stderr = run_command("cat /etc/resolv.conf")
            if code == 0:
                lines = stdout.strip().split('\n')
                dns_servers = []
                for line in lines:
                    if line.startswith('nameserver'):
                        dns_servers.append(line.split()[1])
                dns_info['nameservers'] = dns_servers
            
            # DNS cache
            code, stdout, stderr = run_command("dscacheutil -cachedump -entries Host")
            if code == 0:
                dns_info['dns_cache'] = stdout.strip()
            
            # Hostname
            dns_info['hostname'] = socket.gethostname()
            
            # FQDN
            try:
                dns_info['fqdn'] = socket.getfqdn()
            except Exception:
                dns_info['fqdn'] = dns_info['hostname']
            
        except Exception as e:
            self.add_error(f"DNS bilgileri alınırken hata: {str(e)}")
        
        return dns_info
    
    def _get_arp_table(self) -> List[Dict[str, Any]]:
        """ARP tablosu"""
        arp_table = []
        
        try:
            # arp komutu ile ARP tablosunu al
            code, stdout, stderr = run_command("arp -a")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            arp_table.append({
                                "hostname": parts[0].strip('()'),
                                "ip_address": parts[1].strip('()'),
                                "mac_address": parts[3],
                                "interface": parts[5] if len(parts) > 5 else ""
                            })
            
        except Exception as e:
            self.add_error(f"ARP tablosu alınırken hata: {str(e)}")
        
        return arp_table
    
    def _get_firewall_rules(self) -> Dict[str, Any]:
        """Firewall kuralları"""
        firewall = {}
        
        try:
            # pfctl ile firewall kurallarını al
            code, stdout, stderr = run_command("pfctl -s rules")
            if code == 0:
                firewall['pf_rules'] = stdout.strip()
            
            # pfctl ile firewall durumunu al
            code, stdout, stderr = run_command("pfctl -s info")
            if code == 0:
                firewall['pf_info'] = stdout.strip()
            
            # Application Firewall durumu
            code, stdout, stderr = run_command("defaults read /Library/Preferences/com.apple.alf globalstate")
            if code == 0:
                firewall['app_firewall_state'] = stdout.strip()
            
        except Exception as e:
            self.add_error(f"Firewall kuralları alınırken hata: {str(e)}")
        
        return firewall
    
    def _get_network_stats(self) -> Dict[str, Any]:
        """Ağ istatistikleri"""
        stats = {}
        
        try:
            # netstat ile istatistikleri al
            code, stdout, stderr = run_command("netstat -i")
            if code == 0:
                lines = stdout.strip().split('\n')
                interface_stats = []
                for line in lines[1:]:  # İlk satırı atla
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 10:
                            interface_stats.append({
                                "interface": parts[0],
                                "mtu": parts[1],
                                "network": parts[2],
                                "address": parts[3],
                                "ipkts": parts[4],
                                "ierrs": parts[5],
                                "opkts": parts[6],
                                "oerrs": parts[7],
                                "colls": parts[8]
                            })
                stats['interface_stats'] = interface_stats
            
            # psutil ile ağ istatistikleri
            net_io = psutil.net_io_counters()
            stats['network_io'] = {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            }
            
        except Exception as e:
            self.add_error(f"Ağ istatistikleri alınırken hata: {str(e)}")
        
        return stats 