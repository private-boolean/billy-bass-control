import time
import os
from playsound import playsound

print('Hello yall from %s' %(os.name))

for loopIdx in range(1, 4):
    print('iteration %d' %(loopIdx))
    time.sleep(1)

playsound('media/dont-worry-be-happy.mp3')

print('All done!')

