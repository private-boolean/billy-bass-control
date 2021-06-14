import glob
from gpiozero import LED, Button
import time
from time import sleep
import json
import os
import errno
import subprocess
import configparser

isPlaying = False
fileIndex = 0

mouthControl = LED(24)
headControl = LED(4)
bodyControl = LED(23)
speakerControl = LED(25)

# Configuration files

CONFIG_FILENAME = '.billy.conf'

CONFIG_DEFAULT_MEDIA_DIR = 'media'
CONFIG_DEFAULT_DELAY = -0.75
CONFIG_DEFAULT_PLAY_ON_START = False


def refreshConfig(config):
    try:
        config.read_file(open(CONFIG_FILENAME, 'r'))

    except FileNotFoundError:
        # if config file can't be opened, create one with defaults
        config['DEFAULT'] = {'DefaultDelay': CONFIG_DEFAULT_DELAY,
                             'MediaDir':     CONFIG_DEFAULT_MEDIA_DIR,
                             'PlayOnStart':  CONFIG_DEFAULT_PLAY_ON_START
                             }

        config['all-star'] = {'delay': -0.5}
        with open(CONFIG_FILENAME, 'w') as billyConfigFile:
            config.write(billyConfigFile)

    return config

# this function parses a source file and sound file and animates the fish
def parseFile(sourceFile, soundFile, offset=0.0):
    mvmtFile = open(sourceFile)
    mvmtDirections = json.load(mvmtFile)

    speakerControl.on()

    audioProcess = subprocess.Popen(['aplay', soundFile])

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
    global config

    print("button pressed!")
    if not isPlaying:
        isPlaying = True

        config = refreshConfig(config)

        try:
            mediaFolder = config['DEFAULT']['MediaDir']
        except KeyError:
            mediaFolder = 'media'

        soundFileSearch = "." + os.sep + mediaFolder + os.sep + "*.wav"
        mtnFileSearch = "." + os.sep + mediaFolder + os.sep + "*.mtn"
        soundFiles = glob.glob(soundFileSearch)
        mtnFiles = glob.glob(mtnFileSearch)

        if fileIndex >= min(len(soundFiles), len(mtnFiles)):
            fileIndex = 0

        if (len(soundFiles) != 0) and (len(mtnFiles) != 0):
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
            try:
                songname = fileBase.split(os.pathsep)[-1]
                lookupDelay = config[songname].getfloat('delay')

            except KeyError:
                lookupDelay = CONFIG_DEFAULT_DELAY

            parseFile(mtnFile, soundFile, lookupDelay)
            fileIndex = fileIndex + 1
            # end of if (len(soundFiles) != 0) and (len(mtnFiles) != 0):
        isPlaying = False
    else:
        print("already playing!!")

config = configparser.ConfigParser()
config = refreshConfig(config)

button = Button(18)
button.when_pressed = button_pressed

# do it once when program starts
try:
    shouldPlay = config['DEFAULT'].getboolean('PlayOnStart')
except KeyError:
    shouldPlay = CONFIG_DEFAULT_PLAY_ON_START

if shouldPlay:
    button_pressed()

while True:
    sleep(0.1)
