import picamera
import time
import Adafruit_DHT
import datetime # python date module
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT) # LED1 B
GPIO.setup(22,GPIO.OUT) # LED2 B
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP)  # BUTTON
GPIO.setup(24,GPIO.IN) # PIR
GPIO.setup(25,GPIO.IN) # BUZZER
GPIO.setup(25,GPIO.OUT) # BUZZER
lcd = CharLCD("PCF8574",0x27)
camera = picamera.PiCamera()
camera.resolution = (2592,1944)
intrusion_control = 0
timer = 0
dht_type = 11 # DHT Type
bcm_pin = 23 #PIN Number

def blink_off(): # blink off function
	GPIO.output(21,False)
	GPIO.output(22,False)

def buzz():
	pitch = 1000
	duration = 0.1
	period = 1.0 / pitch
	delay = period /2
	cycles = int(duration * pitch)
	for i in range(cycles):
		GPIO.output(25,True)
		time.sleep(delay)
		GPIO.output(25,False)
		time.sleep(delay)

try:
	while True:
		if GPIO.input(24)==True:
			print("SENSOR ON!!")
			while True:
				print("Motion detection - LED on and Buzzer on")
				GPIO.output(21,True)
				GPIO.output(22,False)
				time.sleep(0.5)
				GPIO.output(21,False)
				GPIO.output(22,True)
				buzz()
				time.sleep(0.5)
				if intrusion_control == 0:   # Motion detect -> Turn on LCD and Take a  Photo at once.
					lcd.clear()
					lcd.write_string("Motion Detected!")
					lcd.crlf()
					lcd.write_string("Emergency")
					print("Taking a photo")
					camera.capture("theft.jpg")
					intrusion_control +=1
				if GPIO.input(12) == False:
					print("Button pressed - off")
					lcd.clear()
					blink_off()
					intrusion_control = 0;
					time.sleep(2)
					break
				time.sleep(0.3)
		else:
			GPIO.output(25,False)
			GPIO.output(21,False)
			GPIO.output(22,False)
			if timer>3 : # check temperature& time at every 3 seconds
				timer=0
				lcd.clear()
				now = datetime.datetime.now() # current time
				nowTime = now.strftime('%H-%M:%S') # current time parsing
				humidity, temperature = Adafruit_DHT.read_retry(dht_type,bcm_pin)
				temp = round(temperature,1)
				print("Now: ",now)
				print("Now Time: ",nowTime)
				print("Temperature: ",temp)
				lcd.write_string("TIME: ")
				lcd.write_string(nowTime)
				lcd.crlf()
				lcd.write_string("TEMP: ")
				lcd.write_string(str(temp))
				lcd.write_string("C")
			timer +=0.3
			time.sleep(0.3)

except KeyboardInterrupt:
	lcd.clear()
	GPIO.cleanup()

finally:
	GPIO.cleanup()

