#!/usr/bin/env python

import signal
import sys
import tubestatus
import datetime
from time import sleep, localtime, strftime
from blinkt import set_pixel, show, set_brightness

RED = (255, 0, 0, 0.6)
GOOD_SERVICE = "Good Service"

line_colors = {
    "Central": {
        "id": 0,
        "color": {
            "on": (90, 0, 0),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Bakerloo": {
        "id": 1,
        "color": {
            "on": (132, 40, 3),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Circle": {
        "id": 2,
        "color": {
            "on": (120, 120, 0),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "District": {
        "id": 3,
        "color": {
            "on": (0, 50, 0),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Hammersmith and City": {
        "id": 4,
        "color": {
            "on": (255, 50, 50),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Jubilee": {
        "id": 5,
        "color": {
            "on": (6, 6, 6),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }

    },
    "Metropolitan": {
        "id": 6,
        "color": {
            "on": (30, 0, 10),
            "off": RED
        },
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Northern": {
        "id": 7,
        "color": {
            "on": (100, 100, 100),
            "off": RED,
        },
        "on": True,
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


def clear(*args):
    for line, line_desc in line_colors.iteritems():
        turn_off(line)
        show()
    sys.exit(0)


def turn_off(line):
    set_pixel(line_colors[line]["id"], 0, 0, 0)


def set_status(line, ok):
    if not ok:
        set_pixel(line_colors[line]["id"], *line_colors[line]["color"]["off"])
    else:
        set_pixel(line_colors[line]["id"], *line_colors[line]["color"]["on"])


def log(message):
    t = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print t + " - " + message
    sys.stdout.flush()


def main(brightness, update_interval, blink_rate=0.1):
    tfl_status = tubestatus.Status()
    while True:
        now = datetime.datetime.now().time()
        log("Updating statuses...")
        for line, line_desc in line_colors.iteritems():
            if time_in_range(line_desc["operating_hours"]["start"],
                             line_desc["operating_hours"]["end"],
                             now):
                try:
                    line_desc["status"] = tfl_status.get_status(line).description
                    line_desc["available"] = True
                except:
                    line_desc["status"] = "error"
                log(line + " line status = " + line_desc["status"])
                sys.stdout.flush()
            else:
                log(line + " line is CLOSED")
                turn_off(line)
                line_desc["available"] = False

        for x in range(0, int(update_interval/blink_rate), 1):
            set_brightness(brightness)
            for line, line_desc in line_colors.iteritems():
                if line_desc["available"]:
                    if line_desc["status"] != GOOD_SERVICE:
                        if line_desc["on"]:
                            set_status(line, False)
                            line_desc["on"] = False
                        else:
                            set_status(line, True)
                            line_desc["on"] = True
                    else:
                        set_status(line, True)

            show()
            sleep(blink_rate)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, clear)
    main(0.2, 120, 0.7)
