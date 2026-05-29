import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    grid_meter_comm_status_n,
    grid_meter_ct_ratio_n,
    grid_meter_pt_ratio_n,
    grid_meter_a_voltage_n,
    grid_meter_b_voltage_n,
    grid_meter_c_voltage_n,
    grid_meter_a_current_n,
    grid_meter_b_current_n,
    grid_meter_c_current_n,
    grid_meter_total_active_power_n,
    grid_meter_positive_energy_n,
    grid_meter_reverse_energy_n,
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
