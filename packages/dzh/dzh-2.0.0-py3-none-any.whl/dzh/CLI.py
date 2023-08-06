from getpass import getpass
from dzh.UI import UI, get_sha256, get_prng, NONCE_MIN


def yes_or_no(question):
    try:
        while True:
            answer = input("{} [y/n]: ".format(question)).lower().strip()[0]
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print("Invalid answer, retry")
                continue
    except EOFError as e:
        print(e)


def get_hidden_int(requested_int_parameter):
    while True:
        try:
            hidden_int = int(getpass(requested_int_parameter).encode('utf-8'))
            if hidden_int < NONCE_MIN:
                raise ValueError
        except ValueError:
            print("Invalid input, {} must be an int of at least {} digits for this implementation".format(
                requested_int_parameter[:len(requested_int_parameter) - 2], len(str(NONCE_MIN))))
            continue
        return hidden_int


def get_hidden_input(nonce):
    return get_sha256(getpass("Password: ")),\
        get_sha256(str(get_hidden_int("Salt: ") + nonce))


class CLI(UI):
    def __init__(self):
        super().__init__()
        self.is_first_time = yes_or_no("Is this the first time?")
        self.nonce = get_prng() if self.is_first_time else get_hidden_int("Nonce: ")
        self.password, self.salt = get_hidden_input(self.nonce)


def run_cli():
    try:
        cli = CLI()

        if cli.is_first_time:
            print("Confirm requested, retype")
            p, s = get_hidden_input(cli.nonce)
            if not cli.check(p, s):
                print("The two input doesn't match, retry.")
                return

        print("Generating...")
        cli.create_secret()
        print("Done!")

        cli.set_clipboard()
        if yes_or_no("Display the QR code?"):
            cli.get_qrcode()

    except KeyboardInterrupt:
        print("\nCtrl-c signal received.")
