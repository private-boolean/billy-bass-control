import time
import keyboard
import argparse

BEAT_CHAR = ' ' # space to record a motion
END_CHAR = 'q' # 'q' to end
START_CHAR = 's' # 's' to start

EXTENSION = '.mtn'

programDescription = ("This program will let you record motor motions by tapping the "
                      "spacebar on your keyboard. You can capture different channels, "
                      "then merge the channels together into a single file.")

INSTRUCTIONS_STRING = ("Press the '%s' key to begin recording. Press the '%s' key to "
                       "initiate a motor event, release the '%s' key to end the event. "
                       "Press the '%s' key to end recording." % (START_CHAR, BEAT_CHAR, BEAT_CHAR, END_CHAR))

MODE_HELP    = ("specify whether you are recording a channel or merging channels together. "
                "If you select 'merge', the program will merge all existing " + EXTENSION + " "
                "files together.")
CHANNEL_HELP = ("name of the channel you'd like to record")
OUTFILE_HELP = ("name of file to output to. The " + EXTENSION + " will not be added automatically.")





def onAction():
    print("action at time ")


def captureMotion(verbose:bool, channelName:str, out_file:str):
    if verbose:
        print("capturing input to channel name %s. Storing in file %s." % (channel, out_file))

    print(INSTRUCTIONS_STRING)

    keyboard.hook_key(' ', onAction)

    # while True:  # making a loop
    #     try:  # used try so that if user pressed other than the given key error will not be shown
    #         if keyboard.read_key
    #             break  # finishing the loop
    #     except:
    #         break  # if user pressed a key other than the given key the loop will break


def mergeFiles(verbose:bool, out_file:str):
    if verbose:
        print("merging all %s files together and outputting to file %s." % (EXTENSION, out_file))



MODE_CAP_STR = 'capture'
MODE_MERGE_STR = 'merge'
OUT_FILE_DEFAULT = '*default-out-file*'
CHANNEL_DEFAULT = 'default-channel'

parser = argparse.ArgumentParser(description=programDescription)
parser.add_argument('--mode',  choices=[MODE_CAP_STR, MODE_MERGE_STR], default=MODE_CAP_STR, help=MODE_HELP)
parser.add_argument('--channel', default=CHANNEL_DEFAULT, help=CHANNEL_HELP)
parser.add_argument('--out-file', default=OUT_FILE_DEFAULT, help=OUTFILE_HELP)
parser.add_argument('-v', '--verbose', action="store_true")

args = parser.parse_args()

mode = args.mode
channel = args.channel
out_file = args.out_file

if out_file == OUT_FILE_DEFAULT:
    if mode == MODE_CAP_STR:
        out_file = channel + EXTENSION
    
    elif mode == MODE_MERGE_STR:
        out_file = 'merge' + EXTENSION
    
    else:
        raise ValueError('unrecognized mode %s' % (mode))


if mode == MODE_CAP_STR:    
    captureMotion(args.verbose, channel, out_file)

elif mode == MODE_MERGE_STR:
    mergeFiles(args.verbose, out_file)

