import base64
from dzh.UI import UI, NONCE_MIN, get_sha256, get_clipboard, get_prng
import PySimpleGUI as sg
from dzh.hasher import HASH_LENGTH

ICON_PATH = "dzh/D1.png"
FONT = "Roboto"
TITLE = "DZ-Hasher"

sg.theme('DarkBlue')


def convert_file_to_base64(filename):
    """
    To display correctly the icon on windows and unix, it is necessary encode the png file into base64
    """
    try:
        contents = open(filename, 'rb').read()
        return base64.b64encode(contents)
    except Exception as error:
        sg.popup_error('Cancelled - An error occurred', error)


def collapse(layout, key, visibility=False):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param visibility: initialize the section displaying it
    :param layout: The layout for the section
    :param key: Key used to make this section visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=visibility))


def build_window_layout():

    showed_section = [
        # nonce
        [sg.T("Nonce", font=FONT)],
        [sg.In(key='nonce', password_char="*")],

        # password
        [sg.T("Password", font=FONT)],
        [sg.In(key='password', password_char='*')],

        # salt
        [sg.T("Salt", font=FONT)],
        [sg.In(key='salt', password_char='*')]
    ]
    hidden_section = [
        # password confirm
        [sg.T("Password confirm", key="Password confirm", font=FONT)],
        [sg.In(key='password_confirm', password_char='*')],

        # salt confirm
        [sg.T("Salt confirm", key="Salt confirm", font=FONT)],
        [sg.In(key='salt_confirm', password_char='*')]
    ]

    return [
        [sg.Checkbox('Is first time', key="is_first_time", default=False, enable_events=True)],
        [collapse(showed_section, 'showed_section', True)],
        [collapse(hidden_section, 'hidden_section')],

        [sg.T(size=(40, 1), key='output', font=FONT)],
        [sg.B('Generate', font=FONT, bind_return_key=True), sg.B('QRCode', font=FONT)],
    ]


class GUI(UI):
    def __init__(self):
        super().__init__()
        self.window = sg.Window(TITLE, build_window_layout(), icon=convert_file_to_base64(ICON_PATH))

    def parse_int(self, parameter_string, parameter):
        try:
            hidden_int = int(parameter.encode('utf-8'))
            if hidden_int < NONCE_MIN:
                raise ValueError
            return hidden_int
        except ValueError:
            self.show_text("Invalid input, {} must be an int of at least {} digits for this implementation".format(
                parameter_string, len(str(NONCE_MIN))))
            return -1

    def parse_values(self, values):
        # values is a dictionary with a tuple as a value
        if len(values['nonce']) == 0:
            return False
        self.nonce = self.parse_int("Nonce", values['nonce'])
        if self.nonce < 0:
            return False

        if len(values['password']) == 0:
            return False
        self.password = get_sha256(values['password'])

        if len(values['salt']) == 0:
            return False
        salt = self.parse_int("Salt", values['salt'])
        if salt < 0:
            return False
        self.salt = get_sha256(str(salt + self.nonce))

        return True

    def show_text(self, text):
        self.window['output'].update(text)

    def show_confirm_fields(self, val):
        self.window["hidden_section"].update(visible=val)
        self.window["nonce"].update(str(get_prng()), password_char="") if val\
            else self.window["nonce"].update("", password_char="*")


def run_gui():
    gui = GUI()

    generated = False
    while True:
        # blocked until the user puts an input and generates some event
        event, values = gui.window.read()

        # if the top-right arrow is pressed, exit
        if event == sg.WINDOW_CLOSED:
            break
        if event == "QRCode":
            if generated and len(get_clipboard()) == HASH_LENGTH*2:
                gui.get_qrcode()
            gui.show_text("Generate new password to get the QRCode")
            continue

        if event == "Generate":
            if not gui.parse_values(values):
                continue

            if values["is_first_time"]:
                salt_confirm = get_sha256(str(gui.parse_int("Salt", values['salt_confirm']) + gui.nonce))
                if not gui.check(get_sha256(values['password_confirm']), salt_confirm):
                    gui.show_text("The password and salt fields must coincide")
                    continue
            gui.show_text("Generating ... the program may appear to be unresponsive")
            gui.window.refresh()

            gui.create_secret()
            gui.show_text("Done!")
            gui.set_clipboard()

            generated = True
        else:
            # if the checkbox "is first time" is checked, then displays the 2 fields for the confirmation
            gui.show_confirm_fields(values["is_first_time"])

    gui.window.close()
