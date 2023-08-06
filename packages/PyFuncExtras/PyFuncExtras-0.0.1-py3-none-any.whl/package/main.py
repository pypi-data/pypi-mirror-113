import os
import subprocess
import time
import sys

def wipe():
    if os.name == "posix":
        os.system('clear')
    elif os.name == "nt":
        os.system('cls')
    else:
        raise OSError('Invalid OS: {os.name}')
def countTo(number):
    for number in range(number+1):
        print(number)
    print("done")
def osfind():
    if os.name == "posix":
        return 'UNIX'
    else:
        return 'NT'
def errorCreate(exceptiontype):
    with open('C:\Program Files\Python39\Lib\extras.py','a') as f:
        f.write(f'\nclass {exceptiontype}(Exception):\n')
        f.write(f'    __module__ = Exception.__module__\n')
        f.write(f'# {exceptiontype} error, created by ErrorCreate')
        f.close()

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def uninstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])
def wait(duration):
    time.sleep(float(duration))
def call(command):
    subprocess.call(str(command))
def findIndexes(item, alist):
    indexes = [n for n in range(len(alist)) if alist[n] == item]
    if len(indexes) > 0:
        return indexes
    else:
        return None
def debugPrint(debugName, text):
    print('Debug:',debugName+':',text)
def failText(text):
    print('\033[91m'+text+'\033[0m')
def typewrite(text,duration,waitDuration=1):
    for l in text:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(duration)
    time.sleep(waitDuration)