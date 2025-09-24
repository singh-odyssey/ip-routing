# 🎯 IP Routing Bot System

# 🎯 IP Routing Bot System

Advanced bot for generating unique viewers with Indian IP addresses and realistic device fingerprinting.

## 🚀 Quick Start

```bash
git clone https://github.com/singh-odyssey/ip-routing.git
cd ip-routing
pip install -r requirements.txt

# Command line
python3 google_ambassador_bot.py

# Web interface (localhost:5000)  
python3 web_ui.py
```

## ✨ Features

- **156+ verified Indian IPs** across 28 states + 8 union territories
- **Advanced anti-detection** with unique browser fingerprints  
- **Realistic timing** (2-5s intervals) and ISP simulation
- **Web dashboard** with real-time monitoring
- **Production ready** (Render/Heroku deployment)

## 📊 What It Does

Simulates authentic Indian users with:
- Geographic diversity (Delhi NCR, Mumbai, Bangalore, etc.)
- ISP variety (Jio, Airtel, Vi, BSNL, regional providers)
- Device fingerprints (Android/iOS, screen resolution, WebGL)  
- Natural browsing patterns and timing

## 🛡️ Anti-Detection

- IP rotation across 100+ cities
- Unique session fingerprints per request
- Human-like delays and headers
- ISP-specific characteristics
- Regional language preferences

## 📁 Files

```
google_ambassador_bot.py    # Main bot
seminar_parallel_bot.py     # Parallel processing
web_ui.py                   # Web interface
smart_indian_simulator.py   # IP/fingerprint engine
manual_indian_ips.json      # IP database
render.yaml                 # Deployment config
```

## 🚀 Deploy to Render

1. Fork this repository
2. Connect to Render  
3. Deploy using `render.yaml`

---

**For educational and research purposes only**d IP Routing Bot System

## 📋 Overview
An advanced bot system that generates unique viewers for any URL using sophisticated IP routing and device fingerprinting. The system simulates authentic Indian users with realistic device characteristics, network conditions, and browsing behavior patterns.

**Key Capabilities:**
- Generate unique views on any target URL
- Simulate real Indian user behavior and device characteristics  
- Advanced anti-detection measures with realistic timing
- Web interface for monitoring and control
- Production-ready deployment configuration

## 🚀 Quick Start

```bash
git clone https://github.com/singh-odyssey/ip-routing.git
cd ip-routing
pip install -r requirements.txt

# Command line
python3 google_ambassador_bot.py

# Web interface (localhost:5000)
python3 web_ui.py
```

## ✨ Features

- **156+ verified Indian IPs** across 28 states + 8 union territories
- **Advanced anti-detection** with unique browser fingerprints
- **Realistic timing** (2-5s intervals) and ISP simulation
- **Web dashboard** with real-time monitoring
- **Production ready** (Render/Heroku deployment)

## 📊 Usage Examples

### Basic URL Processing
```python
# Interactive mode - enter any URL
python3 google_ambassador_bot.py

# Example output:
# 🌐 Enter target URL: https://example.com
# ⚡ Generating 10 unique views...
# ✅ View 1/10 completed from Delhi, Jio 5G
```

### Parallel Processing
```python
# For multiple URLs simultaneously
python3 seminar_parallel_bot.py
```

### Web Dashboard
- **Real-time monitoring** of bot operations
- **Geographic distribution** of simulated users
- **Success/failure statistics** and performance metrics
- **Control interface** for starting/stopping operations

## 📊 Sample Output

```
� ADVANCED IP ROUTING BOT SYSTEM
Target: https://example.com
Features: 156+ Indian IPs, Advanced Fingerprinting, Anti-detection

🚀 GENERATING UNIQUE VIEW #1
⏰ Time: 2025-09-24 14:30:45 IST

🇮🇳 NEW UNIQUE INDIAN VIEWER
📍 Location: Bengaluru, Karnataka  
📡 ISP: Jio Fiber (5G)
🆔 Session: a7b9c3e2f8d1
🌐 IP Address: 157.43.87.142
📱 Device: Mozilla/5.0 (Linux; Android 14; OnePlus 11)

✅ Page loaded successfully (2.3s)
🔍 Generating unique fingerprint...
⚡ Fingerprint created: 47 characteristics
🎯 Registering view with target system...
📊 Response: Success - View registered
✅ UNIQUE VIEW COMPLETED!

📈 Stats: 1 successful, 0 failed (100% success rate)
⏳ Waiting 3.2s before next view...
```

## 📂 Project Structure

```
📁 ip-routing/
├── 🎯 google_ambassador_bot.py          # Main unique viewer bot
├── 🎪 seminar_parallel_bot.py           # Parallel processing bot  
├── 🌐 web_ui.py                         # Web interface dashboard
├── 🔧 smart_indian_simulator.py         # IP & fingerprint simulation engine
├── 🗄️ manual_indian_ips.json           # 156+ verified Indian IP addresses
├── 🚀 wsgi.py                           # Production WSGI server
├── ⚙️ render.yaml                       # Render deployment configuration
├── 📋 requirements.txt                  # Python dependencies
├── 📁 templates/                        # Web UI templates
│   ├── base.html                        # Base HTML template
│   ├── index.html                       # Main dashboard page
│   ├── google_bot.html                  # Google bot interface
│   ├── seminar_bot.html                 # Seminar bot interface
│   └── stats.html                       # Statistics and analytics page
└── 📝 README.md                         # Project documentation
```

## �️ Installation & Setup

### Local Development
```bash
# 1. Clone the repository
git clone https://github.com/singh-odyssey/ip-routing.git
cd ip-routing

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the bot (choose one)
python3 google_ambassador_bot.py    # Command line interface
python3 web_ui.py                   # Web interface (localhost:5000)
```

### Production Deployment
**Render (Recommended):**
1. Fork this repository on GitHub
2. Connect your fork to Render
3. Deploy using the included `render.yaml` configuration
4. Access your deployed web interface

**Other Platforms:**
- Compatible with Heroku, Railway, and other Python hosting platforms
- Uses Gunicorn WSGI server for production stability

## 🔧 Technical Features

### 1. **Advanced Device Fingerprinting**
- **Screen characteristics:** 25+ resolution combinations and pixel densities
- **Hardware simulation:** CPU cores, device memory, GPU specifications
- **WebGL fingerprints:** Support for Mali, Adreno, PowerVR, Intel GPUs
- **Canvas fingerprints:** Font rendering and graphics characteristics
- **Audio context:** Multiple sample rates and channel configurations
- **Platform detection:** Accurate OS, architecture, and browser identification

### 2. **Network & ISP Simulation**
- **Connection types:** 5G Mobile, 4G LTE, Fiber Broadband, Satellite
- **ISP-specific characteristics:** Speed profiles and latency patterns
- **Geographic routing:** Regional ISP distribution across India
- **Mobile/Desktop optimization:** Appropriate headers and capabilities

### 3. **Multi-Bot Architecture**
- **Sequential bot:** Single URL processing with detailed logging
- **Parallel bot:** Multiple URL processing with concurrent sessions
- **Session management:** Prevents fingerprint duplication and conflicts
- **Error recovery:** Automatic retry mechanisms and fallback strategies

### 4. **Anti-Detection Systems**
- **Realistic timing:** Human-like delays and interaction patterns
- **IP rotation:** Automatic switching between verified Indian addresses
- **Header diversity:** Rotating user agents and browser characteristics  
- **Behavior simulation:** Natural page interaction and navigation flows

## � IP Database Overview

### 🇮🇳 **Geographic Coverage**
**156+ manually verified Indian IP addresses** spanning:

- **North India (60+ IPs):** Delhi NCR, Uttar Pradesh, Punjab, Haryana
- **Central India (25+ IPs):** Madhya Pradesh, Rajasthan, Chhattisgarh  
- **South India (35+ IPs):** Karnataka, Maharashtra, Tamil Nadu, Kerala, Telangana
- **East & Northeast (15+ IPs):** West Bengal, Odisha, Assam, Bihar, Jharkhand
- **Other Regions (20+ IPs):** Gujarat, Goa, Himachal Pradesh, J&K, Union Territories

### 📡 **ISP Distribution**
- **Major Mobile Networks:** Jio (40+ IPs), Airtel (35+ IPs), Vi (20+ IPs)
- **Broadband Providers:** BSNL (25+ IPs), ACT Fibernet, Regional ISPs (15+ IPs)
- **Cloud Infrastructure:** AWS, Azure, GCP, DigitalOcean (20+ IPs)
- **Connection Types:** 5G Mobile, 4G LTE, Fiber Broadband, Satellite, Datacenter

## � Security & Detection Avoidance

### ✅ **Anti-Detection Features**
- **Authentic IP rotation** across 100+ Indian cities and ISPs
- **Unique session fingerprints** generated for each request
- **Human-like timing patterns** (2-5 second intervals)
- **Realistic HTTP headers** matching genuine Indian user traffic
- **ISP-appropriate characteristics** (mobile vs broadband behavior)
- **Browser diversity** across Chrome, Firefox, Safari, Edge
- **Regional language preferences** (Hindi/English combinations)

### 🚫 **Patterns Avoided**
- IP address reuse within short timeframes
- Rapid-fire requests that trigger rate limiting
- Missing or suspicious HTTP headers
- Non-Indian geographic or cultural indicators
- Predictable or mechanical request patterns

## ⚙️ Configuration Options

### Regional Preferences
The system includes configurable regional weighting, with optional preference for Delhi NCR region (approximately 70% selection probability). This maintains geographic diversity while allowing focused traffic generation.

### Timing Controls
- **Default interval:** 2-5 seconds between requests
- **Customizable delays:** Adjustable through configuration
- **Human simulation:** Natural variance in timing patterns

## 🤝 Support & Troubleshooting

### Getting Help
1. **Check dependencies:** Ensure all packages are installed with `pip install -r requirements.txt`
2. **Verify Python version:** Requires Python 3.7+
3. **Test network connectivity:** Ensure stable internet connection
4. **Review logs:** Check console output for detailed error messages

### Best Practices
- **Optimal timing:** Run during Indian business hours (10 AM - 6 PM IST)
- **Continuous operation:** Let the bot handle timing and session management
- **Monitor progress:** Watch console output for real-time statistics
- **Graceful shutdown:** Use Ctrl+C to stop operations safely

## 📄 License & Usage

This project is for educational and research purposes. Users are responsible for complying with all applicable terms of service and legal requirements when using this software.

---
**Built with ❤️ for advanced web traffic simulation and analysis**