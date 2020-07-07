HIGHLIGHTS = ['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white']
HIGHLIGHTS = {v: i + 40 for i, v in enumerate(HIGHLIGHTS) if v}

COLORS = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
COLORS = {v: i + 30 for i, v in enumerate(COLORS) if v}

STYLES = ['bold', 'dark', '', 'underline', 'blink', '', 'reverse', 'concealed']
STYLES = {v: i + 1 for i, v in enumerate(STYLES) if v}
STYLES.update(HIGHLIGHTS)
STYLES.update(COLORS)

RESET = '\033[0m'


def colord(*args, color=None, on_color=None, styles=None, **kwargs):
    """
        color: int: use for format "\033[%sm", str: build-in-map, like 'red', 'green'
        on_color: same to color
        styles: list, same to color
    """
    styles = styles if styles else []
    prefix = "\033[%sm" % COLORS.get(color, color) if color else ''
    prefix += "\033[%sm" % HIGHLIGHTS.get(on_color, on_color) if on_color else ''
    for style in styles:
        prefix += "\033[%sm" % STYLES.get(style, style)

    if prefix:
        end = kwargs.pop('end') if 'end' in kwargs else '\n'
        print(prefix, end='')
        print(*args, **kwargs, end=RESET)
        print('', end=end)
    else:
        print(*args, **kwargs)


def grey(*args, **kwargs):
    colord(*args, color='grey', **kwargs)


def red(*args, **kwargs):
    colord(*args, color='red', **kwargs)


def green(*args, **kwargs):
    colord(*args, color='green', **kwargs)


def yellow(*args, **kwargs):
    colord(*args, color='yellow', **kwargs)


def blue(*args, **kwargs):
    colord(*args, color='blue', **kwargs)


def magenta(*args, **kwargs):
    colord(*args, color='magenta', **kwargs)


def cyan(*args, **kwargs):
    colord(*args, color='cyan', **kwargs)


def white(*args, **kwargs):
    colord(*args, color='white', **kwargs)


def info(*args, **kwargs):
    colord(*args, color='92', **kwargs)


def warning(*args, **kwargs):
    colord(*args, color='93', **kwargs)


def error(*args, **kwargs):
    colord(*args, color='91', **kwargs)
