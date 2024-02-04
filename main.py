from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from PalServerStatus import check_server_status, is_server_reachable, count_players,get_online_players, GREEN, RED, BLUE, BOLD, RESET
import mcrcon


#LOAD OUR TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


#MESSAGE FUNCITIONALITY
async def   send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# CHECK SERVER STATUS
async def check_server_status_command(message) -> None:
    server_ip = "110.148.165.86"  # Replace with your actual server IP
    rcon_port = 25575
    rcon_password = "BBC1"  # Replace with your actual RCON password

    if not is_server_reachable(server_ip, rcon_port, rcon_password):
        response = f"```diff\n-Server Status: OFFLINE```"
    else:
        try:
            with mcrcon.MCRcon(server_ip, rcon_password, port=rcon_port, timeout=5) as rcon:
                response_status = rcon.command("info")  # Change the command to the one that works for your game

                if response_status is not None:
                    response = f"```diff\n+Server Status: ONLINE```"
                else:
                    response = f"```diff\n-Server Status: OFFLINE```"
                    return  # Exit the function if server is offline

                response_players = rcon.command("showplayers")  # Change the command to the one that works for your game

                player_count = count_players(response_players)
                response += f"```elm\nPlayer Count: {player_count}```"
                response += f"```ini\n[{response_status[0:11]}" + f"{response_status[32:46]}]```"

        except mcrcon.MCRconException as e:
            response = f"Error: {e} | Server Status: Offline"

    await message.channel.send(response)

# ONLINE PLAYERS COMMAND
async def online_players_command(message) -> None:
    server_ip = "110.148.165.86"  # Replace with your actual server IP
    rcon_port = 25575
    rcon_password = "BBC1"  # Replace with your actual RCON password

    online_players = get_online_players(server_ip, rcon_port, rcon_password)
    if online_players is not None:
        response = f"```md\n> Online Players:\n{online_players}```"
    else:
        response = "Error retrieving online players or server is offline."

    await message.channel.send(response)


#startup for our bot

@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running")

# Handle incoming messages
@client.event
async def on_message(message) -> None:
    if message.author == client.user or not message.content.startswith('!'):
        return  # Ignore messages from the bot and messages without !

    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')
    
    if user_message == "!status":
        await check_server_status_command(message)
    elif user_message == "!onlineplayers":
        await online_players_command(message)
    else:
        await send_message(message, user_message)



#MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()


