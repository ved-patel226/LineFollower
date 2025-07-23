from machine import Pin, PWM
import time

In1 = Pin(6, Pin.OUT)
In2 = Pin(7, Pin.OUT)
EN_A = PWM(Pin(8))

In3 = Pin(4, Pin.OUT)
In4 = Pin(3, Pin.OUT)
EN_B = PWM(Pin(2))

EN_A.freq(1000)
EN_B.freq(1000)

EN_A.duty_u16(65535)  # Full speed initially
EN_B.duty_u16(65535)  # Full speed initially


def set_motor_speed(speed_percent):
    """Set motor speed as percentage (0-100)"""
    if speed_percent < 0:
        speed_percent = 0
    elif speed_percent > 100:
        speed_percent = 100

    # Convert percentage to duty cycle (0-65535)
    duty_value = int((speed_percent / 100) * 65535)
    EN_A.duty_u16(duty_value)
    EN_B.duty_u16(duty_value)


def forward(speed=100):
    """Move forward at specified speed (0-100%)"""
    set_motor_speed(speed)
    In1.high()
    In2.low()
    In3.high()
    In4.low()


def backward(speed=100):
    """Move backward at specified speed (0-100%)"""
    set_motor_speed(speed)
    In1.low()
    In2.high()
    In3.low()
    In4.high()


def turn_left(speed=100):
    """Turn left by rotating motors in opposite directions"""
    set_motor_speed(speed)
    In1.low()  # Motor A backward
    In2.high()
    In3.high()  # Motor B forward
    In4.low()


def turn_right(speed=100):
    """Turn right by rotating motors in opposite directions"""
    set_motor_speed(speed)
    In1.high()  # Motor A forward
    In2.low()
    In3.low()  # Motor B backward
    In4.high()


def stop():
    """Stop all motors"""
    In1.low()
    In2.low()
    In3.low()
    In4.low()
    # Optionally set speed to 0
    set_motor_speed(0)


def main():
    try:
        # Gradually increase speed forward from 0% to 100%
        print("Linear forward acceleration 0% to 100%")
        for speed in range(0, 101, 1):
            forward(speed)
            print(f"Forward at {speed}% speed")
            time.sleep(0.1)
        stop()
        time.sleep(1)

        # Gradually decrease speed backward from 100% to 0%
        print("Linear backward deceleration 100% to 0%")
        for speed in range(100, -1, -5):
            backward(speed)
            print(f"Backward at {speed}% speed")
            time.sleep(0.1)
        stop()
        time.sleep(1)

    except KeyboardInterrupt:
        stop()
        print("Program stopped by user.")


if __name__ == "__main__":
    main()
