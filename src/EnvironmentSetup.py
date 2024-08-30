from . import Webdriver
from .Options import DesktopOptions
from tkinter import filedialog
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys


class EnvironmentSetup:

    def __init__(self, analog_labV: str = None, winAppDriver: str = None) -> None:
        """Initialize the environment by taking in two paths.  One to the Analog Lab V and one to WinAppDriver

        Args:
            analog_labV (str, optional): Path to Analog Lab V. Defaults to None.
            winAppDriver (str, optional): Path to WinAppDriver. Defaults to None.
        """
        self.analog_labV = analog_labV if analog_labV else filedialog.askopenfilename(title="Select your Analog Lab Executable Path")
        self.winAppDriver = winAppDriver if winAppDriver else filedialog.askopenfilename(title="Select your WinAppDriver Executable Path")

        self.initialize_webdriver()

    def initialize_webdriver(self) -> None:
        pass


if __name__ == "__main__":
    # analog_labV = r"C:/Program Files/Arturia/Analog Lab V/Analog Lab V.exe"
    # winAppDriver = r"C:/Program Files (x86)/Windows Application Driver/WinAppDriver.exe"
    # envSetup = EnvironmentSetup(analog_labV=analog_labV, winAppDriver=winAppDriver)

    caps = DesktopOptions()
    caps.set_capability("app","C:\\Windows\\System32\\notepad.exe")

    caps.set_capability("automationName", "Windows")
    caps.set_capability("newCommandTimeout", 60)

    driver = Webdriver.Remote(
                command_executor='http://127.0.0.1:4723',
                options=caps)
    with open(file="example",mode="r") as f:
        content=f.readlines()

    driver.implicitly_wait(30)
    elm = driver.find_element(AppiumBy.NAME, "Text editor")
    editor = driver.create_web_element(list(elm.values())[0])
    for line in content:
        editor.send_keys(line)
        editor.send_keys(Keys.RETURN)
    editor.send_keys(Keys.CONTROL, "s")
