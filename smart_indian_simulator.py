#!/usr/bin/env python3
"""
SMART INDIAN IP SIMULATION AND ROTATION
=======================================

Since we can't actually use all IPs as proxies, this system:
1. Uses real Indian IP database for reference
2. Simulates different users by varying all detectable characteristics
3. Uses working proxies when available
4. Creates unique sessions that appear as different Indian users

Features:
- Real IP rotation when proxies are available
- Comprehensive fingerprint variation when proxies aren't available
- Smart fallback strategies
- Detailed session uniqueness tracking
"""

import requests
import random
import time
import json
import hashlib
import os
from datetime import datetime

class SmartIndianIPSimulator:
    def __init__(self):
        self.indian_ips_db = []
        self.current_session_id = 0
        self.used_sessions = []
        self.load_indian_ip_database()
        # Preferred NCR city names for slight selection bias
        self.ncr_cities = {"New Delhi", "Delhi", "Noida", "Greater Noida", "Ghaziabad", "Gurgaon", "Gurugram", "Faridabad"}
        
        # Advanced session variation parameters
        self.indian_user_agents = [
            # Latest Chrome versions (Windows) - Most popular in India
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Latest Chrome versions (Mac)
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Latest Chrome versions (Linux)
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Popular Android devices in India with latest Chrome
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
            
            # iPhone devices (growing market in India)
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            
            # Firefox versions
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Android 14; Mobile; rv:122.0) Gecko/122.0 Firefox/122.0',
            
            # Edge versions
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            
            # Samsung Internet (very popular in India)
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-A52s) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.0.0 Mobile Safari/537.36',
            
            # Opera versions (popular for data savings)
            'Mozilla/5.0 (Linux; Android 13; CPH2423) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 OPR/80.2.4244.58675',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
        ]
        
        # Network patterns to simulate different ISPs
        self.isp_patterns = [
            {'name': 'Jio', 'speed': 'fast', 'mobile': True},
            {'name': 'Airtel', 'speed': 'very_fast', 'mobile': False},
            {'name': 'Vi', 'speed': 'medium', 'mobile': True},
            {'name': 'BSNL', 'speed': 'slow', 'mobile': False},
            {'name': 'ACT', 'speed': 'very_fast', 'mobile': False},
            {'name': 'Hathway', 'speed': 'fast', 'mobile': False},
            {'name': 'DigitalOcean', 'speed': 'very_fast', 'mobile': False},
        ]
    
    def load_indian_ip_database(self):
        """Load Indian IP database from multiple sources"""
        # Try to load manual IPs first
        try:
            if os.path.exists('manual_indian_ips.json'):
                with open('manual_indian_ips.json', 'r') as f:
                    self.indian_ips_db = json.load(f)
                print(f"📂 Loaded {len(self.indian_ips_db)} IPs from manual database")
            elif os.path.exists('indian_ips.json'):
                with open('indian_ips.json', 'r') as f:
                    self.indian_ips_db = json.load(f)
                print(f"📂 Loaded {len(self.indian_ips_db)} IPs from collected database")
            else:
                self.create_fallback_database()
        except Exception as e:
            print(f"❌ Failed to load database: {e}")
            self.create_fallback_database()
    
    def create_fallback_database(self):
        """Create fallback IP database"""
        self.indian_ips_db = [
            {
                "ip": "20.192.21.53",
                "city": "Pune",
                "region": "Maharashtra",
                "isp": "Microsoft Corporation",
                "method": "direct"
            },
            {
                "ip": "139.59.1.14",
                "city": "Bengaluru",
                "region": "Karnataka",
                "isp": "DigitalOcean",
                "method": "direct"
            }
        ]
        print(f"✅ Created fallback database with {len(self.indian_ips_db)} IPs")
    
    def _choose_ip_biased_to_ncr(self):
        """Choose an IP with a slight bias towards Delhi NCR cities if present."""
        if not self.indian_ips_db:
            return None
        ncr_ips = [ip for ip in self.indian_ips_db if ip.get('city') in self.ncr_cities or ip.get('region') in {"Delhi", "NCR"}]
        # If we have NCR entries, pick from them most of the time, otherwise uniform
        try:
            if ncr_ips and random.random() < 0.7:  # 70% chance to choose NCR when available
                return random.choice(ncr_ips)
            return random.choice(self.indian_ips_db)
        except IndexError:
            return random.choice(self.indian_ips_db)

    def create_unique_session_profile(self):
        """Create a completely unique session profile"""
        # Select IP from database with NCR bias
        selected_ip = self._choose_ip_biased_to_ncr() or random.choice(self.indian_ips_db)
        
        # Create unique session characteristics
        user_agent = random.choice(self.indian_user_agents)
        isp_pattern = random.choice(self.isp_patterns)
        
        # Generate unique session ID
        session_timestamp = int(time.time() * 1000) + random.randint(1, 1000)
        session_id = hashlib.md5(f"{session_timestamp}_{random.random()}".encode()).hexdigest()[:12]
        
        # Create comprehensive profile
        profile = {
            'session_id': session_id,
            'ip_info': selected_ip,
            'user_agent': user_agent,
            'isp_simulation': isp_pattern,
            'timestamp': session_timestamp,
            'unique_signature': f"{selected_ip['ip']}_{session_id}",
            
            # Browser characteristics
            'accept_language': random.choice([
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
                'pa-IN,pa;q=0.9,en;q=0.8'
            ]),
            
            # Enhanced Device Fingerprint characteristics
            'screen_resolution': random.choice([
                # Desktop resolutions
                '1920x1080', '1366x768', '1536x864', '1440x900', '1600x900',
                '1280x720', '1024x768', '1680x1050', '2560x1440', '3840x2160',
                # Mobile resolutions (popular Indian devices)
                '360x640', '375x667', '414x896', '412x915', '393x851',
                '360x780', '375x812', '428x926', '390x844', '384x854',
                # Tablet resolutions
                '768x1024', '1024x768', '800x1280', '1200x1920', '834x1194'
            ]),
            'color_depth': random.choice([24, 32]),
            'pixel_depth': random.choice([24, 32]),
            'device_pixel_ratio': random.choice([1, 1.5, 2, 2.5, 3]),
            
            # Hardware characteristics
            'hardware_concurrency': random.choice([2, 4, 6, 8, 12, 16]),
            'device_memory': random.choice([2, 4, 6, 8, 12, 16, 32]),
            'max_touch_points': random.choice([0, 1, 5, 10]),
            
            # WebGL fingerprint
            'webgl_vendor': random.choice([
                'Google Inc. (Intel)', 'Google Inc. (NVIDIA)', 'Google Inc. (AMD)',
                'Google Inc. (Qualcomm)', 'Google Inc. (Mali)', 'WebKit WebGL',
                'Mozilla Firefox WebGL', 'ANGLE (Intel)', 'ANGLE (NVIDIA)',
                'Mali-G76 MC12', 'Adreno (TM) 640', 'PowerVR GE8320'
            ]),
            'webgl_renderer': random.choice([
                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)',
                'Mali-G76 MC12', 'Adreno (TM) 640', 'PowerVR GE8320',
                'Intel(R) Iris(R) Xe Graphics', 'AMD Radeon(TM) Graphics'
            ]),
            
            # Canvas fingerprint components
            'canvas_fonts': random.choice([
                'Arial,Helvetica,Times New Roman,Courier New,Verdana,Georgia',
                'Roboto,Open Sans,Lato,Montserrat,Oswald,Source Sans Pro',
                'Noto Sans,Poppins,Nunito,Rubik,Work Sans,Inter',
                'Noto Sans Devanagari,Mangal,Kokila,Utsaah,Aparajita'
            ]),
            
            # Audio context fingerprint
            'audio_sample_rate': random.choice([44100, 48000]),
            'audio_max_channel_count': random.choice([2, 6, 8]),
            'audio_number_of_inputs': random.choice([1, 2]),
            'audio_number_of_outputs': random.choice([0, 2]),
            
            # Platform and OS characteristics
            'platform': self._get_platform_from_ua(user_agent),
            'oscpu': self._get_oscpu_from_ua(user_agent),
            'app_version': user_agent,
            
            # Connection characteristics
            'connection_type': random.choice(['4g', 'fiber', 'wifi', 'broadband']),
            'effective_type': random.choice(['4g', '3g', 'slow-2g']),
            'downlink': random.uniform(0.5, 100.0),
            'rtt': random.randint(20, 300),
            
            # Browser features
            'do_not_track': random.choice([None, '1', '0']),
            'dnr': random.choice([0, 1]),  # Do Not Track header (legacy field)
            'cookie_enabled': True,
            'java_enabled': random.choice([True, False]),
            'plugins_length': random.randint(0, 5),
            
            # Viewport and window characteristics
            'viewport': random.choice([
                '1920x1080', '1366x768', '1536x864', '1440x900',
                '360x640', '375x667', '414x896', '412x915'
            ]),
            'outer_width': random.randint(800, 1920),
            'outer_height': random.randint(600, 1080),
            'inner_width': random.randint(700, 1900),
            'inner_height': random.randint(500, 1000),
            
            # Time characteristics
            'timezone': random.choice([
                'Asia/Kolkata', 'Asia/Mumbai', 'Asia/Delhi', 'Asia/Chennai',
                'Asia/Bengaluru', 'Asia/Hyderabad', 'Asia/Pune'
            ]),
            'timezone_offset': '+05:30',  # IST
            'local_time': datetime.now().isoformat(),
        }
        
        self.current_session_id += 1
        return profile
    
    def _get_platform_from_ua(self, user_agent):
        """Extract platform from user agent"""
        if 'Windows NT 10.0' in user_agent:
            return 'Win32'
        elif 'Windows NT 11.0' in user_agent:
            return 'Win32'
        elif 'Windows NT 6.1' in user_agent:
            return 'Win32'
        elif 'Macintosh' in user_agent:
            return 'MacIntel'
        elif 'Linux' in user_agent and 'Android' not in user_agent:
            return 'Linux x86_64'
        elif 'iPhone' in user_agent:
            return 'iPhone'
        elif 'Android' in user_agent:
            return 'Linux armv8l'
        else:
            return 'Win32'
    
    def _get_oscpu_from_ua(self, user_agent):
        """Extract OS CPU from user agent"""
        if 'Windows NT 10.0' in user_agent:
            return 'Windows NT 10.0; Win64; x64'
        elif 'Windows NT 11.0' in user_agent:
            return 'Windows NT 10.0; Win64; x64'  # Windows 11 reports as 10.0
        elif 'Windows NT 6.1' in user_agent:
            return 'Windows NT 6.1; Win64; x64'
        elif 'Macintosh' in user_agent:
            return 'Intel Mac OS X 10_15_7'
        elif 'Linux' in user_agent and 'Android' not in user_agent:
            return 'Linux x86_64'
        elif 'iPhone' in user_agent:
            return 'iPhone'
        elif 'Android' in user_agent:
            return 'Linux armv8l'
        else:
            return 'Windows NT 10.0; Win64; x64'
    
    def create_session_from_profile(self, profile):
        """Create a requests session based on the profile"""
        session = requests.Session()
        
        # Try to use proxy if available
        try:
            from proxy_config import get_proxy_for_session
            proxy_config = get_proxy_for_session()
            if proxy_config:
                session.proxies.update(proxy_config)
                print(f"🔒 Using proxy for enhanced stealth")
        except ImportError:
            pass  # proxy_config not available, continue without proxies
        except Exception as e:
            print(f"⚠️ Proxy configuration error (continuing without proxy): {e}")
        
        # Check if we can use a working proxy for this IP
        proxy_available = session.proxies is not None and len(session.proxies) > 0
        
        # For testing, we'll simulate different session characteristics
        # without actually using proxies (since most are unreliable)
        
        # Set headers based on profile
        headers = {
            'User-Agent': profile['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': profile['accept_language'],
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': str(profile['dnr']),
            'Cache-Control': 'max-age=0',
        }
        
        # Add ISP-specific headers
        isp = profile['isp_simulation']
        if isp['mobile']:
            headers.update({
                'Save-Data': random.choice(['on', 'off']),
                'Viewport-Width': profile['viewport'].split('x')[0],
            })
        
        if isp['name'] == 'Jio':
            headers.update({
                'X-Network-Type': '4G',
                'X-Carrier': 'Jio',
            })
        elif isp['name'] == 'Airtel':
            headers.update({
                'X-Network-Type': 'Fiber',
                'X-Carrier': 'Airtel',
            })
        
        session.headers.update(headers)
        
        # Store profile in session
        session.profile = profile
        
        return session
    
    def get_unique_indian_session(self):
        """Get a completely unique session simulating different Indian user"""
        # Create unique profile
        profile = self.create_unique_session_profile()
        
        # Ensure this combination hasn't been used recently
        while any(used['unique_signature'] == profile['unique_signature'] for used in self.used_sessions[-20:]):
            profile = self.create_unique_session_profile()
        
        # Create session from profile
        session = self.create_session_from_profile(profile)
        
        # Track this session
        self.used_sessions.append({
            'unique_signature': profile['unique_signature'],
            'ip': profile['ip_info']['ip'],
            'city': profile['ip_info']['city'],
            'isp': profile['isp_simulation']['name'],
            'timestamp': profile['timestamp']
        })
        
        return session
    
    def get_session_info(self, session):
        """Get detailed info about a session"""
        if hasattr(session, 'profile'):
            profile = session.profile
            return {
                'simulated_ip': profile['ip_info']['ip'],
                'city': profile['ip_info']['city'],
                'region': profile['ip_info']['region'],
                'isp': profile['isp_simulation']['name'],
                'session_id': profile['session_id'],
                'user_agent': profile['user_agent'][:50] + '...',
                'connection_type': profile['connection_type'],
                'unique_signature': profile['unique_signature'][:16] + '...'
            }
        
        return {'error': 'No profile found'}
    
    def verify_session_uniqueness(self):
        """Verify that recent sessions are actually unique"""
        recent_sessions = self.used_sessions[-10:]  # Last 10 sessions
        
        unique_ips = set(s['ip'] for s in recent_sessions)
        unique_cities = set(s['city'] for s in recent_sessions)
        unique_isps = set(s['isp'] for s in recent_sessions)
        unique_signatures = set(s['unique_signature'] for s in recent_sessions)
        
        return {
            'total_sessions': len(recent_sessions),
            'unique_ips': len(unique_ips),
            'unique_cities': len(unique_cities),
            'unique_isps': len(unique_isps),
            'unique_signatures': len(unique_signatures),
            'ips_used': list(unique_ips),
            'cities_used': list(unique_cities),
            'isps_used': list(unique_isps)
        }