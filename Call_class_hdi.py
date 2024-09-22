# read raw value from hid controller 
# multiple controllers possible


from class_hid import Controller
import time
from time import sleep

# set information in initialization or method init
controller = Controller()
print(controller.get_devices()) # raw out of all hid devices
controller.init('XBOX Controller',"0x045e","0x028e")

controller2 = Controller('SpaceNavigator',"0x046d","0xc626")

print("Available HID",controller.get_devices())


controller.connect()
controller2.connect()


while not controller.data_available():
    print("Warten auf Datenverfügbarkeit...")
    time.sleep(1)  # Warte 1 Sekunde, bevor du erneut prüfst

while not controller2.data_available():
    print("Warten auf Datenverfügbarkeit...")
    time.sleep(1)  # Warte 1 Sekunde, bevor du erneut prüfst



while True:
    data = controller.get_raw_data()
    data2 = controller2.get_raw_data()
    if(data[11] == 4):
        break
    print(data,data2)
    sleep(1)
    
print("End")
controller.close()
controller2.close()