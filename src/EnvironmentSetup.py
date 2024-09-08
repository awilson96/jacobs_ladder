from . import Webdriver
from .Options import DesktopOptions
from tkinter import filedialog
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys
from .Favorites import Favorites
import pyautogui



class EnvironmentSetup:

    def __init__(self, analog_labV: str = None, winAppDriver: str = None, init_instrument: str = "Rom1A 11-E.PIANO 1", init: bool = True) -> None:
        """Initialize the environment by taking in two paths.  One to the Analog Lab V and one to WinAppDriver

        Args:
            analog_labV (str, optional): Path to Analog Lab V. Defaults to None.
            winAppDriver (str, optional): Path to WinAppDriver. Defaults to None.
        """
        self.analog_labV = analog_labV if analog_labV else filedialog.askopenfilename(title="Select your Analog Lab Executable Path")
        self.winAppDriver = winAppDriver if winAppDriver else filedialog.askopenfilename(title="Select your WinAppDriver Executable Path")
        self.num_apps = 12
        self.moved = False

        # Used to keep track of the previous commands web element
        self.current_editor = None
        self.play_panel_toggle = None
        self.previous_instrument = init_instrument
        self.init = init

        if not self.init:
            self.initialize_webdriver()

    def __click__(self, search_str: str, keys: str = None):
        """Used for creating web elements by search ID, clicking that element and optionally sending keys which will be followed by the ENTER key

        Args:
            search_str (str): a search string for searching for a webelement by name
            keys (str, optional): a string to send for a text field. Defaults to None.

        Returns:
            webelement: an Appium webelement
        """
        button = self.driver.find_element(AppiumBy.NAME, search_str)
        editor = self.driver.create_web_element(list(button.values())[0])
        editor.click()
        if keys:
            for key in keys:
                editor.send_keys(key)
            editor.send_keys(Keys.RETURN)
        sleep(0.5)
        return editor
    
    def __click_and_drag__(self):
        """Drag the app out of the way so that the EnvironmentSetup class can interact with other instances behind the current window"""
        title_bar = self.driver.find_element(AppiumBy.XPATH, "//TitleBar")
        editor = self.driver.create_web_element(list(title_bar.values())[0])

        drag_distance = 1000

        editor.click()
        x, y = pyautogui.position()
        pyautogui.mouseDown()
        pyautogui.drag(x=x-drag_distance, y=y, duration=1) if self.moved else pyautogui.dragTo(x=x+drag_distance, y=y, duration=1)
        pyautogui.mouseUp()
        
        self.moved = not self.moved

    def change_instrument(self, instrument_name: str):
        """After an initial configuration has been setup, change an instance to a different instrument

        Args:
            instrument_name (str): the exact name of an Analog Lab V instrument you wish to switch to (see Favorites)
        """
        self.current_editor.click()
        for _ in range(len(self.previous_instrument)):
            self.current_editor.send_keys(Keys.BACKSPACE)
        self.previous_instrument = instrument_name
        self.current_editor.send_keys(instrument_name)

    def create_environment_setup(self) -> list[object]:
        """Create a list of instances with initialized webdrivers capable of interacting with multiple EnvironmentSetup classes at once

        Returns:
            list: a list of EnvironmentSetup classes with initialized webdrivers for interacting with the windows application
        """
        return [EnvironmentSetup(analog_labV=self.analog_labV, winAppDriver=self.winAppDriver, init_instrument=self.previous_instrument, init=False) for _ in range(self.num_apps)]

    def initialize_webdriver(self) -> None:
        """Initialize the custom webdriver to work with windows applications"""
        caps = DesktopOptions()
        caps.set_capability("app", self.analog_labV)
        caps.set_capability("automationName", "Windows")
        caps.set_capability("newCommandTimeout", 60)

        self.driver = Webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            options=caps)
        
        self.driver.implicitly_wait(30)

    def minimize(self):
        """Minimize the Analog Lav V window"""
        button = self.driver.find_element(AppiumBy.NAME, "Minimize")
        editor = self.driver.create_web_element(list(button.values())[0])
        editor.click()

    def select_instrument(self, instrument_name: str):
        """Select an instrument you wish to initialize the instance to

        Args:
            instrument_name (str): the exact name of an Analog Lab V instrument you wish to switch to (see Favorites)
        """
        try:
            self.play_panel_toggle = self.__click__(search_str="Play Panel toggle")
            self.current_editor = self.__click__(search_str="Searchbar", keys=instrument_name)
            self.__click_and_drag__()
            
        except:
            self.play_panel_toggle = self.__click__(search_str="Play Panel toggle")
            self.current_editor = self.__click__(search_str="Searchbar", keys=instrument_name)
            self.__click_and_drag__()
            

if __name__ == "__main__":
    analog_labV = r"C:/Program Files/Arturia/Analog Lab V/Analog Lab V.exe"
    winAppDriver = r"C:/Program Files (x86)/Windows Application Driver/WinAppDriver.exe"
    envSetup = EnvironmentSetup(analog_labV=analog_labV, winAppDriver=winAppDriver, init_instrument="Mark V EP")
    envSetupInstances = envSetup.create_environment_setup()
    [envSetupInstances[instance_index].select_instrument(instrument_name="Mark V EP") for instance_index in range(12)]

