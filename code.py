import board
from random import randint
from gc import collect
from time import sleep
from analogio import AnalogIn
from adafruit_pyportal import PyPortal
from menu import render_menu, clear_menu, keep_alive, reset_display
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

def countdown_formatter(days):
    gen_con_day_of_year = 211

    count = gen_con_day_of_year - days
    if count > 0:
        format_str = "{:,d} Days till Gen Con!".format(count)
    elif count == 0:
        format_str = "Gen Con is here!"
    elif count == -1:
        format_str = "3 more days of Gen Con!"
    elif count == -2:
        format_str = "2 more days of Gen Con!"
    elif count == -3:
        format_str = "1 more day of Gen Con!"
    elif count == -4:
        format_str = "Last day of Gen Con :("
    elif count >= -5:
        format_str = "See you in 2020"

    return format_str

# label, name, pos, size, color
RETURN_MENU = [
    ("<  ","return",(285, 205),(30, 30),),
]


# Setup light sensor.
light_sensor = AnalogIn(board.LIGHT)
mode = 0
mode_change = None
initial_light_value = light_sensor.value

# Setup portal with time feed.
pyportal = PyPortal(url="http://worldtimeapi.org/api/timezone/America/Indiana/Indianapolis",
                                      json_path=["day_of_year"],
                                      default_bg=0xffffff,
                                      )
pyportal.preload_font()

# Render default home menu
buttons = render_menu(pyportal)

try:
    while True:
        # Calibrate light sensor on start to deal with different lighting situations
        # If the mode change isn't responding properly, reset your PyPortal to recalibrate
        collect()

        if light_sensor.value < (initial_light_value * 0.3) and mode_change is None:
            mode_change = "mode_change"
        if light_sensor.value > (initial_light_value * 0.5) and mode_change == "mode_change":
            mode += 1
            mode_change = None
            if mode > 2:
                mode = 0

        touch = pyportal.touchscreen.touch_point
        if touch:
            for button in buttons:
                if button.contains(touch):
                    if button.name == "exhibit_hall_map":
                        img = "/images/2019-exhibit-map.bmp"
                        clear_menu(pyportal)
                        collect()
                        pyportal.set_background(img)
                        buttons = render_menu(pyportal, RETURN_MENU)
                        keep_alive(pyportal, buttons)
                        clear_menu(pyportal)
                        del(img)
                        collect()
                        buttons = render_menu(pyportal)
                        break
                    elif button.name == "con_map":
                        img = "/images/2019-con-map.bmp"
                        clear_menu(pyportal)
                        collect()
                        pyportal.set_background(img)
                        buttons = render_menu(pyportal, RETURN_MENU)
                        keep_alive(pyportal, buttons)
                        clear_menu(pyportal)
                        del(img)
                        collect()
                        buttons = render_menu(pyportal)
                        break
                    elif button.name == "schedule":
                        img = "/images/2019-schedule.bmp"
                        clear_menu(pyportal)
                        collect()
                        pyportal.set_background(img)
                        buttons = render_menu(pyportal, RETURN_MENU)
                        keep_alive(pyportal, buttons)
                        clear_menu(pyportal)
                        del(img)
                        collect()
                        buttons = render_menu(pyportal)
                        break
                    elif button.name == "d20":
                        clear_menu(pyportal)
                        collect()
                        img = "/images/d20.bmp"
                        roll = randint(1, 20)
                        pyportal.set_background(img)
                        buttons = render_menu(pyportal,
                                              [(str(roll),"return",(138, 100),(45, 45))],
                                              (255, 255, 255),
                                              0xffffff)
                        keep_alive(pyportal, buttons)
                        clear_menu(pyportal)
                        del(img)
                        collect()
                        buttons = render_menu(pyportal)
                        break
                    elif button.name == "countdown":
                        img = "/images/gen-con-logo.bmp"
                        clear_menu(pyportal)
                        collect()
                        pyportal.set_background(img)
                        day = pyportal.fetch()
                        buttons = render_menu(pyportal,
                                              [(countdown_formatter(day),"return",(40, 200),(240, 40))],
                                              (0, 0, 0),
                                              0x0,
                                              0xffffff)
                        keep_alive(pyportal, buttons)
                        clear_menu(pyportal)
                        del(img)
                        collect()
                        buttons = render_menu(pyportal)
                        break
                    elif button.name == "badge":
                        img = "/images/2019-con-badge.bmp"
                        clear_menu(pyportal)
                        collect()
                        pyportal.set_background(img)
                        buttons = render_menu(pyportal, RETURN_MENU)
                        keep_alive(pyportal, buttons)
                        clear_menu(pyportal)
                        del(img)
                        collect()
                        buttons = render_menu(pyportal)
                        break
                    else:
                        break
        sleep(0.5)

except MemoryError:
    exit()
