#!/bin/bash

# This script launches multiple instances of the load testing bot,
# each in its own window in a new tmux session.

# --- Configuration ---
SESSION_NAME="bot_swarm"
BOT_SCRIPT="./run.sh"

# --- Main Logic ---

# 1. Get Target URL from user
read -p "🔗 Enter the target URL: " TARGET_URL
if [ -z "$TARGET_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

# 2. Get number of bots to run
read -p "🤖 How many bots do you want to run? (e.g., 5): " BOT_COUNT
if ! [[ "$BOT_COUNT" =~ ^[0-9]+$ ]] || [ "$BOT_COUNT" -le 0 ]; then
    echo "❌ Invalid number. Please enter a positive integer."
    exit 1
fi

# 3. Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "⚠️ tmux is not installed. Please run 'sudo apt-get update && sudo apt-get install -y tmux' to install it."
    exit 1
fi

# 4. Check if the bot script is executable
if [ ! -x "$BOT_SCRIPT" ]; then
    echo "⚠️ Bot script ($BOT_SCRIPT) is not executable. Making it executable..."
    chmod +x "$BOT_SCRIPT"
fi

# 5. Kill any existing tmux session with the same name to ensure a clean start
tmux kill-session -t "$SESSION_NAME" 2>/dev/null
echo "✅ Cleaned up any old sessions."

# 6. Create the new tmux session and the first bot window
echo "🚀 Starting tmux session '$SESSION_NAME' with the first bot..."
tmux new-session -d -s "$SESSION_NAME" -n "bot_1" "$BOT_SCRIPT $TARGET_URL"

# 7. Create the rest of the bot windows in a loop
for (( i=2; i<=$BOT_COUNT; i++ )); do
    echo "   -> Launching bot #$i..."
    tmux new-window -t "$SESSION_NAME:$i" -n "bot_$i" "$BOT_SCRIPT $TARGET_URL"
done

echo ""
echo "✅ SUCCESS! Launched $BOT_COUNT bots in the background."
echo "----------------------------------------------------"
echo "You can now safely close this terminal."
echo ""
echo "💡 MANAGEMENT COMMANDS:"
echo "   - Attach to the session (to see bots):  tmux attach -t $SESSION_NAME"
echo "   - Switch between bots:                  Ctrl+B, then N (Next) or P (Previous)"
echo "   - Detach from session (leave running):  Ctrl+B, then D"
echo "   - Stop ALL bots at once:                tmux kill-session -t $SESSION_NAME"
echo "----------------------------------------------------"

