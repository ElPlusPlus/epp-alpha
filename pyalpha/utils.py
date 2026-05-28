from typing import List

def decode_registers_to_chars(registers: List[int]) -> str:
    """Convert registers to ASCII string, removing null bytes"""
    result = ''
    for register in registers:
        # Convert each register (16 bits) to two characters
        high_byte = register >> 8
        low_byte = register & 0xFF
        if high_byte != 0:
            result += chr(high_byte)
        if low_byte != 0:
            result += chr(low_byte)
    return result.strip()

def convert_to_u32(registers: List[int]) -> int:
    """Convert two registers to unsigned 32-bit integer"""
    if len(registers) != 2:
        raise ValueError("U32 conversion requires exactly 2 registers")
    return (registers[0] << 16) | registers[1]

def convert_to_s32(registers: List[int]) -> int:
    """Convert two registers to signed 32-bit integer"""
    if len(registers) != 2:
        raise ValueError("S32 conversion requires exactly 2 registers")
    value = (registers[0] << 16) | registers[1]
    # Convert to signed
    if value & 0x80000000:
        value -= 0x100000000
    return value

def convert_to_s16(value: int) -> int:
    """Convert register to signed 16-bit integer"""
    if value & 0x8000:
        value -= 0x10000
    return value

def encode_string_to_registers(value: str, count: int) -> List[int]:
    """Convert string to list of registers"""
    # Pad string to even length if necessary
    if len(value) % 2:
        value += '\0'
    
    registers = []
    # Process two characters at a time
    for i in range(0, len(value), 2):
        high_byte = ord(value[i])
        # If there's a second character, use it; otherwise use null byte
        low_byte = ord(value[i + 1]) if i + 1 < len(value) else 0
        register = (high_byte << 8) | low_byte
        registers.append(register)
    
    # Pad with zeros if necessary to match expected count
    while len(registers) < count:
        registers.append(0)
    
    return registers[:count]  # Truncate if string was too long

def split_u32_to_registers(value: int) -> List[int]:
    """Split 32-bit unsigned integer into two 16-bit registers"""
    if not 0 <= value <= 0xFFFFFFFF:
        raise ValueError("U32 value out of range")
    high = (value >> 16) & 0xFFFF
    low = value & 0xFFFF
    return [high, low]

def split_s32_to_registers(value: int) -> List[int]:
    """Split 32-bit signed integer into two 16-bit registers"""
    if not -0x80000000 <= value <= 0x7FFFFFFF:
        raise ValueError("S32 value out of range")
    # Convert negative numbers to 32-bit unsigned
    if value < 0:
        value += 0x100000000
    return split_u32_to_registers(value)

def convert_to_i16(value: int) -> int:
    """Convert register to signed 16-bit integer (same as S16)"""
    if value & 0x8000:
        value -= 0x10000
    return value

def convert_to_i32(registers: List[int]) -> int:
    """Convert two registers to signed 32-bit integer (same as S32)"""
    if len(registers) != 2:
        raise ValueError("I32 conversion requires exactly 2 registers")
    value = (registers[0] << 16) | registers[1]
    if value & 0x80000000:
        value -= 0x100000000
    return value

def split_i32_to_registers(value: int) -> List[int]:
    """Split 32-bit signed integer into two 16-bit registers (same as S32)"""
    if not -0x80000000 <= value <= 0x7FFFFFFF:
        raise ValueError("I32 value out of range")
    if value < 0:
        value += 0x100000000
    return split_u32_to_registers(value)