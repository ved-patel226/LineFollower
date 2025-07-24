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


def set_motor_speed(speed_percent, motor="both"):
    """Set motor speed as percentage (-100 to 100, negative = reverse)"""
    # Handle negative speeds for reverse direction
    abs_speed = abs(speed_percent)
    if abs_speed > 100:
        abs_speed = 100

    # Convert percentage to duty cycle (0-65535)
    duty_value = int((abs_speed / 100) * 65535)

    if motor == "both" or motor == "A":
        EN_A.duty_u16(duty_value)
        # Set direction based on sign
        if speed_percent >= 0:
            In1.low()
            In2.high()
        else:
            In1.high()
            In2.low()

    if motor == "both" or motor == "B":
        EN_B.duty_u16(duty_value)
        # Set direction based on sign
        if speed_percent >= 0:
            In3.low()
            In4.high()
        else:
            In3.high()
            In4.low()


# Input: 0-180 angle
# Output: motor speeds, clamped to 0-100%
def turn_at_angle(angle, speed=60):
    """Turn at a specified angle using differential steering"""
    if angle < 0 or angle > 180:
        raise ValueError("Angle must be between 0 and 180 degrees.")

    # Differential steering logic:
    # 0° = sharp left (A backward, B forward)
    # 90° = straight (both forward at same speed)
    # 180° = sharp right (A forward, B backward)

    if angle < 90:
        # Left turn: Motor A slower/reverse, Motor B faster
        ratio = angle / 90.0  # 0 to 1
        speed_a = speed * (2 * ratio - 1)  # -100 to 100
        speed_b = speed
    elif angle > 90:
        # Right turn: Motor A faster, Motor B slower/reverse
        ratio = (angle - 90) / 90.0  # 0 to 1
        speed_a = speed
        speed_b = speed * (1 - 2 * ratio)  # 100 to -100
    else:
        # Straight: both motors same speed
        speed_a = speed
        speed_b = speed

    set_motor_speed(speed_a, "A")
    set_motor_speed(speed_b, "B")


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

        for angle in range(0, 181, 5):
            print(f"Turning at angle: {angle}")
            turn_at_angle(angle)
            time.sleep(0.5)
        stop()

    except KeyboardInterrupt:
        stop()
        print("Program stopped by user.")


if __name__ == "__main__":
    main()
