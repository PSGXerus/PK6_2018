import RPi.GPIO as GPIO
import time

#Pin Belegung
tasterPin1 = 11
tasterPin2 = 13
tasterPin3 = 15  #Taster vom Drehgeber
drehgeberPin1 = 16
drehgeberPin2 = 18

#Board Modus (Alternativ GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

#Pin Setup als Eingaenge
GPIO.setup(tasterPin1, GPIO.IN)
GPIO.setup(tasterPin2, GPIO.IN)
GPIO.setup(tasterPin3, GPIO.IN)
GPIO.setup(drehgeberPin1, GPIO.IN)
GPIO.setup(drehgeberPin2, GPIO.IN)

value = GPIO.input(tasterPin1)
oldValue = 0
counter = 0

#Konstanten
DIR_NONE = 0x0
DIR_CW = 0x10
DIR_CCW = 0x20

R_START = 0x0
R_CW_FINAL = 0x1
R_CW_BEGIN = 0x2
R_CW_NEXT = 0x3
R_CCW_BEGIN = 0x4
R_CCW_FINAL = 0x5
R_CCW_NEXT = 0x6

#Full Table Deklaration
ttable = [[R_START, R_CW_BEGIN, R_CCW_BEGIN, R_START],
         [R_CW_NEXT, R_START, R_CW_FINAL, R_START|DIR_CW],
         [R_CW_NEXT, R_CW_BEGIN, R_START, R_START],
         [R_CW_NEXT, R_CW_BEGIN, R_CW_FINAL, R_START],
         [R_CCW_NEXT, R_START, R_CCW_BEGIN, R_START],
         [R_CCW_NEXT, R_CCW_FINAL, R_START, R_START|DIR_CCW],
         [R_CCW_NEXT, R_CCW_FINAL, R_CCW_BEGIN, R_START]]

#State Vorinitialisieren
state = R_START

def call1(channel):
    global counter
    counter = counter +1
    print (counter)

def call2(channel):
    global counter
    counter = counter -1
    print (counter)

def call3(channel):
    global counter
    counter = 0
    print (counter)


def call4(channel):
    global state
    pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
    state = ttable[state & 0xf][pinstate]
    if state ==  DIR_CW:
        print ("Rechts")
    elif state == DIR_CCW:
        print ("Links")

GPIO.add_event_detect(tasterPin1, GPIO.FALLING, callback = call1, bouncetime = 200)
GPIO.add_event_detect(tasterPin2, GPIO.FALLING, callback = call2, bouncetime = 200)
GPIO.add_event_detect(tasterPin3, GPIO.FALLING, callback = call3, bouncetime = 200)

GPIO.add_event_detect(drehgeberPin1, GPIO.BOTH, callback = call4)
GPIO.add_event_detect(drehgeberPin2, GPIO.BOTH, callback = call4)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print ("Programm Beendet")
