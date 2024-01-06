import os
import sys
import time

import pyautogui
from pyscreeze import ImageNotFoundException
from pyautogui import ImageNotFoundException


class CreatePorts():

    def __init__(self):
        # Paths
        self.loop_midi_path = r'C:\Program Files (x86)\Tobias Erichsen\loopMIDI\LoopMIDI.exe'
        self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.images_dir = os.path.join(self.script_dir, 'images')
        
        # Images
        self.loop_midi_initialized = os.path.join(self.images_dir, 'LoopMidiInitialized.PNG')
        self.loop_midi_uninitialized = os.path.join(self.images_dir, 'LoopMidiUninitialized.PNG')
        self.minus_button = os.path.join(self.images_dir, 'MinusButton.PNG')
        self.new_port_name = os.path.join(self.images_dir, 'NewPortName.PNG')
        self.new_port_name_unhighlighted = os.path.join(self.images_dir, 'NewPortNameUnhighlighted.PNG')
        self.plus_button = os.path.join(self.images_dir, 'PlusButton.PNG')


    def open_loop_midi(self):
        """Open the loopMidi Application

        Raises:
            Exception: If loopMIDI application does not open
        """

        try:
            os.system(f'start "" "{self.loop_midi_path}"')

        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Failed to open LoopMIDI.")

    def is_loop_midi_installed(self):
        """Check if loopMIDI was launched by looking for the application in the user's window

        Returns:
            bool: True if the application was launched, false otherwise
        """
        # Wait for loopMIDI to open
        time.sleep(1)

        try:
            # Locate the launched loopMIDI application
            position = pyautogui.locateOnScreen(self.loop_midi_uninitialized)
            if position:
                print(f"Image {self.loop_midi_uninitialized} found at position: {position}")
                return True
            else:
                return False
        except:
            print(f"Could not find {self.loop_midi_uninitialized}")
            return False
        
    def get_new_port_name_textbox_position(self):
        """_summary_
        """

        try:
            # Locate positions of new_port_name box if it is not highlighted
            position = pyautogui.locateOnScreen(self.new_port_name_unhighlighted)
            if position:
                print(f"Image {self.new_port_name_unhighlighted} found at position: {position}")
                return position
            else:
                return None
        except:
            try:
                # Locate positions of new_port_name box if it is highlighted
                position = pyautogui.locateOnScreen(self.new_port_name)
                if position:
                    print(f"Image {self.new_port_name} found at position: {position}")
                    return position
                else:
                    return None
            except:
                return None
            
    def _fill_in_port_information(self, box, number_to_write):
        # Calculate the coordinates of the middle of the textbox
        middle_x = box.left + box.width // 2
        middle_y = box.top + box.height // 2

        # Click in the middle of the textbox
        pyautogui.click(middle_x, middle_y)

        # Drag the cursor to the left
        pyautogui.dragTo(box.left, middle_y, duration=1.0)

        # Release the click
        pyautogui.mouseUp()

        # Press the 'Delete' key
        pyautogui.press('delete')

        # Type the specified number
        pyautogui.typewrite(str(number_to_write), interval=0.1)

        
    def add_port(self, box, offset_x, offset_y):
        
        # Calculate the new coordinates
        new_x = box.left - offset_x
        new_y = box.top + offset_y

        # Move the mouse to the new position
        pyautogui.moveTo(new_x, new_y, duration=1.0)

        # Click on the new position
        pyautogui.click()

          

if __name__ == "__main__":
    create_ports = CreatePorts()
    create_ports.open_loop_midi()

    installed = create_ports.is_loop_midi_installed()
    print(installed)

    port_name_position = create_ports.get_new_port_name_textbox_position()
    print(port_name_position)

    create_ports._fill_in_port_information(port_name_position, 0)
    create_ports.add_port(port_name_position, 110, 10)

