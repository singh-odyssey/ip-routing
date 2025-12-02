#!/usr/bin/env python3
"""
HEADLESS TOR BROWSER (Chrome-based)
====================================

Simplified version that uses Chrome/Chromium in headless mode through Tor.
Works in dev containers and headless environments.

This script actually opens the URL in a real browser (headless Chrome),
routes all traffic through Tor, and gets new IPs for each request.
"""

import time
import random
import logging
import subprocess
import socket
import shutil
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('stem').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# Configuration
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051

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
            "--DataDirectory", "/tmp/tor_data_custom"
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

def create_tor_chrome_driver():
    """Create headless Chrome configured for Tor"""
    try:
        chrome_options = ChromeOptions()
        
        # Tor proxy configuration
        chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{TOR_SOCKS_PORT}')
        
        # Headless configuration
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Privacy settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
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
            # First try with system chromedriver
            driver = webdriver.Chrome(options=chrome_options)
        except:
            # Fall back to downloading chromedriver
            from webdriver_manager.chrome import ChromeDriverManager
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remove webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("✅ Chrome driver created with Tor proxy (headless mode)")
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
            import json
            start = page_source.find('{"ip"')
            if start != -1:
                end = page_source.find('}', start) + 1
                data = json.loads(page_source[start:end])
                return data.get('ip', 'Unknown')
        return "Unknown"
    except Exception as e:
        logger.warning(f"⚠️ Could not check IP: {e}")
        return "Unknown"

def visit_url(url, session_id, driver, previous_ip=None, use_linkedin_referrer=False):
    """Visit URL through Tor browser"""
    try:
        # Renew IP
        if not renew_tor_ip():
            print(f"[{session_id}] ⚠️ Failed to renew IP")
            return False, previous_ip
        
        # Check new IP
        current_ip = check_ip(driver)
        print(f"\n[{session_id}] 🌍 Tor IP: {current_ip}")
        
        # IMPORTANT: Visit LinkedIn first to set referrer (for Microsoft tracking)
        if use_linkedin_referrer:
            linkedin_posts = [
                "https://www.linkedin.com/feed/",
                "https://www.linkedin.com/feed/update/urn:li:activity:7000000000000000000/",
                "https://www.linkedin.com/posts/activity-7000000000000000000",
            ]
            linkedin_url = random.choice(linkedin_posts)
            print(f"[{session_id}] 🔵 Setting LinkedIn referrer: {linkedin_url}")
            driver.get(linkedin_url)
            time.sleep(random.uniform(2, 4))  # Simulate reading LinkedIn post
            print(f"[{session_id}] 📱 Simulating LinkedIn interaction...")
            time.sleep(random.uniform(2, 4))
        
        # Visit target URL
        print(f"[{session_id}] 🚀 Loading URL in browser: {url}")
        start_time = time.time()
        
        driver.get(url)
        time.sleep(3)  # Wait for page load
        
        elapsed = time.time() - start_time
        
        # Get page info
        try:
            title = driver.title
            print(f"[{session_id}] 📄 Page Title: {title[:60]}")
        except:
            print(f"[{session_id}] 📄 Page loaded")
        
        print(f"[{session_id}] ✅ Success! (Time: {elapsed:.2f}s)")
        
        # Simulate reading with scrolling
        scroll_count = random.randint(2, 4)
        for i in range(scroll_count):
            try:
                driver.execute_script(f"window.scrollTo(0, {(i+1) * 300});")
                time.sleep(random.uniform(1, 2))
            except:
                pass
        
        view_time = random.uniform(3, 6)
        print(f"[{session_id}] 👀 Viewing for {view_time:.1f}s...")
        time.sleep(view_time)
        
        return True, current_ip
        
    except Exception as e:
        print(f"[{session_id}] ❌ Error: {e}")
        return False, previous_ip

def main():
    print("🧅 HEADLESS TOR BROWSER")
    print("=" * 50)
    print("✨ Chrome headless mode + Tor routing")
    print("=" * 50)
    
    # Start Tor
    if not start_tor_process():
        return

    # Get URL
    target_url = input("\n🔗 Enter URL: ").strip()
    if not target_url:
        print("❌ URL required")
        return
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    # Ask about LinkedIn referrer (IMPORTANT for Microsoft tracking)
    use_linkedin = False
    if 'microsoft.com' in target_url.lower():
        print("\n🔵 MICROSOFT URL DETECTED!")
        linkedin_choice = input("Simulate clicks from LinkedIn? (y/n, default: y): ").strip().lower()
        use_linkedin = linkedin_choice != 'n'
        if use_linkedin:
            print("✅ Will simulate LinkedIn → Microsoft clicks (triggers email notifications)")
        else:
            print("⚠️ Direct visits (may not trigger email notifications)")

    # Get count
    try:
        count = int(input("\n🔢 Number of views (default 5): ").strip() or "5")
        count = max(1, count)
    except:
        count = 5
    
    print(f"\n🚀 Starting {count} requests...")
    print(f"🎯 Target: {target_url}")
    print(f"🖥️ Mode: Chrome headless + Tor")
    if use_linkedin:
        print(f"🔵 Referrer: LinkedIn posts")
    print()
    
    # Create browser
    print("🔧 Setting up Chrome with Tor...")
    driver = create_tor_chrome_driver()
    
    if not driver:
        print("❌ Could not create browser driver")
        print("💡 Try: sudo apt install chromium-browser")
        return
    
    print("✅ Browser ready!\n")
    
    success = 0
    fail = 0
    unique_ips = set()
    previous_ip = None
    start = time.time()
    
    try:
        for i in range(1, count + 1):
            print(f"\n{'='*50}")
            print(f"📊 Request {i}/{count}")
            print(f"{'='*50}")
            
            ok, current_ip = visit_url(target_url, i, driver, previous_ip, use_linkedin_referrer=use_linkedin)
            
            if ok:
                success += 1
                if current_ip != "Unknown":
                    unique_ips.add(current_ip)
                    previous_ip = current_ip
            else:
                fail += 1
            
            rate = (success / i * 100) if i > 0 else 0
            print(f"\n📈 Progress: {success}/{i} success ({rate:.0f}%)")
            print(f"🌐 Unique IPs: {len(unique_ips)}")
            
            if i < count:
                delay = random.uniform(2, 4)
                print(f"💤 Waiting {delay:.1f}s...")
                time.sleep(delay)
    
    finally:
        print("\n🔒 Closing browser...")
        try:
            driver.quit()
        except:
            pass
    
    # Results
    elapsed = time.time() - start
    print(f"\n{'='*50}")
    print(f"🏁 RESULTS")
    print(f"{'='*50}")
    print(f"✅ Success: {success}/{count} ({success/count*100:.0f}%)")
    print(f"❌ Failed: {fail}/{count}")
    print(f"🌐 Unique IPs: {len(unique_ips)}")
    print(f"⏱️ Time: {elapsed:.1f}s ({elapsed/count:.1f}s/request)")
    if use_linkedin:
        print(f"\n📧 Microsoft email notifications should arrive for these {success} LinkedIn visits")
    print(f"\n✨ Done! All requests used Tor in real browser.")

if __name__ == "__main__":
    main()
