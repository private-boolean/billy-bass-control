import time
import keyboard
import argparse

beatChar = ' ' # space to record a motion
endChar = 'q' # 'q' to end

programDescription = ("This program will let you record motor motions by tapping the "
                      "spacebar on your keyboard. You can capture different channels, "
                      "then merge the channels together into a single file.")

MODE_CAP_STR = 'capture'
MODE_MERGE_STR = 'merge'
OUT_FILE_DEFAULT = '*default-out-file*'
CHANNEL_DEFAULT = 'default-channel'

EXTENSION = '.mtn'

parser = argparse.ArgumentParser(description=programDescription)
parser.add_argument('--mode', type=str, nargs=1, choices=[MODE_CAP_STR, MODE_MERGE_STR] default=MODE_CAP_STR)
parser.add_argument('--channel', type=str, nargs=1, default=CHANNEL_DEFAULT)
parser.add_argument('--out-file', type=str, nargs=1, default=OUT_FILE_DEFAULT)

args = parser.parse_args()



if out_file == OUT_FILE_DEFAULT:
    if mode == MODE_CAP_STR:
        out_file = channel + EXTENSION
    
    elif mode == MODE_MERGE_STR:
        out_file = 'merge' + EXTENSION




while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed(' '):  # if key ' ' is pressed 
            print('You Pressed A Key!')
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break