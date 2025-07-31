# p2p-logs

This script monitors p2p bot log files and automatically sends entries from the **last 5 minutes** to a specified **Discord channel** via webhook.

## Features

* Monitors the latest `logfile-*.log` in a folder
* Sends updates every 5 minutes
* Filters log lines by timestamp
* Splits long messages into chunks for Discord
* Mentions a user or role when new entries are posted

---

## Requirements

* Python 3.7+
* `requests` library

Install with:

```bash
pip install requests
```

---

## Setup

1. **Clone or copy the script** into a directory of your choice.

2. **Configure your settings** at the top of the script:

```python
LOG_DIR = Path(r"C:\\path\\to\\your\\logs\\folder")
WEBHOOK_URL = "https://discord.com/api/webhooks/..."
DISCORD_MENTION = "<@your_user_or_role_id>"
```

> Replace `LOG_DIR` with your actual log folder
> Replace `WEBHOOK_URL` with your Discord webhook URL
> Replace `DISCORD_MENTION` with your user or role ID (e.g. `<@123456789012345678>`)

---

## Usage

To run the monitor:

```bash
python discord_monitor.py
```

The script will:

* Continuously check the log folder every 5 minutes
* Read the newest log file
* Filter and send only lines from the past 5 minutes

You can run this as a background process using:

* `nohup` or `pm2` on Linux
* Task Scheduler or a `.bat` file on Windows

---

## Example Log Format

Your log lines must begin with a timestamp in this format:

```
2025-07-31 22:37:38 [INFO] Already have 180 Shark
```

---

## Troubleshooting

* If nothing is sent to Discord, check:

  * That your logs contain timestamps in the expected format
  * That the webhook URL is correct
  * That the webhook is still valid and not deleted

* If you're using Python 3.8 or lower, `zoneinfo` is not supported. This script uses a fallback fixed AEST offset (UTC+10).

---

## License

MIT License
