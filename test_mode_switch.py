import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    # Switch to local auto first
    await client.set(ctrl_ems_mode_n, 0)
    await asyncio.sleep(3)
    result = await client.get(system_mode_n)
    print(f"After set 0: SystemMode = {result.value}")

    # Switch back to dispatch mode
    await client.set(ctrl_ems_mode_n, 3)
    await asyncio.sleep(3)
    result = await client.get(system_mode_n)
    print(f"After set 3: SystemMode = {result.value}")

    await client.close()

asyncio.run(main())
