from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
from typing import Union, Optional
from pyalpha.definition import modbus_map
from pyalpha.definition.models import Result, ModbusType, ModbusAccess
import logging
from pyalpha.definition.register_names import *
from pyalpha.utils import (
    convert_to_s16, convert_to_s32, convert_to_u32, 
    decode_registers_to_chars, encode_string_to_registers, 
    split_s32_to_registers, split_u32_to_registers,
    convert_to_i16, convert_to_i32, split_i32_to_registers
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Stride offsets for multi-device registers
_PCS_BAMS_STRIDE = 2400
_PV_INVERTER_STRIDE = 40

def _get_offset(register_address: int, n: int) -> int:
    if n == 1:
        return 0
    if 5100 <= register_address <= 5769:
        return (n - 1) * _PCS_BAMS_STRIDE
    if 1300 <= register_address < 2580:
        return (n - 1) * _PV_INVERTER_STRIDE
    return 0

class AsyncAlphaClient:
    def __init__(self, host='192.168.1.6', port=502, unit_id=1, serial_port=None):
        """Initialize the Async Alpha Modbus client"""
        self.host = host
        self.port = port
        if serial_port:
            self.client = AsyncModbusSerialClient(
                port=serial_port,
                baudrate=9600,
                bytesize=8,
                parity='N',
                stopbits=1
            )
        else:
            self.client = AsyncModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=3
            )
        self.unit_id = unit_id

    async def connect(self):
        """Establish connection to the inverter"""
        try:
            connected = await self.client.connect()
            if connected:
                logger.info("Successfully connected to the inverter")
            else:
                logger.error("Failed to connect to the inverter")
            return connected
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    async def read_register(self, address, count=1, function_code=3):
        """Read register with proper error handling"""
        try:
            result = None
            if function_code == 3:
                result = await self.client.read_holding_registers(
                    address=address,
                    count=count,
                    slave=self.unit_id
                )
            elif function_code == 4:
                result = await self.client.read_input_registers(
                    address=address,
                    count=count,
                    slave=self.unit_id
                )

            if hasattr(result, 'isError') and result.isError():
                logger.error(f"Error reading register {address}: {result}")
                return None
                
            return result.registers if hasattr(result, 'registers') else None
            
        except Exception as e:
            logger.error(f"Exception reading register {address}: {e}")
            return None

    async def write_register(self, address: int, values: Union[int, list]) -> bool:
        """Write to register with proper error handling"""
        try:
            # Single register write
            if isinstance(values, int):
                result = await self.client.write_register(
                    address=address,
                    value=values,
                    slave=self.unit_id
                )
            # Multiple registers write
            else:
                result = await self.client.write_registers(
                    address=address,
                    values=values,
                    slave=self.unit_id
                )

            if hasattr(result, 'isError') and result.isError():
                logger.error(f"Error writing to register {address}: {result}")
                return False
            
            return True

        except Exception as e:
            logger.error(f"Exception writing to register {address}: {e}")
            return False

    async def _ensure_connection(self):
        """Ensure we have an active connection, creating one if needed."""
        if not self.client.connected:
            bool_connected = await self.client.connect()
            if not bool_connected:
                raise Exception("TCP not connected when ensuring connection")

    async def get(self, register_name: str, n: int = 1) -> Optional[Result]:
        """Get a register value by name using utility functions"""
        try:
            register_value = modbus_map[register_name]
            address = register_value.register + _get_offset(register_value.register, n)
            attempt = 0
            while True:
                try:
                    await self._ensure_connection()
                    result = await self.read_register(address, register_value.count, register_value.function_code)
                    if result is None:
                        raise Exception(f"Failed to read register {register_name}")
                    break
                except Exception as e:
                    logger.error(f"Failed to read register {register_name}: {e}")
                    attempt += 1
                    if attempt > 2:
                        raise e
                    continue


            # Convert the result using utility functions
            converted_value = None
            
            if register_value.modbus_type == ModbusType.STRING:
                converted_value = decode_registers_to_chars(result)
                
            elif register_value.modbus_type == ModbusType.U16:
                converted_value = result[0]
                
            elif register_value.modbus_type == ModbusType.S16:
                converted_value = convert_to_s16(result[0])
                
            elif register_value.modbus_type == ModbusType.I16:
                converted_value = convert_to_i16(result[0])
                
            elif register_value.modbus_type == ModbusType.U32:
                converted_value = convert_to_u32(result)
                
            elif register_value.modbus_type == ModbusType.S32:
                converted_value = convert_to_s32(result)
                
            elif register_value.modbus_type == ModbusType.I32:
                converted_value = convert_to_i32(result)
                
            elif register_value.modbus_type == ModbusType.B16:
                converted_value = bin(result[0])[2:].zfill(16)
                
            elif register_value.modbus_type == ModbusType.E16:
                converted_value = hex(result[0])[2:].upper().zfill(4)
            
            else:
                raise ValueError(f"Unsupported ModbusType: {register_value.modbus_type}")

            if isinstance(converted_value, (int, float)) and register_value.modbus_type not in [ModbusType.STRING, ModbusType.B16, ModbusType.E16]:
                converted_value = converted_value * register_value.gain

            return Result(
                name=register_name,
                value=converted_value,
                modbus_type=register_value.modbus_type,
                register=address,
                count=register_value.count,
                function_code=register_value.function_code,
                modbus_unit=register_value.modbus_unit
            )
            
        except Exception as e:
            logger.error(f"Error reading register {register_name}: {str(e)}")
            return None
        
    async def handle_charge_discharge_maintain(
        self,
        charge_discharge: int = 1,  # 0 for maintain, 1 for charge, 2 for discharge
        charge_source: int = 1,     # Source type (0: PV, 1: PV+GRID)
        power_limit: float = 50.0,  # Power limit in percentage
        start_time: int = 0,        # Start time in HHMM format
        end_time: int = 0          # End time in HHMM format
    ) -> bool:
        """
        Configure charging parameters for Period 1 in Economic Mode
        
        Args:
            charge_discharge: 0 for maintain, 1 for charge, 2 for discharge
            charge_source: 0 for PV only, 1 for PV+GRID
            power_limit: Power limit percentage (0-100)
            start_time: Start time in HHMM format (e.g., 1430 for 14:30)
            end_time: End time in HHMM format (e.g., 1630 for 16:30)
            enable_period: Whether to enable Period 1 (default True)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Input validation
            if charge_discharge not in [0, 1, 2]:
                logger.error(f"Invalid charge_discharge value: {charge_discharge}. Must be 0, 1, or 2")
                return False
                
            if charge_source not in [0, 1]:
                logger.error(f"Invalid charge_source value: {charge_source}. Must be 0 or 1")
                return False
                
            if not 0 <= power_limit <= 100:
                logger.error(f"Invalid power_limit value: {power_limit}. Must be between 0 and 100")
                return False
                
            # Validate time format
            for time_val, time_name in [(start_time, "start_time"), (end_time, "end_time")]:
                hours = time_val // 100
                minutes = time_val % 100
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    logger.error(f"Invalid {time_name}: {time_val}. Must be in HHMM format")
                    return False

            # First set Economic Mode (0x0102 = 258)
            if not await self.set(storage_mode_n, 258):
                logger.error("Failed to set Economic Mode")
                return False

            # Set Period Enable Flag
            # bit0 for period1, bits 1-5 for periods 2-6, bits 7-15 reserved
            # We only set bit0 and keep all others as 0
            period_flag = 0b000001
            if not await self.write_register(53006, period_flag):
                logger.error("Failed to set period enable flags")
                return False

            # Set non-volatile memory write control (immediate write)
            if not await self.write_register(53000, 1):
                logger.error("Failed to set write control")
                return False

            registers = [
                charge_discharge,          # 53007 period1_charge_discharge
                charge_source,             # 53008 period1_charge_source
                0xFF,                      # 53009 period1_reserved1 (set to 0xFF as per spec)
                int(power_limit * 10),     # 53010 period1_power_limit (with gain adjustment)
                0xFF,                      # 53011 period1_reserved2 (set to 0xFF as per spec)
                start_time,                # 53012 period1_start_time
                end_time                   # 53013 period1_end_time
            ]

            # Write all registers in one batch using function code 0x10
            result = await self.write_register(53007, registers)
            if not result:
                logger.error("Failed to write charging parameters")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error configuring charging parameters: {str(e)}")
            return False

    async def set(self, register_name: str, value: Union[int, float, str], n: int = 1) -> bool:
        """Set a register value by name using utility functions"""
        try:
            register_info = modbus_map[register_name]
            address = register_info.register + _get_offset(register_info.register, n)
            
            if register_info.access == ModbusAccess.RO:
                logger.error(f"Register {register_name} is read-only")
                return False

            if isinstance(value, (int, float)) and register_info.modbus_type not in [ModbusType.STRING, ModbusType.B16, ModbusType.E16]:
                value = int(value / register_info.gain)

            registers_to_write = []

            if register_info.modbus_type == ModbusType.STRING:
                if not isinstance(value, str):
                    raise ValueError("String value required for STRING type")
                registers_to_write = encode_string_to_registers(value, register_info.count)

            elif register_info.modbus_type == ModbusType.U16:
                if not 0 <= value <= 0xFFFF:
                    raise ValueError("U16 value must be between 0 and 65535")
                registers_to_write = [value]

            elif register_info.modbus_type == ModbusType.S16:
                if not -0x8000 <= value <= 0x7FFF:
                    raise ValueError("S16 value must be between -32768 and 32767")
                if value < 0:
                    value += 0x10000
                registers_to_write = [value]

            elif register_info.modbus_type == ModbusType.I16:
                if not -0x8000 <= value <= 0x7FFF:
                    raise ValueError("I16 value must be between -32768 and 32767")
                if value < 0:
                    value += 0x10000
                registers_to_write = [value]

            elif register_info.modbus_type == ModbusType.U32:
                if not isinstance(value, int):
                    raise ValueError("Integer value required for U32 type")
                registers_to_write = split_u32_to_registers(value)

            elif register_info.modbus_type == ModbusType.S32:
                if not isinstance(value, int):
                    raise ValueError("Integer value required for S32 type")
                registers_to_write = split_s32_to_registers(value)

            elif register_info.modbus_type == ModbusType.I32:
                if not isinstance(value, int):
                    raise ValueError("Integer value required for I32 type")
                registers_to_write = split_i32_to_registers(value)

            elif register_info.modbus_type == ModbusType.B16:
                if isinstance(value, str):
                    try:
                        value = int(value.replace('0b', ''), 2)
                    except ValueError:
                        raise ValueError("Invalid binary string")
                if not 0 <= value <= 0xFFFF:
                    raise ValueError("B16 value must fit in 16 bits")
                registers_to_write = [value]

            elif register_info.modbus_type == ModbusType.E16:
                if isinstance(value, str):
                    try:
                        value = int(value.replace('0x', ''), 16)
                    except ValueError:
                        raise ValueError("Invalid hex string")
                if not 0 <= value <= 0xFFFF:
                    raise ValueError("E16 value must fit in 16 bits")
                registers_to_write = [value]

            else:
                raise ValueError(f"Unsupported ModbusType: {register_info.modbus_type}")

            attempt = 0
            while True:
                try:
                    await self._ensure_connection()
                    # Write registers based on count
                    if len(registers_to_write) == 1:
                        return await self.write_register(address, registers_to_write[0])
                    else:
                        return await self.write_register(address, registers_to_write)
                except Exception as e:
                    logger.error(f"Failed to read register {register_name}: {e}")
                    attempt += 1
                    if attempt > 2:
                        raise e
                    continue

        except Exception as e:
            logger.error(f"Error writing to register {register_name}: {str(e)}")
            return False

    async def close(self):
        """Close the client connection"""
        self.client.close()