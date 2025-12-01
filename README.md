# IP Routing & Engagement Bot

**Free, rotational engagement generator using Tor and JS fingerprinting.**

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the main bot
python3 free_js_fingerprint_bot.py
```

## 📖 Usage Guide

### 1. Manual Mode (Immediate Results)
Use `free_js_fingerprint_bot.py` to run a quick batch of engagements.
- **Default Behavior**: Runs **3 visits** with a random delay of **20-40 seconds** between them.
- **How to Run**:
  ```bash
  python3 free_js_fingerprint_bot.py
  ```
- **Customization**: To change the number of visits, edit the bottom of the file:
  ```python
  # Change '3' to your desired number of visits
  bot.run_free_campaign(3, (20, 40))
  ```

### 2. Automated Mode (Long-Term)
Use `production_engagement_bot.py` to run the bot continuously in the background.
- **Default Behavior**: Schedules small batches of visits throughout the day to look natural.
- **Daily Limit**: Capped at **10 visits/day** by default to avoid detection.
- **How to Run**:
  ```bash
  python3 production_engagement_bot.py
  ```
- **Note**: This script is designed to run indefinitely. Use `Ctrl+C` to stop it.

## 🧠 How It Works
This tool combines two powerful techniques to bypass detection:
1.  **Tor IP Rotation**: Routes traffic through the Tor network (port `9050`), assigning a new, unique IP address for every request to avoid rate limiting and IP bans.
2.  **JS Fingerprint Simulation**: Generates realistic browser data (Screen Resolution, User Agent, Timezone, Canvas Hash) to mimic a legitimate user environment, satisfying "Layer 3" detection checks.

## ⚙️ Configuration
The bot is pre-configured for immediate use, but you may need to adjust the target:
- **Target URL**: Open `free_js_fingerprint_bot.py` and modify `self.target_url` and `self.api_url` to point to your specific engagement endpoint.
- **Tor Port**: Default is `9050`. If your Tor service runs on a different port, update the proxy settings in the script.

## 🔧 Troubleshooting
- **Connection Refused?** Ensure Tor is running: `sudo service tor start`.
- **Missing Dependencies?** Run `pip install -r requirements.txt`.
- **Stuck?** Check `DETECTION_ANALYSIS.py` to understand why certain requests might be blocked.

## 🌿 Branch Guide
Explore other specialized versions of this project:

| Branch | Description |
|--------|-------------|
| **`main`** | Stable release. Features JS fingerprinting & Tor IP rotation. |
| **`mlsa_bot`** | Specialized variant for **Microsoft Learn Student Ambassadors**. |
| **`bot_3.1_24hr`** | Designed for continuous 24-hour operation cycles. |
| **`undetectable_bot`** | Enhanced stealth features to bypass stricter detection. |
| **`user_input_bot...`** | Interactive version allowing custom user configuration. |
| **`tor_bot`** | Focused purely on Tor-based routing mechanisms. |
| **`bot_2.0` / `bot_3.0`** | Legacy/Iterative versions. |

## 📂 Key Files
- **`free_js_fingerprint_bot.py`**: Main script (High success rate).
- **`production_engagement_bot.py`**: Scheduler for automated daily runs.
- **`DETECTION_ANALYSIS.py`**: Documentation on detection logic.

## 🛠 Prerequisites
- **Tor Service**: Must be running on port `9050`.
- **Python 3**: With `requests` and `schedule`.