import random
import json
import argparse

messages = {
    "password_created": "\nYou can now copy and use your password!",
    "config": '\nYour password settings are now stored next time. Use "pwd-gen -c" to reconfigure them',
    "invalid_num": "Please type a valid number\n",
    "invalid_bool": "Please choose between yes (y) or no (n)\n",
}

passphrase_choices = ["1", "pass", "passphrase", "phrase"]
scrambled_choices = ["2", "scrambled", "scramble", "rand", "random"]

saved_data = {}


def get_json():
    d = {}
    try:
        with open("config.json", "r") as j:
            if j != None:
                d = json.load(j)
    except FileNotFoundError:
        return d
    return d


def write_json():
    with open("config.json", "w") as j:
        json.dump(saved_data, j)


def get_number(current_pwd: str):
    num = random.randrange(10)
    if current_pwd.endswith(str(num - 1)):
        if num == 9:
            num = 0  # Avoids inserting a 10 and making the password more than 15 chars long
        else:
            num += 1
    return num


def get_txt():
    with open("src/clean_words_alpha_revb.txt", "r") as t:
        dictionary_txt = list(t.read().split())
    return dictionary_txt


def get_word_from_txt(txt: list, capitalized: bool):
    word = ""
    while len(word) < 4 or len(word) > 8:
        word = random.choice(txt)
    if capitalized:
        return word.capitalize()
    else:
        return word


def get_scrambled(length: int, include_nums: bool, include_special: bool):
    pw_string = "\n"

    alphabet_lower = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    alphabet_upper = []
    for letter in alphabet_lower:
        alphabet_upper.append(letter.capitalize())
    special_chars = ["!", "?", "@", "#", "$", "%", "&", "*", "^"]

    types = ["lowercase", "uppercase"]
    if include_nums:
        types.append("number")
    if include_special:
        types.append("special")

    has_special = False
    has_nums = False
    i = 0
    while i < length:
        char_type = random.choice(types)
        new_char = ""

        if char_type == "lowercase":
            new_char = alphabet_lower[random.randrange(len(alphabet_lower))]
        elif char_type == "uppercase":
            new_char = alphabet_upper[random.randrange(len(alphabet_upper))]
        elif char_type == "special":
            new_char = special_chars[random.randrange(len(special_chars))]
            has_special = True
        elif char_type == "number":
            new_char = str(get_number(pw_string))
            has_nums = True

        if pw_string.endswith(new_char):
            continue
        else:
            pw_string += new_char
            i += 1

    incomplete = (include_nums and not has_nums) or (
        include_special and not has_special
    )
    check_scrambled(incomplete, length, include_nums, include_special, pw_string)


def check_scrambled(incomplete: bool, len: int, nums: bool, special: bool, pw: str):
    if incomplete:
        get_scrambled(len, nums, special)
    else:
        print(pw)


def get_passphrase(length: int, separator: str, capitalize: bool):
    pw_string = "\n"

    txt = get_txt()
    for i in range(length):
        if i != length - 1:
            pw_string += get_word_from_txt(txt, capitalize) + separator
        else:
            pw_string += get_word_from_txt(txt, capitalize)

    print(pw_string)


def save_input(key: str, input: str | int):
    saved_data[key] = input


def get_int_input(quantity_of: str, default: int):
    is_typing_number = True
    while is_typing_number:
        try:
            num = int(
                input(f'How many {quantity_of}? (default "{default}")\n->') or default
            )

            if num > 0:
                is_typing_number = False
            else:
                print(messages["invalid_num"])
        except ValueError:
            print(messages["invalid_num"])

    save_input("length", num)

    return num


def get_y_or_n_input(to_include: str, key: str):
    yes_choices = ["1", "y", "yes", "true"]
    no_choices = ["0", "n", "no", "false"]

    is_choosing = True
    while is_choosing:
        choice = (
            str(
                input(f'Include {to_include}? yes (y) or no (n) (default "y")\n->')
                or "y"
            )
            .lower()
            .strip()
        )
        if choice in yes_choices:
            include = True
            is_choosing = False
        elif choice in no_choices:
            include = False
            is_choosing = False
        else:
            print(messages["invalid_bool"])

    save_input(key + " bool", str(include))
    return include


def handle_password():

    user_choice = (
        str(
            input(
                'Generate: 1 - passphrase, 2 - scrambled password (default "passphrase")?\n->'
            )
            or "1"
        )
        .lower()
        .strip()
    )

    if user_choice in passphrase_choices:
        length = get_int_input("words", 6)
        separator = str(input('Type a separator (default "-"):\n->') or "-")
        save_input("separator", separator)
        capital_words = get_y_or_n_input("capitalized words", "1st")

        save_input("2nd bool", "")
        get_passphrase(length, separator, capital_words)

    elif user_choice in scrambled_choices:
        length = get_int_input("characters", 15)
        include_nums = get_y_or_n_input("numbers", "1st")
        include_specials = get_y_or_n_input("special characters", "2nd")

        save_input("separator", "")
        get_scrambled(length, include_nums, include_specials)

    else:
        print("Please make a valid choice")
        return

    save_input("pwd_type", user_choice)
    print(messages["password_created"])
    write_json()
    print(messages["config"])


def handle_config(
    type: str, length: int, separator: str, first_bool: str, second_bool: str
):
    if type in passphrase_choices:
        get_passphrase(length, separator, first_bool)
    else:
        get_scrambled(length, first_bool, second_bool)

    print(messages["password_created"])


def generate():
    saved_data = get_json()
    if saved_data != {}:
        d = saved_data
        handle_config(
            d["pwd_type"], d["length"], d["separator"], d["1st bool"], d["2nd bool"]
        )
    else:
        handle_password()
