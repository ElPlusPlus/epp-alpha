import asyncio

from pyalpha import AsyncAlphaClient
from pyalpha.definition import register_names as rn

# Map ReportResponse argument -> (register_name, transform)
#
# Only fields that are derived from a SINGLE register are listed here so we can
# read the register and show the value exactly as it lands in the report.
#
# Skipped on purpose:
#   - meta_data (and its metadata-only registers: work_mode, work_status,
#     ctrl_ems_mode, ctrl_active_power_setpoint)
#   - constants (day_charge=0, day_discharge=0, total_charge=0, total_discharge=0)
#   - computed-from-multiple-registers fields (see COMPUTED_FIELDS below)
#   - epp_version / device_id / inverter_type / serial_number (not from registers)
REPORT_FIELD_MAP = {
    "active_power":                    (rn.system_active_power_n,            lambda v: int(float(v) * 1000)),
    "pv_power":                        (rn.pv_active_power_n,                lambda v: float(v) * 1000),
    "smart_meter_power":               (rn.grid_meter_total_active_power_n,  lambda v: float(v) * 1000),
    "battery_power":                   (rn.total_battery_power_n,            lambda v: float(v) * 1000),
    "load_power":                      (rn.total_load_power_n,               lambda v: float(v) * 1000),
    "grid_power":                      (rn.grid_meter_total_active_power_n,  lambda v: float(v) * 1000),
    "daily_energy_injected_to_grid":   (rn.grid_meter_reverse_energy_n,      float),
    "daily_energy_purchased_from_grid":(rn.grid_meter_positive_energy_n,     float),
    "daily_battery_charging_energy":   (rn.bams_total_charge_n,              float),
    "daily_battery_discharging_energy":(rn.bams_total_discharge_n,           float),
    "daily_pv_generation":             (rn.total_power_generation_n,         float),
    "charge_discharge_power":          (rn.ctrl_active_power_setpoint_n,     float),
    "state_of_charge":                 (rn.system_soc_n,                     float),
    "max_charge_power":                (rn.system_total_rated_power_n,       lambda v: float(v) * 1000),
    "max_discharge_power":             (rn.system_total_rated_power_n,       lambda v: float(v) * 1000),
    "max_charging_power":              (rn.system_total_rated_power_n,       lambda v: float(v) * 1000),
    "max_discharging_power":           (rn.system_total_rated_power_n,       lambda v: float(v) * 1000),
    "active_grid_frequency":           (rn.grid_meter_frequency_n,           float),
    "phase_1_current":                 (rn.grid_meter_a_current_n,           float),
    "phase_1_voltage":                 (rn.grid_meter_a_voltage_n,           float),
    "phase_2_current":                 (rn.grid_meter_b_current_n,           float),
    "phase_2_voltage":                 (rn.grid_meter_b_voltage_n,           float),
    "phase_3_current":                 (rn.grid_meter_c_current_n,           float),
    "phase_3_voltage":                 (rn.grid_meter_c_voltage_n,           float),
    "power_factor":                    (rn.grid_meter_total_pf_n,            float),
    "battery_temperature":             (rn.bams_max_cell_temp_n,             float),
}

# ReportResponse fields computed from more than one register. Listed here just
# so the test can report them too, using the registers it needs.
COMPUTED_FIELDS = {
    "daily_load_consumption": [
        rn.grid_meter_positive_energy_n,
        rn.bams_total_discharge_n,
        rn.total_power_generation_n,
        rn.grid_meter_reverse_energy_n,
        rn.bams_total_charge_n,
    ],
    "storage_rated_capacity": [
        rn.system_chargeable_energy_n,
        rn.system_dischargeable_energy_n,
    ],
    "state_of_charge_capacity": [
        rn.system_soc_n,
        rn.system_chargeable_energy_n,
        rn.system_dischargeable_energy_n,
    ],
    "depth_of_discharge": [rn.system_soc_n],
}


async def _read(client, register_name):
    """Return the raw register value, or None if it can't be resolved."""
    try:
        result = await client.get(register_name)
    except Exception:
        return None
    if result is None:
        return None
    return result.value


async def main():
    client = AsyncAlphaClient(host="192.168.1.121", port=502, unit_id=1)
    await client.connect()

    print(f"{'REPORT ARGUMENT':<34} {'REGISTER':<28} {'VALUE':>16}")
    print("-" * 82)

    # --- Direct single-register fields ---
    for field, (register_name, transform) in REPORT_FIELD_MAP.items():
        raw = await _read(client, register_name)
        if raw is None:
            print(f"{field:<34} {register_name:<28} {'SKIPPED':>16}")
            continue
        try:
            value = transform(raw)
        except (TypeError, ValueError):
            print(f"{field:<34} {register_name:<28} {'SKIPPED':>16}")
            continue
        print(f"{field:<34} {register_name:<28} {value!s:>16}")

    # --- Computed fields ---
    print("-" * 82)
    print("Computed fields (derived from multiple registers):")

    vals = {}
    for names in COMPUTED_FIELDS.values():
        for name in names:
            if name not in vals:
                vals[name] = await _read(client, name)

    def num(name):
        v = vals.get(name)
        return None if v is None else float(v)

    # daily_load_consumption
    parts = [num(rn.grid_meter_positive_energy_n), num(rn.bams_total_discharge_n),
             num(rn.total_power_generation_n), num(rn.grid_meter_reverse_energy_n),
             num(rn.bams_total_charge_n)]
    if None in parts:
        print(f"  {'daily_load_consumption':<32} {'SKIPPED':>16}")
    else:
        gpe, sdd, dpg, gre, sdc = parts
        print(f"  {'daily_load_consumption':<32} {gpe + sdd + dpg - gre - sdc!s:>16}")

    # storage_rated_capacity
    ce, de = num(rn.system_chargeable_energy_n), num(rn.system_dischargeable_energy_n)
    if ce is None or de is None:
        print(f"  {'storage_rated_capacity':<32} {'SKIPPED':>16}")
        storage_rated_capacity = None
    else:
        storage_rated_capacity = int(round(ce + de))
        print(f"  {'storage_rated_capacity':<32} {storage_rated_capacity!s:>16}")

    # state_of_charge_capacity
    soc = num(rn.system_soc_n)
    if soc is None or storage_rated_capacity is None:
        print(f"  {'state_of_charge_capacity':<32} {'SKIPPED':>16}")
    else:
        print(f"  {'state_of_charge_capacity':<32} {(soc / 100) * storage_rated_capacity!s:>16}")

    # depth_of_discharge
    if soc is None:
        print(f"  {'depth_of_discharge':<32} {'SKIPPED':>16}")
    else:
        print(f"  {'depth_of_discharge':<32} {100 - soc!s:>16}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
