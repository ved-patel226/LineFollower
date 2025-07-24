from machine import Pin
import time
from motors import turn_at_angle, stop
import socket
import network


def start_web_server():
    try:
        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        ip = wlan.ifconfig()[0]
        print(f"Web server running on http://{ip}:80/")

        while True:
            cl, addr = s.accept()
            cl_file = cl.makefile("rwb", 0)
            request = cl_file.readline()
            response = """\
    HTTP/1.0 200 OK

    <html>
    <head><title>Hello</title></head>
    <body><h1>Hello World</h1></body>
    </html>
    """
            cl.send(response)
            cl.close()
    except Exception as e:
        print(f"Error starting web server: {e}")
        stop()


# Uncomment below to start the web server
start_web_server()
# Define sensor pins
L = Pin(18, Pin.IN)  # Left sensor
M = Pin(19, Pin.IN)  # Middle sensor
R = Pin(20, Pin.IN)  # Right sensor

# Line following parameters
BASE_SPEED = 80  # Base speed for motors (0-100%)
TURN_SPEED = 70  # Speed when turning
SEARCH_SPEED = 60  # Speed when searching for line


def read_sensors():
    """Read all three sensors and return as tuple"""
    return (L.value(), M.value(), R.value())


def line_follow():
    """Main line following algorithm using differential steering"""
    left, middle, right = read_sensors()

    # Line following logic based on sensor combinations
    # Assuming 0 = line detected, 1 = no line (adjust if opposite)

    if middle == 0:  # Line under middle sensor
        if left == 0 and right == 0:
            # All sensors on line - move straight
            turn_at_angle(90, BASE_SPEED)  # Straight ahead
            return "STRAIGHT - All on line"
        elif left == 0:
            # Left and middle on line - slight right turn
            turn_at_angle(115, TURN_SPEED)  # Slight right
            return "SLIGHT RIGHT"
        elif right == 0:
            # Right and middle on line - slight left turn
            turn_at_angle(65, TURN_SPEED)  # Slight left
            return "SLIGHT LEFT"
        else:
            turn_at_angle(90, BASE_SPEED)  # Straight ahead
            return "STRAIGHT - Middle only"

    elif left == 0:  # Only left sensor on line
        # Sharp right turn to get back on line
        turn_at_angle(180, TURN_SPEED)  # Turn right
        return "SHARP RIGHT"

    elif right == 0:  # Only right sensor on line
        # Sharp left turn to get back on line
        turn_at_angle(0, TURN_SPEED)  # Turn left
        return "SHARP LEFT"

    else:  # No sensors on line - search pattern
        # Move forward slowly to find line
        turn_at_angle(90, SEARCH_SPEED)  # Search forward
        return "SEARCHING"


def main():
    """Main line following program"""
    print("Starting line following robot...")
    print("Sensor layout: L=Left, M=Middle, R=Right")
    print("Press Ctrl+C to stop")

    try:
        while True:
            # Read sensors
            left, middle, right = read_sensors()

            # Execute line following algorithm
            action = line_follow()

            # Print status (optional - remove for better performance)
            print(f"L:{left} M:{middle} R:{right} -> {action}")

            # Small delay to prevent overwhelming the system
            time.sleep(0.05)  # 50ms delay

    except KeyboardInterrupt:
        stop()
        print("\nProgram stopped by user.")
        print("Robot stopped.")


if __name__ == "__main__":
    main()
