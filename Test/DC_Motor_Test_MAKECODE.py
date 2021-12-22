"""
- The default speed & direction of motor is LOW & Forward
- r-run | s-stop | f-forward | b-backward | l-low | m-medium | h-high | e-exit
"""
######################################################################################################
import Jetson.GPIO as GPIO
import time

GPIO.setwarnings = False
######################################################################################################
# for 1st Motor on ENA
ENA, IN1, IN2, ENB, IN3, IN4 = 32, 36, 38, 33, 35, 37

# Set pin numbers to the board's
# Use the board pin diagram layout, the number we use are the number labeled in the silk screen
GPIO.setmode(GPIO.BOARD)





# TEST 1
def test_1():
    # initialize EnA, In1, In2, EnB, In3, In4
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

    # Stop
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)
    
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(1)

    # Forward
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(1)

    # Stop
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(1)

    # Backward
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(1)

    # Stop
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(1)

    GPIO.cleanup()

# TEST 2
def test_2():
    # Create PWM object: Pin & How fast to go
    PWMA = GPIO.PWM(channel=ENA, frequency_hz=1000)
    PWMB = GPIO.PWM(channel=ENB, frequency_hz=1000)
    # The percent duty cycle we want
    PWMA.start(duty_cycle_percent=25)
    PWMB.start(duty_cycle_percent=25)
######################################################################################################
def main():
    test_2()

if __name__ == '__main__':
    main()