"""
simplepipes.

A python library to interact with other programming languages that support the simplepipes project.
"""

__version__ = "0.1.0"
__author__ = "Matthias Wijnsma"
__email__ = "matthiasx95@gmail.com"

from json.decoder import JSONDecodeError
from typing import *
import threading
import time
import json
import os

class Pipe:
    def __init__(self, name: str, onChange: Optional[Callable], pipeLocation: str = ".") -> None:
        # Making sure the pipefile exists
        self.pipeFile = f"{pipeLocation}/.simplepipes/{name}.pipe"
        if not os.path.exists(self.pipeFile):
            if not os.path.exists(f"{pipeLocation}/.simplepipes"):
                os.mkdir(f"{pipeLocation}/.simplepipes")
            with open(self.pipeFile, "w") as f:
                f.write("{}")
        
        # Initializing variables
        self.name = name
        self.pipeLocation = pipeLocation
        
        # Starting a watch thread to watch the pipe
        self.onChange = onChange
        if onChange != None:
            self.thread = threading.Thread(target=self.__watch)
            self.thread.start()
    
    def __watch(self) -> None:
        self.last = None
        while True:
            with open(self.pipeFile, "r") as f:
                content = f.read()
                if content != self.last:
                    self.last = content
                    try:
                        self.onChange(json.loads(content))
                    except JSONDecodeError:
                        self.last = None
                        time.sleep(0.25)
            time.sleep(0.1)
    
    def clear(self) -> None:
        "Clears the contents of the pipe."

        self.last = "{}"
        with open(self.pipeFile, "w") as f:
            f.write("{}")
    
    def set(self, key: str, value: str) -> None:
        "Sets the value of the specified key to the given value."

        with open(self.pipeFile, "r") as f:
            current = json.load(f)
        
        current[key] = value

        with open(self.pipeFile, "w") as f:
            json.dump(current, f)
        
        with open(self.pipeFile, "r") as f:
            self.last = f.read()