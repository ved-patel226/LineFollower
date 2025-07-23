from servo import Servo
import time

servo = Servo(9)

try:
    while True:
        speed = input("Enter speed (0-180) ---> 90 stopped or 'exit' to stop: ")

        try:
            speed = int(speed)
            if speed < 0 or speed > 180:
                print("Speed must be between 0 and 180.")
                continue
            if speed == 90:
                servo.off()
                continue

            servo.write(speed)
        except:
            raise KeyboardInterrupt
except KeyboardInterrupt:
    servo.off()
    print("Program stopped by user.")
