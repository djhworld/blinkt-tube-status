#!/usr/bin/env python

import signal
import sys
import tubestatus
import datetime
from time import sleep, localtime, strftime
from blinkt import set_pixel, show, set_brightness

RED = (255, 0, 0, 0.4)
YELLOW = (255, 255, 0, 0.4)
GOOD_SERVICE = "Good Service"

# the config for the application, stores the colours
# used for each line and when those lines operate
# (night tube is coming soon!)
CONFIG = {
    "Bakerloo": {
        "led_no": 7,
        "colour": {
            "Good Service": (132, 40, 3),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Central": {
        "led_no": 6,
        "colour": {
            "Good Service": (90, 0, 0),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Circle": {
        "led_no": 5,
        "colour": {
            "Good Service": (120, 120, 0),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "District": {
        "led_no": 4,
        "colour": {
            "Good Service": (0, 50, 0),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Hammersmith and City": {
        "led_no": 3,
        "colour": {
            "Good Service": (255, 50, 50),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Jubilee": {
        "led_no": 2,
        "colour": {
            "Good Service": (6, 6, 6),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }

    },
    "Metropolitan": {
        "led_no": 1,
        "colour": {
            "Good Service": (30, 0, 10),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Northern": {
        "led_no": 0,
        "colour": {
            "Good Service": (100, 100, 100),
            "Severe Delays": RED,
            "Minor Delays": YELLOW
        },
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    }
}


def time_in_range(start, end, x):
    today = datetime.date.today()
    start = datetime.datetime.combine(today, start)
    end = datetime.datetime.combine(today, end)
    x = datetime.datetime.combine(today, x)
    if end <= start:
        end += datetime.timedelta(1)  # tomorrow!
    if x <= start:
        x += datetime.timedelta(1)  # tomorrow!
    return start <= x <= end


def turn_led_off_for(line):
    set_pixel(CONFIG[line]["led_no"], 0, 0, 0)


def clear(*args):
    for line, line_desc in CONFIG.iteritems():
        turn_led_off_for(line)
    show()
    sys.exit(0)


def set_led_status(line, line_ok):
    colours = line["colour"]
    led_no = line["led_no"]
    if line_ok:
        set_pixel(led_no, *colours[GOOD_SERVICE])
    else:
        # colour should be set to the colour of the status (if available)
        # otherwise change to RED
        status = line["status"]
        if status in colours:
            set_pixel(led_no, *colours[status])
        else:
            set_pixel(led_no, *RED)


def log(message):
    t = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print t + " - " + message
    sys.stdout.flush()


def line_is_open(line, current_time):
    return time_in_range(line["operating_hours"]["start"],
                         line["operating_hours"]["end"],
                         current_time)


# Update the status of each line
def update_line_statuses(tfl_status_obj):
    now = datetime.datetime.now().time()
    log("Updating statuses...")
    for line, line_desc in CONFIG.iteritems():
        if line_is_open(line_desc, now):
            line_desc["open"] = True
            try:
                line_desc["status"] = tfl_status_obj.get_status(line).description
                log(line + " line status = " + line_desc["status"])
            except:
                line_desc["status"] = "error"
                log(line + " [error] line status = " + line_desc["status"])
                sys.stdout.flush()
        else:
            log(line + " line is CLOSED")
            line_desc["open"] = False
            turn_led_off_for(line)


def main(brightness, update_interval, blink_rate=0.1):
    tfl_status_obj = tubestatus.Status()
    should_blink = True

    while True:
        update_line_statuses(tfl_status_obj)

        # update LEDS
        for x in range(0, int(update_interval/blink_rate), 1):
            set_brightness(brightness)
            for line, line_desc in CONFIG.iteritems():
                if line_desc["open"]:
                    if line_desc["status"] != GOOD_SERVICE:
                        set_led_status(line_desc, should_blink)
                    else:
                        set_led_status(line_desc, True)

            show()
            sleep(blink_rate)
            should_blink = not should_blink


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, clear)
    signal.signal(signal.SIGINT, clear)
    main(0.3, 120, 0.7)
