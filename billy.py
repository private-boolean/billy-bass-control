import glob
from gpiozero import LED, Button
import time
from time import sleep
import json
import os
import errno
import subprocess

isPlaying = False
fileIndex = 0

mouthControl = LED(24)
headControl = LED(4)
bodyControl = LED(23)
speakerControl = LED(25)


def parseFile(sourceFile, soundFile, offset=0.0):
    mvmtFile = open(sourceFile)
    mvmtDirections = json.load(mvmtFile)
    speakerControl.on()

    audioProcess = subprocess.Popen(['aplay',soundFile])

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

    audioProcess.wait()
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

        print("parseFile(%s, %s)" % (mtnFile, soundFile))
        parseFile(mtnFile, soundFile, -0.5)
        isPlaying = False
        fileIndex = fileIndex + 1
    else:
        print("already playing!!")


button = Button(18)
button.when_pressed = button_pressed

# do it once when program starts
# button_pressed()

while True:
    sleep(0.1)
