from machine import Pin

# from motors import forward, backward, turn_left, turn_right

# Define sensor pins
L = Pin(18, Pin.IN)
M = Pin(19, Pin.IN)
R = Pin(20, Pin.IN)

prev_values = [0, 0, 0]

try:
    while True:
        if [L.value(), M.value(), R.value()] != prev_values:
            prev_values = [L.value(), M.value(), R.value()]
            print("L:", L.value(), "M:", M.value(), "R:", R.value())


except KeyboardInterrupt:
    print("Program stopped by user.")
