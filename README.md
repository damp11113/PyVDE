# PyVDE
Virtual Desktop Environment write in python with pygame

![image](https://github.com/damp11113/PyVDE/assets/64675096/0be15192-d88c-4303-81f5-aa3fd2d685c2)

```py
import time

from PyVDE.desktop import Desktop
from PyVDE.App import AppWindow
import pygame
import threading

class MyFirstApp(AppWindow):
    def __init__(self):
        super().__init__()

    def init(self):
        print('Hello')
        self.window.fill((255, 255, 255))


desktopwindow = Desktop()

desktopwindow.register("myapp", MyFirstApp)

def delayopenapp():
    time.sleep(2)
    desktopwindow.runapp("myapp", (50, 50))

delayopenappthread = threading.Thread(target=delayopenapp)
delayopenappthread.start()

desktopwindow.start()
```
