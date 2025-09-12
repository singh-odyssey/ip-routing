#!/usr/bin/env python3
"""
SIMPLE LAUNCHER FOR GOOGLE STUDENT AMBASSADOR TASK
==================================================

Quick launcher script for generating unique views on:
https://aiskillshouse.com/student/qr-mediator.html?uid=2827&promptId=6

Just run this script and it will start generating unique views!
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎓 GOOGLE STUDENT AMBASSADOR - UNIQUE VIEWER GENERATOR")
    print("=" * 65)
    print("🎯 Target: https://aiskillshouse.com/student/qr-mediator?uid=2827&promptId=6")
    print("⚡ Features: 42+ Indian IPs, 2-5 sec timing, Anti-detection")
    print()
    
    try:
        # Import and run the Google Ambassador Bot
        from google_ambassador_bot import GoogleAmbassadorBot
        
        print("🚀 Initializing bot...")
        bot = GoogleAmbassadorBot()
        
        print("✅ Bot ready! Starting unique view generation...")
        print("💡 Press Ctrl+C to stop anytime")
        print()
        
        # Run unlimited views (user can stop with Ctrl+C)
        bot.run_continuous_unique_views()
        
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