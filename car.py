import tkinter as tk
from tkinter import ttk

# Function to calculate energy consumption rate, stats calculated using https://ev-database.org/car/1991/Tesla-Model-3 
def calculate_energy_consumption_rate(driving_mode, vehicle_speed, outside_temperature, aux_systems_usage, trip_length):
     # Coefficients (can be changed as different cars will have different variables)
    optimal_rate = 120  # Wh/km under optimal conditions
    highest_rate = 250  # Wh/km under highest consumption conditions
    base_rate = 50 if driving_mode == "Highway" else 30  # Base rate for highway is higher
    # Coefficients can be changed for different cars
    speed_coefficient = (highest_rate - optimal_rate) / 100 
    temp_deviation_coefficient = (highest_rate - optimal_rate) / 50 
    aux_systems_coefficient = {"Low": 0, "Medium": 2, "High": 5} 
    optimal_temperature = 20
    temperature_deviation = abs(outside_temperature - optimal_temperature)
    #calculate energy_consumption_rate
    energy_consumption_rate = base_rate + (speed_coefficient * vehicle_speed) + (temp_deviation_coefficient * temperature_deviation) + aux_systems_coefficient[aux_systems_usage]

    return energy_consumption_rate

# Function to provide optimization recommendations
def get_optimization_recommendations(energy_consumption_rate, driving_mode, vehicle_speed, outside_temperature, aux_systems_usage):
    recommendations = []
    if energy_consumption_rate > 120:  # Assuming 120 Wh/km is the optimal rate
        if driving_mode == "Highway" and vehicle_speed > 100:  # Assuming 90 km/h as a more efficient highway speed
            recommendations.append("Reduce speed to around 100 km/h on highways.")
        if driving_mode == "City" and vehicle_speed > 60:  # Assuming 90 km/h as a more efficient highway speed
            recommendations.append("Reduce speed to around 60 km/h on city streets.")
        if driving_mode == "City":
           recommendations.append("Switch vehicle to eco mode.") 
        if 15  < outside_temperature < 25:  # Assuming 15°C to 25°C as optimal temperature range
            recommendations.append("Consider adjusting HVAC usage to moderate levels, outside temperature is optimal")
        if aux_systems_usage == "High" or aux_systems_usage == "Medium":
            recommendations.append("Reduce usage of non-essential auxiliary systems.")
    return recommendations if recommendations else ["Battery consumption is within optimal rates."]

def calculate_remaining_range(battery_capacity, energy_consumption_rate):
    if energy_consumption_rate == 0:
        return float('inf') 
    energy_consumption_rate_kWh_km = energy_consumption_rate / 1000
    remaining_range = battery_capacity / energy_consumption_rate_kWh_km
    return remaining_range

def on_submit():
    driving_mode = driving_mode_var.get()
    vehicle_speed = float(vehicle_speed_entry.get())
    outside_temperature = float(outside_temperature_entry.get())
    aux_systems_usage = aux_systems_var.get()
    trip_length = float(trip_length_entry.get())
    battery_capacity = 60  # Assuming a fixed battery capacity for calculation, this can change from car to car. For this case, we assume its a Tesla Modle 3 lithium battery.

    energy_consumption_rate = calculate_energy_consumption_rate(driving_mode, vehicle_speed, outside_temperature, aux_systems_usage, trip_length)
    remaining_range = calculate_remaining_range(battery_capacity, energy_consumption_rate)

    result_label.config(text=f"Energy Consumption Rate: {energy_consumption_rate:.2f} Wh/km")
    range_label.config(text=f"Estimated Range: {remaining_range:.2f} km")

    recommendations = get_optimization_recommendations(energy_consumption_rate, driving_mode, vehicle_speed, outside_temperature, aux_systems_usage)
    recommendations_label.config(text="Recommendations for Optimization:\n" + "\n".join(recommendations))

# GUI Setup
root = tk.Tk()
root.title("Autonomous Vehicle Energy Optimization")

driving_mode_var = tk.StringVar(value="City")
ttk.Radiobutton(root, text="Highway", variable=driving_mode_var, value="Highway").grid(row=0, column=0)
ttk.Radiobutton(root, text="City", variable=driving_mode_var, value="City").grid(row=0, column=1)

vehicle_speed_entry = ttk.Entry(root)
vehicle_speed_entry.grid(row=1, column=1)
ttk.Label(root, text="Vehicle Speed (km/h):").grid(row=1, column=0)

outside_temperature_entry = ttk.Entry(root)
outside_temperature_entry.grid(row=2, column=1)
ttk.Label(root, text="Outside Temperature (°C):").grid(row=2, column=0)

aux_systems_var = tk.StringVar(value="Low")
aux_menu = ttk.Combobox(root, textvariable=aux_systems_var, values=["Low", "Medium", "High"])
aux_menu.grid(row=3, column=1)
ttk.Label(root, text="Auxiliary Systems Usage:").grid(row=3, column=0)

trip_length_entry = ttk.Entry(root)
trip_length_entry.grid(row=4, column=1)
ttk.Label(root, text="Trip Length (km):").grid(row=4, column=0)

submit_button = ttk.Button(root, text="Calculate", command=on_submit)
submit_button.grid(row=5, column=0, columnspan=2)

result_label = ttk.Label(root, text="Energy Consumption Rate: ")
result_label.grid(row=6, column=0, columnspan=2, sticky="w")

recommendations_label = ttk.Label(root, text="Recommendations for Optimization: ")
recommendations_label.grid(row=7, column=0, columnspan=2, sticky="w")

range_label = ttk.Label(root, text="Estimated Range: ")
range_label.grid(row=8, column=0, columnspan=2, sticky="w")

root.mainloop()