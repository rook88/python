import os
import getpass
import keyring
from cryptography.fernet import Fernet
import win32clipboard

def toClipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()

def myEncrypt(txt):
    f = Fernet(keyring.get_password('secrets', 'folder').encode())
    return f.encrypt(txt.encode()).decode()


def myDecrypt(txt):
    f = Fernet(keyring.get_password('secrets', 'folder').encode())
    return f.decrypt(txt.encode()).decode()


class secretsFolder():
    def __init__(self, folder):
        self.__dict__['_folder'] = folder
    def __getattr__(self, name):
        filePath = os.path.join(self.__dict__['_folder'], name)
        if os.path.isfile(filePath):
            with open(filePath, 'r') as f:
                ret = f.read()
                return myDecrypt(ret)
        else:
            ret = getpass.getpass(f"File {filePath} does not exist. Give {name}")
            self.__setitem__(name, ret)
            return ret
    def __setattr__(self, name, txt):
        with open(os.path.join(self.__dict__['_folder'], name), 'w') as f:
            f.write(myEncrypt(txt))
    def __getitem__(self, name):
        return self.__getattr__(name)
    def __setitem__(self, name, txt):
        self.__setattr__(name, txt)
    def __iter__(self):
         yield from [t for t in os.listdir(self.__dict__['_folder'])]
