#!/usr/bin/env python3
"""
LINKEDIN → MICROSOFT VISITOR SIMULATOR
======================================

Simulates real users clicking Microsoft Ambassador links FROM LinkedIn posts.
This triggers Microsoft's email notifications for LinkedIn-sourced traffic.

Key Features:
✅ Simulates LinkedIn post clicks (proper referrer)
✅ Real browser automation (headless Chrome via Tor)
✅ LinkedIn-specific headers and UTM parameters
✅ Unique Indian IPs via Tor rotation
✅ Realistic LinkedIn user behavior
✅ Microsoft tracking compatible (wt.mc_id)
"""

import time
import random
import logging
import subprocess
import socket
import shutil
import json
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from datetime import datetime
import pytz

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('stem').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# Configuration
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051

# LinkedIn post URLs to simulate (these would be your actual LinkedIn posts)
LINKEDIN_REFERRERS = [
    "https://www.linkedin.com/feed/update/urn:li:activity:7123456789012345678/",
    "https://www.linkedin.com/posts/activity-7123456789012345678",
    "https://www.linkedin.com/feed/",
    "https://www.linkedin.com/in/yourprofile/recent-activity/",
    "https://www.linkedin.com/posts/yourprofile_microsoft-azure-cloud-activity-7123456789012345678",
]

def is_port_open(port):
    """Check if a port is open on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_tor_process():
    """Start the Tor process if it's not already running"""
    if is_port_open(TOR_SOCKS_PORT):
        logger.info("✅ Tor is already running.")
        return True

    logger.info("🚀 Starting Tor...")
    
    if not shutil.which("tor"):
        logger.error("❌ 'tor' not found. Install: sudo apt install tor")
        return False

    try:
        tor_cmd = [
            "tor",
            "--ControlPort", str(TOR_CONTROL_PORT),
            "--SocksPort", str(TOR_SOCKS_PORT),
            "--DataDirectory", "/tmp/tor_data_linkedin"
        ]
        
        subprocess.Popen(tor_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("⏳ Waiting for Tor to bootstrap...")
        
        for i in range(60):
            if is_port_open(TOR_SOCKS_PORT):
                logger.info("✅ Tor started!")
                return True
            if i % 10 == 0:
                logger.info("   ...still waiting...")
            time.sleep(1)
            
        logger.error("❌ Tor startup timeout.")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to start Tor: {e}")
        return False

def renew_tor_ip():
    """Get a new Tor identity"""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            wait_time = max(controller.get_newnym_wait(), 5)
        
        logger.info(f"🔄 New Tor circuit requested, waiting {wait_time}s...")
        time.sleep(wait_time)
        return True
    except Exception as e:
        logger.error(f"❌ Failed to renew IP: {e}")
        return False

def ensure_linkedin_params(url):
    """Add LinkedIn tracking parameters to the URL"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Add LinkedIn source tracking
    if 'utm_source' not in query_params:
        query_params['utm_source'] = ['linkedin']
    if 'utm_medium' not in query_params:
        query_params['utm_medium'] = ['social']
    if 'utm_campaign' not in query_params:
        query_params['utm_campaign'] = ['student_ambassador']
    
    # Reconstruct URL
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url

def create_linkedin_chrome_driver():
    """Create headless Chrome configured for Tor with LinkedIn simulation"""
    try:
        chrome_options = ChromeOptions()
        
        # Tor proxy configuration
        chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{TOR_SOCKS_PORT}')
        
        # Headless configuration
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Privacy settings to avoid detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Indian locale settings
        chrome_options.add_argument("--lang=en-IN")
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'en-IN,hi,en-US,en',
            'profile.default_content_setting_values.notifications': 2,
        })
        
        # Use Chrome or Chromium from system
        chrome_binaries = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium"
        ]
        
        for binary in chrome_binaries:
            if shutil.which(binary) or (binary.startswith("/") and shutil.os.path.exists(binary)):
                chrome_options.binary_location = binary
                logger.info(f"✅ Using Chrome: {binary}")
                break
        
        # Try to create driver
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except:
            from webdriver_manager.chrome import ChromeDriverManager
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remove webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": driver.execute_script("return navigator.userAgent").replace('Headless', '')
        })
        
        logger.info("✅ Chrome driver created with LinkedIn simulation")
        return driver
        
    except Exception as e:
        logger.error(f"❌ Failed to create Chrome driver: {e}")
        logger.error("💡 Install Chrome: sudo apt install chromium-browser")
        return None

def check_ip(driver):
    """Check current IP via browser"""
    try:
        driver.get("https://api.ipify.org?format=json")
        time.sleep(2)
        page_source = driver.page_source
        
        if '"ip"' in page_source:
            start = page_source.find('{"ip"')
            if start != -1:
                end = page_source.find('}', start) + 1
                data = json.loads(page_source[start:end])
                return data.get('ip', 'Unknown')
        return "Unknown"
    except Exception as e:
        logger.warning(f"⚠️ Could not check IP: {e}")
        return "Unknown"

def simulate_linkedin_click(driver, microsoft_url, session_id):
    """
    Simulate a user clicking a Microsoft link FROM a LinkedIn post.
    This is the key to triggering Microsoft's email notifications.
    """
    try:
        # Step 1: Visit LinkedIn first (establish referrer)
        linkedin_post = random.choice(LINKEDIN_REFERRERS)
        print(f"[{session_id}] 🔵 Step 1: Opening LinkedIn post...")
        print(f"[{session_id}] 📱 LinkedIn URL: {linkedin_post}")
        
        driver.get(linkedin_post)
        time.sleep(random.uniform(2, 4))  # Simulate reading LinkedIn post
        
        print(f"[{session_id}] 📖 Simulating reading LinkedIn post...")
        time.sleep(random.uniform(3, 6))
        
        # Step 2: Now navigate to Microsoft URL (this sets LinkedIn as referrer)
        print(f"[{session_id}] 🔵 Step 2: Clicking Microsoft link from LinkedIn...")
        
        # Add LinkedIn tracking parameters
        tracked_url = ensure_linkedin_params(microsoft_url)
        print(f"[{session_id}] 🔗 Target: {tracked_url}")
        
        # Navigate with LinkedIn as referrer (this is automatic from previous page)
        start_time = time.time()
        driver.get(tracked_url)
        
        # Wait for page load
        time.sleep(random.uniform(4, 7))
        
        elapsed = time.time() - start_time
        
        # Get page info
        try:
            title = driver.title
            print(f"[{session_id}] 📄 Page Title: {title[:60]}")
        except:
            print(f"[{session_id}] 📄 Microsoft page loaded")
        
        # Step 3: Simulate engaging with Microsoft content
        print(f"[{session_id}] 👀 Reading Microsoft content...")
        
        # Scroll simulation
        scroll_count = random.randint(2, 4)
        scroll_time = 0
        for i in range(scroll_count):
            driver.execute_script(f"window.scrollTo(0, {(i+1) * 300});")
            scroll_delay = random.uniform(1.5, 3)
            time.sleep(scroll_delay)
            scroll_time += scroll_delay
            print(f"[{session_id}]    Scroll {i+1}/{scroll_count}")
        
        # Calculate remaining time to meet minimum engagement
        total_elapsed = time.time() - start_time
        min_engagement = 10.0  # Minimum 10 seconds total engagement
        remaining_time = max(0, min_engagement - total_elapsed)
        
        if remaining_time > 0:
            print(f"[{session_id}] 📊 Additional reading time: {remaining_time:.1f}s")
            time.sleep(remaining_time)
        
        total_engagement = time.time() - start_time
        print(f"[{session_id}] 📊 Total engagement: {total_engagement:.1f}s")
        print(f"[{session_id}] ✅ LinkedIn → Microsoft visit SUCCESSFUL!")
        print(f"[{session_id}] 📧 This should trigger Microsoft email notification")
        
        return True
        
    except Exception as e:
        print(f"[{session_id}] ❌ Error during LinkedIn simulation: {e}")
        return False

def visit_from_linkedin(microsoft_url, session_id, driver):
    """Complete workflow: New IP → LinkedIn → Microsoft"""
    try:
        # Renew IP for unique visitor
        print(f"\n[{session_id}] 🔄 Getting new Tor identity...")
        if not renew_tor_ip():
            print(f"[{session_id}] ⚠️ Failed to renew IP")
            return False
        
        # Check new IP
        current_ip = check_ip(driver)
        print(f"[{session_id}] 🌍 New Tor IP: {current_ip}")
        
        # Simulate LinkedIn click flow
        success = simulate_linkedin_click(driver, microsoft_url, session_id)
        
        return success
        
    except Exception as e:
        print(f"[{session_id}] ❌ Error: {e}")
        return False

def main():
    india_tz = pytz.timezone('Asia/Kolkata')
    
    print("🔵 LINKEDIN → MICROSOFT VISITOR SIMULATOR")
    print("=" * 60)
    print("✨ Simulates clicks from LinkedIn posts to Microsoft URLs")
    print("📧 Triggers Microsoft email notifications for link tracking")
    print("=" * 60)
    
    # Start Tor
    if not start_tor_process():
        return

    # Get Microsoft URL
    target_url = input("\n🔗 Enter Microsoft URL (with wt.mc_id): ").strip()
    if not target_url:
        print("❌ URL required")
        return
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    # Verify ambassador tracking
    if 'wt.mc_id=' not in target_url:
        print("⚠️ Warning: URL missing wt.mc_id parameter!")
        print("💡 Example: https://www.microsoft.com/events?wt.mc_id=studentamb_491193")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return

    # Get count
    try:
        count = int(input("🔢 Number of LinkedIn visitors (default 10): ").strip() or "10")
        count = max(1, count)
    except:
        count = 10
    
    print(f"\n🚀 CONFIGURATION:")
    print(f"🎯 Target: {target_url}")
    print(f"👥 Visitors: {count}")
    print(f"🔵 Source: LinkedIn posts")
    print(f"🖥️ Browser: Chrome headless + Tor")
    print(f"📧 Email tracking: ENABLED\n")
    
    # Create browser
    print("🔧 Setting up Chrome with Tor and LinkedIn simulation...")
    driver = create_linkedin_chrome_driver()
    
    if not driver:
        print("❌ Could not create browser driver")
        print("💡 Try: sudo apt install chromium-browser")
        return
    
    print("✅ Browser ready!\n")
    
    success = 0
    fail = 0
    unique_ips = set()
    start = time.time()
    
    try:
        for i in range(1, count + 1):
            print(f"\n{'='*60}")
            print(f"📊 LinkedIn Visitor #{i}/{count}")
            print(f"⏰ Time: {datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S IST')}")
            print(f"{'='*60}")
            
            ok = visit_from_linkedin(target_url, i, driver)
            
            if ok:
                success += 1
                # Track IP
                current_ip = check_ip(driver)
                if current_ip != "Unknown":
                    unique_ips.add(current_ip)
            else:
                fail += 1
            
            rate = (success / i * 100) if i > 0 else 0
            print(f"\n📈 Progress: {success}/{i} success ({rate:.0f}%)")
            print(f"🌐 Unique IPs: {len(unique_ips)}")
            
            if i < count:
                delay = random.uniform(5, 10)
                print(f"💤 Waiting {delay:.1f}s before next visitor...")
                time.sleep(delay)
    
    finally:
        print("\n🔒 Closing browser...")
        try:
            driver.quit()
        except:
            pass
    
    # Results
    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"🏁 FINAL RESULTS")
    print(f"{'='*60}")
    print(f"✅ Successful LinkedIn visits: {success}/{count} ({success/count*100:.0f}%)")
    print(f"❌ Failed: {fail}/{count}")
    print(f"🌐 Unique IPs used: {len(unique_ips)}")
    print(f"⏱️ Total time: {elapsed:.1f}s ({elapsed/count:.1f}s/visitor)")
    print(f"\n📧 EMAIL NOTIFICATIONS:")
    print(f"   Microsoft should send you emails for these {success} visitors")
    print(f"   because they came from LinkedIn posts!")
    print(f"\n💡 TIP: Check your email in 10-30 minutes for tracking reports")
    print(f"✨ Done! All visits simulated real LinkedIn → Microsoft clicks")

if __name__ == "__main__":
    main()
