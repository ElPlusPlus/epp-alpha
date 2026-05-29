import asyncio
from pyalpha import AsyncAlphaClient
from pyalpha.definition.register_names import *

registers = [
    # Grid Gateway Meter
    grid_meter_a_voltage_n,
    grid_meter_b_voltage_n,
    grid_meter_c_voltage_n,
    grid_meter_a_current_n,
    grid_meter_b_current_n,
    grid_meter_c_current_n,
    grid_meter_frequency_n,
    grid_meter_total_pf_n,
    grid_meter_a_active_power_n,
    grid_meter_b_active_power_n,
    grid_meter_c_active_power_n,
    grid_meter_a_apparent_power_n,
    grid_meter_b_apparent_power_n,
    grid_meter_c_apparent_power_n,
    grid_meter_total_active_power_n,
    grid_meter_total_reactive_power_n,
    grid_meter_total_apparent_power_n,
    grid_meter_positive_energy_n,
    grid_meter_reverse_energy_n,
    grid_meter_max_demand_n,
    grid_meter_comm_status_n,
    grid_meter_ct_ratio_n,
    grid_meter_pt_ratio_n,
    # Diesel Generator Meter
    dg_meter_a_voltage_n,
    dg_meter_b_voltage_n,
    dg_meter_c_voltage_n,
    dg_meter_a_current_n,
    dg_meter_b_current_n,
    dg_meter_c_current_n,
    dg_meter_frequency_n,
    dg_meter_total_pf_n,
    dg_meter_a_active_power_n,
    dg_meter_b_active_power_n,
    dg_meter_c_active_power_n,
    dg_meter_a_apparent_power_n,
    dg_meter_b_apparent_power_n,
    dg_meter_c_apparent_power_n,
    dg_meter_total_active_power_n,
    dg_meter_total_reactive_power_n,
    dg_meter_total_apparent_power_n,
    dg_meter_positive_energy_n,
    dg_meter_reverse_energy_n,
    dg_meter_max_demand_n,
    dg_meter_comm_status_n,
    dg_meter_ct_ratio_n,
    dg_meter_pt_ratio_n,
    # PV Grid-tie Meter
    pv_meter_a_voltage_n,
    pv_meter_b_voltage_n,
    pv_meter_c_voltage_n,
    pv_meter_a_current_n,
    pv_meter_b_current_n,
    pv_meter_c_current_n,
    pv_meter_frequency_n,
    pv_meter_total_pf_n,
    pv_meter_a_active_power_n,
    pv_meter_b_active_power_n,
    pv_meter_c_active_power_n,
    pv_meter_a_apparent_power_n,
    pv_meter_b_apparent_power_n,
    pv_meter_c_apparent_power_n,
    pv_meter_total_active_power_n,
    pv_meter_total_reactive_power_n,
    pv_meter_total_apparent_power_n,
    pv_meter_positive_energy_n,
    pv_meter_reverse_energy_n,
    pv_meter_max_demand_n,
    pv_meter_comm_status_n,
    pv_meter_ct_ratio_n,
    pv_meter_pt_ratio_n,
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
