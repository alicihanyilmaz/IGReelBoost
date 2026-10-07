# Instagram Reels Booster Bot 🚀

An automated Selenium-based Python script designed to organically boost Instagram Reels interactions. By utilizing session cookies (`sessionid`), the bot logs into multiple accounts, watches the target reel to increase retention time, likes it, saves it, and shares it via DM to a specified list of target users.

## ⚠️ Important Warnings

* **Explore Page (Keşfet) Probability:** This algorithm does **NOT** guarantee that your Instagram account or Reel will hit the Explore page with a 100% success rate. It is strictly designed to simulate organic human engagement in order to *increase the probability* of the Instagram algorithm favoring your content. 
* **URL Formatting:** When copying the target Instagram Reels video URL to paste into `main.py`, you must **exclude the username** from the link. 
    * ❌ **Incorrect:** `https://www.instagram.com/username/reel/XYZ123/`
    * ✅ **Correct:** `https://www.instagram.com/reel/XYZ123/`

## Features

- **Passwordless Login:** Uses `sessionid` cookies to bypass login screens and avoid suspicious login attempts.
- **Organic Watch Time:** Simulates human behavior by actually watching the video for a randomized duration (15-35 seconds) before taking action.
- **Automated Engagement:** Automatically clicks the Like and Save buttons using DOM manipulation and JS clicks to bypass invisible UI layers.
- **Targeted Sharing:** Searches for specific usernames from your target list and shares the Reel directly to their DM inbox.
- **Anti-Spam Delays:** Incorporates randomized cooldowns (ranging from seconds to hours) between actions and account switches to prevent algorithmic flagging.

## Prerequisites

- Python 3.x
- Google Chrome Browser
- [Selenium](https://pypi.org/project/selenium/) WebDriver

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/instagram-reel-booster.git](https://github.com/yourusername/instagram-reel-booster.git)
   cd instagram-reel-booster
