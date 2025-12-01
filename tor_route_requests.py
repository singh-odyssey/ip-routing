#!/usr/bin/env python3
"""
TOR ROUTE REQUESTS GENERATOR
============================

This script routes HTTP requests through the Tor network, ensuring a new IP address
and a fresh browser fingerprint for each request.

Features:
- Routes traffic through Tor SOCKS5 proxy (default 127.0.0.1:9050)
- Requests new Tor identity (new IP) for each view
- Rotates User-Agents and headers to simulate different devices
- Configurable target URL and view count
- Simulates realistic user behavior (random delays)

Prerequisites:
- Tor service must be running and listening on port 9050 (SOCKS) and 9051 (Control).
- Control port must be authenticated (or open if configured that way).
"""

import requests
import socks
import socket
import time
import random
import logging
import subprocess
import shutil
import os
from stem import Signal
from stem.control import Controller

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mute stem logging to prevent noise
stem_logger = logging.getLogger('stem')
stem_logger.setLevel(logging.CRITICAL)

# Configuration
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = None  # Set this if your Tor control port requires a password

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
        logger.error("❌ 'tor' executable not found. Please install Tor: sudo apt install tor")
        return False

    try:
        # Start Tor in the background with specific configuration
        # We use a temporary data directory to avoid permission issues
        # and explicitly enable ControlPort and SocksPort
        tor_cmd = [
            "tor",
            "--ControlPort", str(TOR_CONTROL_PORT),
            "--SocksPort", str(TOR_SOCKS_PORT),
            "--DataDirectory", "/tmp/tor_data_custom"
        ]
        
        logger.info(f"🚀 Starting Tor with command: {' '.join(tor_cmd)}")
        subprocess.Popen(tor_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("⏳ Waiting for Tor to bootstrap...")
        
        # Wait up to 60 seconds for Tor to start
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

# Extensive list of User Agents to simulate different devices/browsers
USER_AGENTS = [
    # Windows Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    
    # Mac Chrome
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    
    # Linux Chrome
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    
    # Android Chrome
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    
    # iPhone Safari
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    
    # Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:122.0) Gecko/20100101 Firefox/122.0',
    
    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
]

def get_tor_session():
    """Create a requests session that routes through Tor"""
    session = requests.session()
    # Set the proxy to Tor's SOCKS5 port
    session.proxies = {
        'http': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
        'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}'
    }
    return session

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
            
            # Get wait time before closing
            wait_time = controller.get_newnym_wait()
            
            # Close controller explicitly
            controller.close()
            
            # Wait for the new circuit to be built (minimum 5 seconds for safety)
            actual_wait = max(wait_time, 5)
            time.sleep(actual_wait)
            logger.info("✅ New Tor circuit established")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")
            # Try to close if it failed
            if controller:
                try:
                    controller.close()
                except:
                    pass
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
    
    logger.error("❌ Failed to renew Tor IP after all retries")
    return False

def get_current_ip(session):
    """Check the current public IP address via the session"""
    # Try multiple IP check services for redundancy
    services = [
        'https://api.ipify.org?format=json',
        'https://icanhazip.com',
        'https://ifconfig.me/ip'
    ]
    
    for service in services:
        try:
            response = session.get(service, timeout=10)
            if response.status_code == 200:
                if 'ipify' in service:
                    return response.json().get('ip', 'Unknown')
                else:
                    return response.text.strip()
        except Exception:
            continue
    
    return "Unknown"

def generate_random_headers():
    """Generate random headers to simulate a real browser"""
    user_agent = random.choice(USER_AGENTS)
    
    # Determine if mobile based on user agent
    is_mobile = 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': random.choice([
            'en-US,en;q=0.9',
            'en-GB,en;q=0.9',
            'en-IN,en;q=0.9',
            'en-US,en;q=0.8',
            'en-CA,en;q=0.9',
            'en-AU,en;q=0.9'
        ]),
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': random.choice(['max-age=0', 'no-cache']),
        'DNT': str(random.choice([0, 1])),
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
        'Sec-Fetch-User': '?1'
    }
    
    # Add mobile-specific headers
    if is_mobile:
        headers['Sec-CH-UA-Mobile'] = '?1'
    else:
        headers['Sec-CH-UA-Mobile'] = '?0'
    
    return headers

def visit_url(url, session_id, previous_ip=None):
    """Visit the target URL with a fresh Tor session"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # 1. Renew IP
            if not renew_tor_ip():
                print(f"[{session_id}] ⚠️ Failed to renew IP, attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                return False
            
            # 2. Create new session
            session = get_tor_session()
            
            # 3. Set random headers (fingerprint)
            headers = generate_random_headers()
            session.headers.update(headers)
            
            # 4. Verify new IP address
            current_ip = get_current_ip(session)
            print(f"\n[{session_id}] 🌍 Current Tor IP: {current_ip}")
            
            # Check if IP actually changed
            if previous_ip and current_ip == previous_ip:
                print(f"[{session_id}] ⚠️ IP didn't change, retrying...")
                session.close()
                time.sleep(5)
                continue
            
            print(f"[{session_id}] 🎭 User-Agent: {headers['User-Agent'][:60]}...")
            
            # 5. Visit the target URL
            print(f"[{session_id}] 🚀 Visiting: {url}")
            start_time = time.time()
            response = session.get(url, timeout=30, allow_redirects=True)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                print(f"[{session_id}] ✅ Success! Status: {response.status_code} (Time: {elapsed:.2f}s)")
                print(f"[{session_id}] 📄 Response Size: {len(response.content)} bytes")
                
                # Simulate realistic reading/interaction time
                sleep_time = random.uniform(4, 10)
                print(f"[{session_id}] ⏳ Simulating user interaction ({sleep_time:.2f}s)...")
                time.sleep(sleep_time)
                
                session.close()
                return True, current_ip
            elif response.status_code in [301, 302, 303, 307, 308]:
                print(f"[{session_id}] 🔄 Redirected (Status: {response.status_code})")
                print(f"[{session_id}] ✅ Final URL reached successfully")
                session.close()
                return True, current_ip
            else:
                print(f"[{session_id}] ❌ Failed. Status: {response.status_code}")
                session.close()
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                return False, current_ip
                
        except requests.exceptions.Timeout:
            print(f"[{session_id}] ⏱️ Request timeout, attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return False, None
        except requests.exceptions.RequestException as e:
            print(f"[{session_id}] ❌ Request Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return False, None
        except Exception as e:
            print(f"[{session_id}] ❌ Unexpected Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return False, None
        finally:
            if 'session' in locals():
                try:
                    session.close()
                except:
                    pass
    
    return False, None

def main():
    print("🧅 TOR ROUTE REQUESTS GENERATOR")
    print("=" * 50)
    print("✨ Features: New IP per request, Random fingerprints")
    print("=" * 50)
    
    # Ensure Tor is running
    if not start_tor_process():
        print("❌ Could not start Tor. Please install: sudo apt install tor")
        return

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
        count_input = input("🔢 Number of views (default 10): ").strip()
        count = int(count_input) if count_input else 10
        if count <= 0:
            count = 10
            print(f"⚠️ Invalid count, using default: {count}")
    except ValueError:
        count = 10
        print(f"⚠️ Invalid input, using default: {count}")
        
    print(f"\n🚀 Starting {count} requests via Tor...")
    print(f"🎯 Target: {target_url}")
    print(f"⏱️ Estimated time: {count * 15}-{count * 25} seconds\n")
    
    success_count = 0
    fail_count = 0
    unique_ips = set()
    previous_ip = None
    start_time = time.time()
    
    for i in range(1, count + 1):
        print(f"\n{'='*50}")
        print(f"📊 Request {i}/{count}")
        print(f"{'='*50}")
        
        result = visit_url(target_url, i, previous_ip)
        
        if isinstance(result, tuple):
            success, current_ip = result
            if success:
                success_count += 1
                if current_ip and current_ip != "Unknown":
                    unique_ips.add(current_ip)
                    previous_ip = current_ip
            else:
                fail_count += 1
        else:
            # Backward compatibility
            if result:
                success_count += 1
            else:
                fail_count += 1
        
        # Show progress
        success_rate = (success_count / i * 100) if i > 0 else 0
        print(f"\n📈 Progress: {success_count} success, {fail_count} failed ({success_rate:.1f}% success rate)")
        print(f"🌐 Unique IPs used: {len(unique_ips)}")
        
        # Random delay between requests to be safe
        if i < count:
            delay = random.uniform(3, 7)
            print(f"💤 Cooling down for {delay:.2f}s...")
            time.sleep(delay)
    
    # Final statistics
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"🏁 FINAL RESULTS")
    print(f"{'='*50}")
    print(f"✅ Successful requests: {success_count}/{count} ({success_count/count*100:.1f}%)")
    print(f"❌ Failed requests: {fail_count}/{count}")
    print(f"🌐 Unique IP addresses: {len(unique_ips)}")
    print(f"⏱️ Total time: {elapsed:.2f} seconds")
    print(f"⚡ Average time per request: {elapsed/count:.2f} seconds")
    print(f"\n✨ All done! Your requests were sent through Tor.")

if __name__ == "__main__":
    main()
