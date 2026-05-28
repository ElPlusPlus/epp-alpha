import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    work_mode_n,
    work_status_n,
    system_total_rated_power_n,
    system_chargeable_energy_n,
    system_dischargeable_energy_n,
    system_chargeable_power_n,
    system_dischargeable_power_n,
    max_power_charge_available_time_n,
    max_power_discharge_available_time_n,
    system_soc_n,
    system_active_power_n,
    system_reactive_power_n,
    system_total_charge_n,
    system_total_discharge_n,
    system_daily_charge_n,
    system_daily_discharge_n,
    available_reactive_power_n,
    total_power_generation_n,
    daily_power_generation_n,
    pv_installed_capacity_n,
    pv_theoretical_active_power_n,
    pv_available_active_power_n,
    pv_available_reactive_power_n,
    pv_active_power_n,
    pv_reactive_power_n,
    grid_side_load_total_power_n,
    backup_side_load_total_power_n,
    total_load_power_n,
    total_battery_power_n,
    platform_type_n,
    protocol_version_n,
    dual_power_state_n,
    system_mode_n,
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
