import asyncio
from pyalpha import AsyncAlphaClient

async def main():
    client = AsyncAlphaClient(host='192.168.1.121', port=502, unit_id=1)
    await client.connect()

    # Try grid meter total active power (register 126, count 2) with both function codes
    print("Register 126 (grid meter total active power):")
    result_fc3 = await client.read_register(126, 2, function_code=3)
    print(f"  FC03 (holding): {result_fc3}")

    result_fc4 = await client.read_register(126, 2, function_code=4)
    print(f"  FC04 (input):   {result_fc4}")

    # Try a few more meter registers
    print("\nRegister 100 (grid meter A voltage):")
    result_fc3 = await client.read_register(100, 2, function_code=3)
    print(f"  FC03 (holding): {result_fc3}")

    result_fc4 = await client.read_register(100, 2, function_code=4)
    print(f"  FC04 (input):   {result_fc4}")

    print("\nRegister 112 (grid meter frequency):")
    result_fc3 = await client.read_register(112, 1, function_code=3)
    print(f"  FC03 (holding): {result_fc3}")

    result_fc4 = await client.read_register(112, 1, function_code=4)
    print(f"  FC04 (input):   {result_fc4}")

    await client.close()

asyncio.run(main())
