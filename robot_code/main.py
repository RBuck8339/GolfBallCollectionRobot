import time
from enum import Enum

import motor_control
import perception

SEARCH_DURATION_S   = 10
ROTATE_INTERVAL_MS  = 1000
PERCEIVE_INTERVAL_S = 1.0

TURN_RATE_DEG_PER_SEC = 90.0
DRIVE_SPEED_M_PER_SEC = 0.5
COLLECT_CLEARANCE_M   = 0.4
ROTATE_180_MS         = 1000
REVERSE_MS            = 1000

ALIGN_TOLERANCE_DEG = 5.0
MAX_ALIGN_ATTEMPTS  = 5
DRIVE_STEP_MS       = 1000

SLEEP_DURATION_S = 20

class State(Enum):
    SEARCH  = 'search'
    ALIGN   = 'align'
    DRIVE   = 'drive'
    COLLECT = 'collect'
    SLEEP   = 'sleep'

def search_for_ball():
    elapsed = 0.0

    while elapsed < SEARCH_DURATION_S:
        motor_control.turn_right(ROTATE_INTERVAL_MS)
        elapsed += ROTATE_INTERVAL_MS / 1000

        deadline = time.time() + PERCEIVE_INTERVAL_S
        while time.time() < deadline:
            frame = perception.get_frame()
            if frame is None:
                continue
            target = perception.get_target(frame)
            if target is not None:
                return target
        elapsed += PERCEIVE_INTERVAL_S

    return None


def align_with_target(target):
    for _ in range(MAX_ALIGN_ATTEMPTS):
        angle = target['angle_deg']
        if abs(angle) <= ALIGN_TOLERANCE_DEG:
            break

        turn_ms = int(abs(angle) / TURN_RATE_DEG_PER_SEC * 1000)
        if angle > 0:
            motor_control.turn_right(turn_ms)
        else:
            motor_control.turn_left(turn_ms)

        frame = perception.get_frame()
        if frame is None:
            break
        fresh = perception.get_target(frame)
        if fresh is None:
            break
        target = fresh
        print(f"  Alignment check: {target['angle_deg']:.1f}°")

    return target

def drive_to_target(target):
    while True:
        dist = target['distance_m'] - COLLECT_CLEARANCE_M
        if dist <= 0:
            break

        step_dist = min(DRIVE_SPEED_M_PER_SEC * (DRIVE_STEP_MS / 1000), dist)
        step_ms   = int(step_dist / DRIVE_SPEED_M_PER_SEC * 1000)
        motor_control.forward(step_ms)

        frame = perception.get_frame()
        if frame is None:
            break
        fresh = perception.get_target(frame)
        if fresh is None:
            break
        target = fresh
        print(f"  Step complete: angle={target['angle_deg']:.1f}  distance={target['distance_m']:.2f}m")

        if abs(target['angle_deg']) > ALIGN_TOLERANCE_DEG:
            print(f"  Drift detected ({target['angle_deg']:.1f}), re-aligning...")
            target = align_with_target(target)

    return target

def collect_ball():
    motor_control.turn_right(ROTATE_180_MS)
    motor_control.reverse(REVERSE_MS)

def main():
    motor_control.setup()
    perception.setup()

    state  = State.SEARCH
    target = None

    print("Golf ball collection robot started.")

    try:
        while True:
            if state == State.SEARCH:
                print("Searching for ball...")
                target = search_for_ball()
                if target is not None:
                    print(f"Ball found — angle={target['angle_deg']:.1f}°  distance={target['distance_m']:.2f}m")
                    state = State.ALIGN
                else:
                    print("No ball found. Sleeping before next search.")
                    state = State.SLEEP

            elif state == State.ALIGN:
                print(f"Aligning to {target['angle_deg']:.1f}°...")
                target = align_with_target(target)
                state = State.DRIVE

            elif state == State.DRIVE:
                print(f"Driving to target ({target['distance_m']:.2f}m away)...")
                target = drive_to_target(target)
                state = State.COLLECT

            elif state == State.COLLECT:
                print("Collecting ball...")
                collect_ball()
                print("Collection attempt complete.")
                state = State.SEARCH

            elif state == State.SLEEP:
                print(f"Sleeping {SLEEP_DURATION_S}s...")
                time.sleep(SLEEP_DURATION_S)
                state = State.SEARCH

    finally:
        motor_control.cleanup()
        perception.cleanup()

if __name__ == "__main__":
    main()
