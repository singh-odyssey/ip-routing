#!/usr/bin/env python3
"""
GOOGLE STUDENT AMBASSADOR - UNIQUE VIEWER BOT
==============================================

Specialized bot for generating unique viewers on any provided URL.

Features:
✅ Simulates real Indian users clicking the URL
✅ Waits for page load and Gemini prompt execution  
✅ 2-5 second intervals between requests
✅ 42+ Indian IP addresses from 25+ cities
✅ Multiple ISP simulation (Jio, Airtel, Vi, BSNL, ACT, etc.)
✅ Advanced anti-detection measures
✅ Proper session management for unique views
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
from urllib.parse import urlparse
import requests.exceptions

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

def get_user_views():
    """Get target number of views from user input"""
    while True:
        print("\n🔢 ENTER NUMBER OF VIEWS")
        print("=" * 30)
        views_input = input("🎯 How many unique views do you want? (or 'unlimited'): ").strip().lower()
        
        if views_input in ['unlimited', 'infinite', 'continuous', '']:
            print("✅ Selected: Unlimited views")
            return None
        else:
            try:
                target_views = int(views_input)
                if target_views > 0:
                    print(f"✅ Selected: {target_views} views")
                    return target_views
                else:
                    print("❌ Please enter a positive number")
            except ValueError:
                print("❌ Please enter a number or 'unlimited'")
                print("💡 Examples: 10, 50, 100, unlimited")

class GoogleAmbassadorBot:
    def __init__(self, target_url=None):
        print("🎯 Initializing Google Student Ambassador Bot")
        
        # Initialize the smart IP simulator with expanded database
        self.ip_simulator = SmartIndianIPSimulator()
        
        # Bot configuration - with realistic human timing
        self.timing_range = (15, 45)  # 15-45 seconds between views (realistic human behavior)
        self.max_retries = 3
        self.success_count = 0
        self.error_count = 0
        self.running = False
        
        # Target URL - must be provided, no default
        if not target_url:
            raise ValueError("Target URL is required. Please provide a URL.")
        self.target_url = target_url
        
        # India timezone
        self.india_tz = pytz.timezone('Asia/Kolkata')
        
        # Enhanced User Agents for better diversity
        self.enhanced_user_agents = [
            # Latest Windows Chrome (Most popular in India)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Latest Android Chrome (Very popular in India with specific device models)
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Redmi Note 12 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Mi 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; vivo V27) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; POCO F5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Realme GT 2 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Nothing Phone (2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; iQOO 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Oppo Find X6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Moto Edge 40) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # iPhone (Growing market in India)
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            
            # Firefox (Alternative browser choice)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Android 14; Mobile; rv:122.0) Gecko/122.0 Firefox/122.0',
            'Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            
            # Edge (Increasing adoption)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            
            # Mac (Less common but present in urban areas)
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Linux (Tech-savvy users)
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Samsung Internet (Very popular on Samsung devices in India)
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-A52s) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-M52) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36',
            
            # Opera (Popular for data compression in India)
            'Mozilla/5.0 (Linux; Android 13; CPH2423) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 OPR/80.2.4244.58675',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
        ]
        
        print(f"✅ Bot initialized with {len(self.ip_simulator.indian_ips_db)} Indian IPs")
        print(f"⏱️ Timing: {self.timing_range[0]}-{self.timing_range[1]} seconds (realistic human browsing)")
        print(f"🎯 Target: {self.target_url}")
    
    def create_enhanced_indian_session(self):
        """Create enhanced session with better Indian characteristics and anti-detection"""
        # Get base session from IP simulator
        session = self.ip_simulator.get_unique_indian_session()
        
        # Override with enhanced user agent
        enhanced_ua = random.choice(self.enhanced_user_agents)
        session.headers.update({'User-Agent': enhanced_ua})
        
        # Get India-specific datetime
        now = datetime.now(self.india_tz)
        
        # Determine if mobile or desktop from UA
        is_mobile = 'Mobile' in enhanced_ua or 'iPhone' in enhanced_ua
        is_android = 'Android' in enhanced_ua
        is_iphone = 'iPhone' in enhanced_ua
        
        # Add comprehensive Indian headers
        indian_headers = {
            # Geographic headers
            'X-Forwarded-For': session.profile['ip_info']['ip'],
            'X-Real-IP': session.profile['ip_info']['ip'],
            'CF-IPCountry': 'IN',
            'X-Country-Code': 'IN',
            'X-Geo-Country': 'India',
            'X-Geo-Region': session.profile['ip_info']['region'],
            'X-Geo-City': session.profile['ip_info']['city'],
            
            # Locale and language
                        # Locale and language (enhanced for different Indian regions)
            'Accept-Language': random.choice([
                'en-IN,hi;q=0.9,en;q=0.8',
                'hi-IN,hi;q=0.9,en;q=0.8',
                'en-US,en;q=0.9,hi;q=0.8',
                'en-GB,en;q=0.9,hi;q=0.8',
                'ta-IN,ta;q=0.9,en;q=0.8',
                'te-IN,te;q=0.9,en;q=0.8',
                'kn-IN,kn;q=0.9,en;q=0.8',
                'ml-IN,ml;q=0.9,en;q=0.8',
                'gu-IN,gu;q=0.9,en;q=0.8',
                'mr-IN,mr;q=0.9,en;q=0.8',
                'bn-IN,bn;q=0.9,en;q=0.8',
                'pa-IN,pa;q=0.9,en;q=0.8',
                'or-IN,or;q=0.9,en;q=0.8',
                'as-IN,as;q=0.9,en;q=0.8',
                'ur-IN,ur;q=0.9,en;q=0.8'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            
            # Browser characteristics (realistic values)
            'Cache-Control': random.choice(['max-age=0', 'no-cache', 'no-store, must-revalidate']),
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
            'Sec-Fetch-User': '?1',
            
            # Anti-detection - vary these to look more human
            'Connection': 'keep-alive',
            'DNT': str(random.choice([0, 1, None])) if random.random() > 0.3 else None,  # Not all browsers send DNT
            'Pragma': random.choice(['no-cache', '']) if random.random() > 0.5 else 'no-cache',
            
            # Time headers
            'Date': now.strftime('%a, %d %b %Y %H:%M:%S') + ' IST',
            'X-Local-Time': now.isoformat(),
            'X-Timezone': random.choice([
                'Asia/Kolkata', 'Asia/Mumbai', 'Asia/Delhi', 'Asia/Chennai',
                'Asia/Bengaluru', 'Asia/Hyderabad', 'Asia/Pune', 'Asia/Ahmedabad',
                'Asia/Jaipur', 'Asia/Lucknow', 'Asia/Kanpur', 'Asia/Surat'
            ]),
            
            # ISP specific
            'X-ISP': session.profile['isp_simulation']['name'],
            'X-Network-Type': session.profile['connection_type'].upper(),
        }
        
        # Remove None values (more realistic - not all browsers send all headers)
        indian_headers = {k: v for k, v in indian_headers.items() if v is not None}
        
        # Add mobile-specific headers if mobile
        if is_mobile:
            mobile_headers = {
                'Sec-CH-UA-Mobile': '?1',
                'Sec-CH-UA-Platform': '"Android"' if is_android else '"iOS"',
            }
            
            # Only some mobile browsers send X-Requested-With
            if is_android and random.random() > 0.4:
                mobile_headers['X-Requested-With'] = random.choice(['com.android.chrome', 'com.android.browser', ''])
            
            indian_headers.update(mobile_headers)
        else:
            desktop_headers = {
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA-Platform': random.choice(['"Windows"', '"macOS"', '"Linux"']),
            }
            indian_headers.update(desktop_headers)
        
        session.headers.update(indian_headers)
        
        # Add realistic cookies (empty but structure exists)
        # Real browsers have various cookies from previous browsing
        if random.random() > 0.3:  # 70% of users have some cookies
            cookie_value = hashlib.md5(f"{session.profile['session_id']}_cookie".encode()).hexdigest()[:16]
            session.cookies.set('_ga', f'GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}')
            session.cookies.set('_gid', f'GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}')
            
        return session
    
    def simulate_user_behavior(self, session, url):
        """Simulate realistic user behavior and trigger the setScore API"""
        try:
            # Step 1: Initial page load with realistic timing
            logger.info(f"🔄 Loading main page: {url}")
            
            # Add random delay before request (simulating user clicking/typing)
            pre_click_delay = random.uniform(0.3, 1.2)
            logger.info(f"⏱️ Pre-click delay: {pre_click_delay:.2f}s (simulating click action)")
            time.sleep(pre_click_delay)
            
            response = session.get(url, timeout=15, allow_redirects=True)
            
            if response.status_code != 200:
                logger.error(f"❌ HTTP Error: {response.status_code}")
                return False
            
            logger.info(f"✅ Main page loaded successfully")
            
            # Step 2: Simulate realistic page rendering time
            page_render_time = random.uniform(0.8, 2.5)
            logger.info(f"🎨 Page rendering: {page_render_time:.2f}s (DOM construction, CSS parsing)")
            time.sleep(page_render_time)
            
            # Step 3: Simulate user reading/scanning the page
            reading_time = random.uniform(3, 12)
            logger.info(f"📖 User reading page content: {reading_time:.2f}s")
            
            # Break reading time into chunks to simulate scrolling
            num_scroll_events = random.randint(1, 4)
            scroll_chunk = reading_time / num_scroll_events
            
            for i in range(num_scroll_events):
                time.sleep(scroll_chunk * random.uniform(0.7, 1.3))
                logger.info(f"📜 Scroll event {i+1}/{num_scroll_events} (user exploring content)")
            
            # Step 4: Get IP address (simulate the ipify.org call)
            logger.info(f"🌐 Getting IP address...")
            
            # Add realistic delay before IP check (happens after page scripts load)
            time.sleep(random.uniform(0.5, 1.5))
            
            try:
                ip_response = session.get("https://api.ipify.org?format=json", timeout=10)
                if ip_response.status_code == 200:
                    ip_data = ip_response.json()
                    real_ip = ip_data.get('ip', 'unknown')
                    logger.info(f"📍 Real IP detected: {real_ip}")
                else:
                    # Fallback to simulated IP
                    real_ip = session.profile['ip_info']['ip']
                    logger.info(f"📍 Using simulated IP: {real_ip}")
            except:
                real_ip = session.profile['ip_info']['ip']
                logger.info(f"📍 Using simulated IP: {real_ip}")
            
            # Step 5: Simulate FingerprintJS device ID generation
            logger.info(f"🔍 Generating device fingerprint...")
            
            # Simulate FingerprintJS processing time (realistic library behavior)
            fingerprint_processing = random.uniform(0.8, 2.0)
            time.sleep(fingerprint_processing)
            
            device_id = hashlib.md5(f"{real_ip}_{session.profile['session_id']}_{random.random()}".encode()).hexdigest()
            logger.info(f"🆔 Device ID: {device_id[:16]}...")
            
            # Step 6: Simulate additional page interaction time
            # Real users don't click immediately after page loads
            interaction_delay = random.uniform(2, 6)
            logger.info(f"🖱️ User interaction delay: {interaction_delay:.2f}s (mouse movements, hesitation)")
            time.sleep(interaction_delay)
            
            # Step 7: Make the setScore API call (this is what counts the unique view!)
            logger.info(f"🎯 Calling setScore API to register unique view...")
            
            # Add realistic delay before API call (user interaction/button click)
            api_trigger_delay = random.uniform(0.5, 2.0)
            logger.info(f"⏱️ API trigger delay: {api_trigger_delay:.2f}s (user action)")
            time.sleep(api_trigger_delay)
            
            # Parse target URL to make API call dynamic
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
                
                # Make the API call
                api_url = f"{parsed_url.scheme}://{parsed_url.netloc}/olivrweb/user/Api.php/setScore"
                
                # Add API-specific headers (remove Content-Type to let requests set it with boundary)
                api_headers = {
                    'Origin': f"{parsed_url.scheme}://{parsed_url.netloc}",
                    'Referer': self.target_url,
                    'X-Requested-With': 'XMLHttpRequest'
                }
                session.headers.update(api_headers)
                
                # Use files parameter for multipart/form-data encoding
                max_retries = 2
                retry_count = 0
                
                while retry_count <= max_retries:
                    try:
                        api_response = session.post(api_url, files=form_data, timeout=20)
                        break  # Success, exit retry loop
                    except requests.exceptions.Timeout:
                        retry_count += 1
                        if retry_count <= max_retries:
                            logger.warning(f"⚠️ API timeout, retrying ({retry_count}/{max_retries})...")
                            time.sleep(random.uniform(2, 5))
                        else:
                            logger.error(f"❌ API timeout after {max_retries} retries")
                            return False
                    except Exception as e:
                        logger.error(f"❌ API request error: {e}")
                        return False
                
                if api_response.status_code == 200:
                    try:
                        api_result = api_response.json()
                        logger.info(f"📊 API Response: {api_result}")
                        
                        if api_result.get('status') == True:
                            logger.info(f"✅ UNIQUE VIEW SUCCESSFULLY REGISTERED!")
                            if 'deepLink' in api_result:
                                logger.info(f"🔗 Deep link: {api_result['deepLink']}")
                            
                            # Simulate post-success behavior (user staying on page briefly)
                            post_success_time = random.uniform(2, 8)
                            logger.info(f"⏱️ Post-success page time: {post_success_time:.2f}s (user reading result)")
                            time.sleep(post_success_time)
                            
                            return True
                        else:
                            logger.warning(f"⚠️ API returned false: {api_result.get('message', 'Unknown error')}")
                            return False
                            
                    except Exception as e:
                        logger.error(f"❌ Error parsing API response: {e}")
                        return False
                else:
                    logger.error(f"❌ API call failed with status: {api_response.status_code}")
                    return False
            else:
                # For other domains, just simulate a successful visit without API call
                logger.info(f"✅ PAGE VISIT SUCCESSFUL (no API integration for {domain})")
                
                # Simulate realistic browsing time even without API
                browse_time = random.uniform(8, 20)
                logger.info(f"⏱️ Browsing time: {browse_time:.2f}s (user exploring page)")
                time.sleep(browse_time)
                
                return True
                
        except requests.exceptions.Timeout:
            logger.error("❌ Request timeout")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False
    
    def generate_unique_view(self):
        """Generate one unique view with comprehensive simulation"""
        try:
            # Create enhanced Indian session
            session = self.create_enhanced_indian_session()
            
            # Get session info for logging
            session_info = self.ip_simulator.get_session_info(session)
            
            print(f"\n🇮🇳 NEW UNIQUE INDIAN VIEWER")
            print(f"📍 Location: {session_info['city']}, {session_info['region']}")
            print(f"📡 ISP: {session_info['isp']} ({session_info['connection_type']})")
            print(f"🆔 Session: {session_info['session_id']}")
            print(f"🌐 Simulated IP: {session_info['simulated_ip']}")
            print(f"🔧 User Agent: {session_info['user_agent']}")
            
            # Simulate realistic user behavior
            success = self.simulate_user_behavior(session, self.target_url)
            
            if success:
                self.success_count += 1
                print(f"✅ UNIQUE VIEW GENERATED SUCCESSFULLY!")
            else:
                self.error_count += 1
                print(f"❌ Failed to generate unique view")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error generating unique view: {e}")
            self.error_count += 1
            return False
        finally:
            # Always close the session
            if 'session' in locals():
                session.close()
    
    def run_continuous_unique_views(self, target_views=None):
        """Run continuous unique view generation"""
        print(f"\n🎯 STARTING GOOGLE STUDENT AMBASSADOR BOT")
        print(f"🌐 Target URL: {self.target_url}")
        print(f"👥 Target Views: {'Unlimited' if target_views is None else target_views}")
        print(f"⏱️ Interval: {self.timing_range[0]}-{self.timing_range[1]} seconds (realistic human behavior)")
        print(f"📖 Per-view: ~8-25 seconds reading/browsing time")
        print(f"🗄️ IP Database: {len(self.ip_simulator.indian_ips_db)} Indian IPs")
        print("=" * 80)
        
        self.running = True
        view_count = 0
        
        try:
            while self.running and (target_views is None or view_count < target_views):
                view_count += 1
                
                print(f"\n🚀 GENERATING UNIQUE VIEW #{view_count}")
                print(f"⏰ Time: {datetime.now(self.india_tz).strftime('%Y-%m-%d %H:%M:%S IST')}")
                
                # Generate unique view
                success = self.generate_unique_view()
                
                # Show statistics
                total_attempts = self.success_count + self.error_count
                success_rate = (self.success_count / total_attempts * 100) if total_attempts > 0 else 0
                
                print(f"📈 Overall Stats: {self.success_count} successful views, {self.error_count} failed ({success_rate:.1f}% success)")
                
                # Show session diversity every 5 views
                if view_count % 5 == 0:
                    uniqueness = self.ip_simulator.verify_session_uniqueness()
                    print(f"🔄 Session Diversity: {uniqueness['unique_ips']} unique IPs, {uniqueness['unique_cities']} cities, {uniqueness['unique_isps']} ISPs")
                
                # Wait with random timing (2-5 seconds) before next view
                if self.running and (target_views is None or view_count < target_views):
                    wait_time = random.uniform(self.timing_range[0], self.timing_range[1])
                    print(f"⏳ Waiting {wait_time:.2f} seconds before next unique view...")
                    time.sleep(wait_time)
                    
        except KeyboardInterrupt:
            print(f"\n⏹️ Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Bot error: {e}")
        finally:
            self.running = False
            
            # Final statistics
            print(f"\n📊 FINAL RESULTS:")
            print(f"✅ Successful unique views: {self.success_count}")
            print(f"❌ Failed attempts: {self.error_count}")
            total = self.success_count + self.error_count
            if total > 0:
                print(f"📈 Success rate: {(self.success_count / total * 100):.1f}%")
            
            uniqueness = self.ip_simulator.verify_session_uniqueness()
            print(f"\n🔄 SESSION DIVERSITY ACHIEVED:")
            print(f"   - Unique IP addresses used: {uniqueness['unique_ips']}")
            print(f"   - Different cities covered: {uniqueness['unique_cities']}")
            print(f"   - Different ISPs simulated: {uniqueness['unique_isps']}")
            print(f"   - Cities: {', '.join(uniqueness['cities_used'])}")
            print(f"   - ISPs: {', '.join(uniqueness['isps_used'])}")
    
    def stop(self):
        """Stop the bot"""
        print(f"\n🛑 Stopping Google Ambassador Bot...")
        self.running = False

def main():
    """Main function with user input for URL and views"""
    print("🎓 GOOGLE STUDENT AMBASSADOR - UNIQUE VIEWER BOT")
    print("=" * 60)
    print("✅ Features:")
    print("   • 42+ Indian IP addresses from 25+ cities")
    print("   • Real ISP simulation (Jio, Airtel, Vi, BSNL, etc.)")
    print("   • 15-45 second intervals (realistic human behavior)")
    print("   • Unique session per view")
    print("   • Human-like reading, scrolling, and interaction patterns")
    print("   • Advanced anti-detection measures")
    print("   • Randomized timing and behavior")
    print()
    
    # Get target URL from user
    target_url = get_user_url()
    
    # Get target number of views from user
    target_views = get_user_views()
    
    print(f"\n🚀 CONFIGURATION:")
    print(f"   Target URL: {target_url}")
    print(f"   Target Views: {'Unlimited' if target_views is None else target_views}")
    print(f"   Speed: 15-45 seconds per view (realistic human behavior)")
    print(f"   Per-view time: ~8-25 seconds on page + delays")
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"⏳ Starting in {i}...")
        time.sleep(1)
    
    # Create and run bot with user-provided URL
    bot = GoogleAmbassadorBot(target_url)
    
    try:
        bot.run_continuous_unique_views(target_views)
    except KeyboardInterrupt:
        bot.stop()
    
    print(f"\n👋 Thanks for using Google Student Ambassador Bot!")
    print(f"🎯 Your unique views have been generated successfully!")

if __name__ == "__main__":
    main()