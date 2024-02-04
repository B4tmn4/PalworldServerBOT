from random import choice, randint


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "Well, you\'re awfully silent..."
    elif '!hello' in lowered:
        return "Hello there!"
    elif '!roll dice' in lowered:
        return f"You rolled: {randint(1,6)}"
    elif '!help' in lowered:
        return "**Available commands:**\n" \
               "**!status** - *shows the status of the server*\n" \
               "**!onlineplayers** - *lists the players online*\n" \
               "**!hello** - *says hello*\n" \
               "**!roll dice** - *rolls a dice*"
    else:
        return None