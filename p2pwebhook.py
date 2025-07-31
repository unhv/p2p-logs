import os
import time
import re
import requests
from pathlib import Path
from datetime import datetime, timedelta

# === CONFIG ===
LOG_DIR = Path(r"C:\Users\UserName\DreamBot\Logs\DreamBot")  # ← Adjust this to your actual log folder
WEBHOOK_URL = "https://discord.com/api/webhooks/example"
CHECK_INTERVAL = 300  # 5 minutes
CHUNK_LINE_LIMIT = 20  # max lines per embed field
DISCORD_MENTION = "<@DiscordID>"  # use your actual Discord user ID if needed

def get_latest_log_file():
    print(f"Scanning directory: {LOG_DIR}")
    log_files = sorted(LOG_DIR.glob("logfile-*.log"), key=os.path.getmtime, reverse=True)
    print(f"Found: {[f.name for f in log_files]}")
    return log_files[0] if log_files else None

def parse_log_timestamp(line):
    try:
        return datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def split_chunks(lines, chunk_size):
    for i in range(0, len(lines), chunk_size):
        yield lines[i:i + chunk_size]

def send_lines_in_embeds(lines, filename):
    if not lines:
        return

    now = datetime.utcnow().isoformat()
    chunks = list(split_chunks(lines, CHUNK_LINE_LIMIT))
    print(f"Preparing {len(chunks)} embed chunks...")

    for idx, chunk in enumerate(chunks):
        cleaned = [line.strip() for line in chunk]
        field = {
            "name": f"Log Segment {idx + 1}",
            "value": "```" + "\n".join(cleaned)[:1000] + "\n```",
            "inline": False
        }

        embed = {
            "title": "P2P Log Update",
            "description": f"New entries from `{filename}`",
            "color": 0x7289da,
            "timestamp": now,
            "fields": [field]
        }

        payload = {
            "content": f"{DISCORD_MENTION} – new update!",
            "embeds": [embed]
        }

        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"Failed to send: {response.status_code} - {response.text}")
        else:
            print(f"Sent embed chunk {idx + 1}/{len(chunks)}")

def main():
    print("Starting log monitor daemon with Discord embeds...")
    last_file = None

    while True:
        try:
            latest = get_latest_log_file()
            if not latest:
                print("No log files found.")
                time.sleep(CHECK_INTERVAL)
                continue

            if latest != last_file:
                print(f"📄 New log file detected: {latest.name}")
                last_file = latest

            with open(latest, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()

            now = datetime.now()
            cutoff = now - timedelta(minutes=5)
            recent_lines = []

            for line in all_lines:
                ts = parse_log_timestamp(line)
                if ts and ts > cutoff:
                    recent_lines.append(line)

            if recent_lines:
                print(f"📨 Sending {len(recent_lines)} lines from the last 5 minutes to Discord...")
                send_lines_in_embeds(recent_lines, latest.name)
            else:
                print("No lines in the last 5 minutes.")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
