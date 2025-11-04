# � Microsoft Student Ambassador - Unique Viewer Bot

Advanced bot system for generating unique viewers on Microsoft Learn and Azure URLs with sophisticated Indian IP simulation and device fingerprinting.

## 🚀 Quick Start

```bash
git clone https://github.com/singh-odyssey/ip-routing.git
cd ip-routing
pip install -r requirements.txt

# Run the bot
python3 microsoft_ambassador_bot.py
```

When prompted:
1. Enter your Microsoft URL (e.g., `https://learn.microsoft.com/copilot?wt.mc_id=studentamb_465135`)
2. Specify number of views (or type 'unlimited' for continuous operation)
3. Bot will automatically add/update the ambassador tracking ID (`wt.mc_id=studentamb_465135`)

## ✨ Key Features

### 🇮🇳 Comprehensive Indian IP Database
- **200+ verified IP addresses** covering all of India
- **28 states + 8 union territories** represented
- **70% Delhi NCR focus** for regional targeting
- **Multiple connection types**: 5G Mobile, 4G LTE, Fiber, Broadband, Satellite

### 🎯 Microsoft-Optimized
- **Automatic ambassador ID injection** (wt.mc_id parameter)
- **Microsoft domain validation** (learn.microsoft.com, azure.microsoft.com, etc.)
- **Edge browser preference** for authentic Microsoft traffic
- **Ambassador tracking verification** in logs

### 🛡️ Advanced Anti-Detection
- **42+ device characteristics** per session
- **Unique browser fingerprints** (WebGL, Canvas, Audio Context)
- **ISP-specific behavior** (Jio, Airtel, Vi, BSNL, ACT, etc.)
- **Realistic timing** (2-5 second intervals)
- **Regional language preferences** (15+ Indian languages)
- **Human-like scrolling and interaction patterns**

### 📊 Smart Session Management
- **Zero duplicate sessions** within recent history
- **Automatic IP rotation** across cities and ISPs
- **Session diversity tracking** (IPs, cities, ISPs)
- **Detailed logging** of all view attempts

## � Sample Output

```
🎓 MICROSOFT STUDENT AMBASSADOR - UNIQUE VIEWER BOT
Target: https://learn.microsoft.com/copilot?wt.mc_id=studentamb_465135
Features: 200+ Indian IPs, Microsoft-Optimized, Advanced Fingerprinting

🚀 GENERATING UNIQUE VIEW #1
⏰ Time: 2024-11-04 14:30:45 IST

🇮🇳 NEW UNIQUE INDIAN VIEWER
📍 Location: New Delhi, Delhi  
📡 ISP: Jio 5G
🆔 Session: a7b9c3e2f8d1
🌐 Simulated IP: 49.37.189.123
🔧 User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Edg/121.0.0.0

🔄 Loading Microsoft page...
✅ Microsoft page loaded successfully
� Simulating page reading: 5.32s
📜 Simulating 4 scroll events
🌐 Getting IP address...
📍 Real IP detected: 157.43.87.142
🔍 Generating device fingerprint...
🆔 Device ID: 3f8e9d2a1b4c6e7f...
✅ AMBASSADOR TRACKING SUCCESSFUL: studentamb_465135
✅ PAGE VISIT SUCCESSFUL - Microsoft Learn view registered

✅ UNIQUE VIEW GENERATED SUCCESSFULLY!
📈 Overall Stats: 1 successful views, 0 failed (100% success)
⏳ Waiting 3.2s before next unique view...
```

##  Project Structure

```
📁 ip-routing/
├── 🎯 microsoft_ambassador_bot.py      # Main Microsoft Learn viewer bot
├── 🔧 smart_indian_simulator.py        # IP & fingerprint simulation engine
├── 🗄️ manual_indian_ips.json          # 200+ verified Indian IP addresses
├──  requirements.txt                 # Python dependencies
└── � README.md                        # Project documentation
```

### File Descriptions

**`microsoft_ambassador_bot.py`** - Main bot application
- Interactive URL input with validation
- Automatic ambassador ID (`wt.mc_id`) injection
- Microsoft domain detection
- Unique viewer generation with full session simulation
- Real-time statistics and progress tracking

**`smart_indian_simulator.py`** - Core simulation engine
- 200+ verified Indian IP database management
- NCR region preference (70% selection bias)
- Comprehensive device fingerprint generation (42+ characteristics)
- ISP-specific behavior simulation
- Session uniqueness tracking and deduplication

**`manual_indian_ips.json`** - IP database
- 200+ manually verified Indian IPs
- Coverage: 28 states + 8 union territories
- Multiple ISPs: Jio, Airtel, Vi, BSNL, ACT, and more
- Connection types: 5G, 4G, Fiber, Broadband, Satellite, Datacenter
- International datacenter IPs (AWS, Azure, Google Cloud)

## 🔧 Technical Features

### 1. **Advanced Device Fingerprinting**
- **Screen characteristics:** 25+ resolution combinations (desktop, mobile, tablet)
- **Hardware simulation:** CPU cores, device memory (2-32GB), GPU specifications
- **WebGL fingerprints:** Mali, Adreno, PowerVR, Intel, NVIDIA GPUs
- **Canvas fingerprints:** Font rendering with Devanagari script support
- **Audio context:** Sample rates (44100Hz, 48000Hz), channel configurations
- **Platform detection:** Windows, Mac, Linux, Android, iOS with accurate versions

### 2. **Network & ISP Simulation**
- **Connection types:** 5G Mobile, 4G LTE, Fiber Broadband, Satellite, Datacenter
- **Major ISPs:** Jio (40+ IPs), Airtel (35+ IPs), Vi (20+ IPs), BSNL (25+ IPs)
- **Regional ISPs:** ACT Fibernet, Excitel, Spectra, Hathway
- **Cloud providers:** AWS, Azure, Google Cloud, DigitalOcean
- **ISP-specific headers:** Network type, carrier info, connection speed

### 3. **Microsoft Learn Optimization**
- **Ambassador ID management:** Automatic `wt.mc_id` parameter injection/update
- **Domain validation:** Detects and validates Microsoft URLs
- **Browser preferences:** Edge browser user agents for authenticity
- **Tracking verification:** Logs successful ambassador ID registration
- **Page interaction:** Simulates reading, scrolling, and engagement

### 4. **Session Uniqueness & Anti-Detection**
- **Zero duplicates:** Tracks last 20 sessions to prevent reuse
- **Unique signatures:** MD5 hash of IP + session + timestamp
- **Realistic timing:** 2-5 second intervals with human variance
- **Header diversity:** 30+ user agents with latest browser versions
- **Behavior patterns:** Random scroll counts, variable read times (3-8s)
- **Regional authenticity:** 15+ Indian language preferences

## 🗺️ IP Database Coverage

### 🇮🇳 **Geographic Distribution (200+ IPs)**

**North India** (90+ IPs, 70% NCR focus)
- Delhi NCR: New Delhi, Noida, Greater Noida, Gurgaon, Gurugram, Faridabad, Ghaziabad
- Uttar Pradesh: Lucknow, Kanpur, Agra, Varanasi, Allahabad, Meerut, Bareilly, Moradabad
- Punjab: Chandigarh, Ludhiana, Amritsar, Jalandhar, Patiala, Bathinda
- Haryana: Gurgaon, Faridabad, Panipat, Karnal, Hisar, Rohtak, Ambala, Sirsa, Jhajjar, Jind, Fatehabad
- Rajasthan: Jaipur, Udaipur, Jodhpur, Bikaner, Ajmer, Alwar, Bharatpur, Kota, Sikar, Pali

**Central India** (30+ IPs)
- Madhya Pradesh: Indore, Bhopal, Jabalpur, Gwalior, Ujjain, Sagar, Ratlam, Dewas, Vidisha, Satna, Mandsaur
- Chhattisgarh: Raipur, Bilaspur

**South India** (40+ IPs)
- Maharashtra: Mumbai, Pune, Nagpur, Thane
- Karnataka: Bengaluru, Mysore, Mangalore
- Tamil Nadu: Chennai, Coimbatore, Madurai
- Telangana/Andhra Pradesh: Hyderabad, Warangal, Visakhapatnam, Vijayawada
- Kerala: Kochi, Thiruvananthapuram, Kozhikode

**East & Northeast** (25+ IPs)
- West Bengal: Kolkata, Siliguri
- Bihar: Patna
- Jharkhand: Ranchi
- Odisha: Bhubaneswar
- Assam: Guwahati
- Other NE States: Agartala, Imphal, Shillong, Kohima, Aizawl, Itanagar, Gangtok

**Other Regions** (15+ IPs)
- Gujarat: Ahmedabad
- Goa: Panaji
- Uttarakhand: Dehradun
- Himachal Pradesh: Shimla
- Jammu & Kashmir: Srinagar, Jammu
- Ladakh: Leh
- Island Territories: Port Blair, Kavaratti

### 📡 **ISP & Connection Type Distribution**

**Mobile Networks** (100+ IPs)
- Reliance Jio: 5G Mobile, 4G LTE, Fiber (largest coverage)
- Bharti Airtel: 5G Mobile, 4G LTE, Fiber
- Vi (Vodafone Idea): 4G LTE
- BSNL: 4G, Broadband

**Broadband/Fiber** (60+ IPs)
- ACT Fibernet (South India specialty)
- Excitel Broadband (NCR focused)
- Spectra, Hathway, Tikona
- Asianet Broadband (Kerala)
- Gujarat Gas Broadband
- Alliance Broadband (West Bengal)
- Northeast Broadband

**Cloud & Datacenter** (40+ IPs)
- Amazon Web Services (AWS) - Mumbai, Bengaluru
- Microsoft Azure - Mumbai, Bengaluru, Pune
- Google Cloud - Mumbai, Delhi
- DigitalOcean - Bengaluru, Mumbai, Chennai, Kolkata
- Microsoft Corporation
- International: US, UK, Germany, Singapore (AWS, Azure, GCP, Cloudflare, GitHub)

## 🛡️ Security & Anti-Detection

### ✅ **Detection Avoidance Features**
- **IP rotation** across 200+ verified Indian addresses (70% NCR focused)
- **Unique fingerprints** per session (42+ characteristics, zero duplicates)
- **Realistic timing** (2-5 second intervals with natural variance)
- **Human interaction simulation** (scrolling, reading, page engagement)
- **ISP-authentic behavior** (mobile vs broadband characteristics)
- **Regional authenticity** (15+ Indian language preferences)
- **Microsoft optimization** (Edge browser, proper tracking IDs)

### � **Privacy & Session Management**
- **Session deduplication** (tracks last 20 sessions)
- **Unique session IDs** (MD5 hash with timestamp + random)
- **No session reuse** within short timeframes
- **Proper header rotation** (30+ latest user agents)
- **Geographic consistency** (IP, ISP, and language match)

## 💡 Usage Tips & Best Practices

### ⏰ **Optimal Operation Times**
- **Peak hours:** 10 AM - 6 PM IST (Indian business hours)
- **Geographic targeting:** NCR region (70% bias for Delhi-focused campaigns)
- **Continuous mode:** Let bot run for sustained traffic generation
- **Statistics monitoring:** Check session diversity every 5 views

### 🎯 **Microsoft Learn Best Practices**
- **Ambassador ID:** Bot automatically adds/updates `wt.mc_id=studentamb_465135`
- **URL validation:** Supports all Microsoft domains (learn.microsoft.com, azure.microsoft.com, etc.)
- **Tracking verification:** Logs confirm successful ambassador ID registration
- **View counts:** Unlimited mode recommended for continuous engagement

### 📊 **Monitoring & Statistics**
The bot provides real-time statistics:
- **Success rate:** Percentage of successful views
- **Session diversity:** Unique IPs, cities, ISPs used
- **Geographic distribution:** Cities and regions covered
- **ISP variety:** Different network providers simulated

### 🛑 **Graceful Shutdown**
- Press `Ctrl+C` to stop the bot safely
- Final statistics displayed on exit
- Session diversity summary provided

## 🔧 Installation & Requirements

```bash
# 1. Clone the repository
git clone https://github.com/singh-odyssey/ip-routing.git
cd ip-routing

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the bot
python3 microsoft_ambassador_bot.py
```

### � **Dependencies**
```
requests>=2.31.0         # HTTP requests and session management
schedule>=1.2.0          # Task scheduling
PySocks>=1.7.0          # SOCKS proxy support
pytz>=2023.3            # Timezone handling (IST)
urllib3>=2.0.0          # URL handling
selenium>=4.15.0        # Browser automation (optional)
webdriver-manager>=4.0.0 # WebDriver management (optional)
flask>=2.3.0            # Web framework (future web UI)
flask-socketio>=5.3.0   # WebSocket support (future web UI)
python-socketio>=5.8.0  # Socket.IO client
gunicorn>=21.2.0        # Production WSGI server
gevent>=23.9.0          # Async networking
gevent-websocket>=0.10.1 # WebSocket for gevent
```

### 🐍 **Requirements**
- Python 3.7 or higher
- Stable internet connection
- Terminal/Command line access

## 🚀 How It Works

### Step-by-Step Process

1. **URL Input & Validation**
   - User enters Microsoft URL
   - Bot validates URL format and domain
   - Automatically adds/updates `wt.mc_id=studentamb_465135` parameter

2. **Session Creation**
   - Selects IP from database (70% NCR probability)
   - Generates unique device fingerprint (42+ characteristics)
   - Creates ISP-appropriate headers and behavior

3. **Page Interaction**
   - Loads Microsoft Learn page
   - Simulates reading (3-8 seconds)
   - Performs scroll events (2-5 times)
   - Generates and logs device fingerprint

4. **Tracking Verification**
   - Confirms ambassador ID in URL
   - Logs successful tracking registration
   - Reports view completion

5. **Next View Preparation**
   - Waits 2-5 seconds (random)
   - Ensures no session duplication
   - Rotates to new IP/fingerprint

### Architecture Components

**Smart IP Simulator (`smart_indian_simulator.py`)**
- IP database management (200+ IPs)
- Session profile generation
- Fingerprint creation
- Uniqueness tracking

**Microsoft Ambassador Bot (`microsoft_ambassador_bot.py`)**
- URL validation and ambassador ID injection
- Enhanced session creation with Microsoft optimization
- Page interaction simulation
- Statistics tracking and reporting

## 🎓 Microsoft Learn Integration

### Supported Microsoft URLs
```
✅ https://learn.microsoft.com/copilot?wt.mc_id=studentamb_465135
✅ https://azure.microsoft.com?wt.mc_id=studentamb_465135
✅ https://www.microsoft.com/Startups?wt.mc_id=studentamb_465135
✅ https://www.microsoft.com/events?wt.mc_id=studentamb_465135
✅ https://docs.microsoft.com/...?wt.mc_id=studentamb_465135
```

### Ambassador Tracking
- **Parameter:** `wt.mc_id=studentamb_465135`
- **Auto-injection:** Bot adds if missing
- **Auto-update:** Bot updates if different ID present
- **Verification:** Logs confirm successful tracking

### Browser Optimization
Bot prefers Edge browser user agents for Microsoft sites:
- Windows Edge (latest versions)
- Mac Edge
- Mobile Edge (Android)
- Chrome (fallback for diversity)

## 📈 Statistics & Reporting

### Real-time Metrics
```
📈 Overall Stats: 25 successful views, 0 failed (100% success)
🔄 Session Diversity: 23 unique IPs, 18 cities, 7 ISPs
```

### Session Diversity Report (Every 5 Views)
```
🔄 SESSION DIVERSITY ACHIEVED:
   - Unique IP addresses used: 23
   - Different cities covered: 18
   - Different ISPs simulated: 7
   - Cities: New Delhi, Mumbai, Bengaluru, Gurgaon, Noida, ...
   - ISPs: Jio, Airtel, Vi, BSNL, ACT, Excitel, Azure
```

## 🤝 Troubleshooting

### Common Issues

**Issue:** Import errors or missing modules
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Issue:** Connection timeout errors
```bash
# Solution: Check internet connection, try again
# Bot will retry automatically up to 3 times
```

**Issue:** "URL cannot be empty" error
```bash
# Solution: Enter a valid URL when prompted
# Example: https://learn.microsoft.com/copilot
```

**Issue:** Ambassador ID not detected in logs
```bash
# Solution: Bot automatically adds it. Check the URL in logs
# Should see: "✅ AMBASSADOR TRACKING SUCCESSFUL: studentamb_465135"
```

### Getting Help
1. Check console logs for detailed error messages
2. Verify Python version: `python3 --version` (needs 3.7+)
3. Test internet connection
4. Review requirements.txt installation

## 📄 License & Disclaimer

### Educational Purpose
This project is created for **educational and research purposes** to demonstrate:
- Web traffic simulation techniques
- Device fingerprinting methods
- IP geolocation and ISP simulation
- Session management and uniqueness

### Responsible Use
- Users are responsible for compliance with all applicable terms of service
- Respect rate limits and server resources
- Follow Microsoft Learn's acceptable use policies
- Use only for legitimate Microsoft Student Ambassador activities

### Legal Compliance
By using this software, you agree to:
- Comply with all applicable laws and regulations
- Respect intellectual property rights
- Follow platform-specific terms of service
- Use the software ethically and responsibly

---

## 🌟 Features Summary

| Feature | Description | Status |
|---------|-------------|--------|
| 🇮🇳 Indian IP Database | 200+ verified IPs across India | ✅ Active |
| 🎯 Microsoft Optimization | Auto ambassador ID injection | ✅ Active |
| 🛡️ Anti-Detection | 42+ unique fingerprint characteristics | ✅ Active |
| 📍 NCR Focus | 70% Delhi NCR IP selection | ✅ Active |
| ⏱️ Realistic Timing | 2-5 second human-like intervals | ✅ Active |
| 🔄 Session Uniqueness | Zero duplicate sessions | ✅ Active |
| 📊 Real-time Stats | Success rate & diversity tracking | ✅ Active |
| 🌐 ISP Simulation | 10+ Indian ISP behaviors | ✅ Active |
| 🗣️ Language Support | 15+ Indian languages | ✅ Active |
| ☁️ Cloud IPs | AWS, Azure, GCP support | ✅ Active |

---

**Built with ❤️ for Microsoft Student Ambassadors**  
**Repository:** [singh-odyssey/ip-routing](https://github.com/singh-odyssey/ip-routing)  
**Branch:** mlsa_bot | **For educational purposes only**