"""
built_killer is an built killer that might be needed for killing tasks with Python.
built_killer works only with Windows and not other platforms, as it uses the Sys32
taskkill.exe file to kill processes. It has a kill function to kill a process.
Thanks for reading!
   - Love, KareemTheBest
"""
from sys import platform as sysplatform

def kill(process=''):
    'Kill a process.'
    import os
    os.system("taskkill /f /im "+process)

def idkill(process=''):
    'Kill a process with an ID.'
    import os
    os.system("taskkill /f /im "+process)
    return id(process)

def amdkill(process=''):
    'Kill a process with an AMD.'
    import os
    os.system("taskkill /f /im "+process)
    return "amd-"+process

def amdidkill(process=''):
    'Kill a process with an AMD ID.'
    import os
    os.system("taskkill /f /im "+process)
    return "amd-"+process+"+"+str(id(process))

def platkill(process=''):
    'Kill a process with "sys.platform".'
    import os
    os.system("taskkill /f /im "+process)
    return sysplatform

import built_killer.built_killer as _hidden
import built_killer as __init__

_hidden.__file__ = _hidden.__file__.replace("\\", "/").replace("/", "\\")
__file__ = _hidden.__file__
_hidden.__name__ = __name__
__all__ = ["kill", "idkill", "amdkill", "amdidkill", "platkill", "sysplatform", "_Module"]
_hidden.__all__ = __all__
_Module = _hidden

#end

print("Welcome to built_killer v.{}! Made by kareemPypi @ PyPI / kareemsaf @ Github.".format(__init__._str_version))
print("Your current sysplatform is {}. Thank you for using!".format(sysplatform))

del __init__ # To not keep the imported __init__ file or else it will allow people to see the file.
