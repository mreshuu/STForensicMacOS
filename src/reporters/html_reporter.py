"""
HTML Raporlayıcı - Gelişmiş Tablo Tabanlı Rapor
"""

import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class HTMLReporter:
    """HTML formatında gelişmiş rapor oluşturucu"""
    
    def __init__(self, config, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def generate_report(self, results: Dict[str, Any], output_path: str):
        """HTML raporu oluştur"""
        try:
            # Rapor verilerini hazırla
            report_data = self._prepare_report_data(results)
            
            # HTML şablonunu oluştur
            html_content = self._generate_html_template(report_data)
            
            # HTML dosyasına yaz
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML raporu oluşturuldu: {output_path}")
            
        except Exception as e:
            self.logger.error(f"HTML raporu oluşturma hatası: {str(e)}")
            raise
    
    def _prepare_report_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Rapor verilerini hazırla"""
        report_data = {
            "report_info": {
                "tool": "STForensicMacOS",
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat(),
                "format": "html"
            },
            "analysis_info": results.get("analysis_info", {}),
            "summary": results.get("summary", {}),
            "modules": {}
        }
        
        # Modül sonuçlarını ekle
        for module_name, module_result in results.get("modules", {}).items():
            report_data["modules"][module_name] = {
                "name": module_result.get("module", module_name),
                "description": module_result.get("description", ""),
                "version": module_result.get("version", ""),
                "status": module_result.get("status", "unknown"),
                "start_time": module_result.get("start_time"),
                "end_time": module_result.get("end_time"),
                "duration": module_result.get("duration", 0),
                "data_count": len(module_result.get("data", {})),
                "errors": module_result.get("errors", []),
                "warnings": module_result.get("warnings", []),
                "data": module_result.get("data", {})
            }
        
        return report_data
    
    def _generate_html_template(self, report_data: Dict[str, Any]) -> str:
        """HTML şablonunu oluştur"""
        html_template = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STForensicMacOS - Forensic Raporu</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 4px solid #667eea;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .card h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}
        
        .modules-section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .module {{
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            margin-bottom: 25px;
            overflow: hidden;
            background: white;
        }}
        
        .module-header {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s ease;
        }}
        
        .module-header:hover {{
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        }}
        
        .module-title {{
            font-weight: bold;
            color: #333;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .module-status {{
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        
        .status-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .status-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .module-content {{
            padding: 0;
            display: none;
        }}
        
        .module-content.active {{
            display: block;
        }}
        
        .data-section {{
            margin-bottom: 25px;
            padding: 20px;
        }}
        
        .data-section h4 {{
            color: #667eea;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .data-table th,
        .data-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .data-table th {{
            background: #667eea;
            color: white;
            font-weight: bold;
            font-size: 0.95em;
        }}
        
        .data-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .search-box {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin-bottom: 25px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: #666;
            border-top: 1px solid #e0e0e0;
            margin-top: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .stat-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }}
        
        .error-list {{
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
        }}
        
        .warning-list {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
        }}
        
        .error-list li,
        .warning-list li {{
            margin-bottom: 8px;
            padding-left: 10px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .summary-cards {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-search"></i> STForensicMacOS</h1>
            <p>MacOS Forensic Analysis Report</p>
            <p>Generated: {report_data['report_info']['generated_at']}</p>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <h3><i class="fas fa-cubes"></i> Total Modules</h3>
                <div class="value">{report_data['summary'].get('total_modules', 0)}</div>
            </div>
            <div class="card">
                <h3><i class="fas fa-check-circle"></i> Successful</h3>
                <div class="value">{report_data['summary'].get('successful_modules', 0)}</div>
            </div>
            <div class="card">
                <h3><i class="fas fa-times-circle"></i> Failed</h3>
                <div class="value">{report_data['summary'].get('failed_modules', 0)}</div>
            </div>
            <div class="card">
                <h3><i class="fas fa-clock"></i> Duration</h3>
                <div class="value">{report_data['summary'].get('total_duration', 0):.2f}s</div>
            </div>
        </div>
        
        <div class="modules-section">
            <h2><i class="fas fa-list"></i> Module Results</h2>
            <input type="text" class="search-box" id="searchBox" placeholder="Search modules...">
            
            {self._generate_modules_html(report_data['modules'])}
        </div>
        
        <div class="footer">
            <p>Generated by STForensicMacOS v{report_data['report_info']['version']}</p>
            <p>© 2025 STForensic Team</p>
        </div>
    </div>
    
    <script>
        // Module toggle functionality
        document.querySelectorAll('.module-header').forEach(header => {{
            header.addEventListener('click', () => {{
                const content = header.nextElementSibling;
                content.classList.toggle('active');
            }});
        }});
        
        // Search functionality
        document.getElementById('searchBox').addEventListener('input', (e) => {{
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.module').forEach(module => {{
                const title = module.querySelector('.module-title').textContent.toLowerCase();
                if (title.includes(searchTerm)) {{
                    module.style.display = 'block';
                }} else {{
                    module.style.display = 'none';
                }}
            }});
        }});
        
        // Auto-expand modules with errors
        document.querySelectorAll('.module').forEach(module => {{
            const status = module.querySelector('.module-status');
            if (status && status.textContent.includes('error')) {{
                const content = module.querySelector('.module-content');
                content.classList.add('active');
            }}
        }});
    </script>
</body>
</html>
        """
        
        return html_template
    
    def _generate_modules_html(self, modules: Dict[str, Any]) -> str:
        """Modüller için HTML oluştur"""
        modules_html = ""
        
        for module_name, module_data in modules.items():
            status_class = f"status-{module_data['status']}"
            status_text = module_data['status'].upper()
            
            # Modül ikonu belirle
            module_icon = self._get_module_icon(module_name)
            
            modules_html += f"""
            <div class="module">
                <div class="module-header">
                    <div class="module-title">{module_icon} {module_data['name']}</div>
                    <div class="module-status {status_class}">{status_text}</div>
                </div>
                <div class="module-content">
                    <div class="data-section">
                        <h4><i class="fas fa-info-circle"></i> Module Information</h4>
                        <table class="data-table">
                            <tr><th>Property</th><th>Value</th></tr>
                            <tr><td>Description</td><td>{module_data['description']}</td></tr>
                            <tr><td>Version</td><td>{module_data['version']}</td></tr>
                            <tr><td>Start Time</td><td>{module_data['start_time']}</td></tr>
                            <tr><td>End Time</td><td>{module_data['end_time']}</td></tr>
                            <tr><td>Duration</td><td>{module_data['duration']:.2f}s</td></tr>
                            <tr><td>Data Count</td><td>{module_data['data_count']}</td></tr>
                        </table>
                    </div>
            """
            
            # Errors
            if module_data['errors']:
                modules_html += f"""
                    <div class="data-section">
                        <h4><i class="fas fa-exclamation-triangle"></i> Errors ({len(module_data['errors'])})</h4>
                        <div class="error-list">
                            <ul>
                """
                for error in module_data['errors']:
                    modules_html += f"<li>{error}</li>"
                modules_html += "</ul></div></div>"
            
            # Warnings
            if module_data['warnings']:
                modules_html += f"""
                    <div class="data-section">
                        <h4><i class="fas fa-exclamation-circle"></i> Warnings ({len(module_data['warnings'])})</h4>
                        <div class="warning-list">
                            <ul>
                """
                for warning in module_data['warnings']:
                    modules_html += f"<li>{warning}</li>"
                modules_html += "</ul></div></div>"
            
            # Data - Modül bazlı tablolar
            if module_data['data']:
                modules_html += self._generate_module_data_tables(module_name, module_data['data'])
            
            modules_html += "</div></div>"
        
        return modules_html
    
    def _get_module_icon(self, module_name: str) -> str:
        """Modül için ikon belirle"""
        icons = {
            "system_info": '<i class="fas fa-desktop"></i>',
            "processes": '<i class="fas fa-tasks"></i>',
            "network": '<i class="fas fa-network-wired"></i>',
            "users": '<i class="fas fa-users"></i>',
            "filesystem": '<i class="fas fa-folder-tree"></i>',
            "memory": '<i class="fas fa-memory"></i>',
            "logs": '<i class="fas fa-file-alt"></i>',
            "timeline": '<i class="fas fa-clock"></i>'
        }
        return icons.get(module_name, '<i class="fas fa-cube"></i>')
    
    def _generate_module_data_tables(self, module_name: str, data: Dict[str, Any]) -> str:
        """Modül verilerini tablolar halinde oluştur"""
        tables_html = ""
        
        if module_name == "system_info":
            tables_html += self._generate_system_info_tables(data)
        elif module_name == "processes":
            tables_html += self._generate_processes_tables(data)
        elif module_name == "network":
            tables_html += self._generate_network_tables(data)
        elif module_name == "users":
            tables_html += self._generate_users_tables(data)
        elif module_name == "filesystem":
            tables_html += self._generate_filesystem_tables(data)
        elif module_name == "memory":
            tables_html += self._generate_memory_tables(data)
        elif module_name == "logs":
            tables_html += self._generate_logs_tables(data)
        elif module_name == "timeline":
            tables_html += self._generate_timeline_tables(data)
        else:
            # Genel JSON görünümü
            tables_html += f"""
                <div class="data-section">
                    <h4><i class="fas fa-database"></i> Data</h4>
                    <pre style="background: #f8f9fa; padding: 15px; border-radius: 8px; overflow-x: auto;">{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
                </div>
            """
        
        return tables_html
    
    def _generate_system_info_tables(self, data: Dict[str, Any]) -> str:
        """System Info tabloları"""
        tables_html = ""
        
        # Temel sistem bilgileri
        if "basic_info" in data:
            basic_info = data["basic_info"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-info-circle"></i> Basic System Information</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in basic_info.items():
                if isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        # Donanım bilgileri
        if "hardware_info" in data:
            hardware = data["hardware_info"]
            if "cpu" in hardware:
                tables_html += """
                    <div class="data-section">
                        <h4><i class="fas fa-microchip"></i> CPU Information</h4>
                        <table class="data-table">
                            <tr><th>Property</th><th>Value</th></tr>
                """
                for key, value in hardware["cpu"].items():
                    if isinstance(value, (str, int, float)):
                        tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
                tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_processes_tables(self, data: Dict[str, Any]) -> str:
        """Processes tabloları"""
        tables_html = ""
        
        # Çalışan processler
        if "running_processes" in data and data["running_processes"]:
            processes = data["running_processes"][:20]  # İlk 20 process
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-tasks"></i> Running Processes (Top 20)</h4>
                    <table class="data-table">
                        <tr><th>PID</th><th>Name</th><th>Status</th><th>CPU %</th><th>Memory %</th><th>Threads</th><th>Create Time</th></tr>
            """
            for proc in processes:
                create_time = proc.get('create_time', 'N/A')
                if isinstance(create_time, (int, float)):
                    from datetime import datetime
                    create_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                
                tables_html += f"""
                    <tr>
                        <td>{proc.get('pid', 'N/A')}</td>
                        <td>{proc.get('name', 'N/A')}</td>
                        <td>{proc.get('status', 'N/A')}</td>
                        <td>{proc.get('cpu_percent', 'N/A')}</td>
                        <td>{proc.get('memory_percent', 'N/A')}</td>
                        <td>{proc.get('num_threads', 'N/A')}</td>
                        <td>{create_time}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Process detayları
        if "process_details" in data and data["process_details"]:
            details = data["process_details"]
            for detail in details:
                if "processes" in detail and detail["processes"]:
                    category = detail.get("category", "Unknown")
                    processes = detail["processes"][:10]  # İlk 10 process
                    tables_html += f"""
                        <div class="data-section">
                            <h4><i class="fas fa-chart-line"></i> {category.replace('_', ' ').title()}</h4>
                            <table class="data-table">
                                <tr><th>PID</th><th>Name</th><th>CPU %</th><th>Memory %</th></tr>
                    """
                    for proc in processes:
                        tables_html += f"""
                            <tr>
                                <td>{proc.get('pid', 'N/A')}</td>
                                <td>{proc.get('name', 'N/A')}</td>
                                <td>{proc.get('cpu_percent', 'N/A')}</td>
                                <td>{proc.get('memory_percent', 'N/A')}</td>
                            </tr>
                        """
                    tables_html += "</table></div>"
        
        # Sistem servisleri
        if "system_services" in data and data["system_services"]:
            services = data["system_services"][:20]  # İlk 20 servis
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-cogs"></i> System Services (Top 20)</h4>
                    <table class="data-table">
                        <tr><th>PID</th><th>Status</th><th>Name</th></tr>
            """
            for service in services:
                tables_html += f"""
                    <tr>
                        <td>{service.get('pid', 'N/A')}</td>
                        <td>{service.get('status', 'N/A')}</td>
                        <td>{service.get('name', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_network_tables(self, data: Dict[str, Any]) -> str:
        """Network tabloları"""
        tables_html = ""
        
        # Ağ arayüzleri
        if "network_interfaces" in data and data["network_interfaces"]:
            interfaces = data["network_interfaces"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-network-wired"></i> Network Interfaces</h4>
                    <table class="data-table">
                        <tr><th>Name</th><th>IP Address</th><th>MAC Address</th><th>Status</th><th>Speed</th><th>MTU</th></tr>
            """
            for interface in interfaces:
                tables_html += f"""
                    <tr>
                        <td>{interface.get('name', 'N/A')}</td>
                        <td>{interface.get('ip_address', 'N/A')}</td>
                        <td>{interface.get('mac_address', 'N/A')}</td>
                        <td>{interface.get('status', 'N/A')}</td>
                        <td>{interface.get('speed', 'N/A')}</td>
                        <td>{interface.get('mtu', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Aktif bağlantılar
        if "active_connections" in data and data["active_connections"]:
            connections = data["active_connections"][:30]  # İlk 30 bağlantı
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-plug"></i> Active Connections (Top 30)</h4>
                    <table class="data-table">
                        <tr><th>Protocol</th><th>Local Address</th><th>Foreign Address</th><th>State</th><th>Command</th></tr>
            """
            for conn in connections:
                def addr_to_str(addr):
                    if isinstance(addr, dict):
                        ip = addr.get('ip', '')
                        port = addr.get('port', '')
                        if ip and port:
                            return f"{ip}:{port}"
                        elif ip:
                            return ip
                        else:
                            return ''
                    return str(addr)
                local_addr = addr_to_str(conn.get('local_address', ''))
                foreign_addr = addr_to_str(conn.get('foreign_address', ''))
                tables_html += f"""
                    <tr>
                        <td>{conn.get('protocol', 'N/A')}</td>
                        <td>{local_addr}</td>
                        <td>{foreign_addr}</td>
                        <td>{conn.get('state', 'N/A')}</td>
                        <td>{conn.get('command', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Routing tablosu
        if "routing_table" in data and data["routing_table"]:
            routes = data["routing_table"][:20]  # İlk 20 route
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-route"></i> Routing Table (Top 20)</h4>
                    <table class="data-table">
                        <tr><th>Destination</th><th>Gateway</th><th>Flags</th><th>Interface</th></tr>
            """
            for route in routes:
                tables_html += f"""
                    <tr>
                        <td>{route.get('destination', 'N/A')}</td>
                        <td>{route.get('gateway', 'N/A')}</td>
                        <td>{route.get('flags', 'N/A')}</td>
                        <td>{route.get('interface', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # DNS bilgileri
        if "dns_info" in data:
            dns_info = data["dns_info"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-globe"></i> DNS Information</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in dns_info.items():
                if isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_users_tables(self, data: Dict[str, Any]) -> str:
        """Users tabloları"""
        tables_html = ""
        
        # Kullanıcı hesapları
        if "user_accounts" in data and data["user_accounts"]:
            users = data["user_accounts"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-users"></i> User Accounts</h4>
                    <table class="data-table">
                        <tr><th>Username</th><th>UID</th><th>GID</th><th>Home</th><th>Shell</th><th>Description</th></tr>
            """
            for user in users:
                tables_html += f"""
                    <tr>
                        <td>{user.get('username', 'N/A')}</td>
                        <td>{user.get('uid', 'N/A')}</td>
                        <td>{user.get('gid', 'N/A')}</td>
                        <td>{user.get('home', 'N/A')}</td>
                        <td>{user.get('shell', 'N/A')}</td>
                        <td>{user.get('description', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Grup bilgileri
        if "group_info" in data and data["group_info"]:
            groups = data["group_info"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-user-friends"></i> Group Information</h4>
                    <table class="data-table">
                        <tr><th>Group Name</th><th>GID</th><th>Members</th></tr>
            """
            for group in groups:
                members = group.get('members', [])
                if isinstance(members, list):
                    members_str = ', '.join(members[:5])  # İlk 5 üye
                    if len(members) > 5:
                        members_str += f" (+{len(members) - 5} more)"
                else:
                    members_str = str(members)
                
                tables_html += f"""
                    <tr>
                        <td>{group.get('groupname', 'N/A')}</td>
                        <td>{group.get('gid', 'N/A')}</td>
                        <td>{members_str}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Yetki seviyeleri
        if "permissions" in data:
            permissions = data["permissions"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-shield-alt"></i> Permissions</h4>
                    <table class="data-table">
                        <tr><th>Permission Type</th><th>Users</th></tr>
            """
            for key, value in permissions.items():
                if isinstance(value, list):
                    users_str = ', '.join(value[:5])  # İlk 5 kullanıcı
                    if len(value) > 5:
                        users_str += f" (+{len(value) - 5} more)"
                else:
                    users_str = str(value)
                
                tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{users_str}</td></tr>"
            tables_html += "</table></div>"
        
        # Oturum bilgileri
        if "session_info" in data:
            session = data["session_info"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-sign-in-alt"></i> Session Information</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in session.items():
                if isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_filesystem_tables(self, data: Dict[str, Any]) -> str:
        """Filesystem tabloları"""
        tables_html = ""
        
        # Disk kullanımı
        if "disk_usage" in data and "partitions" in data["disk_usage"]:
            partitions = data["disk_usage"]["partitions"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-hdd"></i> Disk Usage</h4>
                    <table class="data-table">
                        <tr><th>Filesystem</th><th>Size</th><th>Used</th><th>Available</th><th>Use %</th><th>Mounted On</th></tr>
            """
            for partition in partitions:
                tables_html += f"""
                    <tr>
                        <td>{partition.get('filesystem', 'N/A')}</td>
                        <td>{partition.get('size', 'N/A')}</td>
                        <td>{partition.get('used', 'N/A')}</td>
                        <td>{partition.get('available', 'N/A')}</td>
                        <td>{partition.get('use_percent', 'N/A')}</td>
                        <td>{partition.get('mounted_on', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # En büyük dizinler
        if "disk_usage" in data and "largest_directories" in data["disk_usage"]:
            directories = data["disk_usage"]["largest_directories"][:15]  # İlk 15 dizin
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-folder-open"></i> Largest Directories (Top 15)</h4>
                    <table class="data-table">
                        <tr><th>Size</th><th>Path</th></tr>
            """
            for directory in directories:
                tables_html += f"""
                    <tr>
                        <td>{directory.get('size', 'N/A')}</td>
                        <td>{directory.get('path', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Dosya hash'leri
        if "file_hashes" in data:
            hashes = data["file_hashes"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-hashtag"></i> File Hashes (Important Files)</h4>
                    <table class="data-table">
                        <tr><th>File Path</th><th>SHA256</th><th>Size</th><th>Modified</th></tr>
            """
            for file_path, hash_info in hashes.items():
                if isinstance(hash_info, dict):
                    tables_html += f"""
                        <tr>
                            <td>{file_path}</td>
                            <td>{hash_info.get('sha256', 'N/A')}</td>
                            <td>{hash_info.get('size', 'N/A')}</td>
                            <td>{hash_info.get('modified', 'N/A')}</td>
                        </tr>
                    """
            tables_html += "</table></div>"
        
        # Dosya zaman damgaları
        if "timestamps" in data and data["timestamps"]:
            timestamps = data["timestamps"]
            # Özet bilgileri filtrele
            file_timestamps = [ts for ts in timestamps if "path" in ts]
            if file_timestamps:
                tables_html += """
                    <div class="data-section">
                        <h4><i class="fas fa-clock"></i> Recent File Changes (Top 20)</h4>
                        <table class="data-table">
                            <tr><th>Path</th><th>Created</th><th>Modified</th><th>Size</th></tr>
                """
                for ts in file_timestamps[:20]:
                    tables_html += f"""
                        <tr>
                            <td>{str(ts.get('path', 'N/A'))[:50]}{'...' if len(str(ts.get('path', ''))) > 50 else ''}</td>
                            <td>{ts.get('created', 'N/A')}</td>
                            <td>{ts.get('modified', 'N/A')}</td>
                            <td>{ts.get('size', 'N/A')}</td>
                        </tr>
                    """
                tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_memory_tables(self, data: Dict[str, Any]) -> str:
        """Memory tabloları"""
        tables_html = ""
        
        # RAM durumu
        if "ram_status" in data:
            ram = data["ram_status"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-memory"></i> RAM Status</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in ram.items():
                if isinstance(value, dict) and "formatted" in value:
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value['formatted']}</td></tr>"
                elif isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        # En çok bellek kullanan processler
        if "memory_usage" in data and "top_memory_processes" in data["memory_usage"]:
            processes = data["memory_usage"]["top_memory_processes"][:15]  # İlk 15 process
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-chart-pie"></i> Top Memory Processes (Top 15)</h4>
                    <table class="data-table">
                        <tr><th>PID</th><th>Name</th><th>Memory %</th><th>RSS</th><th>VMS</th></tr>
            """
            for proc in processes:
                tables_html += f"""
                    <tr>
                        <td>{proc.get('pid', 'N/A')}</td>
                        <td>{proc.get('name', 'N/A')}</td>
                        <td>{proc.get('memory_percent', 'N/A')}</td>
                        <td>{proc.get('memory_rss', 'N/A')}</td>
                        <td>{proc.get('memory_vms', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Swap durumu
        if "swap_status" in data:
            swap = data["swap_status"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-exchange-alt"></i> Swap Status</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in swap.items():
                if isinstance(value, dict) and "formatted" in value:
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value['formatted']}</td></tr>"
                elif isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        # Kernel modülleri
        if "kernel_modules" in data and data["kernel_modules"]:
            modules = data["kernel_modules"]
            # Sadece dict olan modülleri filtrele
            kernel_modules = [m for m in modules if isinstance(m, dict) and "name" in m]
            if kernel_modules:
                tables_html += """
                    <div class="data-section">
                        <h4><i class="fas fa-microchip"></i> Kernel Modules (Top 20)</h4>
                        <table class="data-table">
                            <tr><th>Index</th><th>Name</th><th>Version</th><th>Size</th><th>Refs</th></tr>
                """
                for module in kernel_modules[:20]:
                    tables_html += f"""
                        <tr>
                            <td>{module.get('index', 'N/A')}</td>
                            <td>{module.get('name', 'N/A')}</td>
                            <td>{module.get('version', 'N/A')}</td>
                            <td>{module.get('size', 'N/A')}</td>
                            <td>{module.get('refs', 'N/A')}</td>
                        </tr>
                    """
                tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_logs_tables(self, data: Dict[str, Any]) -> str:
        """Logs tabloları"""
        tables_html = ""
        
        # Log istatistikleri
        if "log_statistics" in data:
            stats = data["log_statistics"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-chart-bar"></i> Log Statistics</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in stats.items():
                if isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        # Log dosyaları analizi
        if "log_files_analysis" in data and "log_files" in data["log_files_analysis"]:
            log_files = data["log_files_analysis"]["log_files"]
            if log_files:
                tables_html += """
                    <div class="data-section">
                        <h4><i class="fas fa-file-alt"></i> Log Files (Top 30)</h4>
                        <table class="data-table">
                            <tr><th>File Path</th><th>Size</th><th>Modified</th></tr>
                """
                for log_file in log_files[:30]:
                    tables_html += f"""
                        <tr>
                            <td>{log_file.get('path', 'N/A')}</td>
                            <td>{log_file.get('size', 'N/A')}</td>
                            <td>{log_file.get('modified', 'N/A')}</td>
                        </tr>
                    """
                tables_html += "</table></div>"
        
        # Hata logları
        if "error_logs" in data and data["error_logs"]:
            error_logs = data["error_logs"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-exclamation-triangle"></i> Error Logs (Recent)</h4>
                    <table class="data-table">
                        <tr><th>Timestamp</th><th>Type</th><th>Message</th></tr>
            """
            for error in error_logs[:20]:  # Son 20 hata
                tables_html += f"""
                    <tr>
                        <td>{error.get('timestamp', 'N/A')}</td>
                        <td>{error.get('type', 'N/A')}</td>
                        <td>{str(error.get('message', 'N/A'))[:100]}{'...' if len(str(error.get('message', ''))) > 100 else ''}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Crash logları
        if "error_logs" in data:
            crash_logs = [log for log in data["error_logs"] if log.get("type") == "crash_log"]
            if crash_logs:
                tables_html += """
                    <div class="data-section">
                        <h4><i class="fas fa-bug"></i> Crash Logs</h4>
                        <table class="data-table">
                            <tr><th>File</th><th>Size</th><th>Modified</th><th>Path</th></tr>
                """
                for crash in crash_logs[:10]:  # İlk 10 crash log
                    tables_html += f"""
                        <tr>
                            <td>{crash.get('file', 'N/A')}</td>
                            <td>{crash.get('size', 'N/A')}</td>
                            <td>{crash.get('modified', 'N/A')}</td>
                            <td>{crash.get('path', 'N/A')}</td>
                        </tr>
                    """
                tables_html += "</table></div>"
        
        return tables_html
    
    def _generate_timeline_tables(self, data: Dict[str, Any]) -> str:
        """Timeline tabloları"""
        tables_html = ""
        
        # Zaman çizelgesi özeti
        if "timeline_summary" in data:
            summary = data["timeline_summary"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-clock"></i> Timeline Summary</h4>
                    <table class="data-table">
                        <tr><th>Property</th><th>Value</th></tr>
            """
            for key, value in summary.items():
                if isinstance(value, (str, int, float)):
                    tables_html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            tables_html += "</table></div>"
        
        # Dosya zaman çizelgesi
        if "file_timeline" in data and data["file_timeline"]:
            file_timeline = data["file_timeline"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-file"></i> File Timeline (Recent Changes)</h4>
                    <table class="data-table">
                        <tr><th>Type</th><th>Path</th><th>Created</th><th>Modified</th><th>Size</th></tr>
            """
            for file_item in file_timeline[:30]:  # İlk 30 dosya
                tables_html += f"""
                    <tr>
                        <td>{file_item.get('type', 'N/A')}</td>
                        <td>{str(file_item.get('path', 'N/A'))[:50]}{'...' if len(str(file_item.get('path', ''))) > 50 else ''}</td>
                        <td>{file_item.get('created', 'N/A')}</td>
                        <td>{file_item.get('modified', 'N/A')}</td>
                        <td>{file_item.get('size', 'N/A')}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Sistem olayları
        if "system_events" in data and data["system_events"]:
            system_events = data["system_events"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-server"></i> System Events (Recent)</h4>
                    <table class="data-table">
                        <tr><th>Type</th><th>Timestamp</th><th>Source</th><th>Message</th></tr>
            """
            for event in system_events[:20]:  # İlk 20 olay
                tables_html += f"""
                    <tr>
                        <td>{event.get('type', 'N/A')}</td>
                        <td>{event.get('timestamp', 'N/A')}</td>
                        <td>{event.get('source', 'N/A')}</td>
                        <td>{str(event.get('message', 'N/A'))[:80]}{'...' if len(str(event.get('message', ''))) > 80 else ''}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        # Kullanıcı aktiviteleri
        if "user_activities" in data and data["user_activities"]:
            user_activities = data["user_activities"]
            tables_html += """
                <div class="data-section">
                    <h4><i class="fas fa-user"></i> User Activities (Recent)</h4>
                    <table class="data-table">
                        <tr><th>Type</th><th>Timestamp</th><th>Source</th><th>Activity</th></tr>
            """
            for activity in user_activities[:20]:  # İlk 20 aktivite
                tables_html += f"""
                    <tr>
                        <td>{activity.get('type', 'N/A')}</td>
                        <td>{activity.get('timestamp', 'N/A')}</td>
                        <td>{activity.get('source', 'N/A')}</td>
                        <td>{str(activity.get('activity', 'N/A'))[:80]}{'...' if len(str(activity.get('activity', ''))) > 80 else ''}</td>
                    </tr>
                """
            tables_html += "</table></div>"
        
        return tables_html 