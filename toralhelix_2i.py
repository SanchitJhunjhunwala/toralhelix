
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# For saving GIF
from PIL import Image
import io

images = []

turnsize = 40

for turns in range(1, turnsize + 1):  # turns from 1 to turnsize

    # Define parameters for r_p_toralhelix
    a = 50.0            # semi-major axis of ellipse (example value)
    b = 20.0            # semi-minor axis of ellipse (example value)
    R_mean = 100.0 #mean radius of toral-helix
    R_int_z0 = R_mean - a   # inner radius at z=0 (example value)
    R_ext_z0 = R_mean + a  # outer radius at z=0 (example value)

    # Define parameter
    steps = 500*turns
    P = 1   # upper limit for p
    dp = P/steps
    p = np.linspace(0, P, steps)
    p_code = np.arange(1, (P + dp)*steps, dp*steps )
    pitch_p_toralhelix = a/turns # or replace with a function of p for variable pitch

    p_per_turn = P/turns
    p_per_theta = p_per_turn / (2*np.pi)
    n_steps = P/dp
    theta_per_step = turns*(2*np.pi)/n_steps

    #Assuming here elliptical cross section of torus, else can be array or function if needed

    theta_p_toralhelix = turns*(2*np.pi)*p 





    # for now, assume z is dependent only on p
    z_seg1 = (4* (p[0:int(p_code.shape[0]/4)]) * b)
    z_seg2 = b - ((4*(p[int(p_code.shape[0]/4) : 2 * int(p_code.shape[0]/4)]) * b) - b)
    z_seg3 = - (4*(p[2 * int(p_code.shape[0]/4) : 3 * int(p_code.shape[0]/4)]) * b) + 2*b
    z_seg4 = -4*b + 4*(p[3 * int(p_code.shape[0]/4) : 4 * int(p_code.shape[0]/4)]) * b 
    z_p_toralhelix_rect = np.concatenate((z_seg1, z_seg2, z_seg3, z_seg4))

    # Preallocate the radius array
    r_p_toralhelix = np.zeros_like(z_p_toralhelix_rect)

    i0 = 0
    i1 = z_seg1.shape[0]
    i2 = i1 + z_seg2.shape[0]
    i3 = i2 + z_seg3.shape[0]
    i4 = i3 + z_seg4.shape[0]

    # Compute r_p_toralhelix for 0 <= p <= ceil(P/4)
    r_p_toralhelix[i0:i1] = (R_int_z0 + R_ext_z0)/2 - np.sqrt(a**2 * (1 - (z_seg1**2 / b**2)))
    # Compute r_p_toralhelix for ceil(P/4) < p <= floor(2*P/4)
    r_p_toralhelix[i1:i2] = (R_int_z0 + R_ext_z0)/2 + np.sqrt(a**2 * (1 - (z_seg2**2 / b**2)))
    # Compute r_p_toralhelix for ceil(2*P/4) < p <= floor(3*P/4)
    r_p_toralhelix[i2:i3] = (R_int_z0 + R_ext_z0)/2 + np.sqrt(a**2 * (1 - (z_seg3**2 / b**2)))
    # Compute r_p_toralhelix for ceil(3*P/4) < Sp <= floor(4*P/4)
    r_p_toralhelix[i3:i4] = (R_int_z0 + R_ext_z0)/2 - np.sqrt(a**2 * (1 - (z_seg4**2 / b**2)))


    x_p_toralhelix = r_p_toralhelix * np.cos(theta_p_toralhelix)
    y_p_toralhelix = r_p_toralhelix * np.sin(theta_p_toralhelix)
    
    print(z_p_toralhelix_rect)
    print(x_p_toralhelix)
    print(y_p_toralhelix)


    toralhelix = np.vstack((x_p_toralhelix, y_p_toralhelix, z_p_toralhelix_rect))

    fig = plt.figure(figsize=(8, 6), dpi=400)

    

    ax = fig.add_subplot(111, projection='3d')

    fig.patch.set_facecolor('black')   # figure background
    ax.set_facecolor('black')          # axes background
    # Turn panes black (or transparent)
    ax.xaxis.set_pane_color((0, 0, 0, 1))
    ax.yaxis.set_pane_color((0, 0, 0, 1))
    ax.zaxis.set_pane_color((0, 0, 0, 1))

    # Remove grid
    ax.grid(False)

    # Explicitly disable gridlines on all 3 axes
    ax.xaxis._axinfo["grid"].update({"linewidth": 0})
    ax.yaxis._axinfo["grid"].update({"linewidth": 0})
    ax.zaxis._axinfo["grid"].update({"linewidth": 0})

    # Axis lines + ticks in white
    ax.tick_params(colors='black')
    ax.xaxis.line.set_color('black')
    ax.yaxis.line.set_color('black')
    ax.zaxis.line.set_color('black')

    
    ax.plot(toralhelix[0], toralhelix[1], toralhelix[2])
    

    ax.clear()
    ax.plot(toralhelix[0], toralhelix[1], toralhelix[2], color = 'white')

    # Set limits (so the axes don't jump in animation)
    ax.set_xlim(np.min(x_p_toralhelix), np.max(x_p_toralhelix))
    ax.set_ylim(np.min(y_p_toralhelix), np.max(y_p_toralhelix))
    ax.set_zlim(np.min(z_p_toralhelix_rect), np.max(z_p_toralhelix_rect))

    # Move azimuth by 30 degrees for each frame
    azim_angle = (turns * 0.5) % 360
    elev_angle = (turns * 0.5) % 360
    ax.view_init(elev=elev_angle, azim=azim_angle, )

    plt.tight_layout()
    # Render current frame to image buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    images.append(img.copy())
    buf.close()

    plt.close()

import os
print("CWD:", os.getcwd())

print("Number of frames:", len(images))



# Save as GIF
from pathlib import Path

out_path = Path(r"C:\temp\toralhelix.gif")
out_path.parent.mkdir(parents=True, exist_ok=True)

images[0].save(
    out_path,
    save_all=True,
    append_images=images[1:],
    duration=80,
    loop=0
)

print("Saved to:", out_path)
print("Exists after save:", out_path.exists())
print("File size (bytes):", out_path.stat().st_size if out_path.exists() else "N/A")


# images[0].save('C:\temp\toralhelix_turns.gif', save_all=True, append_images=images[1:], duration=60, loop=0)

print("done")

# Display final plot image
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(toralhelix[0], toralhelix[1], toralhelix[2])
plt.show()