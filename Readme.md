Billy Bass Control Suite
========================

The code in this github repo is designed to control a Big Mouth Billy Bass singing fish, which has been modified to be controlled by a Raspberry Pi. The hardware mod is described [in this blog post][1].

[![asdf](https://res.cloudinary.com/marcomontalbano/image/upload/v1639893863/video_to_markdown/images/youtube--LDU_Txk06tM-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=LDU_Txk06tM "asdf")


## Setup
Once you've cloned the repo, install the following python libraries on your main machine and Raspberry Pi:
* `playsound`
* `TkCircuit`

Install these libraries only on your Raspberry Pi:
* `gpiozero`
* `playwav`

## Teaching Billy a New Song
1. Get a .WAV file that you want your Billy Bass to sing. I recommend iTunes for purchasing DRM-free music. You may wish to use a program like [Audacity][2] to trim your song down to less than 1 minute (songs significantly longer than 1 minute are annoying).
2. Run the `record-motion.py` script to author motion vectors for the lips, head, and tail.
3. Run the `record-motion.py` script a final time to collate all the motion vectors together into a single file.
4. Copy the `.wav` audio file and `.mtn` motion vectors to Billy
5. Push the button and enjoy your dancing fish.

## `record-motion.py`
how to use the script here, and how to run emulator.py to check

## transferring files to billy
how to transfer files using scp
how to create a task so billy runs the python script at startup




[1]: link-to-be-added.
[2]: https://www.audacityteam.org/