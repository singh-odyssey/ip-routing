#!/usr/bin/env python3
"""
TOR BROWSER REQUESTS
====================

This script opens URLs in a real web browser (Firefox/Chrome) configured to route
traffic through the Tor network. You'll see the actual browser window open and load
the pages with Tor routing.

Features:
- Opens real browser windows (Firefox/Chrome)
- Routes all browser traffic through Tor SOCKS5 proxy
- Automatically manages Tor service
- Shows visual browser interaction
- Each request gets a new Tor identity (new IP)

Prerequisites:
- Tor service (sudo apt install tor)
- Firefox or Chrome/Chromium browser
- Selenium and WebDriver (installed via requirements.txt)
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
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mute noisy loggers
logging.getLogger('stem').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('WDM').setLevel(logging.WARNING)

# Configuration
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = None

def is_port_open(port):
    """Check if a port is open on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_tor_process():
    """Start the Tor process if it's not already running"""
    if is_port_open(TOR_SOCKS_PORT):
        logger.info("✅ Tor is already running.")
        return True

    logger.info("🚀 Tor is not running. Attempting to start Tor process...")
    
    if not shutil.which("tor"):
        logger.error("❌ 'tor' executable not found. Please install: sudo apt install tor")
        return False

    try:
        tor_cmd = [
            "tor",
            "--ControlPort", str(TOR_CONTROL_PORT),
            "--SocksPort", str(TOR_SOCKS_PORT),
            "--DataDirectory", "/tmp/tor_data_custom"
        ]
        
        logger.info(f"🚀 Starting Tor with command: {' '.join(tor_cmd)}")
        subprocess.Popen(tor_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("⏳ Waiting for Tor to bootstrap...")
        
        for i in range(60):
            if is_port_open(TOR_SOCKS_PORT):
                logger.info("✅ Tor started successfully!")
                return True
            if i % 5 == 0:
                logger.info("   ...still waiting for Tor...")
            time.sleep(1)
            
        logger.error("❌ Timed out waiting for Tor to start.")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to start Tor: {e}")
        return False

def renew_tor_ip(max_retries=3):
    """Signal Tor controller to get a new identity (new IP)"""
    for attempt in range(max_retries):
        controller = None
        try:
            controller = Controller.from_port(port=TOR_CONTROL_PORT)
            if TOR_PASSWORD:
                controller.authenticate(password=TOR_PASSWORD)
            else:
                controller.authenticate()
            
            controller.signal(Signal.NEWNYM)
            logger.info("🔄 Signal sent to Tor for new identity (NEWNYM)")
            
            wait_time = controller.get_newnym_wait()
            controller.close()
            
            actual_wait = max(wait_time, 5)
            time.sleep(actual_wait)
            logger.info("✅ New Tor circuit established")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")
            if controller:
                try:
                    controller.close()
                except:
                    pass
            if attempt < max_retries - 1:
                time.sleep(2)
    
    logger.error("❌ Failed to renew Tor IP after all retries")
    return False

def create_firefox_driver(headless=True):
    """Create a Firefox WebDriver configured to use Tor"""
    try:
        firefox_options = FirefoxOptions()
        
        # Configure Firefox to use Tor SOCKS proxy
        firefox_options.set_preference("network.proxy.type", 1)
        firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
        firefox_options.set_preference("network.proxy.socks_port", TOR_SOCKS_PORT)
        firefox_options.set_preference("network.proxy.socks_version", 5)
        firefox_options.set_preference("network.proxy.socks_remote_dns", True)
        
        # Privacy settings
        firefox_options.set_preference("privacy.trackingprotection.enabled", True)
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference("useAutomationExtension", False)
        
        # Disable WebRTC to prevent IP leaks
        firefox_options.set_preference("media.peerconnection.enabled", False)
        
        # Run in headless mode for containers/servers
        if headless:
            firefox_options.add_argument("--headless")
            logger.info("🔇 Running in headless mode (no GUI)")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        logger.info("✅ Firefox driver created with Tor proxy")
        return driver, "Firefox"
    except Exception as e:
        logger.error(f"❌ Failed to create Firefox driver: {e}")
        return None, None

def create_chrome_driver(headless=True):
    """Create a Chrome WebDriver configured to use Tor"""
    try:
        chrome_options = ChromeOptions()
        
        # Configure Chrome to use Tor SOCKS proxy
        chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{TOR_SOCKS_PORT}')
        chrome_options.add_argument('--host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 127.0.0.1"')
        
        # Privacy and anti-detection settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Run in headless mode for containers/servers
        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            logger.info("🔇 Running in headless mode (no GUI)")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("✅ Chrome driver created with Tor proxy")
        return driver, "Chrome"
def get_browser_driver(browser_type="auto", headless=True):
    """Get a browser driver configured to use Tor"""
    if browser_type.lower() == "firefox":
        return create_firefox_driver(headless)
    elif browser_type.lower() == "chrome":
        return create_chrome_driver(headless)
    else:
        # Auto-detect: Try Firefox first, then Chrome
        logger.info("🔍 Auto-detecting browser...")
        driver, name = create_firefox_driver(headless)
        if driver:
            return driver, name
        
        logger.info("🔍 Firefox not available, trying Chrome...")
        return create_chrome_driver(headless)
            return driver, name
        
        logger.info("🔍 Firefox not available, trying Chrome...")
        return create_chrome_driver()

def check_tor_ip(driver):
    """Check current IP using the browser"""
    try:
        driver.get("https://api.ipify.org?format=json")
        time.sleep(2)
        
        # Get the page source and extract IP
        page_source = driver.page_source
        if '"ip"' in page_source:
            import json
            # Extract JSON from pre tag (rendered by browser)
            start = page_source.find('{"ip"')
            if start != -1:
                end = page_source.find('}', start) + 1
                json_str = page_source[start:end]
                data = json.loads(json_str)
                return data.get('ip', 'Unknown')
        
        return "Unknown"
    except Exception as e:
        logger.warning(f"⚠️ Could not check IP: {e}")
        return "Unknown"

def visit_url_in_browser(url, session_id, driver, browser_name, previous_ip=None):
    """Visit URL in browser through Tor"""
    try:
        # 1. Renew Tor IP
        if not renew_tor_ip():
            print(f"[{session_id}] ⚠️ Failed to renew IP")
            return False, previous_ip
        
        # 2. Verify new IP
        current_ip = check_tor_ip(driver)
        print(f"\n[{session_id}] 🌍 Current Tor IP: {current_ip}")
        
        if previous_ip and current_ip == previous_ip and current_ip != "Unknown":
            print(f"[{session_id}] ⚠️ IP didn't change, but continuing...")
        
        # 3. Visit target URL in browser
        print(f"[{session_id}] 🚀 Opening URL in {browser_name}: {url}")
        start_time = time.time()
        
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        elapsed = time.time() - start_time
        
        # Get page title
        try:
            title = driver.title
            print(f"[{session_id}] 📄 Page Title: {title}")
        except:
            print(f"[{session_id}] 📄 Page loaded")
        
        print(f"[{session_id}] ✅ Successfully opened in browser (Time: {elapsed:.2f}s)")
        
        # Keep browser open for viewing
        view_time = random.uniform(5, 10)
        print(f"[{session_id}] 👀 Keeping browser open for {view_time:.2f}s...")
        time.sleep(view_time)
        
        return True, current_ip
        
    except Exception as e:
        print(f"[{session_id}] ❌ Error: {e}")
        return False, previous_ip

def main():
    print("🧅 TOR BROWSER REQUESTS")
    print("=" * 50)
    print("✨ Opens URLs in real browser through Tor network")
    print("=" * 50)
    
    # Ensure Tor is running
    if not start_tor_process():
        print("❌ Could not start Tor. Please install: sudo apt install tor")
        return

    # Get browser preference
    print("\n🌐 Choose browser:")
    print("  1. Firefox (recommended)")
    print("  2. Chrome/Chromium")
    print("  3. Auto-detect")
    browser_choice = input("Enter choice (1-3, default: 3): ").strip()
    
    browser_map = {"1": "firefox", "2": "chrome", "3": "auto", "": "auto"}
    browser_type = browser_map.get(browser_choice, "auto")
    
    # Ask about headless mode
    print("\n🖥️ Display mode:")
    print("  1. Headless (no GUI, works in containers)")
    print("  2. GUI mode (requires X server)")
    headless_choice = input("Enter choice (1-2, default: 1): ").strip()
    headless = headless_choice != "2"

    # Get URL
    target_url = input("\n🔗 Enter target URL: ").strip()
    if not target_url:
        print("❌ URL is required.")
        return
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
        print(f"💡 Added HTTPS: {target_url}")

    # Get count
    try:
        count_input = input("🔢 Number of views (default 5): ").strip()
    print(f"\n🚀 Starting {count} browser requests via Tor...")
    print(f"🎯 Target: {target_url}")
    print(f"📱 Browser: {browser_type}")
    print(f"🖥️ Mode: {'Headless' if headless else 'GUI'}")
    
    # Create browser driver
    print("\n🔧 Setting up browser with Tor proxy...")
    driver, browser_name = get_browser_driver(browser_type, headless)
    print(f"\n🚀 Starting {count} browser requests via Tor...")
    print(f"🎯 Target: {target_url}")
    print(f"📱 Browser: {browser_type}")
    
    # Create browser driver
    print("\n🔧 Setting up browser with Tor proxy...")
    driver, browser_name = get_browser_driver(browser_type)
    
    if not driver:
        print("❌ Could not create browser driver. Please ensure Firefox or Chrome is installed.")
        print("💡 Install Firefox: sudo apt install firefox")
        print("💡 Install Chrome: sudo apt install chromium-browser")
        return
    
    print(f"✅ {browser_name} is ready and configured to use Tor!\n")
    
    success_count = 0
    fail_count = 0
    unique_ips = set()
    previous_ip = None
    start_time = time.time()
    
    try:
        for i in range(1, count + 1):
            print(f"\n{'='*50}")
            print(f"📊 Request {i}/{count}")
            print(f"{'='*50}")
            
            success, current_ip = visit_url_in_browser(
                target_url, i, driver, browser_name, previous_ip
            )
            
            if success:
                success_count += 1
                if current_ip and current_ip != "Unknown":
                    unique_ips.add(current_ip)
                    previous_ip = current_ip
            else:
                fail_count += 1
            
            # Progress
            success_rate = (success_count / i * 100) if i > 0 else 0
            print(f"\n📈 Progress: {success_count} success, {fail_count} failed ({success_rate:.1f}% success rate)")
            print(f"🌐 Unique IPs used: {len(unique_ips)}")
            
            # Delay between requests
            if i < count:
                delay = random.uniform(3, 6)
                print(f"💤 Waiting {delay:.2f}s before next request...")
                time.sleep(delay)
    
    finally:
        # Close browser
        print("\n🔒 Closing browser...")
        try:
            driver.quit()
        except:
            pass
    
    # Final statistics
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"🏁 FINAL RESULTS")
    print(f"{'='*50}")
    print(f"✅ Successful requests: {success_count}/{count} ({success_count/count*100:.1f}%)")
    print(f"❌ Failed requests: {fail_count}/{count}")
    print(f"🌐 Unique IP addresses: {len(unique_ips)}")
    print(f"⏱️ Total time: {elapsed:.2f} seconds")
    print(f"\n✨ All done! Your requests were sent through Tor in a real browser.")

if __name__ == "__main__":
    main()
