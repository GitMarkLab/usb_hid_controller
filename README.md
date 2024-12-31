# usb_hid_controller
- read raw data from usb controller
- all data available in a large array so any controller can be connected. The mapping can be done on your own
- Automatic detection of win or linux system

run get_controller to find out the vid and pid.

add this to the init and run again.

in the notebook is an example on how to find elements in the array on value change.



# OS Windows 
it is nessesary to install libusb and to define the environment Variables

Windows libusb Umgebungsvariablen  / Environment Variables
Environment Variables --> System variables --> Path

for my system:
C:\Users\[USER]\AppData\Roaming\Python\Python312\site-packages\libusb\_platform\_windows\x86  
C:\Users\[USER]\AppData\Roaming\Python\Python312\site-packages\libusb\_platform\_windows\x64

tested with USB game controller and 3Dconnexion SpaceNavigator in an virtual windows machine


# Linux 
it is tested with an XBOX 360 controller clone and SNES clone

# Android
### TODO

