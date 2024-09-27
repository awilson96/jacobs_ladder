from . import Webdriver
from .Options import DesktopOptions
from tkinter import filedialog
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys
from .Favorites import Favorites
import subprocess
import pyautogui


class EnvironmentSetup:

    def __init__(self, analog_labV: str = None, winAppDriver: str = None, loopMidi: str = None, midiOX: str = None,
                 init_instruments: list[str] = ["Rom1A 11-E.PIANO 1"], init: bool = True) -> None:
        """Initialize the environment by taking in two paths.  One to the Analog Lab V and one to WinAppDriver

        Args:
            analog_labV (str, optional): Path to Analog Lab V. Defaults to None.
            winAppDriver (str, optional): Path to WinAppDriver. Defaults to None.
            loopMidi (str, optional): Path to loopMidi. Defaults to None.
            midiOX (str, optional): Path to midiOX. Defaults to None.
            init_instruments (list[str], optional): a list of instruments whose length is divisible by 12. Defaults to ["Rom1A 11-E.PIANO 1"].
            init (bool, optional): True for main controller, use false when instantiating other instances. Defaults to True.
        """
        self.analog_labV = analog_labV if analog_labV else filedialog.askopenfilename(
            title="Select your Analog Lab Executable Path")
        self.winAppDriver = winAppDriver if winAppDriver else filedialog.askopenfilename(
            title="Select your WinAppDriver Executable Path")
        self.loopMidi = loopMidi
        self.midiOX = midiOX if midiOX else filedialog.askopenfilename(
            title="Select your midiOX Executable Path")
        
        if loopMidi: subprocess.Popen(self.loopMidi)
        
        self.num_apps = 12
        self.moved = False

        # Used to keep track of the previous commands web element
        self.current_editor = None
        self.play_panel_toggle = None
        self.init = init
        self.init_instrument = init_instruments if isinstance(
            init_instruments, str) else None

        if not self.init:
            self.initialize_webdriver(executable_path=self.analog_labV)
        else:
            if loopMidi:
                self.initialize_webdriver(executable_path=self.loopMidi)
                self.create_loop_midi_ports()         
            self.initialize_webdriver(executable_path=self.midiOX)
            self.initialize_webdriver(executable_path=self.midiOX)
            self.envInstances = self.create_environment_setup(
                init_instruments=init_instruments)
            [self.envInstances[instance_index].select_instrument(
                instrument_name=self.envInstances[instance_index].init_instrument, port_number=instance_index) for instance_index in range(12)]
            self.menu()

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
            editor.send_keys(keys)
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

        if self.moved:
            pyautogui.dragTo(x=x-drag_distance, y=y, duration=1)
        else:
            pyautogui.dragTo(x=x+drag_distance, y=y, duration=1)

        pyautogui.mouseUp()

        self.moved = not self.moved

    def create_loop_midi_ports(self):
        """Consistently create the necissary virtual Midi ports needed for the application to run

        Raises:
            NotImplementedError: Used to save code, I'll admit it's kinda hacky :/
        """
        try:    
            scroll_button = self.driver.find_element(AppiumBy.NAME, "Position")
            scroll_editor = self.driver.create_web_element(list(scroll_button.values())[0])
            scroll_editor.click()
            plus_button = self.driver.find_element(AppiumBy.NAME, "+")
            plus_editor = self.driver.create_web_element(list(plus_button.values())[0])
            plus_editor.click()
            plus_editor.send_keys(Keys.UP + Keys.DOWN)
            minus_button = self.driver.find_element(AppiumBy.NAME, "-")
            minus_editor = self.driver.create_web_element(list(minus_button.values())[0])
            minus_editor.click()
            for _ in range(26):
                minus_editor.click()
            raise NotImplementedError("Throw into the except to save code")
        except Exception as e:
            plus_button = self.driver.find_element(AppiumBy.NAME, "+")
            plus_editor = self.driver.create_web_element(list(plus_button.values())[0])
            plus_editor.click()
            plus_editor.send_keys(Keys.UP + Keys.DOWN)
            minus_button = self.driver.find_element(AppiumBy.NAME, "-")
            minus_editor = self.driver.create_web_element(list(minus_button.values())[0])
            minus_editor.click()
            for i in range(26):
                if i < 24:
                    plus_editor.send_keys(Keys.RIGHT + Keys.BACK_SPACE + str(i))
                elif i == 24:
                    plus_editor.send_keys(Keys.RIGHT + Keys.BACK_SPACE + "jacobs_ladder")
                elif i == 25:
                    plus_editor.send_keys(Keys.RIGHT + Keys.BACK_SPACE + "jacob")
                plus_editor.click()

        self.__click__("Close")

    def change_instrument(self, instrument_name: str):
        """After an initial configuration has been setup, change an instance to a different instrument

        Args:
            instrument_name (str): the exact name of an Analog Lab V instrument you wish to switch to (see Favorites)
        """
        self.current_editor.click()
        self.current_editor.send_keys(
            Keys.CONTROL + Keys.SHIFT + Keys.HOME + Keys.BACKSPACE)
        self.current_editor.send_keys(instrument_name + Keys.ENTER)
        self.__click_and_drag__()

    def create_environment_setup(self, init_instruments: list[str]) -> list[object]:
        """Create a list of instances with initialized webdrivers capable of interacting with multiple EnvironmentSetup classes at once

        Returns:
            list: a list of EnvironmentSetup classes with initialized webdrivers for interacting with the windows application

        Raises:
            ValueError: If the list length is not evenly divisible by self.num_apps (12)

        Returns:
            list[object]: a list of self.num_apps (12) EnvironmentSetup() objects
        """
        envs = []
        if len(init_instruments) == 1:
            init_instruments = init_instruments * 12
        elif len(init_instruments) == 2:
            init_instruments = init_instruments * 6
        elif len(init_instruments) == 3:
            init_instruments = init_instruments * 4
        elif len(init_instruments) == 4:
            init_instruments = init_instruments * 3
        elif len(init_instruments) == 6:
            init_instruments = init_instruments * 2
        elif len(init_instruments) == 12:
            pass
        else:
            raise ValueError("Initializer list length must be evenly divisible by 12")
        for init_instrument in init_instruments:
            env = EnvironmentSetup(
                analog_labV=self.analog_labV, winAppDriver=self.winAppDriver, loopMidi=None, midiOX="placeholder",
                init_instruments=init_instrument, init=False)
            envs.append(env)
        return envs

    def initialize_webdriver(self, executable_path: str) -> None:
        """Initialize the custom webdriver to work with windows applications"""
        caps = DesktopOptions()
        caps.set_capability("app", executable_path)
        caps.set_capability("automationName", "Windows")
        caps.set_capability("newCommandTimeout", 60)

        self.driver = Webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            options=caps)

        self.driver.implicitly_wait(30)

    def menu(self):
        try:
            while True:
                print("Environment Setup Manual Mode: \n")
                print("Select an option from the following choices: ")
                print("1. Change Instrument")
                choice = input("Enter your choice: ")
                if choice == "1":
                    try:
                        while True:
                            instruments = input(
                                "Enter the exact name of the instrument(s) separated by commas if there is more than one: ")
                            instruments_list = instruments.split(", ")
                            isValid = self.configure_instruments(
                                instruments_list=instruments_list)
                            if isValid:
                                break
                    except KeyboardInterrupt:
                        print("Exiting Option 1...")
                if choice.lower() in ["q", "quit", "exit"]:
                    print("Exiting...")
                    break
        except KeyboardInterrupt:
            print("Exiting...")

    def configure_instruments(self, instruments_list: list[str]):
        if 12 % len(instruments_list) == 0:
            if len(instruments_list) == 1:
                self.single_instrument(instrument_name=instruments_list[0])
            elif len(instruments_list) == 2:
                self.two_instruments(instruments_list=instruments_list)
            elif len(instruments_list) == 3:
                self.three_instruments(instruments_list=instruments_list)
            elif len(instruments_list) == 4:
                self.four_instruments(instruments_list=instruments_list)
            elif len(instruments_list) == 6:
                self.six_instruments(instruments_list=instruments_list)
            elif len(instruments_list) == 12:
                self.twelve_instruments(instruments_list=instruments_list)
            return True

        print("Invalid selection! Please enter a number of instruments that is evenly divisible by 12. \n")
        return False

    def single_instrument(self, instrument_name: str):
        [self.envInstances[i].change_instrument(
            instrument_name=instrument_name) for i in range(self.num_apps)]

    def two_instruments(self, instruments_list: list[str]):
        for i in range(self.num_apps):
            if i % 2 == 0:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[0])
            else:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[1])

    def three_instruments(self, instruments_list: list[str]):
        for i in range(self.num_apps):
            if i % 3 == 0:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[0])
            elif i % 3 == 1:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[1])
            else:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[2])

    def four_instruments(self, instruments_list: list[str]):
        for i in range(self.num_apps):
            if i % 4 == 0:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[0])
            elif i % 4 == 1:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[1])
            elif i % 4 == 2:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[2])
            else:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[3])

    def six_instruments(self, instruments_list: list[str]):
        for i in range(self.num_apps):
            if i % 6 == 0:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[0])
            elif i % 6 == 1:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[1])
            elif i % 6 == 2:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[2])
            elif i % 6 == 3:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[3])
            elif i % 6 == 4:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[4])
            else:
                self.envInstances[i].change_instrument(
                    instrument_name=instruments_list[5])

    def twelve_instruments(self, instruments_list: list[str]):
        for i in range(self.num_apps):
            self.envInstances[i].change_instrument(
                instrument_name=instruments_list[i])

    def minimize(self):
        """Minimize the Analog Lav V window"""
        button = self.driver.find_element(AppiumBy.NAME, "Minimize")
        editor = self.driver.create_web_element(list(button.values())[0])
        editor.click()

    def select_instrument(self, instrument_name: str, port_number: int):
        """Select an instrument you wish to initialize the instance to by configuring its instrument type and port number

        Args:
            instrument_name (str): the exact name of an Analog Lab V instrument you wish to switch to (see Favorites)
            port_number (int): the port number you wish to assign to this instance
        """
        try:
            self.play_panel_toggle = self.__click__(
                search_str="Play Panel toggle")
            self.current_editor = self.__click__(
                search_str="Searchbar", keys=instrument_name)
            sleep(0.3)
            self.select_midi_port(port_number=port_number)
            sleep(0.3)
            self.__click_and_drag__()
            sleep(0.5)
            
        except:
            self.play_panel_toggle = self.__click__(
                search_str="Play Panel toggle")
            self.current_editor = self.__click__(
                search_str="Searchbar", keys=instrument_name)
            sleep(0.3)
            self.select_midi_port(port_number=port_number)
            sleep(0.3)
            self.__click_and_drag__()
            sleep(0.5)

    def select_midi_port(self, port_number: int):
        try:
            self.__click__(search_str="Home tab")
            pyautogui.moveRel(-85, -80)
            sleep(0.3)
            pyautogui.click()
            sleep(0.3)
            pyautogui.moveRel(50, 155)
            sleep(0.3)
            pyautogui.click()
            self.play_panel_toggle = self.__click__(
                search_str="Analog Lab V")
            sleep(0.3)
            pyautogui.moveRel(145, -90)
            sleep(0.3)
            color = self.determine_color()
            # Color is cyan blue indicating the button is selected
            if color == (0, 188, 250):
                pyautogui.click()

            if port_number == 0:
                pyautogui.scroll(-840)
            elif port_number == 1:
                pyautogui.scroll(-880)
            elif port_number == 2:
                pyautogui.scroll(-920)
            elif port_number == 3:
                pyautogui.scroll(-960)
            elif port_number == 4:
                pyautogui.scroll(-1000)
                pyautogui.moveRel(0, 10)
            elif port_number == 5:
                pyautogui.scroll(-1000)
                pyautogui.moveRel(0, 30)
            elif port_number == 6:
                pyautogui.scroll(-1000)
                pyautogui.moveRel(0, 50)
            elif port_number == 7:
                pyautogui.scroll(-1000)
                pyautogui.moveRel(0, 70)
            elif port_number == 8:
                pyautogui.scroll(-1000)
                pyautogui.moveRel(0, 90)
            elif port_number == 9:
                pyautogui.scroll(-1000)
                pyautogui.moveRel(0, 110)
            if port_number == 10:
                pyautogui.scroll(-100)
            elif port_number == 11:
                pyautogui.scroll(-140)
            
            # Color is light or dark grey indicating it is not selected or is the rim of the button
            color = self.determine_color()
            if color in ((54, 53, 58), (67, 66, 73), (31, 30, 36), (55, 55, 62)):
                sleep(0.3)
                pyautogui.click()
            sleep(0.3)
            self.play_panel_toggle = self.__click__(
                search_str="Analog Lab V")
            sleep(0.3)
            pyautogui.moveRel(265, 160)
            sleep(0.3)
            pyautogui.click()

        except Exception as e:
            print(f"Error: {e}")

    def determine_color(self):
        """Determine what the rgb value tuple is at the given mouse location

        Returns:
            tuple: rgb tuple
        """
        x, y = pyautogui.position()
        screenshot = pyautogui.screenshot()
        return screenshot.getpixel((x, y))

    @staticmethod
    def get_rgb_val_from_mouse_position(self):
        """An integration tool for determining the rgb value based on where the mouse position is. Prints value in the same spot in the terminal"""
        try:
            while True:
                color = self.determine_color()
                print(f"\rColor: {color}", end="", flush=True)
        except KeyboardInterrupt:
            print("Exiting...")


if __name__ == "__main__":
    analog_labV = r"C:/Program Files/Arturia/Analog Lab V/Analog Lab V.exe"
    winAppDriver = r"C:/Program Files (x86)/Windows Application Driver/WinAppDriver.exe"
    loopMidi = r"C:/Program Files (x86)/Tobias Erichsen/loopMIDI/loopMIDI.exe"
    midiOX = r"C:/Program Files (x86)/MIDIOX/midiox.exe"
    envSetup = EnvironmentSetup(
        analog_labV=analog_labV, winAppDriver=winAppDriver, loopMidi=None, midiOX=midiOX,
        init_instruments=["Butter"])
    
