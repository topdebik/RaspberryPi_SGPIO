from SGPIO import SGPIO
from time import sleep


sgpio = SGPIO(sclock=17, sload=27, sdataout=22, speed=500)
data = [[0, 0, 0] for _ in range(4)]
data[0] = [1, 0, 0]

print("1st state")
sgpio.startTransmittion(data)
sleep(5)
print("2nd state")
data = [[0, 0, 0] for _ in range(4)]
data[0] = [1, 1, 1]
sgpio.changeState(data)
sleep(5)
print("3rd state")
data = [[0, 0, 0] for _ in range(4)]
data[0] = [1, 0, 0]
sgpio.changeState(data)
sleep(5)
sgpio.stopTransmittion()
