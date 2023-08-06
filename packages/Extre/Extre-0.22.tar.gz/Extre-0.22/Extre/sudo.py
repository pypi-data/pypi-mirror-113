from Extre import ExtremedB, extremepro_bot

CMD_HELP = {}


def sudoers():
    return ExtremedB["SUDOS"].split()


def should_allow_sudo():
    if ExtremedB["SUDO"] == "True":
        return True
    else:
        return False


def owner_and_sudos():
    return [str(extremepro_bot.uid), *sudoers()]
