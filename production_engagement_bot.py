#!/usr/bin/env python3
"""
PRODUCTION-READY FREE ENGAGEMENT BOT
====================================

Scale the successful fingerprint bot for continuous engagement generation.
This version includes scheduling, error handling, and stealth features.
"""

import schedule
import time
import random
import sys
import os

# Import our successful bot
sys.path.append('/workspaces/ip-routing')
from free_js_fingerprint_bot import FreeJSFingerprintBot

class ProductionEngagementBot:
    def __init__(self):
        self.bot = FreeJSFingerprintBot()
        self.daily_limit = 10  # Max visits per day to avoid detection
        self.today_count = 0
        
    def run_scheduled_engagement(self):
        """Run scheduled engagement with safety limits"""
        
        if self.today_count >= self.daily_limit:
            print(f"✋ Daily limit reached ({self.daily_limit} visits)")
            return
        
        print(f"\n🤖 Running scheduled engagement ({self.today_count + 1}/{self.daily_limit})")
        
        # Run 1-2 visits with random timing
        num_visits = random.randint(1, 2)
        delay_range = (45, 90)  # Longer delays for stealth
        
        try:
            success_before = self.bot.success_count
            self.bot.run_free_campaign(num_visits, delay_range)
            
            # Update daily counter
            new_successes = self.bot.success_count - success_before
            self.today_count += new_successes
            
            print(f"✅ Session complete: +{new_successes} engagements")
            print(f"📊 Today's total: {self.today_count}/{self.daily_limit}")
            
        except Exception as e:
            print(f"❌ Session failed: {e}")
    
    def reset_daily_counter(self):
        """Reset daily counter at midnight"""
        self.today_count = 0
        print("🔄 Daily counter reset")
    
    def start_production_schedule(self):
        """Start the production engagement schedule"""
        
        print("🏭 PRODUCTION ENGAGEMENT BOT STARTED")
        print("=" * 50)
        print(f"📊 Daily limit: {self.daily_limit} visits")
        print("⏰ Schedule: Every 2-4 hours")
        print("🎯 Target: Google Student Ambassador")
        print("💰 Cost: $0 (completely free)")
        print("=" * 50)
        
        # Schedule engagements throughout the day
        schedule.every(2).to(4).hours.do(self.run_scheduled_engagement)
        
        # Reset counter daily at midnight
        schedule.every().day.at("00:00").do(self.reset_daily_counter)
        
        print("⏰ Scheduler started. Press Ctrl+C to stop.")
        
        # Run immediately first time
        self.run_scheduled_engagement()
        
        # Keep running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print("\n👋 Production bot stopped")
                break
            except Exception as e:
                print(f"⚠️ Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retry

def quick_test():
    """Quick test of the successful bot"""
    print("🧪 QUICK SUCCESS TEST")
    print("=" * 30)
    
    bot = FreeJSFingerprintBot()
    bot.run_free_campaign(2, (15, 25))  # Quick 2 visits

def production_mode():
    """Start production mode with scheduling"""
    prod_bot = ProductionEngagementBot()
    prod_bot.start_production_schedule()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Production Engagement Bot')
    parser.add_argument('--mode', choices=['test', 'production'], default='test',
                       help='Run mode: test (quick) or production (scheduled)')
    
    args = parser.parse_args()
    
    if args.mode == 'test':
        quick_test()
    else:
        production_mode()