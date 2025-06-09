=================================================== TELEGRAM SOLANA CA MONITORING BOT
This Python bot, built using the 'telethon' library, monitors a specified
Telegram group chat for messages from a list of target users. If a message
from a target user contains a pattern that looks like a Solana Contract
Address (CA), the bot forwards that message to a designated private chat
(which can be your personal chat or a BotFather bot's chat).

This project is designed to be easily configurable using environment
variables, making it safe to share on platforms like GitHub without
exposing your personal API credentials.

FEATURES
Monitors a specific Telegram group for new messages.

Filters messages based on a list of predefined user handles.

Identifies potential Solana Contract Addresses (44-character Base58 strings)
within messages.

Forwards matching messages to a designated private Telegram chat for
notifications.

PREREQUISITES
Before you begin, ensure you have:

Python 3.8+ installed.

A Telegram Account and your API ID and API Hash. You can get these from
https://my.telegram.org/.

(Optional but Recommended) A Telegram Bot created via @BotFather if you
want notifications sent to a dedicated bot chat.

The 'telethon', 'python-dotenv', and 'requests' Python libraries installed.

SETUP
Follow these steps to set up and run the bot:

CLONE OR DOWNLOAD THE REPOSITORY
If you're uploading to GitHub later, you'll start by preparing your local project.

Example:

mkdir telegram-solana-monitor
cd telegram-solana-monitor

Then place the main Python script (e.g., 'telegram_monitor.py') inside this folder.

INSTALL DEPENDENCIES
Install the required Python libraries:

pip install telethon python-dotenv requests

CONFIGURE ENVIRONMENT VARIABLES
Create a file named '.env' in the root directory of your project (the same
directory as 'telegram_monitor.py'). This file will hold your sensitive
information and configuration.

.env file content example:

TELEGRAM_API_ID=YOUR_TELEGRAM_API_ID
TELEGRAM_API_HASH='YOUR_TELEGRAM_API_HASH'
TELEGRAM_PHONE='+YOUR_PHONE_NUMBER' # E.g., +16477721913

TELEGRAM_ME_ID=YOUR_NOTIFICATION_CHAT_ID
TELEGRAM_TARGET_GROUP_ID=YOUR_TARGET_GROUP_ID
TELEGRAM_TARGET_USER_HANDLES=user1,user2,user3

Replace the placeholder values with your actual information:

YOUR_TELEGRAM_API_ID: Your API ID from my.telegram.org.

YOUR_TELEGRAM_API_HASH: Your API Hash from my.telegram.org. Enclose it in single quotes.

YOUR_PHONE_NUMBER: Your Telegram phone number, including the international prefix.

YOUR_NOTIFICATION_CHAT_ID: The numeric ID of your private chat or your BotFather bot's private chat.
(Instructions for getting this are in the chat history, usually involves a helper script
and sending a message to your bot.)

YOUR_TARGET_GROUP_ID: The negative numeric ID of the Telegram group to monitor.
(Instructions for getting this are in the chat history, usually involves a helper script
and typing the group name.)

TELEGRAM_TARGET_USER_HANDLES: A comma-separated list of the usernames you want to monitor
(without the '@' symbol).

CREATE A .gitignore FILE
Create a file named '.gitignore' in the root directory of your project. This
file tells Git to ignore certain files, preventing you from accidentally
committing sensitive data or temporary files.

.gitignore file content:

.env
*.session

RUN THE BOT
Once your .env file is configured and saved, run the main bot script:

python telegram_monitor.py

The bot will connect to Telegram, and if 'me_id' and 'target_group_id' are
correctly set, it will start monitoring. Check your terminal for output and
your designated notification chat for forwarded messages.