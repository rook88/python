import sys
import os
import inspect
import importlib

__version__ = 1.01

class myFunction():
    def __init__(self, fun, tools):
        self.fun = fun
        self.tools = tools
    def __call__(self, *args, **kwargs):
        return self.fun(*args, **kwargs)
    def edit(self):
        self.tools.edit(self.fun.__name__)
    def edit(self):
        self.tools.clear(self.fun.__name__)

class Tools():
    def __init__(self, folder):
        self.__dict__['_folder'] = folder
        sys.path.append(folder)
    def filePath(self, name):
        return os.path.join(self.__dict__['_folder'], name) + '.py'
    def getCode(self, name):
        with open(self.filePath(name), 'r') as f:
            code = f.read()
        return code
    def edit(self, name):
        if name in sys.modules:
            with open(sys.modules[name].__file__, 'r') as f:
                code = f.read()
        elif os.path.isfile(self.filePath(name)):
            getCode(name)
        else:
            code = f"def {name}():\n    return '{name} called'"
        get_ipython().set_next_input(f"%%writefile {self.filePath(name)}\n{code}")
    def __getattr__(self, name):
        try:
            print(f"import {name}")
            __import__(name)
            importlib.reload(sys.modules[name])
            try:
                ret = myFunction(getattr(sys.modules[name], name), self)
            except AttributeError:
                print(f'Module {name} has no function {name}')
                self.edit(name)
                return None
            self.__dict__[name] = ret
            return ret
        except ModuleNotFoundError:
            print(f"{name} not found")
            self.edit(name)
            if name in self.__dict__:
                del self.__dict__[name]
    def commit(self, function):
        with open(self.filePath(function.__name__), 'w') as f:
            f.write(inspect.getsource(function))
        if function.__name__ in self.__dict__:
            del self.__dict__[function.__name__]
    def clear(self, name):
        del self.__dict__[name]
    def __iter__(self):
         yield from [t.replace('.py', '') for t in os.listdir(self.__dict__['_folder']) if not '__' in t]
    def find(self, txt):
        return [name for name in self if txt.lower() in self.getCode(name).lower()]
            
