from enum import Enum
from typing import Union

class ModbusAccess(Enum):
    RO = "RO"
    RW = "RW" 
    WO = "WO"

class ModbusType(Enum):
   """Types of data used in Modbus registers"""
   STRING = "String"
   U16 = "U16"        
   E16 = "E16"          
   U32 = "U32"        
   S16 = "S16"      
   S32 = "S32"          
   B16 = "B16"         
   I16 = "I16"
   I32 = "I32"

class ModbusUnit(Enum):
   """Units of measurement for Modbus register values"""
   NONE = ""
   WATT = "W"
   KW = "kW"
   VOLT = "V"
   AMPERE = "A"
   HERTZ = "Hz"
   CELSIUS = "℃"
   KWH = "kWh"
   KVA = "kVA"
   HOUR = "H"
   MINUTE = "min"
   SECOND = "s"
   VA = "VA"
   VAR = "Var"
   KVAR = "kVar"
   PF = "PF"
   PERCENTAGE = "%"
   KOHM = "kΩ"
   WH = "WH"
   MILLISECOND = "MILLISECOND"

class WorkingMode(Enum):
    GENERAL_MODE = 0x0101
    ECONOMIC_MODE = 0x0102
    UPS_MODE = 0x0103
    OFF_GRID_MODE = 0x0200
    EMS_AC_CTRL_MODE = 0x0301
    EMS_GENERAL_MODE = 0x0302
    EMS_BATT_CTRL_MODE = 0x0303
    EMS_OFF_GRID_MODE = 0x0304
    TOU_GENERAL_MODE = 0x0401
    TOU_BATTERY_CHARGE_MODE = 0x0402
    TOU_PV_CHARGING_MODE = 0x0403
    TOU_PEAK_SHIFTING = 0x0404
    TOU_FEED_IN_MODE = 0x0405
    TOU_BATTERY_DISCHARGE_MODE = 0x0406

class ModbusRegister():
   """Definition of a Modbus register including its address range, type, unit and function code"""
   def __init__(self, 
                 register: int,
                 count: int, 
                 function_code: int,
                 modbus_type: ModbusType,
                 modbus_unit: ModbusUnit,
                 access: ModbusAccess = ModbusAccess.RO,
                 gain: float = 1.0
                 ):
        self.register: int = register
        self.count: int = count
        self.function_code: int = function_code 
        self.modbus_type: ModbusType = modbus_type
        self.modbus_unit: ModbusUnit = modbus_unit
        self.access: ModbusAccess = access
        self.gain:float = gain

class Result:
    """Definition of a Returned Modbus register including its address range, type, unit and function code"""
    def __init__(self,
            name: str,
            value: Union[str, int],
            modbus_type: ModbusType,
            register: int,
            count: int, 
            function_code: int,
            modbus_unit: ModbusUnit):
        self.name = name
        self.register: int = register
        self.count: int = count
        self.modbus_type: ModbusType = modbus_type
        self.function_code: int = function_code 
        self.value: Union[str, int] = value
        self.modbus_unit: ModbusUnit = modbus_unit

    def __str__(self):
        return ((self.name or "Name NaN")
                + " ("
                + str(self.register or "")
                + ", "
                + str(self.function_code or "")
                + ", "
                + str(self.count or "")
                + ", "
                + (self.modbus_type.value if self.modbus_type is not None else "")
                + "): "
                + str(self.value or "")
                + " "
                + (self.modbus_unit.value if self.modbus_unit is not None else ""))