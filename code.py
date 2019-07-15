"""
Main module for the Gen Con 2019 PyPortal badge.

Setup the PyPortal with a connection to a time api for the countdown clock functionality
and then monitor for button events and route to the menu.py module.

For more information about the PyPortal see https://learn.adafruit.com/adafruit-pyportal
"""
import board
from random import randint
from time import sleep
from analogio import AnalogIn
from adafruit_pyportal import PyPortal
from utils import countdown_formatter
from menu import new_screen, init_home_screen, RETURN_MENU

try:
    from secrets import secrets  # noqa
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Setup light sensor.
light_sensor = AnalogIn(board.LIGHT)
mode = 0
mode_change = None
initial_light_value = light_sensor.value

# Setup portal with time feed.
pyportal = PyPortal(
    url="http://worldtimeapi.org/api/timezone/America/Indiana/Indianapolis",
    json_path=["day_of_year"],
    default_bg=0xFFFFFF,
)
pyportal.preload_font()

# Render default home menu
buttons = init_home_screen(pyportal)

# Setup our super loop to manage screen brightness and monitor our home menu for
# button events.
while True:
    # Calibrate light sensor on start to deal with different lighting situations
    # If the mode change isn't responding properly, reset your PyPortal to recalibrate
    if light_sensor.value < (initial_light_value * 0.3) and mode_change is None:
        mode_change = "mode_change"
    if (
        light_sensor.value > (initial_light_value * 0.5)
        and mode_change == "mode_change"
    ):
        mode += 1
        mode_change = None
        if mode > 2:
            mode = 0

    touch = pyportal.touchscreen.touch_point
    # In the case of a button event figure out which button was pressed and render
    # that buttons screen.
    if touch:
        for button in buttons:
            if button.contains(touch):
                if button.name == "exhibit_hall_map":
                    buttons = new_screen(
                        pyportal,
                        new_background="/images/2019-exhibit-map.bmp",
                        menu=RETURN_MENU,
                    )
                    break
                elif button.name == "con_map":
                    buttons = new_screen(
                        pyportal,
                        new_background="/images/2019-con-map.bmp",
                        menu=RETURN_MENU,
                    )
                    break
                elif button.name == "schedule":
                    buttons = new_screen(
                        pyportal,
                        new_background="/images/2019-schedule.bmp",
                        menu=RETURN_MENU,
                    )
                    break
                elif button.name == "d20":
                    buttons = new_screen(
                        pyportal,
                        new_background="/images/d20.bmp",
                        menu=[
                            (
                                str(randint(1, 20)),
                                "return",
                                (138, 100),
                                (45, 45),
                                (255, 255, 255),
                                0xFFFFFF,
                                0x0,
                            )
                        ],
                    )
                    break
                elif button.name == "countdown":
                    day = pyportal.fetch()
                    buttons = new_screen(
                        pyportal,
                        new_background="/images/gen-con-logo.bmp",
                        menu=[
                            (
                                countdown_formatter(day),
                                "return",
                                (40, 200),
                                (240, 40),
                                (0, 0, 0),
                                0x0,
                                0xFFFFFF,
                            )
                        ],
                    )
                    break
                elif button.name == "badge":
                    buttons = new_screen(
                        pyportal,
                        new_background="/images/2019-con-badge.bmp",
                        menu=RETURN_MENU,
                    )
                    break
                else:
                    break
    sleep(0.5)
