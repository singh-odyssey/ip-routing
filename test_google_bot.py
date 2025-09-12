#!/usr/bin/env python3
"""
QUICK TEST SCRIPT FOR GOOGLE AMBASSADOR BOT
==========================================

Test script to verify the bot works correctly before running the full version.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_bot():
    print("🧪 TESTING GOOGLE STUDENT AMBASSADOR BOT")
    print("=" * 50)
    
    try:
        # Import the bot
        from google_ambassador_bot import GoogleAmbassadorBot
        
        print("✅ Successfully imported GoogleAmbassadorBot")
        
        # Initialize bot
        bot = GoogleAmbassadorBot()
        print("✅ Bot initialized successfully")
        
        # Test generating 2 unique views
        print("\n🔄 Testing 2 unique views...")
        bot.run_continuous_unique_views(target_views=2)
        
        print("\n✅ Test completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required files are in the same directory")
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bot()