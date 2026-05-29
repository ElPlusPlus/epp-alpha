import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    sts_ab_voltage_grid_n,
    sts_bc_voltage_grid_n,
    sts_ca_voltage_grid_n,
    sts_frequency_grid_n,
    sts_a_active_power_grid_n,
    sts_b_active_power_grid_n,
    sts_c_active_power_grid_n,
    sts_a_apparent_power_grid_n,
    sts_b_apparent_power_grid_n,
    sts_c_apparent_power_grid_n,
    sts_total_active_power_grid_n,
    sts_total_reactive_power_grid_n,
    sts_total_apparent_power_grid_n,
    sts_total_pf_grid_n,
    sts_ab_voltage_load_n,
    sts_bc_voltage_load_n,
    sts_ca_voltage_load_n,
    sts_a_current_load_n,
    sts_b_current_load_n,
    sts_c_current_load_n,
    sts_frequency_load_n,
    sts_a_active_power_load_n,
    sts_b_active_power_load_n,
    sts_c_active_power_load_n,
    sts_a_reactive_power_load_n,
    sts_b_reactive_power_load_n,
    sts_c_reactive_power_load_n,
    sts_a_apparent_power_load_n,
    sts_b_apparent_power_load_n,
    sts_c_apparent_power_load_n,
    sts_total_active_power_load_n,
    sts_total_reactive_power_load_n,
    sts_total_apparent_power_load_n,
    sts_total_pf_load_n,
    sts_comm_timeout_n,
    sts_grid_mode_n,
    sts_work_state_n,
    sts_module_temperature_n,
    sts_fault1_n,
    sts_fault2_n,
    sts_fault3_n,
    sts_fault4_n,
    sts_comm_status_n,
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
