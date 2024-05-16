#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation

# Constants
G = 6.67430e-11  # gravitational constant, m^3 kg^-1 s^-1
M = 5.972e24  # mass of the central body (e.g., Earth), kg

# Function to compute the derivatives
def derivatives(y):
    r, v = y[:2], y[2:]
    r_norm = np.linalg.norm(r)
    a = -G * M * r / r_norm**3
    return np.array([v[0], v[1], a[0], a[1]])

# Runge-Kutta 4th Order method
def rk4_step(y, dt):
    k1 = dt * derivatives(y)
    k2 = dt * derivatives(y + 0.5 * k1)
    k3 = dt * derivatives(y + 0.5 * k2)
    k4 = dt * derivatives(y + k3)
    return y + (k1 + 2*k2 + 2*k3 + k4) / 6

# Get initial conditions from the user
r0_x = float(input("Enter the initial x position (in meters): "))
r0_y = float(input("Enter the initial y position (in meters): "))
v0_x = float(input("Enter the initial x velocity (in meters/second): "))
v0_y = float(input("Enter the initial y velocity (in meters/second): "))
t0 = float(input("Enter the initial time (in seconds): "))

r0 = np.array([r0_x, r0_y])  # initial position
v0 = np.array([v0_x, v0_y])  # initial velocity

# Time parameters
t_end = 27.3 * 24 * 3600  # 27.3 days in seconds (one orbit period)
dt = 3600  # time step in seconds

# Initial state vector
y = np.array([r0[0], r0[1], v0[0], v0[1]])

# Arrays to store the positions and times for output
output_data = []

# Time integration loop
t = t0
while t < t0 + t_end:
    output_data.append([t, y[0], y[1]])
    y = rk4_step(y, dt)
    t += dt

# Convert output data to numpy array
output_data = np.array(output_data)

# Save the output data to a file
output_file_path = 'orbit_output.txt'
np.savetxt(output_file_path, output_data, header='Time(s) x(m) y(m)', comments='')

# Convert trajectory list to numpy array for plotting
r_traj = output_data[:, 1:3]

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))

# Load Earth image
earth_img_path = 'C:/Users/Noha/Downloads/RK4-Orbiting-Satellite-master/RK4-Orbiting-Satellite-master/earth.png'
earth_img = plt.imread(earth_img_path)
earth_marker = OffsetImage(earth_img, zoom=0.1)
earth_ab = AnnotationBbox(earth_marker, (0, 0), frameon=False)
ax.add_artist(earth_ab)

# Load orbiting body icon
orbiting_body_img_path = 'C:/Users/Noha/Downloads/RK4-Orbiting-Satellite-master/RK4-Orbiting-Satellite-master/sat.png'
orbiting_body_img = plt.imread(orbiting_body_img_path)
orbiting_body_marker = OffsetImage(orbiting_body_img, zoom=0.02)
orbiting_body_ab = AnnotationBbox(orbiting_body_marker, (r_traj[0][0], r_traj[0][1]), frameon=False)
ax.add_artist(orbiting_body_ab)

# Plot the trajectory of the orbiting body
ax.plot(r_traj[:, 0], r_traj[:, 1], color='black')  # plot the orbit trajectory

# Labels and title
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title('2-body system using RK4 Integration')

# Update function for animation
def update(frame):
    # Update the position of the satellite icon
    orbiting_body_ab.xybox = (r_traj[frame][0], r_traj[frame][1])
    return orbiting_body_ab,

# Create animation
ani = FuncAnimation(fig, update, frames=len(r_traj), interval=50, blit=True)

# Save the output data to a file at each step
output_file_dynamic_path = 'orbit_output_dynamic.txt'
with open(output_file_dynamic_path, 'w') as f:
    f.write('Time(s) x(m) y(m)\n')
    for data in output_data:
        f.write(f"{data[0]} {data[1]} {data[2]}\n")

plt.show()
