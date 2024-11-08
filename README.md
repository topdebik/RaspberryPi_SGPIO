# RaspberryPi_SGPIO
Realization of software SGPIO bus (https://wikipedia.org/wiki/SGPIO) on Raspberry Pi with RPi.GPIO  
Optimized to work with hard disk enclosures

## Dependencies
Python libraries - `RPi.GPIO`

## Installation
Install RPi.GPIO:
```shell
pip install RPi.GPIO
```

## Using (example)
Import SGPIO:
```Python
from SGPIO import SGPIO
```
Create SGPIO object. Define SCLK (sclock), SLOAD (sload), SDOUT (sdataout) pins on Raspberry Pi and preferred communication speed in Hz (It's not recommended to set speed faster than 1000 Hz, Raspberry Pi will not like it and timings will break):
```Python
sgpio = SGPIO(sclock=17, sload=27, sdataout=22, speed=500)
```
Create data list (every list inside represents one hard disk and it's LED state (activity, fail, locate)):
```Python
data = [[0, 0, 0] for _ in range(4)]
```
Start transmittion:
```Python
sgpio.startTransmittion(data)
```
When needed, change state:
```Python
data = [[1, 0, 0] for _ in range(4)]
sgpio.changeState(data)
```
On transmittion end, close transmittion (this is needed to free processes and pins):
```Python
sgpio.stopTransmittion()
```
You can find an example in [main.py](main.py)

## Info
Tested on Supermicro hard disk enclosure. Because SGPIO is not so popular (as SES), every vendor can implement it as he wants (usually, LED bytes are shuffled in random order). You probably would need to debug these sharp edges before using