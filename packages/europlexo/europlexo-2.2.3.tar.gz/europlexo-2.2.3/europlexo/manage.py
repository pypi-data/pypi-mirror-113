from datetime import datetime
from json import dump, load
from os import path, walk
from re import search

from colorifix.colorifix import erase, paint, ppaint
from europlexo.seriesfinder import get_suggestion_list
from halo import Halo
from pymortafix.utils import direct_input, multisub, strict_input
from requests import get
from telegram import Bot
from telegram.error import InvalidToken

SPINNER = Halo()

# --- Config file


def get_config():
    return load(open(f"{path.abspath(path.dirname(__file__))}/config.json"))


def save_config(config_dict):
    return dump(
        config_dict,
        open(f"{path.abspath(path.dirname(__file__))}/config.json", "w"),
        indent=4,
    )


def remove_serie(index):
    config = get_config()
    config["serie"] = [
        serie for i, serie in enumerate(config.get("serie")) if index != i
    ]
    save_config(config)


def add_serie(name, link, folder, lang, mode):
    new = {"name": name, "site": link, "folder": folder, "language": lang, "mode": mode}
    config = get_config()
    config["serie"] += [new]
    save_config(config)


def add_new_path(path):
    config = get_config()
    config["path"] = path.strip()
    save_config(config)


def is_folder_unique(folder_name):
    folders = [serie.get("folder") for serie in get_config().get("serie")]
    return folder_name not in folders


def add_telegram_config(bot_token, chat_id):
    config = get_config()
    config["telegram-bot-token"] = bot_token
    config["telegram-chat-id"] = chat_id
    save_config(config)


def add_eurostreaming_site(es_url):
    config = get_config()
    config["eurostreaming"] = es_url
    save_config(config)


# --- Pretty Print


def pprint_row(serie_name, lang, mode, index=False, remove=False):
    if index and remove:
        return paint(f"[!red][#] {serie_name} [{mode}]")
    if index and not remove:
        ret_str = paint(f"[#green][>] {serie_name}")
    else:
        ret_str = f"[ ] {serie_name}"
    return ret_str + paint(f" [#cyan]({lang}) [#blue][{mode}]")


def pprint_serie(serie_list, index, remove=None):
    if not serie_list:
        return "No serie added.."
    return "\n".join(
        [
            pprint_row(name, lang, mode, index == i, remove=remove)
            for i, (name, _, _, lang, mode) in enumerate(serie_list)
        ]
    )


def pprint_actions(mode=None):
    if mode == "confirm":
        actions = {"y": "confirm", "n": "back"}
    elif mode == "add":
        actions = {"ws": "move", "c": "confirm", "b": "back"}
    elif mode == "back":
        actions = {"b": "back"}
    elif mode == "settings":
        actions = {
            "u": "backup",
            "r": "restore",
            "p": "path",
            "t": "telegram",
            "e": "eurostreaming",
            "b": "back",
        }
    elif mode == "path":
        actions = {"e": "edit", "b": "back"}
    else:
        actions = {
            "ws": "move",
            "a": "add",
            "r": "remove",
            "e": "settings",
            "q": "quit",
        }
    return (
        "-" * sum(len(action) + 5 for action in actions.values())
        + "\n"
        + " ".join(
            paint(f"[[@bold]{key}[/@]]:[#magenta]{action}")
            for key, action in actions.items()
        )
    )


def pprint_query(query_list, selected):
    return "\n".join(
        paint(f"[#green][>] {name}") if selected == i else f"[ ] {name}"
        for i, (name, _) in enumerate(query_list)
    )


def pprint_settings():
    config = get_config()
    labels = ("Eurostreaming", "Current path", "Backup", "Telegram")
    eurostreaming_url = f"[#blue]{config.get('eurostreaming')}"
    path_str = f"[#blue]{config.get('path')}"
    backup_str = f"[#blue]{get_last_backup()}"
    telegram_str = (
        f"[#blue]{config.get('telegram-bot-token')}[/# @bold]:"
        f"[/@ #blue]{config.get('telegram-chat-id')}"
    )
    telegram_str = config.get("telegram-bot-token") and telegram_str or ""
    values = (eurostreaming_url, path_str, backup_str, telegram_str)
    return "\n".join(
        paint(f"[@bold]{lab}[/]: {val}") for lab, val in zip(labels, values)
    )


def get_last_backup():
    _, _, files = list(walk("."))[0]
    backups = sorted(
        [file for file in files if search(r"europlexo-backup\.json$", file)],
        reverse=True,
    )
    return backups[0] if backups else ""


def recap_new_serie(name, url, folder, lang, mode):
    return paint(
        f"Name: [#blue]{name}[/]\nLink: [#blue]{url}[/]\nFolder: [#blue]{folder}[/]\n"
        f"Language: [#blue]{lang}[/]\nMode: [#blue]{mode}",
    )


# --- Input


def is_bot_valid(token):
    try:
        Bot(token)
        return True
    except InvalidToken:
        return False


def is_eurostreaming_valid(es_url):
    try:
        get(es_url)
        return search("eurostreaming", es_url)
    except Exception:
        return False


# --- Manage


def manage(eurostreaming_url):
    index = 0
    k = "start"
    while k != "q":
        serie_list = [list(serie.values()) for serie in get_config().get("serie")]
        print(pprint_serie(serie_list, index))
        print(pprint_actions())
        k = direct_input(choices=("w", "s", "e", "a", "r", "q"))
        erase(len(serie_list or [0]) + 2)

        if k in ("w", "s"):
            if k == "w" and index:
                index -= 1
            if k == "s" and index < len(serie_list) - 1:
                index += 1

        if k == "e":
            e_k = "start"
            while e_k != "b":
                print(pprint_settings())
                print(pprint_actions(mode="settings"))
                e_k = direct_input(choices=("u", "r", "p", "t", "y", "e", "b"))
                erase(6)
                if e_k == "p":
                    base = paint("[@bold]Path[/]: ")
                    new_path = strict_input(
                        base,
                        wrong_text=paint(f"[#red]Wrong path![/] {base}"),
                        check=lambda x: path.exists(x.strip()),
                        flush=True,
                    )
                    add_new_path(new_path)
                    e_k = ""
                elif e_k == "r":
                    backup_filename = get_last_backup()
                    if backup_filename:
                        backup_dict = load(open(backup_filename))
                        save_config(backup_dict)
                elif e_k == "u":
                    now = datetime.now()
                    config = get_config()
                    dump(
                        config,
                        open(f"{now:%Y-%m-%d}_europlexo-backup.json", "w"),
                        indent=4,
                    )
                elif e_k == "t":
                    base = paint("[@bold]Telegram bot token[/]: ")
                    telegram_bot_token = strict_input(
                        base,
                        wrong_text=paint(f"[#red]Invalid token! {base}"),
                        check=is_bot_valid,
                        flush=True,
                    )
                    base = paint("[@bold]Telegram chat ID[/]: ")
                    telegram_chat_id = strict_input(
                        base,
                        wrong_text=paint(f"[#red]Invalid chat ID![/] {base}"),
                        regex=r"\-?\d+$",
                        flush=True,
                    )
                    add_telegram_config(telegram_bot_token, telegram_chat_id)
                elif e_k == "e":
                    base = paint("[@bold]Eurostreaming site[/]: ")
                    eurostreaming_url = strict_input(
                        base,
                        wrong_text=paint(f"[#red]Wrong site, unreacheable![/] {base}"),
                        check=is_eurostreaming_valid,
                        flush=True,
                    )
                    add_eurostreaming_site(eurostreaming_url)

        if serie_list and k == "r":
            print(pprint_serie(serie_list, index, remove=True))
            print(pprint_actions(mode="confirm"))
            r_k = direct_input(choices=("y", "n"))
            if r_k == "y":
                remove_serie(index)
                index = 0
            erase(len(serie_list) + 2)

        if k == "a":
            q_index = 0
            q_k = "start"
            # serie search
            query = input(paint("[@bold]Serie name[/]: "))
            erase()
            SPINNER.start(paint(f"Searching for [#blue]{query}"))
            query_list = get_suggestion_list(eurostreaming_url, query)
            SPINNER.stop()
            if not query_list:
                ppaint(f"No serie found with [#blue]{query}")
                print(pprint_actions(mode="back"))
                q_k = direct_input(choices=("b",))
                erase(3)
            while q_k not in ("c", "b"):
                print(pprint_query(query_list, q_index))
                print(pprint_actions(mode="add"))
                q_k = direct_input()
                erase(len(query_list) + 2)
                if q_k in ("w", "s"):
                    if q_k == "w" and q_index:
                        q_index -= 1
                    if q_k == "s" and q_index < len(query_list) - 1:
                        q_index += 1
            # new serie
            if q_k == "c":
                base = paint("[@bold]Folder name[/]: ")
                folder = strict_input(
                    base,
                    paint(f"[#red]Folder name must be unique![/] {base}"),
                    check=is_folder_unique,
                    flush=True,
                )
                base = paint("[@bold]Language [eng|ita][/]: ")
                lang = strict_input(
                    base,
                    paint(f"[#red]Language must be 'eng' or 'ita'![/] {base}"),
                    choices=("eng", "ita"),
                    flush=True,
                )
                base = paint("[@bold]Mode [full|new|last][/]: ")
                mode = strict_input(
                    base,
                    paint(f"[#red]Mode must be 'full', 'new' or 'last'![/] {base}"),
                    choices=("full", "new", "last"),
                    flush=True,
                )
                print(recap_new_serie(*query_list[q_index], folder, lang, mode))
                print(pprint_actions(mode="confirm"))
                c_k = direct_input(choices=("y", "n"))
                if c_k == "y":
                    name, link = query_list[q_index]
                    link = multisub({eurostreaming_url: "", "/": ""}, link)
                    add_serie(name, link, folder, lang, mode)
                erase(7)
                index = 0
