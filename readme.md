# Pylax

[Read this document in other languages](doc/docs/global_docs.md)

Pylax is an [Open Source](https://en.wikipedia.org/wiki/Open_source) project of a bot to help manage the **Truth or Dare** game in [Discord](https://discord.com/) communities. The project was initially created to be used in the [Ballerini Community](https://discord.gg/wagxzStdcR), but is now available in an open way. Pylax is the **2.0** version of the project that previously was called [Calax](https://en.wikipedia.org/wiki/Truth_or_Dare_(2018_film))

## Bot settings
To run this project, first you need to create an application on the [Developer Portal](https://discord.com/developers/applications). In the `General information` tab fill in the **Name**, **Description** and **App Icon** fields. In the `Bot` tab click on the **Add bot** button and add your bot. Fill in the **Username** and **icon** fields. Now let's set the bot settings, mark the following fields and then save the changes:

**Authorization Flow**
- [X] PUBLIC BOT
- [ ] REQUIRES OAUTH2 CODE GRANT

**Privileged Gateway Intents**
- [X] PRESENCE INTENT
- [X] SERVER MEMBERS INTENT
- [X] MESSAGE CONTENT INTENT

On the `pylax/` directory duplicate the `example.env` file and rename it as `.env` and fill in your fields.
In your server, create a text channel called `authentication` and put its id in the file mentioned above. Each game takes place in a room, each room is composed of a pair of channels (1 voice and 1 text), create the number of rooms depending on the number of games you want. Don't forget to edit the permissions of the members for these rooms (that's up to you = D).

On the `pylax/src/json` directory duplicate the `example.rooms.json` file and rename it as `rooms.json` and fill in your fields.
In this file there is a list that stores which are the rooms where the games will take place. Example of filling:
```json
[
    {
        "bot_master": "123456789",
        "id_text_channel": "75656456745",
        "id_voice_channel": "25435498675687"
    },
    {
        "bot_master": "987654321",
        "id_text_channel": "567453563",
        "id_voice_channel": "656754674"
    }
]
```
`bot_master` is the person who will manage a certain room, use the *snowflake* standard.

**Now let's bring the bot to your server!**

On the page of your application in the `OAuth2 > URL Generator` tab select the **Scope** `bot` and in **Bot Permissions** select all the permissions below:

**General permissions**
- [X] Manage server
- [X] Manage channels
- [X] Manage emojis and stickers
- [X] Read messages/View Channels
- [X] Moderate members

**Text permissions**
- [X] Send messages
- [X] Manage messages
- [X] Embed links
- [X] Attach files
- [X] Read message history
- [X] Use external emojis
- [X] Use external stickers
- [X] Add reactions

**Voice permissions**
- [X] Connect
- [X] Use voice activity
- [X] Use embedded activities

These permissions are necessary for the bot to work correctly. Now copy the generated url and paste it into your browser, select the server you want to add the bot to and click **Authorize**. When the bot is online, one of the `bot masters` must enter a voice channel and type in their room the command ??add_auth_message so that the bot sends an authentication message to the `authentication` text channel. Members must react with the verification emoji so that the bot adds them to the room.

## Setting the bot online
Para colocar o bot online, você precisa ter o [Python](https://www.python.org/downloads/) instalado na sua máquina. Depois de instalado, abra o terminal e execute o seguinte comando:
To set the bot online, you need to have [Python](https://www.python.org/downloads/) installed on your machine. After installed, open the terminal and run the following command:
```bash
pip install -r requirements.txt
```
This command will install all the necessary dependencies to run the project. Now let's run the bot, run the following command:
```bash
python pylax
```
All done! The bot is online and ready to be used.

## Commands
The bot commands are executed through messages sent in the text channel of the voice room. The commands are started with `??` and followed by the command name. Example: `??add_auth_message`. The commands are:

**Game commands**
- `??start` - Starts the game.
- `?spin` - Spins the bottle and chooses a victim.
- `??op [o] [v]` - Selects the victim's option.
- `??help` - Pylax selects a question from the database.
- `??done` - The victim indicates that it answered the question.

**Bot master commands**
- `??add_auth_message` - Sends an authentication message to the `authentication` text channel.
- `??kick <member_id> [0] [1] [2]` - Removes the member from the voice room and from the text room. `0` to remove only from the game, `1` to remove only from the room `2` to remove from both.
- `??next` - Goes to the next member.
- `??restart` - Restarts the game.
- `??rules` - Shows the game rules.
- `??show_players` - Shows the players in the room.
- `??status` - Shows the game status.

## About the game
**Game script**
- The game starts when the bot master types the command `??start`.
- The person in turn (asker) must spin the bottle to choose a victim.
- The victim must choose an option between the 2 available (v: truth, c: consequence).
- Based on what the victim chose, the asker must ask a question.
- After the victim answers the question, she must type the command `??done`.
- It will be a vote to decide whether the victim is lying or not.
- After the vote, the next person in turn (asker) must spin the bottle to choose a new victim.

**Game rules**
- To play the game, you must be in a voice room of the game and have reacted with the verification emoji in the authentication message.
- Only the bot master can start the game.
- The game has no end.
- If a player chooses 3 times the option `v`, he will be forced to choose the option `c`.
- If the people decide that the victim is lying, it will receive a flag. With 2 flags, the victim is unable to play for two rounds. If they decide that the victim is telling the truth, it wins a star.

## Contributing
[I want to contribute!](doc/docs/en/contributing.md)

## [LICENSE](LICENSE)
