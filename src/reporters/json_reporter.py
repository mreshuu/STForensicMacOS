"""
JSON Raporlayıcı
"""

import json
import logging
from typing import Dict, Any
from datetime import datetime


class JSONReporter:
    """JSON formatında rapor oluşturucu"""
    
    def __init__(self, config, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def generate_report(self, results: Dict[str, Any], output_path: str):
        """JSON raporu oluştur"""
        try:
            # Rapor verilerini hazırla
            report_data = self._prepare_report_data(results)
            
            # JSON dosyasına yaz
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"JSON raporu oluşturuldu: {output_path}")
            
        except Exception as e:
            self.logger.error(f"JSON raporu oluşturma hatası: {str(e)}")
            raise
    
    def _prepare_report_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Rapor verilerini hazırla"""
        report_data = {
            "report_info": {
                "tool": "STForensicMacOS",
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat(),
                "format": "json"
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