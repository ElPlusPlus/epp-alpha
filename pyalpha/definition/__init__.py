from pyalpha.definition.register_names import *
from pyalpha.definition.register_values import *

modbus_map = {
    # Device Information
    device_sn_n: device_sn,

    # Summary Registers
    work_mode_n: work_mode,
    work_status_n: work_status,
    system_total_rated_power_n: system_total_rated_power,
    system_chargeable_energy_n: system_chargeable_energy,
    system_dischargeable_energy_n: system_dischargeable_energy,
    system_chargeable_power_n: system_chargeable_power,
    system_dischargeable_power_n: system_dischargeable_power,
    max_power_charge_available_time_n: max_power_charge_available_time,
    max_power_discharge_available_time_n: max_power_discharge_available_time,
    system_soc_n: system_soc,
    system_active_power_n: system_active_power,
    system_reactive_power_n: system_reactive_power,
    system_total_charge_n: system_total_charge,
    system_total_discharge_n: system_total_discharge,
    system_daily_charge_n: system_daily_charge,
    system_daily_discharge_n: system_daily_discharge,
    available_reactive_power_n: available_reactive_power,
    total_power_generation_n: total_power_generation,
    daily_power_generation_n: daily_power_generation,
    pv_installed_capacity_n: pv_installed_capacity,
    pv_theoretical_active_power_n: pv_theoretical_active_power,
    pv_available_active_power_n: pv_available_active_power,
    pv_available_reactive_power_n: pv_available_reactive_power,
    pv_active_power_n: pv_active_power,
    pv_reactive_power_n: pv_reactive_power,
    grid_side_load_total_power_n: grid_side_load_total_power,
    backup_side_load_total_power_n: backup_side_load_total_power,
    total_load_power_n: total_load_power,
    total_battery_power_n: total_battery_power,
    platform_type_n: platform_type,
    protocol_version_n: protocol_version,
    dual_power_state_n: dual_power_state,
    system_mode_n: system_mode,
}
