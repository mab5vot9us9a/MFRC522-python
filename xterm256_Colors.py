#!/usr/bin/env python3
# coding=utf-8


class tcolors:
    CYAN          = "\033[38;5;051m"
    BLUE          = "\033[38;5;021m"
    BLUE_BRIGHT   = "\033[38;5;111m"
    GREEN         = "\033[38;5;034m"
    GREEN_BRIGHT  = "\033[38;5;121m"
    RED           = "\033[38;5;196m"
    RED_BRIGHT    = "\033[38;5;173m"
    PURPLE        = "\033[38;5;127m"
    PURPLE_BRIGHT = "\033[38;5;140m"
    ORANGE        = "\033[38;5;208m"
    ORANGE_BRIGHT = "\033[38;5;215m"
    YELLOW        = "\033[38;5;220m"
    GRAY_50       = "\033[38;5;244m"
    GRAY_22       = "\033[38;5;251m"
    ENDC          = '\033[0m'
    BOLD          = '\033[1m'
    UNDERLINE     = '\033[4m'

if __name__ == '__main__':
    print(tcolors.BOLD + "{}Cyan".format(tcolors.CYAN))
