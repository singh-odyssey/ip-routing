#!/usr/bin/env python3
"""
SEMINAR PARALLEL BOT - 100 STUDENTS SCANNING SIMULTANEOUSLY
===========================================================

Simulates a realistic seminar scenario where 100+ students scan the QR code
at the same time during a Google Student Ambassador presentation.

Features:
✅ 100+ simultaneous QR scans
✅ Realistic seminar timing (burst scanning)
✅ Different student devices and locations
✅ Thread-safe parallel execution
✅ Seminar-like behavior patterns
✅ Real-time progress monitoring
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
        print(f"🎓 SEMINAR PARALLEL BOT - GOOGLE STUDENT AMBASSADOR")
        print(f"👥 Simulating {max_students} students scanning QR code simultaneously")
        print("=" * 70)
        
        # Initialize the smart IP simulator
        self.ip_simulator = SmartIndianIPSimulator()
        
        # Seminar configuration
        self.max_students = max_students
        self.semaphore = Semaphore(max_students)
        
        # Thread-safe counters
        self.stats_lock = Lock()
        self.success_count = 0
        self.error_count = 0
        self.running = False
        self.start_event = Event()
        
        # Bot configuration - can be provided during initialization or use default
        self.target_url = target_url or "https://aiskillshouse.com/student/qr-mediator?uid=2827&promptId=6"
        
        # India timezone
        self.india_tz = pytz.timezone('Asia/Kolkata')
        
        # Student device patterns (realistic seminar devices)
        self.student_devices = [
            # Popular student smartphones in India
            'Mozilla/5.0 (Linux; Android 13; SM-A54) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; Redmi 9 Power) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; OnePlus Nord CE 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Realme 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; vivo Y20G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; OPPO A78) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Samsung Galaxy M33) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            
            # Some students with iPhones
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
            
            # Some students with laptops (fewer)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        print(f"✅ Seminar bot initialized with {len(self.ip_simulator.indian_ips_db)} student locations")
        print(f"👥 Max simultaneous students: {self.max_students}")
        print(f"🎯 Target URL: {self.target_url}")
    
    def create_student_session(self, student_id):
        """Create a session representing a student at the seminar"""
        # Get unique session from IP simulator
        session = self.ip_simulator.get_unique_indian_session()
        
        # Select student device (mobile-heavy as expected in seminar)
        device_weights = [1, 1, 1, 1, 1, 1, 1, 1, 0.3, 0.3, 0.2, 0.2]  # More mobile devices
        device_ua = random.choices(self.student_devices, weights=device_weights)[0]
        session.headers.update({'User-Agent': device_ua})
        
        # Add student ID for tracking
        session.student_id = student_id
        
        # Determine if mobile or desktop
        is_mobile = 'Mobile' in device_ua or 'iPhone' in device_ua
        
        # Get current seminar time
        now = datetime.now(self.india_tz)
        
        # Student-specific headers
        student_headers = {
            # Location headers
            'X-Forwarded-For': session.profile['ip_info']['ip'],
            'X-Real-IP': session.profile['ip_info']['ip'],
            'CF-IPCountry': 'IN',
            'X-Country-Code': 'IN',
            'X-Geo-Country': 'India',
            'X-Geo-Region': session.profile['ip_info']['region'],
            'X-Geo-City': session.profile['ip_info']['city'],
            
            # Student language preferences (more diverse in seminar)
            'Accept-Language': random.choice([
                'en-IN,hi;q=0.9,en;q=0.8',
                'hi-IN,hi;q=0.9,en;q=0.8',
                'en-US,en;q=0.9,hi;q=0.8',
                'en-GB,en;q=0.9,hi;q=0.8',
                'en-IN,en;q=0.9,hi;q=0.8,ta;q=0.7',
                'en-IN,en;q=0.9,hi;q=0.8,te;q=0.7',
            ]),
            
            # Browser headers
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            
            # Time headers
            'Date': now.strftime('%a, %d %b %Y %H:%M:%S') + ' IST',
            'X-Timezone': 'Asia/Kolkata',
            
            # Network type (mostly mobile data in seminar)
            'X-Network-Type': random.choice(['4G', '5G']) if is_mobile else 'WiFi',
            'X-Connection-Speed': random.choice(['fast', 'medium']) if is_mobile else 'very_fast',
            
            # Student context
            'X-Student-ID': str(student_id),
            'X-Seminar-Context': 'google_ambassador_presentation',
            'X-Scan-Method': 'QR_code',
        }
        
        # Mobile-specific headers
        if is_mobile:
            student_headers.update({
                'Sec-CH-UA-Mobile': '?1',
                'Sec-CH-UA-Platform': '"Android"' if 'Android' in device_ua else '"iOS"',
                'X-Requested-With': random.choice(['', 'com.android.chrome']) if 'Android' in device_ua else '',
            })
        else:
            student_headers.update({
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA-Platform': '"Windows"' if 'Windows' in device_ua else '"macOS"',
            })
        
        session.headers.update(student_headers)
        return session
    
    def simulate_student_qr_scan(self, session, student_id):
        """Simulate a student scanning QR code and accessing the URL"""
        try:
            # Step 1: Load the main page (QR scan result)
            response = session.get(self.target_url, timeout=15, allow_redirects=True)
            
            if response.status_code != 200:
                return False, f"Student {student_id}: HTTP Error {response.status_code}"
            
            # Step 2: Get student's real IP (like real browser)
            try:
                ip_response = session.get("https://api.ipify.org?format=json", timeout=10)
                if ip_response.status_code == 200:
                    ip_data = ip_response.json()
                    real_ip = ip_data.get('ip', 'unknown')
                else:
                    real_ip = session.profile['ip_info']['ip']
            except:
                real_ip = session.profile['ip_info']['ip']
            
            # Step 3: Generate unique student device fingerprint
            device_id = hashlib.md5(f"{real_ip}_{session.profile['session_id']}_{student_id}_{random.random()}".encode()).hexdigest()
            
            # Step 4: Simulate page processing time (students reading/understanding)
            processing_time = random.uniform(1.5, 3.5)  # Realistic student reaction time
            time.sleep(processing_time)
            
            # Step 5: Call the setScore API (register the unique view)
            form_data = {
                'uid': '2827',
                'promptId': '6',
                'deviceId': device_id,
                'ipAddress': real_ip
            }
            
            api_url = "https://aiskillshouse.com/olivrweb/user/Api.php/setScore"
            
            # API headers
            api_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://aiskillshouse.com',
                'Referer': 'https://aiskillshouse.com/student/qr-mediator?uid=2827&promptId=6',
                'X-Requested-With': 'XMLHttpRequest'
            }
            session.headers.update(api_headers)
            
            api_response = session.post(api_url, data=form_data, timeout=15)
            
            if api_response.status_code == 200:
                try:
                    api_result = api_response.json()
                    
                    if api_result.get('status') == True:
                        return True, f"Student {student_id}: ✅ Scan successful - {api_result.get('message', 'Registered')}"
                    else:
                        message = api_result.get('message', 'Unknown error')
                        return False, f"Student {student_id}: ⚠️ API returned false - {message}"
                        
                except Exception as e:
                    return False, f"Student {student_id}: ❌ Error parsing response - {e}"
            else:
                return False, f"Student {student_id}: ❌ API call failed - {api_response.status_code}"
                
        except Exception as e:
            return False, f"Student {student_id}: ❌ Scan error - {e}"
    
    def student_worker(self, student_id):
        """Worker function for each student"""
        # Wait for seminar start signal
        self.start_event.wait()
        
        try:
            # Create student session
            session = self.create_student_session(student_id)
            
            try:
                # Get student info
                session_info = self.ip_simulator.get_session_info(session)
                
                # Simulate QR scan
                success, message = self.simulate_student_qr_scan(session, student_id)
                
                # Update thread-safe statistics
                with self.stats_lock:
                    if success:
                        self.success_count += 1
                        print(f"✅ {message} | {session_info['city']}, {session_info['region']}")
                    else:
                        self.error_count += 1
                        print(f"❌ {message}")
                
                return success
                
            finally:
                session.close()
                
        except Exception as e:
            with self.stats_lock:
                self.error_count += 1
            print(f"❌ Student {student_id}: Worker error - {e}")
            return False
    
    def simulate_seminar_qr_scanning(self, num_students):
        """Simulate students scanning QR codes simultaneously during seminar"""
        print(f"\n🎓 SIMULATING SEMINAR QR CODE SCANNING")
        print(f"👥 Students in seminar: {num_students}")
        print(f"📱 Each student will scan the QR code simultaneously")
        print(f"🎯 Target: Google Student Ambassador presentation")
        print("=" * 70)
        
        self.running = True
        start_time = time.time()
        
        # Countdown like in real seminar
        print(f"\n📢 Seminar announcement:")
        print(f"'Please take out your phones and scan the QR code on the screen'")
        
        for i in range(3, 0, -1):
            print(f"📱 Students preparing to scan... {i}")
            time.sleep(1)
        
        print(f"\n🔥 ALL STUDENTS SCANNING NOW!")
        print("=" * 70)
        
        # Start all student threads
        with ThreadPoolExecutor(max_workers=num_students) as executor:
            # Submit all student tasks
            futures = [executor.submit(self.student_worker, student_id) for student_id in range(1, num_students + 1)]
            
            # Signal all students to start simultaneously (like real seminar)
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
                        print(f"📊 Progress: {completed}/{num_students} students scanned ({elapsed:.1f}s)")
                
            except KeyboardInterrupt:
                print(f"\n⏹️ Seminar interrupted by presenter")
                self.running = False
        
        # Final seminar results
        end_time = time.time()
        elapsed = end_time - start_time
        total_scans = self.success_count + self.error_count
        
        print(f"\n" + "=" * 70)
        print(f"📊 SEMINAR QR SCANNING RESULTS")
        print(f"=" * 70)
        print(f"👥 Total students: {num_students}")
        print(f"✅ Successful scans: {self.success_count}")
        print(f"❌ Failed scans: {self.error_count}")
        print(f"📈 Success rate: {(self.success_count / total_scans * 100):.1f}%" if total_scans > 0 else "N/A")
        print(f"⏱️ Total seminar time: {elapsed:.2f} seconds")
        print(f"🚀 Peak scanning rate: {total_scans / elapsed:.1f} scans/second" if elapsed > 0 else "N/A")
        
        # Geographic diversity of students
        uniqueness = self.ip_simulator.verify_session_uniqueness()
        print(f"\n🌍 STUDENT GEOGRAPHIC DIVERSITY:")
        print(f"   📍 Different cities: {uniqueness['unique_cities']}")
        print(f"   🌐 Different IPs: {uniqueness['unique_ips']}")
        print(f"   📡 Different ISPs: {uniqueness['unique_isps']}")
        print(f"   🏙️ Cities: {', '.join(uniqueness['cities_used'][:10])}{'...' if len(uniqueness['cities_used']) > 10 else ''}")
        
        if self.success_count > 0:
            print(f"\n🎉 SEMINAR SUCCESS!")
            print(f"✅ {self.success_count} students successfully accessed the Google Ambassador prompt!")
            print(f"🎯 All unique views have been registered for your task!")
        
    def stop(self):
        """Stop the seminar simulation"""
        print(f"\n🛑 Stopping seminar...")
        self.running = False

def main():
    """Main function for seminar simulation with user input"""
    print("🎓 SEMINAR PARALLEL BOT - GOOGLE STUDENT AMBASSADOR")
    print("=" * 65)
    print("👨‍🏫 Simulate students scanning QR code during presentation")
    print("📱 Perfect for realistic bulk unique view generation")
    print()
    
    # Get target URL from user
    target_url = get_user_url()
    
    # Get seminar size
    print("\n📊 SEMINAR CONFIGURATION:")
    print("1. 🏫 Small seminar (50 students)")
    print("2. 🎓 Medium seminar (100 students)")
    print("3. 🏛️ Large seminar (200 students)")
    print("4. 🎯 Custom size")
    print()
    
    choice = input("Choose seminar size (1-4): ").strip()
    
    if choice == "1":
        num_students = 50
    elif choice == "2":
        num_students = 100
    elif choice == "3":
        num_students = 200
    elif choice == "4":
        while True:
            try:
                num_students = int(input("Enter number of students (1-500): "))
                if 1 <= num_students <= 500:
                    break
                else:
                    print("❌ Please enter a number between 1 and 500")
            except ValueError:
                print("❌ Please enter a valid number")
    else:
        print("❌ Invalid choice, using default (100 students)")
        num_students = 100
    
    print(f"\n🎓 SEMINAR SETUP:")
    print(f"   Target URL: {target_url}")
    print(f"   Students: {num_students}")
    print(f"   Scenario: Google Student Ambassador presentation")
    print(f"   Action: All students scan QR code simultaneously")
    print(f"   Expected time: ~{max(3, num_students // 50)} seconds")
    print()
    
    # Create and run seminar bot with user-provided URL
    bot = SeminarParallelBot(max_students=num_students, target_url=target_url)
    
    try:
        bot.simulate_seminar_qr_scanning(num_students)
    except KeyboardInterrupt:
        bot.stop()
    
    print(f"\n🎉 Seminar simulation completed!")
    print(f"📈 Your unique views have been generated successfully!")

if __name__ == "__main__":
    main()