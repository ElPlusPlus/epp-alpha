import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    pcs_start_stop_state_n,
    pcs_fault_state_n,
    pcs_fault1_n,
    pcs_fault2_n,
    pcs_fault3_n,
    pcs_fault4_n,
    pcs_fault5_n,
    bams_fault1_n,
    bams_fault2_n,
    bams_fault3_n,
    bams_fault4_n,
    bams_fault5_n,
    bams_fault6_n,
    bams_fault7_n,
    bams_fault8_n,
    bams_comm_status_n,
    pcs_comm_status_n,
]

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    for name in registers:
        result = await client.get(name)
        if result:
            print(f"{result.name}: {result.value}")
        else:
            print(f"{name}: READ FAILED")

    await client.close()

asyncio.run(main())
