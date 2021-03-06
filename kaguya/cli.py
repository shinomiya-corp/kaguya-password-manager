# Command-line Interface

import argparse
import random
import re
import string

import pyperclip
from loguru import logger

# Description
_desc = """Welcome to Kaguya Password Manager!

%(prog)s - A bad password manager.

Stores and retrieves your passwords in a secure manner.

You may also check the strength of your passwords, or generate a strong password for your accounts.

"""


def create_argparser() -> argparse.ArgumentParser:
    kaguya_parser = argparse.ArgumentParser(
        prog="kaguya.py",
        description=_desc,
        usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    kaguya_parser.add_argument(
        "-r",
        "--retrieve",
        action="store_true",
        help="activate the search and retrieve function",
    )

    kaguya_parser.add_argument(
        "-e",
        "--edit",
        action="store_true",
        help="activate the edit function to edit an existing entry",
    )

    kaguya_parser.add_argument(
        "-i",
        "--insert",
        action="store_true",
        help="activate the insert function to create a new entry",
    )

    kaguya_parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="activate the password generator",
    )

    kaguya_parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="activate the password checker",
    )

    kaguya_parser.add_argument(
        "-d",
        "--domain",
        type=str,
        help="domain that the account is used for",
    )

    kaguya_parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="username for the specified domain",
    )

    kaguya_parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="password for the specified username",
    )

    logger.debug("argparser created")

    return kaguya_parser


class HandleArgs:
    def __init__(self, args: argparse.Namespace):
        self.args = args

        if args.retrieve:
            logger.info("retrieve option found")
            self.retrieve()

        # TODO add logic here
        ...

    def retrieve(self, domain, username):
        pass

    def edit(self, domain=None, username=None, password=None):
        while not (domain or username or password):
            print("Please provide an argument with either the -d, -u or -p flags.")
            break
        # Placeholder code:
        if domain:
            print(domain)
        if username:
            print(username)
        if password:
            print(password)

    def insert(self, domain=None, username=None, password=None):
        pass

    @staticmethod
    def generate():
        """
        Creates a password based on below criteria.
        Checks itself to be a strong password before being returned as a value.
        """
        upperletters = string.ascii_uppercase
        lowerletters = string.ascii_lowercase
        digits = string.digits
        symbols = r"[!#$%&'()*+,-.\^_`{|}~" + r'"]'
        allchar = upperletters + lowerletters + digits + symbols

        length = random.randint(8, 32)
        strong_password = [
            random.choice(upperletters),
            random.choice(lowerletters),
            random.choice(digits),
            random.choice(symbols),
        ]
        for i in range(length - 3):
            strong_password.append(random.choice(allchar))
        random.shuffle(strong_password)
        strong_password = "".join(strong_password)
        # Check that it is strong
        if not HandleArgs.check(strong_password):
            HandleArgs.generate()
        else:
            print("Password generated and copied to the clipboard.")
            pyperclip.copy(strong_password)

    # The strong password checker. Takes the password as the only argument,
    #  outputs a boolean value on strength of password.
    @staticmethod
    def check(password) -> bool:
        """
        Verify the strength of a 'password'.
        Returns the strength of the password.
        A password is considered strong if:
            At least 8 characters in length.
            1 digit or more.
            1 symbol or more.
            1 uppercase letter or more.
            1 lowercase letter or more.
        """
        # Check for input
        if not password:
            print("Please enter a password using the -p option.")
            exit()
        else:
            # Checks the length.
            length_error = len(password) < 8

            # Checks for digit.
            digit_error = re.search(r"\d", password) is None

            # Checks for symbol.
            symbol_error = re.search(r"\W", password) is None

            # Checks for uppercase letter.
            uppercase_error = re.search(r"[A-Z]", password) is None

            # Checks for lowercase letter.
            lowercase_error = re.search(r"[a-z]", password) is None

            # Overall result
            password_ok = not (
                length_error
                or digit_error
                or symbol_error
                or uppercase_error
                or lowercase_error
            )

            print("Password is strong.") if password_ok else print("Password is weak.")

            return password_ok
