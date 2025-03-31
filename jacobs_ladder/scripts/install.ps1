# Check if PowerShell Core is installed
$pwshInstalled = winget list --id Microsoft.PowerShell
if ($pwshInstalled -match "Microsoft.PowerShell") {
    Write-Output "PowerShell Core is already installed."
} else {
    Write-Output "Installing PowerShell Core..."
    winget install --id Microsoft.PowerShell --source winget --silent --accept-package-agreements --accept-source-agreements
    winget install --id Microsoft.PowerShell.Preview --source winget --silent --accept-package-agreements --accept-source-agreements;
}

# -------------------------------
# Install MIDI-OX
# -------------------------------
$MIDI_OX_Url = "http://www.midiox.com/zip/midioxse.exe"
$MIDI_OX_Path = "$env:USERPROFILE\Downloads\midioxse.exe"
$MIDI_OX_InstallDir = "C:\Program Files (x86)\MIDIOX"

if (-Not (Test-Path "$MIDI_OX_InstallDir\MIDIOX.EXE")) {
    Write-Output "Downloading MIDI-OX..."
    Invoke-WebRequest -Uri $MIDI_OX_Url -OutFile $MIDI_OX_Path
    Write-Output "Installing MIDI-OX..."
    Start-Process -FilePath $MIDI_OX_Path -Wait
} else {
    Write-Output "MIDI-OX is already installed."
}

# -------------------------------
# Install loopMIDI Driver
# -------------------------------
$loopMIDI_Url = "https://www.tobias-erichsen.de/wp-content/uploads/2020/01/loopMIDISetup_1_0_16_27.zip"
$loopMIDI_Zip_Path = "$env:USERPROFILE\Downloads\loopMIDISetup_1_0_16_27.zip"
$loopMIDI_InstallDir = "C:\Program Files (x86)\Tobias Erichsen\loopMIDI"

if (-Not (Test-Path "$loopMIDI_InstallDir\loopMIDI.exe")) {
    Write-Output "Downloading loopMIDI ZIP..."
    Invoke-WebRequest -Uri $loopMIDI_Url -OutFile $loopMIDI_Zip_Path

    # Extract the ZIP file
    Write-Output "Extracting loopMIDI ZIP..."
    $extractPath = "$env:USERPROFILE\Downloads\loopMIDISetup"
    Expand-Archive -Path $loopMIDI_Zip_Path -DestinationPath $extractPath

    # Run the installer (loopMIDISetup.exe)
    $loopMIDIInstaller = "$extractPath\loopMIDISetup.exe"
    Write-Output "Running loopMIDI setup..."
    Start-Process -FilePath $loopMIDIInstaller -ArgumentList "/S" -Wait
} else {
    Write-Output "loopMIDI driver is already installed."
}