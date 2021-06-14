import configparser

from gpiozero import exc

config = configparser.ConfigParser()

CONFIG_FILENAME = '.billy.conf'

try:
    config.read_file(open(CONFIG_FILENAME, 'r'))

except FileNotFoundError:
    config['DEFAULT'] = {'DefaultDelay': -0.75,
                         'MediaDir': 'media',
                         'PlayOnStart': 'no',
                         'StartRandom': 'yes'
                         }

    config['all-star'] = {'delay': -0.5}
    with open(CONFIG_FILENAME, 'w') as billyConfigFile:
        config.write(billyConfigFile)

for a in config:
    print(a)

print(list(config.keys()))

try:
    lookupDelay = float(config['all-star']['delay'])
except KeyError:
    lookupDelay = -0.75
mDelay = lookupDelay + 1.1
print(str(mDelay))


# config['DEFAULT'] = {'DefaultDelay': -0.5,
#                      'MediaDir': 'media',
#                      'PlayOnStart': 'no',
#                      'StartRandom': 'yes'
#                      }

# config['all-star'] = {'delay': -0.5}


# config['dont-worry'] = {'delay': -0.5}

# with open('billy.ini', 'w') as billyConfigFile:
#     config.write(billyConfigFile)
