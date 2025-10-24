#!/usr/bin/env python3
"""
PROXY CONFIGURATION FOR ENHANCED STEALTH
========================================

Optional proxy support for better IP rotation.
If you have access to residential proxies, configure them here.

Recommended proxy services (paid):
- Bright Data (formerly Luminati): https://brightdata.com
- Smartproxy: https://smartproxy.com
- Oxylabs: https://oxylabs.io
- GeoSurf: https://www.geosurf.com
- Storm Proxies: https://stormproxies.com

Cost: $50-200/month for residential proxies
"""

# Enable proxy rotation (set to True if you have proxies)
ENABLE_PROXIES = False

# Proxy configuration
# Format: 'http://username:password@proxy-server:port'
# Or for simple proxies: 'http://proxy-server:port'

PROXY_LIST = [
    # Example configurations (replace with your actual proxies):
    # 'http://user:pass@proxy1.example.com:8080',
    # 'http://user:pass@proxy2.example.com:8080',
    # 'http://user:pass@proxy3.example.com:8080',
]

# Rotating residential proxy (single endpoint that rotates IPs automatically)
# Many services provide a single endpoint that automatically rotates
ROTATING_PROXY = {
    'enabled': False,
    'http': None,  # 'http://username:password@proxy.provider.com:port'
    'https': None,  # 'https://username:password@proxy.provider.com:port'
}

# Proxy settings
PROXY_TIMEOUT = 30  # seconds
PROXY_MAX_RETRIES = 3

def get_random_proxy():
    """Get a random proxy from the list"""
    import random
    if not ENABLE_PROXIES or not PROXY_LIST:
        return None
    return random.choice(PROXY_LIST)

def get_rotating_proxy():
    """Get the rotating proxy configuration"""
    if not ROTATING_PROXY['enabled']:
        return None
    return {
        'http': ROTATING_PROXY['http'],
        'https': ROTATING_PROXY['https']
    }

def get_proxy_for_session():
    """Get proxy configuration for a session"""
    # Try rotating proxy first
    rotating = get_rotating_proxy()
    if rotating:
        return rotating
    
    # Fall back to proxy list
    proxy = get_random_proxy()
    if proxy:
        return {
            'http': proxy,
            'https': proxy
        }
    
    return None

# Usage instructions
USAGE_INSTRUCTIONS = """
HOW TO USE PROXIES:
==================

1. Purchase residential proxies from a provider (see list above)

2. Get your proxy credentials:
   - Username
   - Password
   - Proxy server address
   - Port number

3. Update this file:
   
   Option A - Rotating proxy (recommended):
   ROTATING_PROXY = {
       'enabled': True,
       'http': 'http://your_username:your_password@proxy.provider.com:port',
       'https': 'https://your_username:your_password@proxy.provider.com:port'
   }
   
   Option B - Proxy list:
   ENABLE_PROXIES = True
   PROXY_LIST = [
       'http://user:pass@proxy1.provider.com:8080',
       'http://user:pass@proxy2.provider.com:8080',
       'http://user:pass@proxy3.provider.com:8080',
   ]

4. Set ENABLE_PROXIES = True

5. Run your bot normally - proxies will be used automatically

BENEFITS OF PROXIES:
===================
✅ Real IP rotation (not simulated)
✅ Residential IPs (look like real users)
✅ Geographic targeting (Indian IPs if configured)
✅ Better stealth and harder to detect
✅ No datacenter IP flags

COST vs BENEFIT:
===============
Cost: $50-200/month
Benefit: Near-impossible detection, real IP diversity

Note: Even without proxies, the bot uses advanced simulation
      and should work reasonably well from Codespaces.
"""

if __name__ == "__main__":
    print(USAGE_INSTRUCTIONS)
