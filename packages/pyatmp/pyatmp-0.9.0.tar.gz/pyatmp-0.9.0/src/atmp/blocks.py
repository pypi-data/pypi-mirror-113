import sqlite3 as sql
import numpy as np
from . import TCP
import time

indexColumnName = "idx"
timeColumnName = "timestamp"



class Database():
    def __init__(self):
        self.path = ""
        self.opened = False
        
    def execute(self, data : str):
        if(not self.opened):
            self.open()
        assert self.opened, "Cannot open database"
        return self.db.execute(data)
        
    def commit(self, alias : str = None, full : bool = False):
        self.db.commit()
        if(not alias is None):
            TCP.updateDatabase(alias, full)
        else:
            TCP.updateDatabase()
        
        
    def open(self):
        self.path = TCP.getDatabasePath()
        if(type(self.path) == bytearray):
            self.path = self.path.decode()
        try:
            self.db = sql.connect(self.path, timeout=10)
            self.opened = True
        except sql.Error as er:
            print("Couldn't open data base : " + er.args)
            self.opened = False

    def _blockExists(self, alias):
        val = self.execute('SELECT count(*) FROM sqlite_master WHERE type=\'table\' AND name=\'' + alias + '\'')
        exists = False
        for v in val:
            exists = v[0] > 0
        return exists
        
    def _listBlocks(self):
        val = self.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
        tables = []
        for x in val:
            name = x[0]
            if(name != 'sqlite_sequence'):
                tables.append(name)
        return tables
    
    
    def _newBlock(self, alias : str):
        if(not self._blockExists(alias)):
            command = 'CREATE TABLE \'' + alias + '\' (\"' + indexColumnName + '\" INTEGER PRIMARY KEY AUTOINCREMENT, \"' + timeColumnName + '\" REAL)'
            self.execute(command)
            #for c in columns:
            #    if(c[1] == int):
            #        columnsStr += c[0] + " INTEGER"
            #    elif(c[1] == float):
            #        columnsStr += c[0] + " REAL"
            #    elif(c[1] == str):
            #        columnsStr += c[0] + " TEXT"
            #    elif(c[1] == bytearray):
            #        columnsStr += c[0] + " BLOB"
            #    count += 1
        self.commit()   
    
    def _removeBlock(self, alias : str):
        self.execute('DROP TABLE ' + alias)
        self.execute('DELETE FROM sqlite_sequence WHERE name = \'' + alias + '\'')
        self.commit()
    
    def _truncate(self, alias):
        self.execute('DELETE FROM ' + alias)
        self.execute('DELETE FROM sqlite_sequence WHERE name = \'' + alias + '\'')
        self.commit(alias, True)
            
db = Database()

    
def removeBlock(alias : str):
    if(db._blockExists(alias)):
        db._removeBlock(alias)
        return True
    else:
        return False
    
    
    
def block(alias : str):
    if(not db._blockExists(alias)):
        db._newBlock(alias)
    return Block(alias)
    
    
    
def listBlocks():
    return db._listBlocks()
    


class Block:
    def __init__(self, alias : str):
        self.alias = alias
        self.exists = True

    def _listColumns(self):
        if(not self.exists):
            return None
        else:
            cursor = db.execute('select * from ' + self.alias)
            names = list(map(lambda x: x[0], cursor.description))
            return names
    
    def _columnName(self, index : int):
        
        if(index == 0):
            # "index" column
            name = indexColumnName
        elif(index == 1):
            # "time" column
            name = timeColumnName
        else:
            name = ""
            value = index - 1
            while(value > 0):
                mod = (value-1) % 26
                c = chr(mod + ord('A'))
                name = c + name
                value = (value-mod)//26
        return name
        
    def columnTypeByDataType(self, dataType):
        if(dataType is None):
            return "NULL"
        if(dataType == int):
            return "INTEGER"
        elif(dataType == float):
            return "REAL"
        elif(dataType == str):
            return "TEXT"
        elif(dataType == bytearray):
            return "BLOB"
        else:
            return "NULL"

    def _rows(self):
        vals = db.execute('SELECT COUNT(*) FROM ' + self.alias + '')
        for v in vals:
            return v[0]

    def _insertRow(self, timestamp : float):
        command = 'INSERT INTO ' + self.alias + ' (%s) VALUES(%f)' % (timeColumnName, timestamp)
        try:
            db.execute(command)
        except:
            print("Error trying to do command : " + command)
        return self._rows()# Returning the index of the added row
        
    def _setSingleValue(self, line, column, value):
        # Line=0 -> column A
        assert line <= self._rows(), "Current line doesn't exist !"

        strVal = str(value)
        strVal = strVal.replace('\'', '\'\'')
        
        command = 'UPDATE %s SET %s = \'' % (self.alias, self._columnName(column+2)) + strVal + '\' WHERE ' + indexColumnName + '= %d' % (line)
        try:
            db.execute(command)      
        except:
            print("Error trying to do command : " + command)

    def _addColumn(self, alias : str, columnType : str):
        db.execute('ALTER TABLE \'' + self.alias + '\' ADD COLUMN \'' + alias + '\' ' + columnType + ' ;')
        
    
    def log(self, values):
        if(not self.exists):
            print("Block has been deleted")
            return None
        else:
            self.logAt(time.time(), values)
        
    def logAt(self, timestamp : float, values):
        if(not self.exists):
            print("Block has been deleted")
        else:
            columnCount = len(self._listColumns())

            if(type(values) == tuple or type(values) == list):
                # List / Tuple
                columnsNeeded = len(values)
            elif(type(values) == np.ndarray):
                # List of values
                columnsNeeded = values.size
            else:
                # Single value
                columnsNeeded = 1

            # Adding missing columns
            for i in range(0, columnsNeeded+2): #2 : index + time
                if(i >= columnCount):
                    self._addColumn(self._columnName(i), self.columnTypeByDataType('TEXT'))
            
            
            # Adding a new row with the timestamp
            row = self._insertRow(timestamp)
            if(columnsNeeded > 1):
                #Adding multiple values
                for i in range(0, len(values)):
                    self._setSingleValue(row, i, values[i]) 
            else:
                #Adding a single value
                self._setSingleValue(row, 0, values)

            db.commit(self.alias, False)

    def clear(self):
        if(not self.exists):
            print("Block has been deleted")
        else:
            db._truncate(self.alias)

    def delete(self):
        db._removeBlock(self.alias)
        self.exists = False
        
