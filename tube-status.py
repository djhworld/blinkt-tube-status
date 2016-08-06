#!/usr/bin/env python

import signal
import sys
import tubestatus
import datetime
from time import sleep, localtime, strftime
from blinkt import set_pixel, show, set_brightness

line_colors = {
    "Central": {
        "id": 0,
        "color": (100, 0, 0),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Bakerloo": {
        "id": 1,
        "color": (132, 40, 3),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Circle": {
        "id": 2,
        "color": (120, 120, 0),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "District": {
        "id": 3,
        "color": (0, 50, 0),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Hammersmith and City": {
        "id": 4,
        "color": (255, 50, 50),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Jubilee": {
        "id": 5,
        "color": (6, 6, 6),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }

    },
    "Metropolitan": {
        "id": 6,
        "color": (30, 0, 10),
        "on": True,
        "operating_hours": {
            "start": datetime.time(5, 0, 0),
            "end": datetime.time(1, 0, 0),
        }
    },
    "Northern": {
        "id": 7,
        "color": (0, 0, 0),
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
        set_pixel(line_desc["id"], 0, 0, 0, 0)
        show()
    sys.exit(0)


def turn_off(line):
    set_pixel(line_colors[line]["id"], 0, 0, 0)


def set_status(line, ok):
    if not ok:
        set_pixel(line_colors[line]["id"], 255, 255, 255)
    else:
        set_pixel(line_colors[line]["id"], *line_colors[line]["color"])


def log(message):
    t = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print t + " - " + message
    sys.stdout.flush()


def main(brightness, update_interval, blink_rate=0.1):
    set_brightness(brightness)
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
            for line, line_desc in line_colors.iteritems():
                if line_desc["available"]:
                    if line_desc["status"] != "Good Service":
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
