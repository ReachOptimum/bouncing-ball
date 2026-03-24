from time import time
import numpy as np
import matplotlib.pyplot as plt
import os
import logs

logs.ntfy("Starting bouncing ball simulation...")
logs.log.info("Starting bouncing ball simulation...")

# -----------------------------
# Parameters
# -----------------------------
g = 9.81         # gravity [m/s^2]
k = 2000.0       # spring constant [N/m]
b = 5.0          # damping constant [N.s/m]
t_max = 3.0      # total simulation time [s]
dt = 0.0005      # time step [s]


class Ball:
    def __init__(self, mass: float, radius: float, x0: float = 1.0, v0: float = 0.0):
        """
        Args:
            mass:   Ball mass [kg]
            radius: Ball radius [m]
            x0:     Initial height of ball center [m]
            v0:     Initial velocity [m/s]
        """
        self.mass = mass
        self.radius = radius
        self.x0 = x0
        self.v0 = v0

        # Simulation results (populated after calling simulate)
        self.t = None
        self.x = None
        self.v = None
        self.a = None

    def _compute_acceleration(self, x: float, v: float) -> float:
        """Compute acceleration based on current position and velocity."""
        if x > self.radius:
            return -g                                           # free flight
        else:
            return (-b * v + k * (self.radius - x) - self.mass * g) / self.mass  # contact

    def simulate(self, t_max: float = t_max, dt: float = dt) -> None:
        """Run the Euler integration and store results in self.t / x / v / a."""
        self.t = np.arange(0, t_max + dt, dt)
        n = len(self.t)

        self.x = np.zeros(n)
        self.v = np.zeros(n)
        self.a = np.zeros(n)

        self.x[0] = self.x0
        self.v[0] = self.v0

        for i in range(n - 1):
            acc = self._compute_acceleration(self.x[i], self.v[i])
            self.a[i] = acc
            self.v[i + 1] = self.v[i] + acc * dt
            self.x[i + 1] = self.x[i] + self.v[i + 1] * dt

        self.a[-1] = self.a[-2]

    def plot(self, save_path: str = "images/bb.pdf") -> None:
        """Plot position over time and optionally save to file."""
        if self.t is None:
            raise RuntimeError("No simulation data — call simulate() first.")

        plt.figure(figsize=(8, 4))
        plt.plot(self.t, self.x)
        plt.xlabel("Time [s]")
        plt.ylabel("Position [m]")
        plt.title("Bouncing ball simulation")
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.grid(True)
        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)

        plt.show()


def main():
    ball = Ball(mass=0.2, radius=0.05, x0=1.0, v0=0.0)
    ball.simulate(t_max=t_max, dt=dt)
    ball.plot(save_path="images/bb.pdf")


if __name__ == "__main__":
    main()
    logs.ntfy("Bouncing ball simulation completed successfully.")
    logs.log.info("Bouncing ball simulation completed successfully.")