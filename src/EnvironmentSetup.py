from . import Webdriver
from .Options import DesktopOptions
from tkinter import filedialog
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
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
        self.select_instrument(instrument_name="Rom1A 11-E.PIANO 1")
        

    def initialize_webdriver(self) -> None:
        caps = DesktopOptions()
        caps.set_capability("app", self.analog_labV)
        caps.set_capability("automationName", "Windows")
        caps.set_capability("newCommandTimeout", 60)

        self.driver = Webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            options=caps)
        
        self.driver.implicitly_wait(30)

    def __click__(self, search_str: str, keys: str = None):
        button = self.driver.find_element(AppiumBy.NAME, search_str)
        editor = self.driver.create_web_element(list(button.values())[0])
        editor.click()
        if keys:
            editor.send_keys(keys)
            editor.send_keys(Keys.RETURN)
        sleep(0.5)

    def select_instrument(self, instrument_name: str):
        self.__click__(search_str="Play Panel toggle")
        self.__click__(search_str="Searchbar", keys=instrument_name)
        


if __name__ == "__main__":
    analog_labV = r"C:/Program Files/Arturia/Analog Lab V/Analog Lab V.exe"
    winAppDriver = r"C:/Program Files (x86)/Windows Application Driver/WinAppDriver.exe"
    envSetup = EnvironmentSetup(analog_labV=analog_labV, winAppDriver=winAppDriver)
