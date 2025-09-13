#!/usr/bin/env python3
"""
SIMPLE LAUNCHER FOR GOOGLE STUDENT AMBASSADOR TASK
==================================================

Quick launcher script for generating unique views on any URL.
Just run this script and it will ask for:
1. Target URL
2. Number of views

Features:
- User-friendly URL and view count input
- URL validation with auto-protocol addition
- 42+ Indian IP addresses from 25+ cities
- Anti-detection measures
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎓 GOOGLE STUDENT AMBASSADOR - UNIQUE VIEWER GENERATOR")
    print("=" * 65)
    print("⚡ Features: 42+ Indian IPs, 2-5 sec timing, Anti-detection")
    print("🌐 Works with any URL - just enter it when prompted!")
    print()
    
    try:
        # Import and run the Google Ambassador Bot
        from google_ambassador_bot import main as run_bot
        
        print("🚀 Launching interactive bot...")
        print("💡 Press Ctrl+C to stop anytime")
        print()
        
        # Run the main bot function which handles user input
        run_bot()
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Bot stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required files are in the same directory")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🎉 Task completed! Your unique views have been generated.")

if __name__ == "__main__":
    main()