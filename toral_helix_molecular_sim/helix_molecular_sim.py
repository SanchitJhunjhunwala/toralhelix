
# Toral Helix Molecular Encounter Simulation
# -------------------------------------------
# Simulates two helical molecular strands undergoing Brownian motion,
# with weak interaction potentials. Estimates residence-time enhancement
# and binding probability for enzyme encounters.

import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
N = 40
steps = 40000
dt = 1e-4

kT = 0.1
gamma = 1.0

# Helix parameters
R = 2.0
r = 0.5
n = 3

# Binding parameters
bind_distance = 0.4
tau_threshold = 0.002

theta = np.linspace(0, 2*np.pi, N)

def toral_helix(theta, phase=0):
    x = (R + r*np.cos(n*theta)) * np.cos(theta + phase)
    y = (R + r*np.cos(n*theta)) * np.sin(theta + phase)
    z = r*np.sin(n*theta)
    return np.vstack([x,y,z]).T

def LJ_force(r):
    d = np.linalg.norm(r)
    if d == 0:
        return np.zeros(3)
    A = 1.0
    B = 1.0
    f = 12*A/d**13 - 6*B/d**7
    return f * r/d

strand1 = toral_helix(theta, phase=0)
strand2 = toral_helix(theta, phase=0.5)

vel1 = np.zeros_like(strand1)
vel2 = np.zeros_like(strand2)

encounter_time = 0
binding_events = 0

trajectory_dist = []

for step in range(steps):

    noise1 = np.random.normal(0, np.sqrt(kT), strand1.shape)
    noise2 = np.random.normal(0, np.sqrt(kT), strand2.shape)

    for i in range(N):
        for j in range(N):

            rvec = strand1[i] - strand2[j]
            f = LJ_force(rvec)

            vel1[i] += -f*dt
            vel2[j] += f*dt

    vel1 += noise1
    vel2 += noise2

    strand1 += vel1 * dt
    strand2 += vel2 * dt

    # measure closest distance between strands
    min_d = np.min([np.linalg.norm(a-b) for a in strand1 for b in strand2])
    trajectory_dist.append(min_d)

    if min_d < bind_distance:
        encounter_time += dt
    else:
        if encounter_time > tau_threshold:
            binding_events += 1
        encounter_time = 0

print("Binding events detected:", binding_events)

plt.plot(trajectory_dist)
plt.xlabel("time step")
plt.ylabel("min strand distance")
plt.title("Helix proximity over time")
plt.show()

#visualize the strands in a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(strand1[:,0], strand1[:,1], strand1[:,2], color='red')
ax.scatter(strand2[:,0], strand2[:,1], strand2[:,2], color='blue')
plt.show()