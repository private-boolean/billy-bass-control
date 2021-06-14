from playsound import playsound
import glob
from tkgpio import TkCircuit

# initialize the circuit inside the

configuration = {
    "width": 300,
    "height": 200,
    "leds": [
        {"x": 50,  "y": 40, "name": "Mouth",      "pin": 24},
        {"x": 100, "y": 40, "name": "Head",       "pin":  4},
        {"x": 150, "y": 40, "name": "Body",       "pin": 23},
        {"x": 200, "y": 40, "name": "speaker_en", "pin": 25}
    ],
    "buttons": [
        {"x": 50, "y": 130, "name": "Press to toggle LED 2", "pin": 18},
    ]
}

circuit = TkCircuit(configuration)


isPlaying = False
fileIndex = 0


@circuit.run
def main():

    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    import time
    from time import sleep
    import json
    import os
    import errno

    mouthControl = LED(24)
    headControl = LED(4)
    bodyControl = LED(23)
    speakerControl = LED(25)

    def parseFile(sourceFile, soundFile, offset=0.0):
        mvmtFile = open(sourceFile)
        mvmtDirections = json.load(mvmtFile)

        speakerControl.on()
        playsound(soundFile, block=False)

        idx = 0
        startTime = time.monotonic() + offset
        elapsedTime = time.monotonic() - startTime

        while idx < len(mvmtDirections["events"]):

            while (idx < len(mvmtDirections["events"])) and (elapsedTime > mvmtDirections["events"][idx]["time"]):
                if "mouth" == mvmtDirections["events"][idx]["channel-name"]:
                    if "motor-on" == mvmtDirections["events"][idx]["event-name"]:
                        mouthControl.on()
                    elif "motor-off" == mvmtDirections["events"][idx]["event-name"]:
                        mouthControl.off()

                elif "head" == mvmtDirections["events"][idx]["channel-name"]:
                    if "motor-on" == mvmtDirections["events"][idx]["event-name"]:
                        headControl.on()
                    elif "motor-off" == mvmtDirections["events"][idx]["event-name"]:
                        headControl.off()

                elif "body" == mvmtDirections["events"][idx]["channel-name"]:
                    if "motor-on" == mvmtDirections["events"][idx]["event-name"]:
                        bodyControl.on()
                    elif "motor-off" == mvmtDirections["events"][idx]["event-name"]:
                        bodyControl.off()

                idx = idx + 1

            elapsedTime = time.monotonic() - startTime
            sleep(0.01)

        speakerControl.off()

    def button_pressed():
        global isPlaying
        global fileIndex
        print("button pressed!")
        if not isPlaying:
            isPlaying = True
            soundFiles = glob.glob("media/*.wav")
            mtnFiles = glob.glob("media/*.mtn")

            if fileIndex >= min(len(soundFiles), len(mtnFiles)):
                fileIndex = 0

            soundFile = soundFiles[fileIndex]
            fileBase = soundFile.split(".wav")[0]
            mtnFile = fileBase + ".mtn"

            fileIndexOriginal = fileIndex

            while not os.path.exists(mtnFile):
                fileIndex = fileIndex + 1
                if fileIndex >= min(len(soundFiles), len(mtnFiles)):
                    fileIndex = 0

                if fileIndex == fileIndexOriginal:
                    isPlaying = False
                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), "no WAV and MTN have matching names")

                soundFile = soundFiles[fileIndex]
                fileBase = soundFile.split(".wav")[0]
                mtnFile = fileBase + ".mtn"

            parseFile(mtnFile, soundFile)
            isPlaying = False
            fileIndex = fileIndex + 1
        else:
            print("already playing!!")

    button = Button(18)
    button.when_pressed = button_pressed

    while True:
        sleep(0.1)
