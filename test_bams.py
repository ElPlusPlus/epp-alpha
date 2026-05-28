import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    bams_total_voltage_n,
    bams_total_current_n,
    bams_soc_n,
    bams_soh_n,
    bams_max_charge_current_n,
    bams_max_discharge_current_n,
    bams_actual_power_n,
    bams_max_cell_voltage_n,
    bams_min_cell_voltage_n,
    bams_max_cell_temp_n,
    bams_min_cell_temp_n,
    bams_cycle_count_n,
    bams_comm_status_n,
    bams_total_charge_n,
    bams_total_discharge_n,
    bams_cycle_count_n
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
