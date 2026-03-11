import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    # Parameters
    g = 9.81
    e = 0.8
    dt = 0.01

    # Initial conditions
    x0 = 0.0
    h0 = 10.0
    vx0 = 2.0      # initial horizontal speed (m/s)
    vy0 = 0.0      # initial vertical speed (m/s)

    # Stop condition
    v_stop = 0.1

    # Ball appearance
    ball_radius = 0.25

    # Simulation variables
    t = 0.0
    x = x0
    y = h0
    vx = vx0
    vy = vy0

    time_list = []
    x_list = []
    y_list = []

    # Simulate until the ball has effectively stopped
    while True:
        time_list.append(t)
        x_list.append(x)
        y_list.append(y)

        # Update motion
        x += vx * dt
        vy += -g * dt
        y += vy * dt

        # Bounce condition
        if y <= 0:
            y = 0
            vy = -vy * e

            # Stop when vertical bounce becomes very small
            if abs(vy) < v_stop:
                time_list.append(t + dt)
                x_list.append(x)
                y_list.append(0)
                break

        t += dt

    # Figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(min(x_list) - 1, max(x_list) + 1)
    ax.set_ylim(0, h0 + 1)
    ax.set_title("Bouncing Ball Animation with Trajectory")
    ax.set_xlabel("Horizontal Position (m)")
    ax.set_ylabel("Height (m)")

    # Ground
    ax.axhline(0, linewidth=2)

    # Ball
    ball, = ax.plot([x_list[0]], [y_list[0] + ball_radius], 'o', markersize=20)

    # Dotted trace line
    trace, = ax.plot([], [], ':', linewidth=1.5)

    # Time label
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top')

    def update(frame):
        # Ball position
        ball.set_data([x_list[frame]], [y_list[frame] + ball_radius])

        # Trajectory trace
        trace.set_data(x_list[:frame + 1], [y + ball_radius for y in y_list[:frame + 1]])

        # Time text
        time_text.set_text(f"Time: {time_list[frame]:.2f} s")

        return ball, trace, time_text

    ani = FuncAnimation(
        fig,
        update,
        frames=len(time_list),
        interval=1,
        blit=True,
        repeat=False
    )

    plt.show()

if __name__ == "__main__":
    main()