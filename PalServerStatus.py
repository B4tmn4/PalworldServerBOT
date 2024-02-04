import mcrcon
import time
import socket
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ANSI escape codes for text formatting
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

def count_players(response_players):
    # Count the number of lines in the response, excluding the extra line
    player_count = len(response_players.splitlines()) - 1
    return max(0, player_count)  # Ensure player count is not negative

def is_server_reachable(server_ip, rcon_port, rcon_password):
    try:
        with socket.create_connection((server_ip, rcon_port), timeout=5):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False
def get_online_players(server_ip, rcon_port, rcon_password):
    if not is_server_reachable(server_ip, rcon_port, rcon_password):
        return None  # Server is offline

    try:
        with mcrcon.MCRcon(server_ip, rcon_password, port=rcon_port, timeout=5) as rcon:
            response_players = rcon.command("showplayers")
            if response_players is not None:
                # Split the lines, excluding the first line, and extract only the names
                lines = response_players.strip().split('\n')[1:]
                names = [line.split(',')[0] for line in lines]
                return '\n'.join(names)
            else:
                return None
    except mcrcon.MCRconException as e:
        return None  # RCON connection error
    
def check_server_status(server_ip, rcon_port, rcon_password):
    if not is_server_reachable(server_ip, rcon_port):
        print(f"\r{BOLD}{RED}Server is Offline{RESET}", end="")
        return

    try:
        with mcrcon.MCRcon(server_ip, rcon_password, port=rcon_port, timeout=5) as rcon:
            response_status = rcon.command("info")  # Change the command to the one that works for your game

            if response_status is not None:
                print(f"\r{BOLD}Server Status:{GREEN} Running{RESET}", end="")
            else:
                print(f"\r{BOLD}{RED}Server Status: Offline{RESET}", end="")
                return  # Exit the function if server is offline

            response_players = rcon.command("showplayers")  # Change the command to the one that works for your game

            player_count = count_players(response_players)
            print(f"{BOLD} | Player Count:{BLUE} {player_count}{RESET}", end="")

            print(f"{BOLD} | {response_status[0:11]}{RESET}", end=""), print(f"{BOLD}{response_status[32:46]}{RESET}", end="", flush=True)

    except mcrcon.MCRconException as e:
        print(f"\r{BOLD}{RED}Error: {e} | Server Status: Offline{RESET}", end="")

def main():
    server_ip = "110.148.165.86"  # Replace with your actual server IP
    rcon_port = 25575
    rcon_password = "BBC1"  # Replace with your actual RCON password

    while True:
        check_server_status(server_ip, rcon_port, rcon_password)
        time.sleep(10)  # Sleep for 10 seconds before checking again

if __name__ == "__main__":
    main()
