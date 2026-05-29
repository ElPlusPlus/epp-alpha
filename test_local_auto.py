import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    # Switch to local auto mode
    await client.set(ctrl_ems_mode_n, 0)
    print("Set to Local Auto Mode")

    poll_registers = [
        work_mode_n,
        work_status_n,
        system_mode_n,
        ctrl_ems_mode_n,
        ctrl_active_power_setpoint_n,
        system_soc_n,
        system_active_power_n,
        total_battery_power_n,
        grid_meter_total_active_power_n,
        total_load_power_n,
    ]

    for i in range(6):
        await asyncio.sleep(10)
        print(f"\n--- {(i+1)*10}s ---")
        for name in poll_registers:
            result = await client.get(name)
            if result:
                print(f"  {result.name}: {result.value} {result.modbus_unit.value}")

    await client.close()

asyncio.run(main())
