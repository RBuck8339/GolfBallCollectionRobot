import RPi.GPIO as GPIO
import time

LEFT_FORWARD_PIN = 22
LEFT_REVERSE_PIN = 23
RIGHT_FORWARD_PIN = 24
RIGHT_REVERSE_PIN = 25

ALL_PINS = (LEFT_FORWARD_PIN, LEFT_REVERSE_PIN, RIGHT_FORWARD_PIN, RIGHT_REVERSE_PIN)

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in ALL_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def _set_motors(lf, lr, rf, rr, duration_ms=None):
    GPIO.output(LEFT_FORWARD_PIN, lf)
    GPIO.output(LEFT_REVERSE_PIN, lr)
    GPIO.output(RIGHT_FORWARD_PIN, rf)
    GPIO.output(RIGHT_REVERSE_PIN, rr)

    if duration_ms is not None:
        time.sleep(duration_ms / 1000)
        stop()

def forward(duration_ms=None):
    _set_motors(1, 0, 1, 0, duration_ms)

def reverse(duration_ms=None):
    _set_motors(0, 1, 0, 1, duration_ms)

def turn_left(duration_ms=None):
    _set_motors(0, 1, 1, 0, duration_ms)

def turn_right(duration_ms=None):
    _set_motors(1, 0, 0, 1, duration_ms)

def stop(duration_ms=None):
    _set_motors(0, 0, 0, 0, duration_ms)

def cleanup():
    stop()
    GPIO.cleanup()
