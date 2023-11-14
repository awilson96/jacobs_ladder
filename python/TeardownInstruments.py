import subprocess
import pyautogui
import time

# Path to your Analog Lab 4 executable
analog_lab_path = "C:\\Program Files\\Arturia\\Analog Lab 4\\Analog Lab 4.exe"

# Coordinates of the icon you want to click
x1, y1 = 724, 357
x2, y2 = 716, 565
p1, q1 = 1424, 789
p2, q2 = 1425, 807
p3, q3 = 1425, 830
p4, q4 = 1425, 726
p5, q5 = 1425, 746
p6, q6 = 1425, 765
p7, q7 = 1425, 785
p8, q8 = 1425, 807
p9, q9 = 1425, 827
s1, t1 = 1612, 722
s2, t2 = 1612, 765
s3, t3 = 1612, 807
s4, t4 = 1612, 850
x4, y4 = 1612, 629
c1, d1 = 1904, 321
c2, d2 = -34, 342
c3, d3 = -992, 350

# clean up instance 
subprocess.Popen([analog_lab_path])
time.sleep(6)
# Click Analog Lab
pyautogui.click(x1, y1)
time.sleep(0.3)
# Click Audio Midi Settings
pyautogui.click(x2, y2)
time.sleep(0.3)

pyautogui.mouseDown(s1, t1)
pyautogui.dragTo(s4, t4, duration=0.5)
pyautogui.mouseUp()
time.sleep(0.5)
color = pyautogui.pixel(p8, q8)
if color == (0, 188, 250):
    pyautogui.click(p8, q8)
    time.sleep(0.5)
color = pyautogui.pixel(p9, q9)
if color == (0, 188, 250):
    pyautogui.click(p9, q9)
    time.sleep(0.5)
    
# Close out of audio midi settings and application
pyautogui.click(x4, y4)
pyautogui.click(c1, d1)
pyautogui.click(c2, d2)
pyautogui.click(c3, d3)
time.sleep(3)

# Define the PowerShell command
powershell_cmd = 'Get-Process -Name "Analog Lab 4" | Stop-Process -Force'

# Run the PowerShell command
subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)

# # Get the current mouse position
# x, y = pyautogui.position()

# print("Icon coordinates (x, y):", x, y)
