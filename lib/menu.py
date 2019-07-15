from time import sleep
from utils import collect
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font


# Load the font at the beginning for use across the application.
FONT = bitmap_font.load_font("/fonts/Arial-Bold-12.bdf")

# label, name, pos, size, fill_color, outline_color, label_color
RETURN_MENU = [("<  ", "return", (285, 205), (30, 30), (255, 170, 0), 0x222222, 0x0)]


def _home_menu():
    """
    Return the structure for the Gen Con badge home menu.

    See the render_menu function docs for more information on the expected structure
    for a menu object.
    """
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
def _clear_menu(portal):
    """
    Remove the buttons that have been added to the portal splash object. This should
    be done when transitioning from one menu to another, for instance the home
    menu to a screen with the return menu.
    """
    items = len(portal.splash) - 1

    if items >= 1:
        for i in range(items):
            portal.splash.pop()


@collect
def _set_new_background(portal, img_or_color=0xFFFFFF):
    """
    Set a new background on the PyPortal and perform garbage collection to remove
    references to open resources such as images that can have a large impact on
    memory use.
    """
    portal.set_background(img_or_color)
    del img_or_color


@collect
def _keep_alive(portal, buttons):
    """
    After transitioning to a new screen we want to stay on that screen
    until the user selects a new screen to transition to.
    """
    stay = True

    while stay:
        touch = portal.touchscreen.touch_point
        if touch:
            for button in buttons:
                if button.name == "return":
                    _clear_menu(portal)
                    stay = False
                    break

        sleep(0.5)


@collect
def _render_menu(portal, menu):
    """
    Provided a new menu render that menu on screen.

    The menu object is a list of tuples.

    The tuple layout is (label, name, pos, size, fill_color, outline_color, label_color)
    """
    buttons = []

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


@collect
def new_screen(portal, new_background=0xFFFFFF, menu=None):
    """
    This function manages transitioning from one screen to another. In the scope of
    this project it specifically handles transitioning from the home screen/menu
    to a new screen and back.

    This function is almost a mini FSM, but doesn't maintain a lot of state since
    for the Gen Con portal badge the state is either Home Menu, or a menu item screen
    that only allows you to return to the home menu.

    If the menu object is provided it needs to be compatible with the _render_menu
    function which expects a menu to represented by the following data structure format:

    [
        (label, name, pos, size, fill_color, outline_color, label_color),
    ]

    With N tuples allowed although menus with more than 6 buttons or extremely
    large buttons in quantities greater than 4 may provde unstable.
    """

    # If we are not given a new menu assume we are transitioning back to the home menu
    # which is the default menu for this project.
    if not menu:
        menu = _home_menu()

    # Begin transition to the menu item screen.
    _clear_menu(portal)
    _set_new_background(portal, new_background)

    # Capture the new menu buttons so we can wait for the next button event indicating
    # the next transition back to the home screen.
    buttons = _render_menu(portal, menu)
    _keep_alive(portal, buttons)

    # Begin transition back to home
    _clear_menu(portal)
    _set_new_background(portal)

    # Return the new buttons to the super loop to monitor for the next event on the
    # home menu.
    buttons = _render_menu(portal, _home_menu())
    return buttons


@collect
def init_home_screen(portal):
    """
    When the device first starts we need to load the home menu for the first time, but
    then return control to let the super loop takeover.
    """
    menu = _home_menu()
    buttons = _render_menu(portal, menu)
    return buttons
