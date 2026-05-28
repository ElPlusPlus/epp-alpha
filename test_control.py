import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    ctrl_active_power_setpoint_n,
    ctrl_reactive_power_setpoint_n,
    ctrl_dispatch_timeout_n,
    ctrl_dispatch_interrupt_mode_n,
    ctrl_on_off_command_n,
    ctrl_fault_clearance_n,
    ctrl_ems_mode_n,
]

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    for name in registers:
        result = await client.get(name)
        if result:
            print(f"{result.name}: {result.value} {result.modbus_unit.value}")
        else:
            print(f"{name}: READ FAILED")

    await client.close()

asyncio.run(main())
