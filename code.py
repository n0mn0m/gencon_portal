import board
from random import randint
from time import sleep
from analogio import AnalogIn
from adafruit_pyportal import PyPortal
from utils import countdown_formatter
from menu import render_menu, clear_menu, keep_alive, new_background, RETURN_MENU

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
buttons = render_menu(pyportal)

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
    if touch:
        for button in buttons:
            if button.contains(touch):
                if button.name == "exhibit_hall_map":
                    clear_menu(pyportal)
                    new_background(pyportal, "/images/2019-exhibit-map.bmp")
                    buttons = render_menu(pyportal, RETURN_MENU)
                    keep_alive(pyportal, buttons)
                    clear_menu(pyportal)
                    new_background(pyportal)
                    buttons = render_menu(pyportal)
                    break
                elif button.name == "con_map":
                    clear_menu(pyportal)
                    new_background(pyportal, "/images/2019-con-map.bmp")
                    buttons = render_menu(pyportal, RETURN_MENU)
                    keep_alive(pyportal, buttons)
                    clear_menu(pyportal)
                    new_background(pyportal)
                    buttons = render_menu(pyportal)
                    break
                elif button.name == "schedule":
                    clear_menu(pyportal)
                    new_background(pyportal, "/images/2019-schedule.bmp")
                    buttons = render_menu(pyportal, RETURN_MENU)
                    keep_alive(pyportal, buttons)
                    clear_menu(pyportal)
                    new_background(pyportal)
                    buttons = render_menu(pyportal)
                    break
                elif button.name == "d20":
                    roll = randint(1, 20)
                    clear_menu(pyportal)
                    new_background(pyportal, "/images/d20.bmp")
                    buttons = render_menu(
                        pyportal,
                        [
                            (
                                str(roll),
                                "return",
                                (138, 100),
                                (45, 45),
                                (255, 255, 255),
                                0xFFFFFF,
                                0x0,
                            )
                        ],
                    )
                    keep_alive(pyportal, buttons)
                    clear_menu(pyportal)
                    new_background(pyportal)
                    buttons = render_menu(pyportal)
                    break
                elif button.name == "countdown":
                    clear_menu(pyportal)
                    new_background(pyportal, "/images/gen-con-logo.bmp")
                    day = pyportal.fetch()
                    buttons = render_menu(
                        pyportal,
                        [
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
                    keep_alive(pyportal, buttons)
                    clear_menu(pyportal)
                    new_background(pyportal)
                    buttons = render_menu(pyportal)
                    break
                elif button.name == "badge":
                    clear_menu(pyportal)
                    new_background(pyportal, "/images/2019-con-badge.bmp")
                    buttons = render_menu(pyportal, RETURN_MENU)
                    keep_alive(pyportal, buttons)
                    clear_menu(pyportal)
                    new_background(pyportal)
                    buttons = render_menu(pyportal)
                    break
                else:
                    break
    sleep(0.5)
