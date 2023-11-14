import subprocess
import pyautogui
import time

# Path to your Analog Lab 4 executable
analog_lab_path = "C:\\Program Files\\Arturia\\Analog Lab 4\\Analog Lab 4.exe"

midiOX_path = "C:\\Program Files (x86)\\MIDIOX\\midiox.exe"

# Number of instances you want to open
num_instances = 16

# Open two instances of MIDI-OX
for i in range(2):
    subprocess.Popen([midiOX_path])
    time.sleep(1)
    
pyautogui.mouseDown(-1124, 812)
pyautogui.dragTo(-1920, 650, duration=0.5)
pyautogui.mouseUp()
time.sleep(0.5)
pyautogui.click(-549, 566)

time.sleep(5)
x, y = pyautogui.position()

print("Icon coordinates (x, y):", x, y)

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

# Launch 16 instances of Analog Lab 4
for i in range(num_instances):
    subprocess.Popen([analog_lab_path])
    
    time.sleep(6)

    # Click Analog Lab
    pyautogui.click(x1, y1)
    time.sleep(0.3)
    # Click Audio Midi Settings
    pyautogui.click(x2, y2)
    time.sleep(0.3)
    if i == 0:
        # Get the color of the port icon
        color = pyautogui.pixel(p1, q1)
        # If the port is the color grey than click it
        if color == (54, 53, 58):
            pyautogui.click(p1, q1)
            time.sleep(0.3)
        color = pyautogui.pixel(p2, q2)
        if color == (0, 188, 250):
            pyautogui.click(p2, q2)
            time.sleep(0.3)
        color = pyautogui.pixel(p3, q3)
        if color == (0, 188, 250):
            pyautogui.click(p3, q3)
            time.sleep(0.3)
            
    elif i == 1:
        # Get the color of the port icon
        color = pyautogui.pixel(p1, q1)
        # If the port is not the color grey than click it
        if color != (54, 53, 58):
            pyautogui.click(p1, q1)
            time.sleep(0.3)
            color = pyautogui.pixel(p2, q2)
            if color == (31, 30, 36):
                pyautogui.click(p2, q2)
                time.sleep(0.3)
    elif i == 2:
        # Get the color of the port icon
        color = pyautogui.pixel(p3, q3)
        # If the port is not the color grey than click it
        if color == (54, 53, 58):
            pyautogui.click(p3, q3)
            time.sleep(0.3)
            color = pyautogui.pixel(p2, q2)
            if color != (31, 30, 36):
                pyautogui.click(p2, q2)
                time.sleep(0.3)
                
    elif i == 3:
        color = pyautogui.pixel(p3, q3)
        if color == (0, 188, 250):
            pyautogui.click(p3, q3)
            time.sleep(0.5)
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        color = pyautogui.pixel(p4, q4)
        if color == (31, 30, 36):
            pyautogui.click(p4, q4)
            time.sleep(0.5)
            
    elif i == 4:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p4, q4)
        if color == (0, 188, 250):
            pyautogui.click(p4, q4)
            time.sleep(0.5)
        color = pyautogui.pixel(p5, q5)
        if color == (54, 53, 58):
            pyautogui.click(p5, q5)
            time.sleep(0.5)
            
    elif i == 5:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p5, q5)
        if color == (0, 188, 250):
            pyautogui.click(p5, q5)
            time.sleep(0.5)
        color = pyautogui.pixel(p6, q6)
        if color == (31, 30, 36):
            pyautogui.click(p6, q6)
            time.sleep(0.5)
            
    elif i == 6:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p6, q6)
        if color == (0, 188, 250):
            pyautogui.click(p6, q6)
            time.sleep(0.5)
        color = pyautogui.pixel(p7, q7)
        if color == (54, 53, 58):
            pyautogui.click(p7, q7)
            time.sleep(0.5)
            
    elif i == 7:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p7, q7)
        if color == (0, 188, 250):
            pyautogui.click(p7, q7)
            time.sleep(0.5)
        color = pyautogui.pixel(p8, q8)
        if color == (31, 30, 36):
            pyautogui.click(p8, q8)
            time.sleep(0.5)
            
    elif i == 8:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p8, q8)
        if color == (0, 188, 250):
            pyautogui.click(p8, q8)
            time.sleep(0.5)
        color = pyautogui.pixel(p9, q9)
        if color == (54, 53, 58):
            pyautogui.click(p9, q9)
            time.sleep(0.5)
            
    elif i == 9:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s2, t2, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p9, q9)
        if color == (0, 188, 250):
            pyautogui.click(p9, q9)
            time.sleep(0.5)
        pyautogui.mouseDown(s2, t2)
        pyautogui.dragTo(s3, t3, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p4, q4)
        if color == (31, 30, 36):
            pyautogui.click(p4, q4)
            time.sleep(0.5)
            
    elif i == 10:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s3, t3, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p4, q4)
        if color == (0, 188, 250):
            pyautogui.click(p4, q4)
            time.sleep(0.5)
        color = pyautogui.pixel(p5, q5)
        if color == (54, 53, 58):
            pyautogui.click(p5, q5)
            time.sleep(0.5)
            
    elif i == 11:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s3, t3, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p5, q5)
        if color == (0, 188, 250):
            pyautogui.click(p5, q5)
            time.sleep(0.5)
        color = pyautogui.pixel(p6, q6)
        if color == (31, 30, 36):
            pyautogui.click(p6, q6)
            time.sleep(0.5)
            
    elif i == 12:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s3, t3, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p6, q6)
        if color == (0, 188, 250):
            pyautogui.click(p6, q6)
            time.sleep(0.5)
        color = pyautogui.pixel(p7, q7)
        if color == (54, 53, 58):
            pyautogui.click(p7, q7)
            time.sleep(0.5)
            
    elif i == 13:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s3, t3, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p7, q7)
        if color == (0, 188, 250):
            pyautogui.click(p7, q7)
            time.sleep(0.5)
        color = pyautogui.pixel(p8, q8)
        if color == (31, 30, 36):
            pyautogui.click(p8, q8)
            time.sleep(0.5)
            
    elif i == 14:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s3, t3, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p8, q8)
        if color == (0, 188, 250):
            pyautogui.click(p8, q8)
            time.sleep(0.5)
        color = pyautogui.pixel(p9, q9)
        if color == (54, 53, 58):
            pyautogui.click(p9, q9)
            time.sleep(0.5)
            
    elif i == 15:
        pyautogui.mouseDown(s1, t1)
        pyautogui.dragTo(s4, t4, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)
        color = pyautogui.pixel(p8, q8)
        if color == (0, 188, 250):
            pyautogui.click(p8, q8)
            time.sleep(0.5)
        color = pyautogui.pixel(p9, q9)
        if color == (31, 30, 36):
            pyautogui.click(p9, q9)
            time.sleep(0.5)
        
      
    # Close out of audio midi settings
    pyautogui.click(x4, y4)
    # Drag the window to the other screen so it is out of the way
    pyautogui.mouseDown(1296, 327)
    new_x, new_y = -1103, 771
    pyautogui.dragTo(new_x, new_y, duration=1)
    pyautogui.mouseUp()

# print("Configuration completed for", num_instances, "instances.")
# # Get the current mouse position
# x, y = pyautogui.position()

# print("Icon coordinates (x, y):", x, y)