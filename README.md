# Tor Network Bot & Anonymous Load Testing Tool

Educational project demonstrating web automation and anonymous load testing through the Tor network.

This repository includes two different tools:
1. **tor_bot.py** - Browser-based bot with realistic human behavior simulation through Tor
2. **boom.py** - Anonymous HTTP load testing tool with Tor routing and IP rotation

## Setup

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

## Usage

### Option 1: Browser-Based Bot (Realistic Human Simulation)

Run the bot with Firefox browser:

```bash
python3 tor_bot.py
```

- Opens real Firefox browser through Tor
- Simulates realistic human behavior (scrolling, mouse movements, etc.)
- Randomizes browser fingerprints for each visit
- Asks for number of visits (1-1000)
- Shows success/failure status for each visit
- Best for: Realistic browsing simulation with detailed tracking

### Option 2: Anonymous HTTP Load Testing Tool (boom.py)

Run the anonymous load testing tool:

```bash
python3 boom.py
```

Interactive prompts will ask you for:
- Target URL to test
- Number of requests (1 to 10,000,000)
- Concurrency level (1-1000)
- HTTP method (GET/POST)
- IP rotation frequency

**Anonymity Features:**
- ✅ **All traffic routed through Tor network - YOUR REAL IP IS HIDDEN**
- ✅ Automatic IP rotation (configurable frequency)
- ✅ Randomized browser fingerprints (User-Agent, headers)
- ✅ Randomized referrers and request patterns
- ✅ Variable timing delays to avoid detection patterns
- ✅ Multiple Tor exit node IPs used during testing
- ✅ Shows unique IPs observed during test
- ⚠️ **ONLY for testing your own applications**

## How It Works

### Browser-Based Bot (tor_bot.py)

1. Connects Firefox browser to Tor network (SOCKS5 proxy on port 9050)
2. Randomizes browser fingerprint (user agent, screen resolution, etc.)
3. Injects JavaScript to spoof additional browser properties
4. Visits the provided URL with realistic human behavior
5. Simulates scrolling, mouse movements, and reading patterns
6. Requests new Tor circuit to change IP between visits
7. Repeats for requested number of visits
8. Tracks and reports success/failure for each visit

### HTTP Load Testing Tool (boom.py)

1. Ensures Tor service is running and connected
2. Prompts user for target URL and test parameters
3. Creates thread pool with specified concurrency level
4. Routes all requests through Tor SOCKS5 proxy
5. Rotates IP address at configurable intervals (renews Tor circuit)
6. Randomizes headers, user agents, and referrers for each request
7. Adds random timing delays to avoid pattern detection
8. Tracks response times, success/failure, and IPs used
9. Shows real-time progress with statistics
10. Provides comprehensive summary report with anonymity metrics

## Features

### tor_bot.py Features
- Real browser automation using Selenium + Firefox
- Advanced fingerprint randomization and spoofing
- Realistic human behavior simulation
- Routes all traffic through Tor network
- Automatic IP rotation between visits
- Success/failure tracking for each visit
- Support for up to 1000 sequential visits
- Detailed visit reports

### boom.py Features
- **Tor-routed anonymous load testing**
- Support for up to 10 million requests
- Configurable concurrency (1-1000 threads)
- **Automatic IP rotation** (configurable frequency)
- **Advanced fingerprint randomization:**
  - 17+ diverse User-Agent strings
  - Randomized Accept-Language headers
  - Random referrers (Google, Bing, DuckDuckGo, etc.)
  - Varied request headers and cache controls
- Random timing delays to avoid pattern detection
- Real-time progress with anonymity metrics
- Tracks unique IPs used during testing
- Performance metrics (requests/sec, response times)
- **Strong confirmation prompts for large tests**
- **For testing your own applications only**

## Requirements

- Python 3.7+
- **Firefox ESR** (for tor_bot.py only)
- **Geckodriver** (for tor_bot.py only)
- **Tor service** (REQUIRED for both tools)
- Internet connection
- Required Python packages (installed via setup.sh):
  - selenium (for tor_bot.py)
  - stem (for both - Tor control)
  - requests (for both tools)
  - PySocks (for both - SOCKS proxy support)

## Comparison: Which Bot to Use?

| Feature | tor_bot.py | boom.py |
|---------|-----------|---------|
| Purpose | Anonymous browsing simulation | Anonymous load testing |
| Uses Tor | Yes | Yes |
| Speed | Slower (browser overhead) | Fast (lightweight HTTP) |
| Realism | High (real browser) | Medium (HTTP + fingerprinting) |
| Concurrent | No (sequential) | Yes (multi-threaded) |
| Max Requests | 1000 sequential | 10,000,000 |
| IP Rotation | After each visit | Configurable (every N requests) |
| Anonymity | Very High | High |
| Fingerprinting | Full browser spoofing | Headers + timing randomization |
| Human Behavior | Yes (scrolling, clicks) | Simulated (delays, patterns) |
| Resource Usage | High (Firefox instances) | Low (HTTP sessions) |
| Best For | Realistic anonymous browsing | High-volume anonymous testing |

## Educational Purpose

This project demonstrates:
- **Anonymous communication through Tor network**
- **IP rotation and circuit management**
- Browser automation with Selenium and fingerprint spoofing
- Multi-threaded concurrent programming
- **Advanced anonymity techniques (header randomization, timing variation)**
- SOCKS proxy configuration for anonymity
- Python stem library for Tor control
- HTTP session management and threading
- Performance optimization for high-volume requests
- **Privacy-preserving load testing techniques**

## ⚠️ Legal Disclaimer & Important Warnings

This project is for **educational purposes only**.

### For boom.py (Load Testing):
- ✅ **Uses Tor network - your real IP is HIDDEN from target**
- ✅ **ONLY test websites/applications you OWN or have explicit written permission to test**
- ✅ Use test/staging environments, not production systems
- ❌ **NEVER test third-party websites without authorization**
- ❌ Sending unauthorized high-volume requests is **ILLEGAL** (DDoS/DoS attack)
- ❌ **Tor does NOT make illegal activities untraceable**
- ⚖️ Violators face criminal prosecution under computer fraud laws
- ⚖️ Law enforcement CAN trace attacks even through Tor

### For tor_bot.py (Tor Browser):
- ✅ Use for privacy research and understanding anonymity
- ✅ Educational purposes and security research only
- ❌ Do not use for illegal activities or to violate terms of service
- ❌ Do not use to bypass access controls or rate limits

### Legal Consequences:
Using these tools to attack, overload, or disrupt services without authorization can result in:
- Criminal charges under Computer Fraud and Abuse Act (CFAA) and similar laws
- Significant fines and imprisonment
- Civil liability for damages
- Permanent criminal record

**The authors are not responsible for misuse of this software. You are solely responsible for your actions.**
