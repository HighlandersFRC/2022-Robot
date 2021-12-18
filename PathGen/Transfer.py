import math
import Convert

isTimedOut = False

def get(name):
    match name:
        case 'isTimedOut':
            return isTimedOut
        
        case _:
            return None

def set(name, val):
    match name:
        case 'isTimedOut':
            isTimedOut = val

        case _:
            pass