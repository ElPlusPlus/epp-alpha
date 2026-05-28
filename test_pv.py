import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    pv_inverter_active_regulator_n,
    pv_inverter_a_voltage_n,
    pv_inverter_b_voltage_n,
    pv_inverter_c_voltage_n,
    pv_inverter_frequency_n,
    pv_inverter_daily_energy_n,
    pv_inverter_active_power_n,
    pv_inverter_work_mode_n,
    pv_inverter_temperature_n,
    pv_inverter_total_energy_n,
    pv_inverter_fault1_n,
    pv_inverter_fault2_n,
    pv_inverter_comm_status_n,
    pv_inverter_real_comm_status_n,
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
