from .blocks import block

consoleBlock = block('console')

def _log(message : str, level : str):
    consoleBlock.log([level, message])

def clear():
    consoleBlock.clear()

def logInfo(message : str):
    _log(message, 'info')
    
def logWarning(message : str):
    _log(message, 'warning')

def logError(message : str):
    _log(message, 'error')
    
def logDebug(message : str):
    _log(message, 'debug')
    
def logCritical(message : str):
    _log(message, 'critical')
    
def logTrace(message : str):
    _log(message, 'trace')
    
def logUnknown(message : str):
    _log(message, 'unknown')

