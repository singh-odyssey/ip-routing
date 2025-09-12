#!/usr/bin/env python3
"""
FREE JAVASCRIPT FINGERPRINT BOT
===============================

This bot simulates FingerprintJS by:
1. Generating fake but realistic browser fingerprints
2. Executing JavaScript-like requests
3. Sending proper deviceId + ipAddress to the server
4. Using rotating Tor IPs (free unique IPs)

NO PAID SERVICES REQUIRED!
"""

import requests
import random
import time
import hashlib
import json
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class FreeJSFingerprintBot:
    def __init__(self):
        self.target_url = "https://aiskillshouse.com/student/qr-mediator.html?uid=2827&promptId=6"
        self.api_url = "https://aiskillshouse.com/olivrweb/user/Api.php/setScore"
        self.success_count = 0
        self.failed_count = 0
        self.used_fingerprints = set()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Realistic browser characteristics for fingerprinting
        self.screen_resolutions = [
            [1920, 1080], [1366, 768], [1536, 864], [1440, 900],
            [1280, 720], [1024, 768], [1600, 900], [1680, 1050]
        ]
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'
        ]
        
        self.timezones = [
            'America/New_York', 'America/Los_Angeles', 'America/Chicago',
            'Europe/London', 'Europe/Paris', 'Europe/Berlin',
            'Asia/Tokyo', 'Asia/Shanghai', 'Asia/Kolkata'
        ]
        
        self.languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.9',
            'en-US,en;q=0.8,es;q=0.6',
            'en-CA,en;q=0.9',
            'de-DE,de;q=0.9,en;q=0.8'
        ]
        
        # WebGL and Canvas fingerprint components
        self.webgl_vendors = [
            'Google Inc. (Intel)', 'Google Inc. (NVIDIA)',
            'Google Inc. (AMD)', 'WebKit WebGL',
            'Mozilla Firefox WebGL'
        ]
        
        self.canvas_fonts = [
            'Arial', 'Helvetica', 'Times New Roman', 'Courier New',
            'Verdana', 'Georgia', 'Palatino', 'Garamond'
        ]
    
    def generate_realistic_fingerprint(self):
        """Generate a realistic browser fingerprint like FingerprintJS"""
        
        # Basic browser info
        user_agent = random.choice(self.user_agents)
        screen_res = random.choice(self.screen_resolutions)
        timezone = random.choice(self.timezones)
        language = random.choice(self.languages)
        
        # Advanced fingerprint components
        webgl_vendor = random.choice(self.webgl_vendors)
        canvas_font = random.choice(self.canvas_fonts)
        
        # Simulate hardware concurrency (CPU cores)
        hardware_concurrency = random.choice([2, 4, 6, 8, 12, 16])
        
        # Simulate device memory (GB)
        device_memory = random.choice([2, 4, 8, 16, 32])
        
        # Color depth and pixel depth
        color_depth = random.choice([24, 32])
        pixel_depth = random.choice([24, 32])
        
        # Audio context fingerprint (simulated)
        audio_hash = hashlib.md5(f"{random.random()}".encode()).hexdigest()[:8]
        
        # Build fingerprint object like FingerprintJS would
        fingerprint_data = {
            'userAgent': user_agent,
            'screenResolution': f"{screen_res[0]}x{screen_res[1]}",
            'timezone': timezone,
            'language': language,
            'hardwareConcurrency': hardware_concurrency,
            'deviceMemory': device_memory,
            'colorDepth': color_depth,
            'pixelDepth': pixel_depth,
            'webglVendor': webgl_vendor,
            'canvasFont': canvas_font,
            'audioHash': audio_hash,
            'touchSupport': random.choice([True, False]),
            'cookieEnabled': True,
            'doNotTrack': random.choice([True, False, None]),
            'platform': 'Win32' if 'Windows' in user_agent else 'MacIntel' if 'Mac' in user_agent else 'Linux x86_64'
        }
        
        # Create unique deviceId by hashing all components
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        device_id = hashlib.sha256(fingerprint_string.encode()).hexdigest()[:16]
        
        return device_id, fingerprint_data
    
    def setup_tor_session(self):
        """Setup session with Tor proxy"""
        session = requests.Session()
        
        # Tor SOCKS proxy
        session.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get_current_ip(self, session):
        """Get current IP through Tor"""
        try:
            response = session.get('http://httpbin.org/ip', timeout=10)
            return response.json().get('origin', 'unknown')
        except:
            return 'unknown'
    
    def restart_tor_circuit(self):
        """Get new Tor circuit for different IP"""
        try:
            import subprocess
            subprocess.run(['sudo', 'service', 'tor', 'restart'], check=True, timeout=15)
            time.sleep(8)  # Wait for new circuit
            return True
        except:
            return False
    
    def simulate_page_load_and_fingerprint(self, visit_id):
        """Simulate loading the page and executing FingerprintJS"""
        
        session = self.setup_tor_session()
        
        try:
            # Generate unique fingerprint for this visit
            device_id, fingerprint_data = self.generate_realistic_fingerprint()
            
            # Ensure fingerprint is unique
            if device_id in self.used_fingerprints:
                # Regenerate if duplicate
                device_id, fingerprint_data = self.generate_realistic_fingerprint()
            
            self.used_fingerprints.add(device_id)
            
            # Get current IP
            current_ip = self.get_current_ip(session)
            
            self.logger.info(f"Visit {visit_id}: Generated fingerprint")
            self.logger.info(f"Visit {visit_id}: Device ID: {device_id}")
            self.logger.info(f"Visit {visit_id}: Current IP: {current_ip}")
            self.logger.info(f"Visit {visit_id}: Browser: {fingerprint_data['userAgent'][:50]}...")
            
            # Set realistic headers based on fingerprint
            headers = {
                'User-Agent': fingerprint_data['userAgent'],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': fingerprint_data['language'],
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
            session.headers.update(headers)
            
            # Step 1: Load the main page (simulate browser loading)
            self.logger.info(f"Visit {visit_id}: Loading main page...")
            response = session.get(self.target_url, timeout=30)
            
            if response.status_code != 200:
                self.logger.error(f"Visit {visit_id}: Failed to load page: {response.status_code}")
                return False
            
            # Simulate JavaScript execution delay
            js_execution_time = random.uniform(3, 8)
            self.logger.info(f"Visit {visit_id}: Simulating JS execution ({js_execution_time:.1f}s)...")
            time.sleep(js_execution_time)
            
            # Step 2: Send fingerprint data to setScore API (like JavaScript would)
            self.logger.info(f"Visit {visit_id}: Sending fingerprint to API...")
            
            # Prepare form data exactly like the JavaScript does
            form_data = {
                'uid': '2827',
                'promptId': '6',
                'deviceId': device_id,
                'ipAddress': current_ip
            }
            
            # API request headers
            api_headers = headers.copy()
            api_headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://aiskillshouse.com',
                'Referer': self.target_url,
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            # Send to API
            api_response = session.post(
                self.api_url,
                data=form_data,
                headers=api_headers,
                timeout=30
            )
            
            self.logger.info(f"Visit {visit_id}: API Response: {api_response.status_code}")
            
            if api_response.status_code == 200:
                try:
                    response_data = api_response.json()
                    self.logger.info(f"Visit {visit_id}: API Response: {response_data}")
                    
                    if response_data.get('status') == True:
                        self.logger.info(f"Visit {visit_id}: ✅ ENGAGEMENT ACCEPTED!")
                        return True
                    else:
                        self.logger.warning(f"Visit {visit_id}: ⚠️ API rejected: {response_data.get('message', 'Unknown error')}")
                        return False
                        
                except json.JSONDecodeError:
                    self.logger.info(f"Visit {visit_id}: ✅ API called successfully (non-JSON response)")
                    return True
            else:
                self.logger.error(f"Visit {visit_id}: API request failed: {api_response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Visit {visit_id}: ❌ Error: {e}")
            return False
    
    def run_free_campaign(self, num_visits=3, delay_range=(30, 60)):
        """Run free fingerprint campaign with Tor rotation"""
        
        print("🆓 FREE JAVASCRIPT FINGERPRINT BOT")
        print("=" * 60)
        print("✅ Generates realistic browser fingerprints")
        print("✅ Simulates FingerprintJS execution")
        print("✅ Uses free Tor IP rotation")
        print("✅ Sends proper deviceId + ipAddress")
        print("=" * 60)
        
        self.logger.info(f"🎯 Target: {self.target_url}")
        self.logger.info(f"📊 Planned visits: {num_visits}")
        self.logger.info(f"⏱️ Delay range: {delay_range[0]}-{delay_range[1]}s")
        
        for i in range(1, num_visits + 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"🚀 Starting visit {i}/{num_visits}")
            
            # Get new Tor IP for this visit
            if i > 1:
                self.logger.info(f"Visit {i}: Getting new Tor IP...")
                self.restart_tor_circuit()
            
            # Make fingerprinted engagement
            success = self.simulate_page_load_and_fingerprint(i)
            
            if success:
                self.success_count += 1
                self.logger.info(f"📝 Visit {i}: ✅ SUCCESS")
            else:
                self.failed_count += 1
                self.logger.info(f"📝 Visit {i}: ❌ FAILED")
            
            # Wait before next visit
            if i < num_visits:
                delay = random.uniform(delay_range[0], delay_range[1])
                self.logger.info(f"⏳ Waiting {delay:.1f}s before next visit...")
                time.sleep(delay)
        
        # Final results
        success_rate = (self.success_count / num_visits) * 100
        
        print(f"\n🏆 FREE FINGERPRINT CAMPAIGN RESULTS:")
        print(f"✅ Successful engagements: {self.success_count}")
        print(f"❌ Failed attempts: {self.failed_count}")
        print(f"📊 Success rate: {success_rate:.1f}%")
        print(f"🧬 Unique fingerprints generated: {len(self.used_fingerprints)}")
        print(f"🆓 Total cost: $0 (completely free!)")

def main():
    import subprocess
    
    # Check Tor service
    try:
        result = subprocess.run(['pgrep', 'tor'], capture_output=True)
        if result.returncode != 0:
            print("❌ Tor service not running. Starting Tor...")
            subprocess.run(['sudo', 'service', 'tor', 'start'], check=True)
            time.sleep(5)
    except:
        print("❌ Could not start Tor service")
        return
    
    bot = FreeJSFingerprintBot()
    bot.run_free_campaign(3, (20, 40))

if __name__ == "__main__":
    main()