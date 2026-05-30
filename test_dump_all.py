import asyncio
import csv
from pyalpha import AsyncAlphaClient
from pyalpha.definition import modbus_map

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    rows = []
    for name in modbus_map:
        reg = modbus_map[name]
        result = await client.get(name)
        rows.append({
            'name': name,
            'address': reg.register,
            'function_code': reg.function_code,
            'type': reg.modbus_type.value,
            'unit': reg.modbus_unit.value,
            'gain': reg.gain,
            'value': result.value if result else 'ERROR',
        })

    with open('register_dump.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['address', 'name', 'function_code', 'type', 'unit', 'gain', 'value'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} registers to register_dump.csv")
    await client.close()

asyncio.run(main())
