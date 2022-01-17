from serial.tools.list_ports_common import ListPortInfo
import sys, os
from pystray import Icon as icon, MenuItem as item, Menu as menu
from PIL import Image
import pyperclip

import serial.tools.list_ports

def on_clicked(icon, item):
    global active
    #print('"{0}"'.format(item.text))
    if item.text == '__quit__':
        icon.visible = False
        icon.stop()
    else:
        port = findport(item.text)
        pyperclip.copy(port)
        icon.notify('{0} copied to clipboard'.format(port))

def findport(desc):
    comports = [(port.name, port.description) for port in serial.tools.list_ports.comports()]
    return next((x for x,y in comports if y==desc), 'none')

def genlist():
    comports = [(port.description, False, True) for port in serial.tools.list_ports.comports()]
    comports.append(('__quit__', False, True))
    return (item('{0}'.format(desc), on_clicked, visible=isvisible, default=isdefault) for desc, isdefault, isvisible in comports )

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

#application_path = str(os.path.dirname(__file__))

myimage = Image.open(os.path.join(application_path, 'EnumCom.png'))

mymenu = menu(genlist)

icon('test', myimage, menu=mymenu).run()
