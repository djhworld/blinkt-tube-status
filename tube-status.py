#!/usr/bin/env python

import signal
import sys
import tubestatus
from time import sleep, localtime, strftime
from blinkt import set_pixel, show, set_brightness

line_colors = {
    "Central": {
        "id": 0,
        "color": (100, 0, 0),
        "on": True
    },
    "Bakerloo": {
        "id": 1,
        "color": (132, 40, 3),
        "on": True
    },
    "Circle": {
        "id": 2,
        "color": (120, 120, 0),
        "on": True
    },
    "District": {
        "id": 3,
        "color": (0, 50, 0),
        "on": True
    },
    "Hammersmith and City": {
        "id": 4,
        "color": (255, 50, 50),
        "on": True
    },
    "Jubilee": {
        "id": 5,
        "color": (6, 6, 6),
        "on": True
    },
    "Metropolitan": {
        "id": 6,
        "color": (30, 0, 10),
        "on": True
    },
    "Northern": {
        "id": 7,
        "color": (0, 0, 0),
        "on": True
    }
}


def clear(*args):
    for line, line_desc in line_colors.iteritems():
        set_pixel(line_desc["id"], 0, 0, 0, 0)
        show()
    sys.exit(0)


def set_status(line, ok):
    if not ok:
        set_pixel(line_colors[line]["id"], 255, 0, 0)
        show()
    else:
        set_pixel(line_colors[line]["id"], *line_colors[line]["color"])
        show()


def log(message):
    t = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print t + " - " + message
    sys.stdout.flush()


def main(brightness, update_interval, blink_rate=0.1):
    set_brightness(brightness)
    tfl_status = tubestatus.Status()
    while True:
        log("Updating statuses...")
        for line, line_desc in line_colors.iteritems():
            try:
                line_desc["status"] = tfl_status.get_status(line).description
            except:
                line_desc["status"] = "error"
            log(line + " line status = " + line_desc["status"])
            sys.stdout.flush()

        for x in range(0, int(update_interval/blink_rate), 1):
            for line, line_desc in line_colors.iteritems():
                if line_desc["status"] != "Good Service":
                    if line_desc["on"]:
                        set_status(line, False)
                        line_desc["on"] = False
                    else:
                        set_status(line, True)
                        line_desc["on"] = True
                else:
                    set_status(line, True)
            sleep(blink_rate)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, clear)
    main(0.09, 120, 0.4)
