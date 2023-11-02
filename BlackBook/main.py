from classes import (
    AddressBook,
    NoteBook,
    Storage,
)
from commands import (
    AddContactCommand,
    EditContactCommand,
    RemoveContactCommand,
    SearchContactsCommand,
    AddNoteCommand,
    EditNoteCommand,
    RemoveNoteCommand,
    SearchNotesCommand,
    HelloCommand,
    HelpCommand,
)
from constants import BINARY_STORAGE_FILENAME, BINARY_NOTEBOOK_STORAGE_FILENAME, RECORD_ARGS, COMMANDS
import re
import gnureadline


gnureadline.set_completer_delims(' \t\n;')


def completer(text, state):
    options = []
    if text.startswith('--') or text.startswith('-'):
        options = [i for i in RECORD_ARGS if i.startswith(text)]
    elif text == 'add-' or text.startswith('add-'):
        options = [i for i in COMMANDS if i.startswith(text)]
    elif '-' in text:
        return None
    else:
        options = [i for i in COMMANDS if i.startswith(text)]

    try:
        return options[state]
    except IndexError:
        return None


gnureadline.set_completer(completer)
gnureadline.parse_and_bind("tab: complete")

commands = {
    "add": AddContactCommand(),
    "delete": RemoveContactCommand(),
    "edit": EditContactCommand(),
    "search": SearchContactsCommand(),
    "add-note": AddNoteCommand(),
    "edit-note": EditNoteCommand(),
    "remove-note": RemoveNoteCommand(),
    "get-notes": SearchNotesCommand(),
    "hello": HelloCommand(),
    "help": HelpCommand(),
}


def split_arguments(input_string):
    args = re.findall(
        r"(?:--[a-zA-Z-]+|-{1,2}[a-zA-Z]+|[^\s-]+(?:\s+[^\s-]+)*)", input_string
    )

    return args


def execute_console():
    address_book = AddressBook(
        storage=Storage(BINARY_STORAGE_FILENAME),
    )
    note_book = NoteBook(
        storage=Storage(BINARY_NOTEBOOK_STORAGE_FILENAME),
    )

    while True:
        user_input = split_arguments(input("Enter a command: "))
        command = user_input[0].strip().lower()
        args = user_input[1:]

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in commands:
            response = commands[command].executor(
                address_book, note_book, args)
            if response is not None:
                print(response)

        else:
            print("Invalid command.")


if __name__ == "__main__":
    execute_console()
