# module containing useful functions
import re

def searchIndex(item, list):
    for i in range(0, len(list)):
        if list[i].id == str(item):
            return i
    return False

def searchContacts():
    return 'Hello'
