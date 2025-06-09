# Import necessary libraries for Telegram bot functionality
from telethon.sync import TelegramClient, events
import asyncio # Used for asynchronous operations, especially for the event loop
import re    # Import the regular expression module (still needed if SOLANA_ADDRESS_PATTERN is kept for reference, but not for filtering)
import os    # Used to access environment variables
from dotenv import load_dotenv # Used to load environment variables from a .env file

# Load environment variables from a .env file (if it exists)
# This is crucial for securely managing sensitive information like API keys.
load_dotenv()

# --- Configuration ---
# Your Telegram API credentials. These should be loaded from environment variables
# for security. NEVER hardcode sensitive information directly in your script when
# sharing on GitHub.
# TELEGRAM_API_ID: Your API ID from my.telegram.org
api_id = int(os.getenv('TELEGRAM_API_ID', '0')) # Default to 0 if not set, will cause connection error
# TELEGRAM_API_HASH: Your API hash from my.telegram.org
api_hash = os.getenv('TELEGRAM_API_HASH', '') # Default to empty string
# TELEGRAM_PHONE: Your phone number (e.g., '+12345678900')
phone = os.getenv('TELEGRAM_PHONE', '')

# The ID of the Telegram group chat you want to monitor.
# This should be the exact negative integer ID of the target group.
# Users should obtain this from their own Telegram client (e.g., via @RawDataBot or a helper script).
# Example: -1001234567890
target_group_id = int(os.getenv('TELEGRAM_TARGET_GROUP_ID', '0')) # Default to 0

# A list of user handles (usernames) of the specific persons you want to monitor.
# The bot will look for messages from these users.
# Users should customize this list with the handles they wish to monitor.
target_user_handles_str = os.getenv('TELEGRAM_TARGET_USER_HANDLES', '')
target_user_handles = [handle.strip() for handle in target_user_handles_str.split(',') if handle.strip()]


# The ID where messages from the monitored users will be forwarded.
# This should be the unique positive integer ID of a user's private chat or a BotFather bot's private chat.
# Users should obtain this from their own Telegram client or a helper script.
# Example: 123456789
me_id = int(os.getenv('TELEGRAM_ME_ID', '0')) # Default to 0


# --- Regular Expression for Solana Contract Addresses ---
# This pattern is now included for reference but is NO LONGER USED for filtering
# if the goal is to forward all messages from target users.
SOLANA_ADDRESS_PATTERN = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{44}\b')


# --- Bot Initialization ---
# Initialize the TelegramClient.
# 'session_name': A string that will be used as the name of the session file.
#                 This file stores authentication data, so you don't have to log in every time.
#                 Keep this file secure!
# 'api_id' and 'api_hash': Your API credentials.
client = TelegramClient('user_monitor_session', api_id, api_hash)

# --- Event Handler Function (Main Monitoring Logic) ---
@client.on(events.NewMessage)
async def handler(event):
    """
    Handles new messages in Telegram.
    Checks if the message is from the target group and from a target user,
    then forwards it privately to the designated chat (me_id).
    This version forwards ALL messages from target users, without CA filtering.
    """
    if event.text and event.chat_id:
        # Check if the message originates from the specific target group.
        if event.chat_id == target_group_id:
            print(f"[DEBUG] Message matched target group ({target_group_id}).")
            sender = await event.get_sender()

            if sender and sender.username:
                if sender.username in target_user_handles:
                    print(f"[DEBUG] Sender @{sender.username} is a target user. Forwarding message...")
                    forward_message_text = (
                        f"**New message from @{sender.username} in group:**\n" # Removed "Potential Solana CA found!"
                        f"{event.text}"
                    )
                    # Only attempt to forward if me_id is configured.
                    if me_id != 0: # Check against default 0
                        await client.send_message(me_id, forward_message_text, parse_mode="md")
                        print(f"Forwarded message from @{sender.username} to {me_id}.")
                    else:
                        print("Warning: 'TELEGRAM_ME_ID' is not set. Message not forwarded.")
                # else: # No need to print for every non-target user
                #     print(f"Sender @{sender.username} is NOT in target_user_handles.")
            # else: # No need to print for every sender without username
            #     print(f"Sender has NO username. Sender ID: {sender.id}. Message not from a target user.")
        # else: # No need to print for every message not from target group
        #     print(f"Message is NOT from target group. From chat ID: {event.chat_id}.")

# --- Main Bot Execution ---
async def main():
    """
    Main function to connect the client and start the bot.
    """
    print("Connecting to Telegram...")
    # Validate essential environment variables
    if not api_id or not api_hash or not phone:
        print("ERROR: TELEGRAM_API_ID, TELEGRAM_API_HASH, or TELEGRAM_PHONE environment variables are not set.")
        print("Please set them in a .env file or directly in your environment.")
        return # Exit if essential config is missing

    try:
        await client.start(phone=phone)
        print("Client connected successfully!")
    except Exception as e:
        print(f"ERROR: Failed to connect to Telegram. Please check your API ID, API Hash, and Phone Number.")
        print(f"Error details: {e}")
        print("Exiting...")
        return # Exit if connection fails

    me = await client.get_me()
    print(f"Logged in as: {me.first_name} (@{me.username}) with ID: {me.id}")

    if me_id == 0:
        print("\n*** IMPORTANT: 'TELEGRAM_ME_ID' environment variable is not set. ***")
        print("Messages will NOT be forwarded until this is configured.")
        print("Set TELEGRAM_ME_ID to the unique numeric ID of your personal chat or your bot's chat.")
    else:
        print(f"Messages will be forwarded to configured 'me_id': {me_id}")

    if target_group_id == 0:
        print("\n*** IMPORTANT: 'TELEGRAM_TARGET_GROUP_ID' environment variable is not set. ***")
        print("The bot will not monitor any specific group until this is configured.")
        print("Set TELEGRAM_TARGET_GROUP_ID to the negative numeric ID of the group you want to monitor.")
    else:
        print(f"Monitoring group ID: {target_group_id}")
    
    if not target_user_handles:
        print("\n*** IMPORTANT: 'TELEGRAM_TARGET_USER_HANDLES' environment variable is empty. ***")
        print("The bot will not filter for specific users until this is configured.")
        print("Set TELEGRAM_TARGET_USER_HANDLES to a comma-separated list of usernames (e.g., 'user1,user2').")
    else:
        print(f"For messages from users: {', '.join(target_user_handles)}")


    print("Bot is running... Press Ctrl+C to stop.")

    await client.run_until_disconnected()
    print("Bot stopped.")

# --- Run the Main Function ---
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
