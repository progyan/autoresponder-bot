# test-autoresponder-bot
My primitive test autoresponder telegram bot server, based on GPT-3. Works _only for Linux_.
The code is not clean. I wrote it for an experiment, so it may be hard to understand.

## Preparation
Download the files and add three `.txt` files that the program will use:
- `ar-save.txt` - Leave this file empty, the program will save and recover some data from this file if the program gets reastrted for any reason;
- `log.txt` - Leave this file empty too, here you will be able to see what happened with the bot at every minute (or configure it to any other period of time).
- `keys.txt` - Here you will need to save important configuration information for the server, in this exact order:
  - Line 1: Your OpenAI api key,
  - Line 2: Your Telegram bot ID,
  - Line 3: Description of AI's job (e.g. "_You are now the Autoresponder. You need to..._ etc.")
 
## Running
Run `ar.py` in your console. The bot will respond while the program is running.
