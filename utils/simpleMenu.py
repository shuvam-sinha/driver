#!/usr/bin/env python3

from simple_term_menu import TerminalMenu


def getOption():
    options = ["[a] Previous Day", "[b] Previous Week", "[c] Previous Month", "[d] Previous Year", "[e] All time", "[x] Exit"]
    terminal_menu = TerminalMenu(options, title="Select a time range for metrics")
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]


if __name__ == "__main__":
    isRun = True
    while isRun:
      myOption = getOption()
      print(f"You have selected {myOption}!")
      if myOption == "[x] Exit":
        isRun = False

