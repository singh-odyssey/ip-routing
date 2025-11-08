# Anonymous Load Testing Toolkit

This project contains a set of scripts to run a high-intensity, Tor-routed load testing application. It is designed for resilience and can be run as a single instance or as a swarm of multiple bots.

**⚠️ WARNING: This tool is for testing YOUR OWN applications only. Unauthorized use against websites you do not own is illegal and can have severe consequences.**

---

## 1. Setup (One-Time Only)

Before running the scripts for the first time, you need to make them executable.

```bash
chmod +x run.sh
chmod +x start_swarm.sh
```

You may also need to install `tmux` if it's not already on your system. This is required for the swarm script.
```bash
sudo apt-get update && sudo apt-get install -y tmux
```

---

## 2. Single Bot Mode (`run.sh`)

This is the simplest way to run a single, persistent bot. The `run.sh` script acts as a watchdog, ensuring that the Python bot (`boom.py`) restarts automatically if it ever stops.

### How to Run

```bash
./run.sh
```
The script will then prompt you to enter the target URL. Once provided, the bot will start with default settings and run continuously.

### How to Stop

Press `Ctrl+C` in the terminal where `run.sh` is running.

---

## 3. Swarm Mode (`start_swarm.sh`)

This is the recommended way to generate significant load. The `start_swarm.sh` script launches and manages multiple bot instances in the background using `tmux`. Each bot is managed by its own watchdog (`run.sh`), making the entire swarm highly resilient.

### How to Run

```bash
./start_swarm.sh
```
The script will ask for:
1.  The target URL.
2.  How many bots you want to launch.

After you provide the inputs, the script will create a background `tmux` session and launch all the bots. You can safely close your terminal, and the swarm will continue to run.

### How to Manage and Monitor the Swarm

You can manage the swarm using `tmux` commands from any terminal.

*   **Attach to the Swarm (to see the bots in action):**
    ```bash
    tmux attach -t bot_swarm
    ```

*   **Navigate Between Bots (while attached):**
    - Press `Ctrl+B`, then `N` to switch to the **N**ext bot window.
    - Press `Ctrl+B`, then `P` to switch to the **P**revious bot window.
    - Press `Ctrl+B`, then `[Window Number]` (e.g., `Ctrl+B`, `3`) to jump directly to a bot.

*   **Detach from the Swarm (leave it running in the background):**
    - Press `Ctrl+B`, then `D`.

*   **Stop the Entire Swarm:**
    This command will instantly kill all running bots and clean up the session.
    ```bash
    tmux kill-session -t bot_swarm
    ```

