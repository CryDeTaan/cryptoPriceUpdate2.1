# cryptoPriceUpdate2.1

This is a simple bot-based crypto currency price updater that will send you an update of the price for the given tokens you 
specify in the config file.

Version 2.1 is a complete rewrite of the original bot which I wrote and no longer available. 
## Installation and running cryptoPriceUpdate2.1

I used python 3, so you might wont to figure out how to use run python3 and pip3. 
Let me know if you are not familiar with his and I'll gladly help. 
```commandline
git clone https://github.com/CryDeTaan/cryptoPriceUpdate2.1.git
pip3 install -r requirements.txt
```
You would want to look at the Setup and config sections before actually running the bot
```commandline
python3 cryptoBot.py & 
# NOTE: & to run in the background.
```
 
## Setup Telegram and API Token
You will need telegram installed on any device and a Telegram bot. 

1. First, telegram; you can get it on any of the platform's app stores, just search for telegram.
   https://telegram.org/ for more information.
   
2. Next we need to create a bot using a bot called @BotFather the telegram team created specifically for this.
   
   To access the bot create a new message and search for the @BotFather.
   
   Once you clicked on start you can follow the instruction to create a new bot, its really simple though and 
   I am not going into detail here.
   
   What is important here we need the API access token which is a string along the lines of 
   `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw` that is required to authorize the bot and send requests to the Bot API.
   
3. Lastly, but is totally optional, we can add commands to the bot.
   This will add a `/` key that when selected you will get all the command that your bot knows of.
   
   You can use the @Botfather chat commands to do this:
   
   `/mybots` — returns a list of your bots with handy controls to edit their settings
   
   `/setcommands` — hang  the list of commands supported by your bot. Users will see these commands as suggestions 
   when they type / in the chat with your bot.
   
   NOTE: There is a bit of a caveat here; some of the ticker IDs are double-barrel and specifying it this way does not 
   play nicely with the `/setcommand` function. If you use double-barrel ticker other than bitcoin-cash, 
   you will have to type out the ticker as a command manually, for example `/bitcoin-gold`
   
   The reason why I say other than Bitcoin Cash, is because I built in a way to cater for Bitcoin Cash
   by specifying the command as `/bitcoincash` which I rewrite to `bitcoin-cash` before sending to the API.
   
## Configure the bot
Copy and update the config.py.example with your telegram API token from step 2 of Setup Telegram and API Token,
your chat_id, and also the ticker IDs. 

`cp config.py.example config.py && vi config.py`

example of config.py

```yaml
telegram_bot = {
        'token': '110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw',
        'chat_id': '75371905',
        'coin_list': ["bitcoin", "neo", "bitcoin-cash"]
        }
```
##### Obtaining your chat ID:
Using telegram you can chat with the @userinfobot which will return your chat_id

##### Obtaining ticker IDs:
You can get a list of them from https://api.coinmarketcap.com/v1/ticker/ and as an example `"id": "bitcoin"` from:
```json
{
    "id": "bitcoin",
    "name": "Bitcoin",
    "symbol": "BTC",
    "rank": "1",
    "price_usd": "8954.05",
    "price_btc": "1.0",
    "24h_volume_usd": "4493800000.0",
    "market_cap_usd": "149548752290",
    "available_supply": "16701800.0",
    "total_supply": "16701800.0",
    "max_supply": "21000000.0",
    "percent_change_1h": "0.7",
    "percent_change_24h": "8.49",
    "percent_change_7d": "15.06",
    "last_updated": "1511673552"
}
```
## Future Work
- At this stage when any API requests fail the code will continue, I'd like to have some sort of retry.
- I may want to run this as a daemon.
- Adding tickers via the bot and not manually in the config file.
- Using inline keyboards.

## License

See the [LICENSE](https://github.com/CryDeTaan/cryptoPriceUpdate2.1/blob/master/LICENSE) file for license rights and limitations (MIT).
