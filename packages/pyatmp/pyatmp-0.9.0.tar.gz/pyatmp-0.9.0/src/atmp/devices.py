from . import TCP
import os
import importlib


def device(alias: str):
    # full driver path
    driverPath = TCP.getDeviceDriverPath(alias)
    if(driverPath is not None):
        # extract the filename without the extension
        path, module = os.path.split(driverPath)
        moduleName, extension = os.path.splitext(module)

        spec = importlib.util.spec_from_file_location(moduleName, driverPath)
        if(spec is None):
            print(f"Le driver n'as pas été trouvé ({driverPath})")
            return None
        else:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.new(Device(alias))


class Device():
    def __init__(self, alias: str):
        self.alias = alias

    def write(self, data):
        if(type(data) == str):
            data = data.encode()
        return TCP.writeToDevice(self.alias, data)

    def read(self, timeout_ms=0):
        return TCP.readFromDevice(self.alias, False, timeout_ms)

    def close(self):
        return TCP.closeDevice(self.alias)
