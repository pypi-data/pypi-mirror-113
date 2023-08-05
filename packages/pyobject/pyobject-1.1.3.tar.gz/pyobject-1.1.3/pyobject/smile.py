# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2rc1 (tags/v3.7.2rc1:75a402a217, Dec 11 2018, 22:09:03) [MSC v.1916 32 bit (Intel)]
# Embedded file name: smile.pyc
import sys, os, random, time
try:
    import console_tool
except ImportError:
    console_tool = None

from random import choice
SCREEN_SIZE = 39
COLORS = '123456777789ABCDEF'
BACKCOLORS = '0012'
SECS = [0.4] * 10 + [0] * 250
big_smileicon = '\n                     \x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01                                        \n                  \x01                      \x01                                     \n                 \x01                        \x01                                    \n                \x01                          \x01                                   \n               \x01        \x01         \x01         \x01                                  \n               \x01                            \x01                                  \n               \x01                            \x01                                  \n               \x01                            \x01                                  \n               \x01                            \x01                                  \n               \x01                            \x01                                  \n               \x01                            \x01                                  \n               \x01                            \x01                                  \n               \x01        \x01         \x01         \x01                                  \n               \x01         \x01\x01\x01\x01\x01\x01\x01\x01\x01          \x01                                  \n                \x01                          \x01                                   \n                 \x01                        \x01                                    \n                  \x01                      \x01                                     \n                    \x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01                                       \n\n'

def change_color():
    arg = random.choice(COLORS) + random.choice(BACKCOLORS)
    os.system('color ' + arg)


def smile():
    for second in SECS:
        print('\x01 \x02 ' * (SCREEN_SIZE // 2) + '\x01')
        change_color()
        time.sleep(second)


def colorful_smile(consolescreen):
    for second in SECS:
        consolescreen.ctext(('\x01 \x02' * int(SCREEN_SIZE / 1.5) + '  '), (choice(console_tool.RAINBOW)), (choice(console_tool.RAINBOW)),
          reset=False, end='')
        time.sleep(second)


def big_smile(consolescreen):
    count = 0
    rainbow = console_tool.RAINBOW[:-1]
    for line in big_smileicon.splitlines():
        color = rainbow[count]
        consolescreen.ctext(line, 'white', color)
        count += 1
        if count >= len(rainbow):
            count = 0
        time.sleep(0.04)


def main():
    big = '--small' not in sys.argv
    small = '--big' not in sys.argv
    classic = '--classic' in sys.argv
    if console_tool:
        c = console_tool.Console()
        c.colorize(stdout=None)
    else:
        c=None
    try:
        if small:
            if c:
                classic or colorful_smile(c)
            else:
                smile()
        if big:
            for i in range(4):
                big_smile(c)

    except KeyboardInterrupt:
        print(('{:-^80}'.format('BYE!')), file=(sys.stderr))
        os.system('color')


if __name__ == '__main__':
    main()
# okay decompiling D:\IT\python\pyobject\smile.pyc
