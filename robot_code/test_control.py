import select
import sys
import termios
import tty

import motor_control

KEY_TIMEOUT_S = 0.05

def _get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ready, _, _ = select.select([sys.stdin], [], [], KEY_TIMEOUT_S)
        return sys.stdin.read(1) if ready else None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    motor_control.setup()

    try:
        while True:
            key = _get_key()

            if key is None:
                motor_control.stop()
                continue

            key = key.lower()

            if key == 'w':
                print("Forward")
                motor_control.forward()
            elif key == 'a':
                print("Turn Left")
                motor_control.turn_left()
            elif key == 's':
                print("Reverse")
                motor_control.reverse()
            elif key == 'd':
                print("Turn Right")
                motor_control.turn_right()
            elif key in ('q', '\x03'):
                break
            else:
                motor_control.stop()

    finally:
        motor_control.cleanup()
        print("Remote control stopped.")

if __name__ == "__main__":
    main()
