from time import sleep
from utils import collect
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font


FONT = bitmap_font.load_font("/fonts/Arial-Bold-12.bdf")

# label, name, pos, size, fill_color, outline_color, label_color
RETURN_MENU = [("<  ", "return", (285, 205), (30, 30), (255, 170, 0), 0x222222, 0x0)]


def default_menu():
    # label, name, pos, size, fill_color, outline_color, label_color
    return [
        ("Badge", "badge", (5, 35), (150, 50), (255, 170, 0), 0x222222, 0x0),
        ("Countdown", "countdown", (5, 95), (150, 50), (255, 170, 0), 0x222222, 0x0),
        ("Roll 20!", "d20", (5, 155), (150, 50), (255, 170, 0), 0x222222, 0x0),
        ("Schedule", "schedule", (165, 35), (150, 50), (255, 170, 0), 0x222222, 0x0),
        (
            "Exhibit Map",
            "exhibit_hall_map",
            (165, 95),
            (150, 50),
            (255, 170, 0),
            0x222222,
            0x0,
        ),
        ("Con Map", "con_map", (165, 155), (150, 50), (255, 170, 0), 0x222222, 0x0),
    ]


@collect
def clear_menu(portal):
    items = len(portal.splash) - 1

    if items >= 1:
        for i in range(items):
            portal.splash.pop()


@collect
def new_background(portal, img_or_color=0xFFFFFF):
    portal.set_background(img_or_color)
    del img_or_color


@collect
def keep_alive(portal, buttons):
    stay = True

    while stay:
        touch = portal.touchscreen.touch_point
        if touch:
            for button in buttons:
                if button.name == "return":
                    clear_menu(portal)
                    stay = False
                    break

        sleep(0.5)


@collect
def render_menu(portal, menu=None):
    buttons = []

    if not menu:
        menu = default_menu()

    for item in menu:
        button = Button(
            x=item[2][0],
            y=item[2][1],
            width=item[3][0],
            height=item[3][1],
            name=item[1],
            style=Button.SHADOWROUNDRECT,
            fill_color=item[4],
            outline_color=item[5],
            label=item[0],
            label_font=FONT,
            label_color=item[6],
        )
        portal.splash.append(button.group)
        buttons.append(button)

    return buttons
