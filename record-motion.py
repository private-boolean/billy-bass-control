import time
import argparse
import keyboard
import queue
import threading
import json
import glob
from playsound import playsound
import os

BEAT_CHAR = ' '  # space to record a motion
END_CHAR = 'q'  # 'q' to end
START_CHAR = 's'  # 's' to start

EXTENSION = '.mtn'

programDescription = ("This program will let you record motor motions by tapping the "
                      "spacebar on your keyboard. You can capture different channels, "
                      "then merge the channels together into a single file.")

INSTRUCTIONS_STRING = ("Press the '%s' key to begin recording. Press the '%s' key to "
                       "initiate a motor event, release the '%s' key to end the event. "
                       "Press the '%s' key to end recording." % (START_CHAR, BEAT_CHAR, BEAT_CHAR, END_CHAR))

MODE_HELP = ("specify whether you are recording a channel or merging channels together. "
             "If you select 'merge', the program will merge all existing " + EXTENSION + " "
             "files together.")

CHANNEL_HELP = ("name of the channel you'd like to record")
OUTFILE_HELP = ("name of file to output to. The " +
                EXTENSION + " will not be added automatically.")

SOUNDFILE_HELP = ("name of the sound file to play while you record motion.")

beatEvents = queue.Queue()

didPress: bool = False
keepGoing: bool = False


def writeFile(filename, channelName, soundFile):
    global beatEvents

    keepWriting = True

    print('start writeFile thread')

    motionEvents = []

    startTime: float
    while keepWriting:
        # determine event
        event = beatEvents.get(block=True, timeout=None)

        if event.name == START_CHAR:
            startTime = event.time
            print('-- start time: %f' % (startTime))
            
            if os.path.exists(soundFile):
                playsound(soundFile, block=False)

        if event.name == 'space':
            delta = event.time - startTime
            if event.event_type == keyboard.KEY_DOWN:
                print('-- beat start: %f' % (delta))
                motionEvents.append({
                    "time": delta,
                    "channel-name": channelName,
                    "event-name": "motor-on"
                })

            if event.event_type == keyboard.KEY_UP:
                print('-- beat end: %f' % (delta))
                motionEvents.append({
                    "time": delta,
                    "channel-name": channelName,
                    "event-name": "motor-off"
                })

        if event.name == END_CHAR:
            delta = event.time - startTime
            keepWriting = False
            print('-- end time: %f' % (delta))

            events = {"events": motionEvents}

            jsonString = json.dumps(events, indent=4, separators=(", ", ": "))

            # print(jsonString)

            f = open(filename, "w")
            f.write(jsonString)
            f.close()


def startRecordingCallback(kb_event: keyboard.KeyboardEvent):
    global keepGoing, beatEvents
    if not keepGoing:
        beatEvents.put(kb_event)
        keepGoing = True


def endRecordingCallback(kb_event: keyboard.KeyboardEvent):
    global keepGoing, beatEvents
    if keepGoing:
        beatEvents.put(kb_event)
        keepGoing = False


def startBeatCallback(kb_event: keyboard.KeyboardEvent):
    global didPress, beatEvents
    if keepGoing and not didPress:
        beatEvents.put(kb_event)

    didPress = True


def endBeatCallback(kb_event: keyboard.KeyboardEvent):
    global didPress, beatEvents

    if keepGoing and didPress:
        beatEvents.put(kb_event)
        didPress = False


def captureMotion(verbose: bool, channelName: str, out_file: str, sound_file: str):
    if verbose:
        print("capturing input to channel name %s. Storing in file %s." %
              (channel, out_file))

    print(INSTRUCTIONS_STRING)

    keyboard.on_release_key(START_CHAR, startRecordingCallback, suppress=True)
    keyboard.on_press_key(BEAT_CHAR, startBeatCallback, suppress=True)
    keyboard.on_release_key(BEAT_CHAR, endBeatCallback, suppress=True)
    keyboard.on_release_key(END_CHAR, endRecordingCallback)

    t = threading.Thread(target=writeFile, args=[out_file, channelName, sound_file])
    t.start()

    # keyboard.wait()
    t.join()


def mergeFiles(verbose: bool, out_file: str):
    if verbose:
        print("merging all %s files together and outputting to file %s." %
              (EXTENSION, out_file))

    aggregatedMotion = []

    for motionFile in glob.iglob("*.mtn"):
        print("found file %s" % (motionFile))

        f = open(motionFile, "r")
        motionFileJson = json.load(f)
        f.close()

        mergedList = []
        i = 0
        j = 0
        while i < len(motionFileJson["events"]) or j < len(aggregatedMotion):
            if i < len(motionFileJson["events"]) and j < len(aggregatedMotion):
                if motionFileJson["events"][i]["time"] < aggregatedMotion[j]["time"]:
                    mergedList.append(motionFileJson["events"][i])
                    i = i + 1
                else:
                    mergedList.append(aggregatedMotion[j])
                    j = j + 1

            elif i < len(motionFileJson["events"]):
                mergedList.append(motionFileJson["events"][i])
                i = i + 1

            elif j < len(aggregatedMotion):
                mergedList.append(aggregatedMotion[j])
                j = j + 1

        aggregatedMotion = mergedList

    events = {"events": aggregatedMotion}
    jsonString = json.dumps(events, indent=4, separators=(", ", ": "))

    with open(out_file, "w") as f:
        f.write(jsonString)
        f.close()


MODE_CAP_STR = 'capture'
MODE_MERGE_STR = 'merge'
OUT_FILE_DEFAULT = '*default-out-file*'
CHANNEL_DEFAULT = 'default-channel'

parser = argparse.ArgumentParser(description=programDescription)
parser.add_argument(
    '--mode',  choices=[MODE_CAP_STR, MODE_MERGE_STR], default=MODE_CAP_STR, help=MODE_HELP)
parser.add_argument('--channel', default=CHANNEL_DEFAULT, help=CHANNEL_HELP)
parser.add_argument('--out-file', default=OUT_FILE_DEFAULT, help=OUTFILE_HELP)
parser.add_argument('-v', '--verbose', action="store_true")
parser.add_argument('--sound-file', default='', help=SOUNDFILE_HELP)

args = parser.parse_args()

mode = args.mode
channel = args.channel
out_file = args.out_file
sound_file = args.sound_file

if out_file == OUT_FILE_DEFAULT:
    if mode == MODE_CAP_STR:
        out_file = channel + EXTENSION

    elif mode == MODE_MERGE_STR:
        out_file = 'merge' + EXTENSION

    else:
        raise ValueError('unrecognized mode %s' % (mode))


if mode == MODE_CAP_STR:
    captureMotion(args.verbose, channel, out_file, sound_file)

elif mode == MODE_MERGE_STR:
    mergeFiles(args.verbose, out_file)
