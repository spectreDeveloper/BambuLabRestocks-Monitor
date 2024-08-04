# BambuLabRestocks-Monitor
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoring BambuLab Products Availability</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #f4f4f4;
        }
        h1, h2, h3 {
            color: #444;
        }
        code {
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 90%;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .note {
            color: #ff5722;
        }
        .highlight {
            background-color: #e3f2fd;
            border-left: 4px solid #03a9f4;
            padding: 10px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Monitoring Your Desired BambuLab Products' Availability 🛠️</h1>
        <p>
            This project was originally created for fun months ago when the BambuLab A1 was OUT-OF-STOCK. It ensures you catch the availability when it comes back. I've also used it to get notified when certain PLA types come back in stock. This project is tailored for the European Marketplace but can be easily adapted for the US.
        </p>
        <p>
            This is the first release, but if the project is adopted by the BambuLab community members, I will update and optimize it in the future.
        </p>
        <p class="note">
            For any questions, feel free to open an issue.
        </p>

        <h2>How to Configure 🛠️</h2>
        <p>To configure the monitor, follow these steps:</p>
        
        <h3>1. Install Python 3.12 🐍</h3>
        <p>Ensure you have Python 3.12 installed on your system.</p>
        
        <h3>2. Install the Required Packages 📦</h3>
        <p>First, install the packages listed in the <code>requirements.txt</code> file:</p>
        <pre><code>python3.12 -m pip install -r requirements.txt</code></pre>
        
        <h3>3. Install the Latest Version of Pyrogram 🚀</h3>
        <p>Additionally, install the latest version of Pyrogram with the following command:</p>
        <pre><code>python3.12 -m pip install https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip --force-reinstall</code></pre>
        
        <h3>4. Configure <code>__main__.py</code> 📝</h3>
        <p>Open <code>__main__.py</code> with your preferred text editor and configure the following parameters:</p>

        <div class="highlight">
            <h4><code>timeout_to_wait</code></h4>
            <p>Set the interval (in seconds) between each check. The default is 300 seconds (5 minutes). You can adjust this value as needed.</p>
            <pre><code>timeout_to_wait: int = 300</code></pre>
        </div>
        
        <div class="highlight">
            <h4><code>variants_to_check</code></h4>
            <p>Provide a list of product variant IDs that you want to monitor. You can find these IDs on the product's website.</p>
            <pre><code>variants_to_check = [/* list of product variant IDs */]</code></pre>
        </div>
        
        <div class="highlight">
            <h4><code>pyro_client</code></h4>
            <p>Fill in the details for the Pyrogram client. You'll need the following:</p>
            <ul>
                <li><strong>name</strong>: The session name for the Pyrogram session file (e.g., <code>"bambulabbot"</code>).</li>
                <li><strong>api_id</strong>: Your Telegram API ID.</li>
                <li><strong>api_hash</strong>: Your Telegram API hash.</li>
                <li><strong>bot_token</strong>: The token for your Telegram bot.</li>
            </ul>
            <p>Here's an example configuration:</p>
            <pre><code>from pyrogram import Client

pyro_client: Client = Client(
    name="bambulabbot",
    api_id=YOUR_API_ID,  # Replace with your API ID
    api_hash="YOUR_API_HASH",  # Replace with your API hash
    bot_token="YOUR_BOT_TOKEN"  # Replace with your bot token
)</code></pre>
        </div>
        
        <p>To obtain the <code>api_id</code>, <code>api_hash</code>, and <code>bot_token</code>:</p>
        <ul>
            <li>Create a new application on the <a href="https://my.telegram.org">Telegram API development tools</a> to get your API ID and API hash.</li>
            <li>Create a new bot using <a href="https://t.me/botfather">BotFather</a> on Telegram to get your bot token.</li>
        </ul>

        <p class="note">
            Feel free to reach out if you need further assistance! 🌟
        </p>
    </div>
</body>
</html>
