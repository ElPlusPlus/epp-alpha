import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    pcs_start_stop_state_n,
    pcs_fault_state_n,
    pcs_grid_frequency_n,
    pcs_work_mode_n,
    pcs_dc_voltage_n,
    pcs_dc_current_n,
    pcs_dc_power_n,
    pcs_active_power_n,
    pcs_reactive_power_n,
    pcs_daily_charge_n,
    pcs_daily_discharge_n,
    pcs_comm_status_n,
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
