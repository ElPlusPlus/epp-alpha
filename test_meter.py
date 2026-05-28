import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    grid_meter_frequency_n,
    grid_meter_total_active_power_n,
    grid_meter_total_reactive_power_n,
    grid_meter_total_apparent_power_n,
    dg_meter_frequency_n,
    dg_meter_total_active_power_n,
    dg_meter_total_reactive_power_n,
    dg_meter_total_apparent_power_n,
    pv_meter_frequency_n,
    pv_meter_total_active_power_n,
    pv_meter_total_reactive_power_n,
    pv_meter_total_apparent_power_n,
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
