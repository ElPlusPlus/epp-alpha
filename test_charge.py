import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    # Switch to dispatch mode and set charge at 10 kW (negative = charge)
    await client.set(ctrl_ems_mode_n, 3)
    await client.set(ctrl_dispatch_timeout_n, 120)
    await client.set(ctrl_active_power_setpoint_n, -10)
    print("Charge set to 10 kW")

    poll_registers = [
        work_mode_n,
        work_status_n,
        system_mode_n,
        ctrl_ems_mode_n,
        ctrl_active_power_setpoint_n,
        system_chargeable_power_n,
        system_dischargeable_power_n,
        system_soc_n,
        system_active_power_n,
        total_battery_power_n,
        pcs_active_power_n,
        pcs_dc_current_n,
        pcs_dc_power_n,
        grid_meter_total_active_power_n,
        total_load_power_n,
        bams_total_voltage_n,
        bams_total_current_n,
    ]

    for i in range(6):
        await asyncio.sleep(10)
        print(f"\n--- {(i+1)*10}s ---")
        for name in poll_registers:
            result = await client.get(name)
            if result:
                print(f"  {result.name}: {result.value} {result.modbus_unit.value}")

    # Stop charge
    await client.set(ctrl_active_power_setpoint_n, 0)
    print("\nCharge stopped (power set to 0)")

    await client.close()

asyncio.run(main())
