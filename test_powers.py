import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    # System powers
    system_total_rated_power_n,
    system_active_power_n,
    system_reactive_power_n,
    system_chargeable_power_n,
    system_dischargeable_power_n,
    available_reactive_power_n,
    total_battery_power_n,
    total_load_power_n,
    # PV powers
    pv_theoretical_active_power_n,
    pv_available_active_power_n,
    pv_available_reactive_power_n,
    pv_active_power_n,
    pv_reactive_power_n,
    pv_inverter_active_power_n,
    # Grid/load powers
    grid_side_load_total_power_n,
    backup_side_load_total_power_n,
    # Grid meter powers
    grid_meter_a_active_power_n,
    grid_meter_b_active_power_n,
    grid_meter_c_active_power_n,
    grid_meter_a_apparent_power_n,
    grid_meter_b_apparent_power_n,
    grid_meter_c_apparent_power_n,
    grid_meter_total_active_power_n,
    grid_meter_total_reactive_power_n,
    grid_meter_total_apparent_power_n,
    # DG meter powers
    dg_meter_a_active_power_n,
    dg_meter_b_active_power_n,
    dg_meter_c_active_power_n,
    dg_meter_a_apparent_power_n,
    dg_meter_b_apparent_power_n,
    dg_meter_c_apparent_power_n,
    dg_meter_total_active_power_n,
    dg_meter_total_reactive_power_n,
    dg_meter_total_apparent_power_n,
    # PV meter powers
    pv_meter_a_active_power_n,
    pv_meter_b_active_power_n,
    pv_meter_c_active_power_n,
    pv_meter_a_apparent_power_n,
    pv_meter_b_apparent_power_n,
    pv_meter_c_apparent_power_n,
    pv_meter_total_active_power_n,
    pv_meter_total_reactive_power_n,
    pv_meter_total_apparent_power_n,
    # PCS powers
    pcs_a_active_power_n,
    pcs_b_active_power_n,
    pcs_c_active_power_n,
    pcs_active_power_n,
    pcs_reactive_power_n,
    pcs_apparent_power_n,
    pcs_dc_power_n,
    # BAMS
    bams_actual_power_n,
    # STS grid side powers
    sts_a_active_power_grid_n,
    sts_b_active_power_grid_n,
    sts_c_active_power_grid_n,
    sts_a_apparent_power_grid_n,
    sts_b_apparent_power_grid_n,
    sts_c_apparent_power_grid_n,
    sts_total_active_power_grid_n,
    sts_total_reactive_power_grid_n,
    sts_total_apparent_power_grid_n,
    # STS load side powers
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
    # Control setpoint
    ctrl_active_power_setpoint_n,
    ctrl_reactive_power_setpoint_n,
    # DCDC powers
    dcdc_bus_power_n,
    dcdc_dc_power_n,
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
