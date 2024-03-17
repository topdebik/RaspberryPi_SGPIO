from time import sleep
from multiprocessing import Process, Queue
import RPi.GPIO as gpio


class SGPIO:
    def __init__(self, sclock, sload, sdataout, speed=100):
        self.sclock, self.sload, self.sdataout, self.speed = sclock, sload, sdataout, speed
        self.speed = 1 / (self.speed * 2)  # max 1000 Hz is preferred
        self.transmitting = False

        gpio.setmode(gpio.BCM)
        gpio.setup(self.sclock, gpio.OUT)
        gpio.setup(self.sload, gpio.OUT)
        gpio.setup(self.sdataout, gpio.OUT)
        gpio.output(self.sclock, gpio.LOW)
        gpio.output(self.sload, gpio.LOW)
        gpio.output(self.sdataout, gpio.LOW)

    def startTransmittion(self, data):
        if not self.transmitting:
            s, l = self.convert(data)
            self.s = Queue(maxsize=1)
            self.s.put(s)
            self.l = Queue(maxsize=1)
            self.l.put(l)
            self.tp = Process(target=self.transmit, args=(self.s, self.l))
            self.tp.start()
            self.transmitting = True
        else:
            print("transmittion is already started")

    def changeState(self, data):
        if self.transmitting:
            s, l = self.convert(data)
            self.s.put(s)
            self.l.put(l)
        else:
            print("transmittion is not started")

    def stopTransmittion(self):
        if self.transmitting:
            self.tp.kill()
            gpio.output(self.sclock, gpio.LOW)
            gpio.output(self.sload, gpio.LOW)
            gpio.output(self.sdataout, gpio.LOW)
            sleep(1)
            self.reset()
        else:
            print("transmittion is not started")

    def convert(self, data):
        s = []
        for i in data:  # convert data to bytes
            s.append(i[0])  # activity
            s.append(i[1])  # fail
            s.append(i[2])  # locate (not used)
        l = len(s) - 2
        return s, l

    def transmit(self, ss, ll):
        while True:
            if not ss.empty():
                s = ss.get()
            if not ll.empty():
                l = ll.get()
            sleep(self.speed * 30)  # nobody knows why this is needed
            gpio.output(self.sload, gpio.HIGH)
            sleep(0.01)
            gpio.output(self.sclock, gpio.HIGH)
            gpio.output(self.sdataout, s[-1])
            sleep(self.speed)
            gpio.output(self.sclock, gpio.LOW)
            sleep(self.speed)
            gpio.output(self.sclock, gpio.HIGH)
            gpio.output(self.sload, gpio.LOW)
            gpio.output(self.sdataout, s[0])
            sleep(self.speed)
            gpio.output(self.sclock, gpio.LOW)
            sleep(self.speed)
            for d in range(l):
                gpio.output(self.sclock, gpio.HIGH)
                gpio.output(self.sdataout, s[d + 1])
                sleep(self.speed)
                gpio.output(self.sclock, gpio.LOW)
                sleep(self.speed)

    def reset(self):
        gpio.output(self.sclock, gpio.HIGH)
        gpio.output(self.sload, gpio.HIGH)
        gpio.output(self.sdataout, gpio.HIGH)
        sleep(0.064)
        gpio.output(self.sclock, gpio.LOW)
        gpio.output(self.sload, gpio.LOW)
        gpio.output(self.sdataout, gpio.LOW)
