import gc


def collect(func):
    """
    For potentially expensive operations perform a garbage collection cycle before
    and after the operation.
    """

    def collect_before_and_after(*args, **kwargs):
        gc.collect()
        val = func(*args, **kwargs)
        gc.collect()
        return val

    return collect_before_and_after


def countdown_formatter(days):
    """
    Given we know what day Gen Con is occuring on do some math
    and format the string to provide a count down of days until
    Gen Con.
    """
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
