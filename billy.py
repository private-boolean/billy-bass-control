import time
import os
import vlc

print('Hello yall from %s' %(os.name))

for loopIdx in range(1, 4):
    print('iteration %d' %(loopIdx))
    time.sleep(1)

instance = vlc.Instance()
p = instance.media_player_new()
m = instance.media_new('media/dont-worry-be-happy.mp3')
p.set_media(m)
p.play()

print('All done!')

