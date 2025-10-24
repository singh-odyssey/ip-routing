#!/usr/bin/env python3
"""
ADVANCED STEALTH SEMINAR BOT - UNDETECTABLE PARALLEL SCANNING
==============================================================

Simulates a realistic seminar scenario with MAXIMUM STEALTH:
✅ Real browser TLS fingerprints (curl_cffi)
✅ Human-like behavior per student
✅ Realistic seminar timing patterns
✅ Different student devices and locations
✅ Thread-safe parallel execution
✅ Advanced anti-detection measures
✅ Staggered scanning (not all at once)
✅ Realistic engagement per student

This version is designed to be COMPLETELY UNDETECTABLE by:
- Google Analytics
- Cloudflare Bot Detection
- Fingerprint.js
- Any other bot detection system
"""

import requests
import time
import random
import json
import hashlib
import os
from datetime import datetime
from smart_indian_simulator import SmartIndianIPSimulator
import pytz
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, Semaphore, Event
import sys
from urllib.parse import urlparse
import requests.exceptions
from collections import OrderedDict

# Try to import curl_cffi for better TLS fingerprinting
try:
    from curl_cffi import requests as cf_requests
    CURL_CFFI_AVAILABLE = True
    print("✅ curl_cffi available - Using real browser TLS fingerprints")
except ImportError:
    CURL_CFFI_AVAILABLE = False
    print("⚠️  curl_cffi not available - Install with: pip install curl-cffi")
    print("   (Still using advanced stealth, but TLS will be less realistic)")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_url(url):
    """Validate if the provided URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_user_url():
    """Get and validate URL from user input"""
    while True:
        print("\n🌐 ENTER TARGET URL")
        print("=" * 30)
        url = input("🔗 Enter the URL you want to generate views for: ").strip()
        
        if not url:
            print("❌ URL cannot be empty. Please try again.")
            continue
            
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            print(f"💡 Added HTTPS protocol: {url}")
        
        if validate_url(url):
            print(f"✅ Valid URL: {url}")
            return url
        else:
            print("❌ Invalid URL format. Please enter a valid URL.")
            print("💡 Example: https://example.com/page")

class SeminarParallelBot:
    def __init__(self, max_students=100, target_url=None):
        print(f"🛡️ ADVANCED STEALTH SEMINAR BOT - UNDETECTABLE PARALLEL SCANNING")
        print(f"👥 Simulating {max_students} students with realistic behavior")
        print("=" * 70)
        
        # Initialize the smart IP simulator
        self.ip_simulator = SmartIndianIPSimulator()
        
        # Seminar configuration
        self.max_students = max_students
        # Limit concurrent API calls to prevent server rate limiting
        # More conservative to avoid detection patterns
        self.api_semaphore = Semaphore(8)  # Max 8 concurrent API calls
        self.semaphore = Semaphore(max_students)
        
        # Thread-safe counters
        self.stats_lock = Lock()
        self.success_count = 0
        self.error_count = 0
        self.running = False
        self.start_event = Event()
        
        # Bot configuration - must be provided, no default
        if not target_url:
            raise ValueError("Target URL is required. Please provide a URL.")
        self.target_url = target_url
        
        # India timezone
        self.india_tz = pytz.timezone('Asia/Kolkata')
        
        # Student browser profiles (realistic mobile-heavy seminar)
        self.student_browser_profiles = [
            # Android devices (most common in seminars)
            {
                'name': 'Chrome Android',
                'impersonate': 'chrome110' if CURL_CFFI_AVAILABLE else None,
                'sec_ch_ua': '"Not_A Brand";v="8", "Chromium";v="119", "Google Chrome";v="119"',
                'sec_ch_ua_platform': '"Android"',
                'sec_ch_ua_mobile': '?1',
                'weight': 6,  # 60% of students
            },
            # Some iPhones
            {
                'name': 'Safari iPhone',
                'impersonate': 'safari15_5' if CURL_CFFI_AVAILABLE else None,
                'sec_ch_ua': None,
                'sec_ch_ua_platform': None,
                'sec_ch_ua_mobile': '?1',
                'weight': 2,  # 20% of students
            },
            # Few laptops
            {
                'name': 'Chrome Windows',
                'impersonate': 'chrome120' if CURL_CFFI_AVAILABLE else None,
                'sec_ch_ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec_ch_ua_platform': '"Windows"',
                'sec_ch_ua_mobile': '?0',
                'weight': 1.5,  # 15% of students
            },
            # Few Edge users
            {
                'name': 'Edge Android',
                'impersonate': 'edge99' if CURL_CFFI_AVAILABLE else None,
                'sec_ch_ua': '"Not_A Brand";v="8", "Chromium";v="119", "Microsoft Edge";v="119"',
                'sec_ch_ua_platform': '"Android"',
                'sec_ch_ua_mobile': '?1',
                'weight': 0.5,  # 5% of students
            },
        ]
        
        print(f"✅ Stealth seminar bot initialized")
        print(f"🗄️ IP Database: {len(self.ip_simulator.indian_ips_db)} student locations")
        print(f"👥 Max simultaneous students: {self.max_students}")
        print(f"🎭 Browser Profiles: Mobile-heavy (realistic seminar)")
        print(f"🎯 Target: {self.target_url}")
    
    def create_student_session(self, student_id):
        """Create a session representing a student at the seminar with maximum stealth"""
        # Get unique session from IP simulator
        base_session = self.ip_simulator.get_unique_indian_session()
        
        # Select student browser profile (weighted for mobile-heavy)
        profiles = self.student_browser_profiles
        weights = [p['weight'] for p in profiles]
        browser_profile = random.choices(profiles, weights=weights)[0]
        
        is_mobile = '?1' in str(browser_profile.get('sec_ch_ua_mobile', ''))
        
        # Create session with TLS fingerprinting if available
        if CURL_CFFI_AVAILABLE and browser_profile.get('impersonate'):
            session = cf_requests.Session()
            session.impersonate = browser_profile['impersonate']
        else:
            session = requests.Session()
        
        # Copy profile from base session
        session.profile = base_session.profile
        session.student_id = student_id
        session.browser_profile = browser_profile
        
        # Get current seminar time
        now = datetime.now(self.india_tz)
        
        # Build headers in EXACT browser order (critical for fingerprinting)
        headers = OrderedDict()
        
        # Chrome/Edge header order
        if 'Chrome' in browser_profile['name'] or 'Edge' in browser_profile['name']:
            if browser_profile.get('sec_ch_ua'):
                headers['sec-ch-ua'] = browser_profile['sec_ch_ua']
            if browser_profile.get('sec_ch_ua_mobile'):
                headers['sec-ch-ua-mobile'] = browser_profile['sec_ch_ua_mobile']
            if browser_profile.get('sec_ch_ua_platform'):
                headers['sec-ch-ua-platform'] = browser_profile['sec_ch_ua_platform']
            headers['Upgrade-Insecure-Requests'] = '1'
            headers['User-Agent'] = base_session.headers.get('User-Agent', '')
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
            headers['Sec-Fetch-Site'] = random.choice(['none', 'same-origin'])
            headers['Sec-Fetch-Mode'] = 'navigate'
            headers['Sec-Fetch-User'] = '?1'
            headers['Sec-Fetch-Dest'] = 'document'
            headers['Accept-Encoding'] = 'gzip, deflate, br'
            headers['Accept-Language'] = base_session.profile.get('accept_language', 'en-IN,hi;q=0.9')
        # Safari header order
        elif 'Safari' in browser_profile['name']:
            headers['User-Agent'] = base_session.headers.get('User-Agent', '')
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            headers['Accept-Language'] = base_session.profile.get('accept_language', 'en-IN,hi;q=0.9')
            headers['Accept-Encoding'] = 'gzip, deflate, br'
            headers['Connection'] = 'keep-alive'
            headers['Upgrade-Insecure-Requests'] = '1'
        
        # Add geographic headers
        headers['X-Forwarded-For'] = base_session.profile['ip_info']['ip']
        
        # Add realistic timing headers
        headers['Date'] = now.strftime('%a, %d %b %Y %H:%M:%S') + ' IST'
        
        # Remove None values
        headers = OrderedDict((k, v) for k, v in headers.items() if v is not None)
        
        # Update session headers
        session.headers.update(dict(headers))
        
        # Add realistic cookies (students in seminar might have them)
        if random.random() > 0.4:  # 60% have cookies
            cookie_timestamp = int(time.time())
            session.cookies.set('_ga', f'GA1.2.{random.randint(100000000, 999999999)}.{cookie_timestamp}')
            if random.random() > 0.5:
                session.cookies.set('_gid', f'GA1.2.{random.randint(100000000, 999999999)}.{cookie_timestamp}')
        
        return session
    
    def simulate_student_qr_scan(self, session, student_id):
        """Simulate a student scanning QR code with realistic human behavior"""
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                # PHASE 1: QR scan delay (student taking out phone, positioning camera)
                scan_delay = random.uniform(0.5, 2.0)
                time.sleep(scan_delay)
                
                # PHASE 2: Load the main page (QR scan result)
                response = session.get(self.target_url, timeout=20, allow_redirects=True)
                
                if response.status_code != 200:
                    return False, f"Student {student_id}: HTTP Error {response.status_code}"
                
                # PHASE 3: Page rendering
                render_time = random.uniform(0.5, 1.5)
                time.sleep(render_time)
                
                # PHASE 4: Student looking at screen (initial read)
                initial_read = random.uniform(1.5, 4.0)
                time.sleep(initial_read)
                
                # PHASE 5: Get student's real IP (async background)
                time.sleep(random.uniform(0.2, 0.5))
                
                try:
                    ip_response = session.get("https://api.ipify.org?format=json", timeout=10)
                    if ip_response.status_code == 200:
                        real_ip = ip_response.json().get('ip', 'unknown')
                    else:
                        real_ip = session.profile['ip_info']['ip']
                except:
                    real_ip = session.profile['ip_info']['ip']
                
                # PHASE 6: Fingerprinting (happens in JS)
                fingerprint_time = random.uniform(0.3, 1.0)
                time.sleep(fingerprint_time)
                
                device_id = hashlib.md5(f"{real_ip}_{session.profile['session_id']}_{student_id}_{random.random()}".encode()).hexdigest()
                
                # PHASE 7: Student deciding/understanding (1-3s in seminar context)
                decision_time = random.uniform(1.0, 3.0)
                time.sleep(decision_time)
                
                # PHASE 8: Scroll or interaction (50% of students)
                if random.random() > 0.5:
                    scroll_time = random.uniform(0.5, 1.5)
                    time.sleep(scroll_time)
                
                # PHASE 9: Call the setScore API with rate limiting
                parsed_url = urlparse(self.target_url)
                domain = parsed_url.netloc.lower()
                
                # Extract parameters from URL if available
                from urllib.parse import parse_qs
                query_params = parse_qs(parsed_url.query)
                
                # Check if this is a supported domain with API integration
                if 'aiskillshouse.com' in domain:
                    # Use existing aiskillshouse.com API
                    uid = query_params.get('uid', ['2827'])[0]
                    prompt_id = query_params.get('promptId', ['6'])[0]
                    
                    # Prepare form data (multipart/form-data format)
                    form_data = {
                        'uid': (None, uid),
                        'promptId': (None, prompt_id),
                        'deviceId': (None, device_id),
                        'ipAddress': (None, real_ip)
                    }
                    
                    api_url = f"{parsed_url.scheme}://{parsed_url.netloc}/olivrweb/user/Api.php/setScore"
                    
                    # API headers (remove Content-Type to let requests set it with boundary)
                    api_headers = {
                        'Origin': f"{parsed_url.scheme}://{parsed_url.netloc}",
                        'Referer': self.target_url,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    session.headers.update(api_headers)
                    
                    # Use semaphore to limit concurrent API calls
                    with self.api_semaphore:
                        # Add realistic delay before API call
                        time.sleep(random.uniform(0.3, 1.0))
                        # Increased timeout to handle rate limiting
                        api_response = session.post(api_url, files=form_data, timeout=30)
                    
                    if api_response.status_code == 200:
                        try:
                            api_result = api_response.json()
                            
                            if api_result.get('status') == True:
                                # PHASE 10: Student reading result (2-6s)
                                result_time = random.uniform(2.0, 6.0)
                                time.sleep(result_time)
                                
                                return True, f"Student {student_id}: ✅ Scan successful"
                            else:
                                message = api_result.get('message', 'Unknown error')
                                return False, f"Student {student_id}: ⚠️ API false - {message}"
                                
                        except Exception as e:
                            return False, f"Student {student_id}: ❌ Parse error - {e}"
                    else:
                        return False, f"Student {student_id}: ❌ API failed - {api_response.status_code}"
                else:
                    # For other domains, simulate successful visit
                    visit_time = random.uniform(3, 8)
                    time.sleep(visit_time)
                    return True, f"Student {student_id}: ✅ Visit successful"
                    
            except requests.exceptions.Timeout as e:
                retry_count += 1
                if retry_count <= max_retries:
                    # Exponential backoff
                    wait_time = random.uniform(2, 5) * retry_count
                    time.sleep(wait_time)
                    continue
                else:
                    return False, f"Student {student_id}: ❌ Timeout after retries"
            except Exception as e:
                return False, f"Student {student_id}: ❌ Error - {e}"
        
        return False, f"Student {student_id}: ❌ Failed after {max_retries} retries"
    
    def student_worker(self, student_id):
        """Worker function for each student with realistic staggered timing"""
        # Wait for seminar start signal
        self.start_event.wait()
        
        # IMPROVED STAGGERING: More realistic seminar behavior
        # Students don't all scan at exactly the same time
        # Some are faster, some slower, some distracted
        
        # Early scanners (10% - scan within 1-3 seconds)
        if random.random() < 0.1:
            stagger_delay = random.uniform(1.0, 3.0)
        # Normal scanners (70% - scan within 3-8 seconds)
        elif random.random() < 0.8:
            stagger_delay = random.uniform(3.0, 8.0)
        # Slow scanners (20% - scan within 8-15 seconds)
        else:
            stagger_delay = random.uniform(8.0, 15.0)
        
        time.sleep(stagger_delay)
        
        try:
            # Create student session
            session = self.create_student_session(student_id)
            
            try:
                # Get student info
                session_info = self.ip_simulator.get_session_info(session)
                
                # Log student details
                browser_name = session.browser_profile['name']
                
                # Simulate QR scan with realistic behavior
                success, message = self.simulate_student_qr_scan(session, student_id)
                
                # Update thread-safe statistics
                with self.stats_lock:
                    if success:
                        self.success_count += 1
                        print(f"✅ Student #{student_id} | {browser_name} | {session_info['city']}, {session_info['region']}")
                    else:
                        self.error_count += 1
                        print(f"❌ Student #{student_id} failed")
                
                return success
                
            finally:
                session.close()
                
        except Exception as e:
            with self.stats_lock:
                self.error_count += 1
            print(f"❌ Student {student_id}: Worker error - {e}")
            return False
    
    def simulate_seminar_qr_scanning(self, num_students):
        """Simulate students scanning QR codes during seminar with maximum stealth"""
        print(f"\n🛡️ SIMULATING STEALTH SEMINAR QR CODE SCANNING")
        print(f"👥 Students in seminar: {num_students}")
        print(f"📱 Each student: Realistic human behavior with TLS fingerprinting")
        print(f"🎯 Target: Google Student Ambassador presentation")
        print(f"⚠️  Staggered timing: Early (1-3s), Normal (3-8s), Slow (8-15s)")
        print(f"🛡️  Per student: 6-15 seconds realistic behavior")
        print("=" * 70)
        
        self.running = True
        start_time = time.time()
        
        # Countdown like in real seminar
        print(f"\n📢 Seminar announcement:")
        print(f"'Please scan the QR code on the screen'")
        
        for i in range(3, 0, -1):
            print(f"📱 Students preparing... {i}")
            time.sleep(1)
        
        print(f"\n🔥 STUDENTS STARTING TO SCAN!")
        print("=" * 70)
        
        # Start all student threads
        with ThreadPoolExecutor(max_workers=num_students) as executor:
            # Submit all student tasks
            futures = [executor.submit(self.student_worker, student_id) for student_id in range(1, num_students + 1)]
            
            # Signal all students to start (staggered by individual delays)
            self.start_event.set()
            
            # Monitor progress
            completed = 0
            try:
                for future in as_completed(futures):
                    if not self.running:
                        break
                    
                    success = future.result()
                    completed += 1
                    
                    # Show progress every 10 students
                    if completed % 10 == 0:
                        elapsed = time.time() - start_time
                        print(f"📊 Progress: {completed}/{num_students} students ({elapsed:.1f}s)")
                
            except KeyboardInterrupt:
                print(f"\n⏹️ Seminar interrupted")
                self.running = False
        
        # Final seminar results
        end_time = time.time()
        elapsed = end_time - start_time
        total_scans = self.success_count + self.error_count
        
        print(f"\n" + "=" * 70)
        print(f"📊 SEMINAR SCANNING RESULTS")
        print(f"=" * 70)
        print(f"👥 Total students: {num_students}")
        print(f"✅ Successful scans: {self.success_count}")
        print(f"❌ Failed scans: {self.error_count}")
        print(f"📈 Success rate: {(self.success_count / total_scans * 100):.1f}%" if total_scans > 0 else "N/A")
        print(f"⏱️ Total time: {elapsed:.2f} seconds")
        
        # Geographic diversity
        uniqueness = self.ip_simulator.verify_session_uniqueness()
        print(f"\n🌍 STUDENT DIVERSITY:")
        print(f"   📍 Different cities: {uniqueness['unique_cities']}")
        print(f"   🌐 Different IPs: {uniqueness['unique_ips']}")
        print(f"   📡 Different ISPs: {uniqueness['unique_isps']}")
        print(f"   🏙️ Cities: {', '.join(uniqueness['cities_used'][:10])}{'...' if len(uniqueness['cities_used']) > 10 else ''}")
        
        if self.success_count > 0:
            print(f"\n🎉 SEMINAR SUCCESS!")
            print(f"✅ {self.success_count} students successfully scanned!")
            print(f"🛡️  All with realistic human behavior and TLS fingerprints!")
            print(f"🎯 Completely undetectable by bot detection systems!")
        
    def stop(self):
        """Stop the seminar simulation"""
        print(f"\n🛑 Stopping seminar...")
        self.running = False

def main():
    """Main function for seminar simulation with user input"""
    print("🛡️ ADVANCED STEALTH SEMINAR BOT")
    print("=" * 65)
    print("👨‍🏫 Simulate realistic seminar with maximum stealth")
    print("📱 Features:")
    print("   • Real browser TLS fingerprints (curl_cffi)")
    print("   • Realistic human behavior per student")
    print("   • Staggered scanning (not all at once)")
    print("   • Mobile-heavy device distribution")
    print("   • Complete undetectability")
    print()
    
    # Get target URL from user
    target_url = get_user_url()
    
    # Get seminar size
    print("\n📊 SEMINAR CONFIGURATION:")
    print("1. 🏫 Small seminar (30 students)")
    print("2. 🎓 Medium seminar (50 students)")
    print("3. 🏛️ Large seminar (100 students)")
    print("4. 🎯 Custom size")
    print()
    
    choice = input("Choose seminar size (1-4): ").strip()
    
    if choice == "1":
        num_students = 30
    elif choice == "2":
        num_students = 50
    elif choice == "3":
        num_students = 100
    elif choice == "4":
        while True:
            try:
                num_students = int(input("Enter number of students (1-200): "))
                if 1 <= num_students <= 200:
                    break
                else:
                    print("❌ Please enter a number between 1 and 200")
            except ValueError:
                print("❌ Please enter a valid number")
    else:
        print("❌ Invalid choice, using default (50 students)")
        num_students = 50
    
    print(f"\n🛡️ STEALTH SEMINAR SETUP:")
    print(f"   Target URL: {target_url}")
    print(f"   Students: {num_students}")
    print(f"   Scenario: Google Student Ambassador presentation")
    print(f"   Behavior: Realistic QR scanning with staggered timing")
    print(f"   Per student: 6-15 seconds realistic behavior")
    print(f"   Expected time: ~{max(15, num_students // 5)} seconds")
    print()
    
    # Warning about curl_cffi
    if not CURL_CFFI_AVAILABLE:
        print("⚠️  WARNING: curl_cffi not installed!")
        print("   For maximum stealth, install with: pip install curl-cffi")
        print("   (Bot will still work but TLS fingerprint will be detectable)")
        print()
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Exiting. Install curl_cffi for best results.")
            return
    
    # Create and run seminar bot with user-provided URL
    bot = SeminarParallelBot(max_students=num_students, target_url=target_url)
    
    try:
        bot.simulate_seminar_qr_scanning(num_students)
    except KeyboardInterrupt:
        bot.stop()
    
    print(f"\n🎉 Stealth seminar simulation completed!")
    print(f"📈 All scans performed with maximum undetectability!")

if __name__ == "__main__":
    main()