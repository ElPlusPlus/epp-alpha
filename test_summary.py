import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import system_soc_n, system_active_power_n

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    soc = await client.get(system_soc_n)
    power = await client.get(system_active_power_n)

    print(f"System SOC: {soc.value} {soc.modbus_unit.value}")
    print(f"System Active Power: {power.value} {power.modbus_unit.value}")

    await client.close()

asyncio.run(main())
