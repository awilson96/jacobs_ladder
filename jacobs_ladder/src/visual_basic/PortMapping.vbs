' MIDI-OX Test - Load Profile Example (Dynamic Path)
' Keeps the terminal open until the user closes it

Option Explicit

Dim mox, profilePath, args
Set args = WScript.Arguments

' Ensure a profile path is provided
If args.Count = 0 Then
    WScript.Echo "Error: No profile path provided."
    WScript.Echo "Usage: cscript load_profile.vbs <full_profile_path>"
    WScript.Quit 1
End If

' Get the profile path from arguments
profilePath = args(0)

' Create MIDI-OX Object
Set mox = WScript.CreateObject("Midiox.MoxScript.1", "Sink_")

' Load the profile
mox.LoadProfile profilePath

WScript.Echo "Loaded MIDI-OX Profile: " & profilePath
WScript.Echo "Script running... Press Enter to exit."

' Wait for user input in the terminal
WScript.StdIn.ReadLine ' This will pause the script until the user presses Enter

' Clean up and close the MIDI-OX instance when input is received
WScript.Echo "User input received. Closing MIDI-OX..."
Set mox = Nothing ' Release MIDI-OX object
WScript.Quit