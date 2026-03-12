import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Ball:
    def __init__(self, diameter, color, e, h0, vx0, x0=0.0, vy0=0.0, v_stop=0.1):
        self.diameter = diameter
        self.radius = diameter / 2.0
        self.color = color
        self.e = e
        self.h0 = h0
        self.vx0 = vx0
        self.x0 = x0
        self.vy0 = vy0
        self.v_stop = v_stop

        self.reset()

    def reset(self):
        self.t = 0.0
        self.x = self.x0
        self.y = self.h0
        self.vx = self.vx0
        self.vy = self.vy0

        self.time_list = []
        self.x_list = []
        self.y_list = []

    def simulate(self, g=9.81, dt=0.01):
        self.reset()

        while True:
            self.time_list.append(self.t)
            self.x_list.append(self.x)
            self.y_list.append(self.y)

            # Update motion
            self.x += self.vx * dt
            self.vy += -g * dt
            self.y += self.vy * dt

            # Bounce condition
            if self.y <= 0:
                self.y = 0
                self.vy = -self.vy * self.e

                if abs(self.vy) < self.v_stop:
                    self.t += dt
                    self.time_list.append(self.t)
                    self.x_list.append(self.x)
                    self.y_list.append(0.0)
                    break

            self.t += dt


def animate_balls(balls, dt=0.01, animation_speed=1.0, save_path=None):
    for ball in balls:
        ball.simulate(dt=dt)

    max_frames = max(len(ball.time_list) for ball in balls)

    all_x = [x for ball in balls for x in ball.x_list]
    all_y = [y for ball in balls for y in ball.y_list]
    max_radius = max(ball.radius for ball in balls)

    x_min = min(all_x) - max_radius - 0.5
    x_max = max(all_x) + max_radius + 0.5
    y_max = max(all_y) + max_radius + 0.5

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, y_max)
    ax.set_title("Bouncing Ball Animation")
    ax.set_xlabel("Horizontal Position (m)")
    ax.set_ylabel("Height (m)")

    # Ground
    ax.axhline(0, linewidth=2)

    ball_artists = []
    trace_artists = []

    for ball in balls:
        ball_artist, = ax.plot(
            [ball.x_list[0]],
            [ball.y_list[0] + ball.radius],
            'o',
            markersize=ball.diameter * 20,
            color=ball.color
        )

        trace_artist, = ax.plot(
            [],
            [],
            ':',
            color=ball.color,
            linewidth=1.5
        )

        ball_artists.append(ball_artist)
        trace_artists.append(trace_artist)

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top')

    def update(frame):
        artists = []

        for i, ball in enumerate(balls):
            idx = min(frame, len(ball.time_list) - 1)

            x = ball.x_list[idx]
            y = ball.y_list[idx]

            ball_artists[i].set_data([x], [y + ball.radius])
            trace_artists[i].set_data(
                ball.x_list[:idx + 1],
                [yy + ball.radius for yy in ball.y_list[:idx + 1]]
            )

            artists.append(ball_artists[i])
            artists.append(trace_artists[i])

        current_time = min(frame * dt, max(ball.time_list[-1] for ball in balls))
        time_text.set_text(f"Time: {current_time:.2f} s")
        artists.append(time_text)

        return artists

    ani = FuncAnimation(
        fig,
        update,
        frames=max_frames,
        interval=animation_speed,
        blit=True,
        repeat=False
    )

    if save_path is not None:
        for i, ball in enumerate(balls):
            trace_artists[i].set_data(
                ball.x_list,
                [yy + ball.radius for yy in ball.y_list]
            )
            ball_artists[i].set_data(
                [ball.x_list[-1]],
                [ball.y_list[-1] + ball.radius]
            )

        final_time = max(ball.time_list[-1] for ball in balls)
        time_text.set_text(f"Time: {final_time:.2f} s")

        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def main():
    ball1 = Ball(
        diameter=0.5,
        color="#54A2D3",
        e=0.8,
        h0=10.0,
        vx0=2.0
    )

    balls = [ball1]

    animate_balls(
        balls,
        dt=0.01,
        animation_speed=1.0,
        save_path=r'res/balls.pdf'
    )


if __name__ == "__main__":
    main()