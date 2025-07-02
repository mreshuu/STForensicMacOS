#!/usr/bin/env python3
"""
STForensicMacOS - MacOS Forensic Analysis Tool
Main application file
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Import project modules
from src.core.config import Config
from src.core.logger import setup_logger
from src.core.forensic_engine import ForensicEngine
from src.utils.helpers import check_root_permissions, create_output_directory


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="STForensicMacOS - MacOS Forensic Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --mode lite --output ./reports
  python main.py --mode full --output ./reports --image-size 50GB
  python main.py --modules system,filesystem,network --output ./reports
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["lite", "full"],
        default="lite",
        help="Analysis mode: lite (quick) or full (complete image)"
    )
    
    parser.add_argument(
        "--modules",
        type=str,
        help="Modules to run (comma-separated)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./reports",
        help="Report output directory"
    )
    
    parser.add_argument(
        "--image-size",
        type=str,
        help="Image size (e.g., 50GB, 100GB)"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "html", "pdf", "csv"],
        default="json",
        help="Report format"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--no-hash",
        action="store_true",
        help="Skip hash calculations"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Configuration file path"
    )
    
    return parser.parse_args()


def main():
    """Main application function"""
    print("=" * 60)
    print("STForensicMacOS - MacOS Forensic Analysis Tool")
    print("=" * 60)
    
    # Parse arguments
    args = parse_arguments()
    
    # Check root permissions
    if not check_root_permissions():
        print("❌ Error: This application requires root/administrator privileges!")
        print("   Please run with 'sudo python main.py'")
        sys.exit(1)
    
    # Load configuration
    config = Config(args.config)
    
    # Setup logger
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_level, args.output)
    
    logger.info("Starting STForensicMacOS...")
    logger.info(f"Analysis mode: {args.mode}")
    logger.info(f"Output directory: {args.output}")
    
    try:
        # Create output directory
        create_output_directory(args.output)
        
        # Initialize forensic engine
        engine = ForensicEngine(config, logger)
        
        # Start analysis
        start_time = datetime.now()
        logger.info(f"Starting analysis: {start_time}")
        
        if args.modules:
            # Run specific modules
            module_list = [m.strip() for m in args.modules.split(",")]
            print(f"\n🎯 Running specific modules: {', '.join(module_list)}")
            results = engine.run_modules(module_list, args)
        else:
            # Run by mode
            results = engine.run_mode(args.mode, args)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"Analysis completed: {end_time}")
        logger.info(f"Total duration: {duration}")
        
        # Generate reports
        print(f"\n📄 Generating reports...")
        engine.generate_reports(results, args.output, args.format)
        
        print(f"\n🎉 Analysis completed successfully!")
        print(f"📊 Reports: {args.output}")
        print(f"⏱️  Total duration: {duration}")
        
    except KeyboardInterrupt:
        logger.warning("Stopped by user")
        print("\n⚠️  Analysis stopped by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        print(f"\n❌ Critical error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 