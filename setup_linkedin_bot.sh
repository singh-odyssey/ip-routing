#!/bin/bash

echo "🚀 LINKEDIN → MICROSOFT BOT - QUICK START"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python 3 found"

# Check Tor
if ! command -v tor &> /dev/null; then
    echo "📦 Installing Tor..."
    sudo apt update
    sudo apt install -y tor
else
    echo "✅ Tor installed"
fi

# Check Chromium
if ! command -v chromium-browser &> /dev/null && ! command -v chromium &> /dev/null && ! command -v google-chrome &> /dev/null; then
    echo "📦 Installing Chromium..."
    sudo apt install -y chromium-browser
else
    echo "✅ Chromium/Chrome found"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "🔵 To simulate LinkedIn → Microsoft clicks:"
echo "   python3 linkedin_microsoft_bot.py"
echo ""
echo "🧅 To use Tor browser with LinkedIn option:"
echo "   python3 headless_tor_browser.py"
echo ""
echo "📖 Read the guide:"
echo "   cat LINKEDIN_TRACKING_GUIDE.md"
echo ""
