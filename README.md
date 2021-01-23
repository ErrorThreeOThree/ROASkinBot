This is a fan-made skin generation discord chat-bot for the video game Rivals of Aether. This bot uses the roaskins python library.

# Usage
Write your Discord chat bot token to the **token.secret** file. You can start the bot using either Docker or without Docker.

## Docker
You can use the provided Dockerfile to run this bot.
1. Build the container
`docker build --tag roaskinbot .`
2. Run the container
`docker run roaskinbot`

## Native
1. Install the dependencies with pip:
`pip install -r requirements.txt`
2. Run the bot
`python3 ROASkinBot.py`

# Bot commands:
- `!skin [RIVALNAME] [1-4]` Generate 1-4 random skins for the rival RIVALNAME
- `!skin present [RIVALNAME] [COLORCODE] [DESCRIPTION]` Generate a preview image for the rival RIVALNAME with the skin color code COLORCODE. You may add a description.
- `!skin help` Show help message.

## Demo
![](https://i.imgur.com/9uThwl1.png)