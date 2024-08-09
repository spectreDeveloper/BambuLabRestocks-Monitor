# BambuLab Product Availability Monitor 🛠️

This project was originally created for fun months ago when the BambuLab A1 was OUT-OF-STOCK. It ensures you catch the availability when it comes back. I've also used it to get notified when certain PLA types come back in stock. This project is tailored for the European Marketplace but can be easily adapted for the US.

This is the first release, but if the project is adopted by the BambuLab community members, I will update and optimize it in the future.

### BOT EXAMPLE PICTURES :D ###

![Monitor Running](https://telegra.ph/file/6c2b8b7d5e2aa13bf71a1.jpg)
![Telegram Results](https://telegra.ph/file/e3e09672497806d27ac33.jpg)


**For any questions, feel free to open an issue.**

## How to Configure 🛠️

To configure the monitor, follow these steps:

### 1. Install Python 3.12 🐍

Ensure you have Python 3.12 installed on your system.

### 2. Install the Required Packages 📦

First, install the packages listed in the `requirements.txt` file:

```bash
python3.12 -m pip install -r requirements.txt
```
### 3. Install the Latest Version of Pyrogram 🚀 ###
```bash
python3.12 -m pip install https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip --force-reinstall
```
### 4. Configure __main__.py 📝 ###
Open __main__.py with your preferred text editor and configure the following parameters:

### Configuration Details

**1. Timeout Between Checks**

- **Description:** Set the interval (in seconds) between each check.
- **Default:** 300 seconds (5 minutes)
- **Note:** You can adjust this value as needed.

  ```python
  timeout_to_wait = 300  # Adjust this value as needed

**2. Variants to Check**

- **Description:** Provide a list of product variant IDs that you want to monitor. You can find these IDs on the product's website.
- **Format:** List of integers or strings representing the product variant IDs.

  ```python
  variants_to_check = [
      # Example IDs
      1234567890,
      9876543210,
      # Add more IDs as needed
  ]

**3. Pyrogram Client Configuration**

Fill in the details for the Pyrogram client with the following:

- **`name`:** The session name for the Pyrogram session file (e.g., `"bambulabbot"`).
- **`api_id`:** Your Telegram API ID.
- **`api_hash`:** Your Telegram API hash.
- **`bot_token`:** The token for your Telegram bot.

  ```python
  from pyrogram import Client

  pyro_client = Client(
      session_name="bambulabbot",  # Replace with your session name
      api_id=123456,               # Replace with your API ID
      api_hash="your_api_hash",    # Replace with your API hash
      bot_token="your_bot_token"   # Replace with your bot token
  )

## Getting Your API ID and Token for Telegram 🟦 ###

- Create a new application on the [Telegram API development tools](https://my.telegram.org) to get your API ID and API hash.
- Create a new bot using [BotFather](https://t.me/botfather) on Telegram to get your bot token.

### Contributing 🤝 ###

Contributions are welcome! Fork the repository and submit a pull request.
### Support ℹ️ ###

Feel free to open an issue here on GitHub to keep in touch.
