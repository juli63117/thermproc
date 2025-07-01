import numpy as np
import matplotlib.pyplot as plt

class HeatEquationSolver:
    def __init__(self, R, koeff, c, T):
        self.R = R  # Радиус
        self.koeff = koeff  # Коэффициент теплопроводности
        self.c = c  # Удельная теплоёмкость
        self.T = T  # Время моделирования

    def run_method_modified(self, I, K):
        h_tetta = 0.5 * np.pi / I  # Шаг по углу
        h_t = self.T / K  # Шаг по времени

        tetta_values = np.linspace(0, np.pi / 2, I)
        t_values = np.linspace(0, self.T, K)

        P = self.koeff * h_t / (self.R**2 * self.c * h_tetta**2)
        Q = self.koeff * h_t / (self.R**2 * self.c * 2 * h_tetta)

        u = [np.cos(tetta_values) ** 6]

        for k in range(1, K):
            p = [0] * I
            q = [0] * I

            p[0] = 4 * P / (1 + 4 * P)
            q[0] = u[k-1][0] / (1 + 4 * P)

            for i in range(1, I - 1):
                denominator = 1 + 2 * P + Q / np.tan(tetta_values[i]) * p[i-1] - P * p[i-1]
                p[i] = (Q / np.tan(tetta_values[i]) + P) / denominator
                q[i] = (u[k-1][i] - Q / np.tan(tetta_values[i]) * q[i-1] + P * q[i-1]) / denominator

            u_I = (u[k-1][I-1] + 2 * P * q[I-2]) / (1 + 2 * P - 2 * P * p[I-2])

            u_k = [0] * I
            u_k[-1] = u_I
            for i in range(I - 2, -1, -1):
                u_k[i] = p[i] * u_k[i+1] + q[i]

            u.append(u_k)

        return tetta_values, t_values, np.array(u)

    def plot_temperature_distribution(self, tetta_values, t_values, u):
        selected_t_indices = np.linspace(0, len(t_values) - 1, 5, dtype=int)

        fig, ax = plt.subplots(figsize=(10, 6))
        for t_idx in selected_t_indices:
            ax.plot(tetta_values, u[t_idx, :], label=f"t = {t_values[t_idx]:.1f}")

        ax.set_xlabel('θ (рад)')
        ax.set_ylabel('Температура')
        ax.set_title('Распределение температуры по углу')
        ax.legend()
        ax.grid(True)
        plt.show()

    def plot_temperature_evolution(self, tetta_values, t_values, u):
        selected_tetta_indices = np.linspace(0, len(tetta_values) - 1, 5, dtype=int)

        fig, ax = plt.subplots(figsize=(10, 6))

        for tetta_idx in selected_tetta_indices:
            ax.plot(t_values, u[:, tetta_idx], label=f"tetta = {tetta_values[tetta_idx]:.2f}")

        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Температура')
        ax.set_title('Зависимость изменения температуры от времени')
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_convergence_tetta_zero(self):
        I_separation = [6]
        K_separation = [6]

        while I_separation[-1] < 32:
            I_separation.append(2 * I_separation[-1])
            K_separation.append(4 * K_separation[-1])

        plt.figure(figsize=(10, 6))
        for I_step, K_step in zip(I_separation, K_separation):
            tetta_values, t_values, u = self.run_method_modified(I_step, K_step)
            k_point = int(74.9 / (self.T / K_step))
            u_0 = u[k_point]
            plt.plot(tetta_values, u_0, label=f'I={I_step}, K={K_step}')

        plt.xlabel('θ')
        plt.ylabel('u(θ, t=74.9)')
        plt.title('Сходимость решения при t=74.9')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_convergence_t_zero(self):
        I_separation = [6]
        K_separation = [6]

        while I_separation[-1] < 32:
            I_separation.append(2 * I_separation[-1])
            K_separation.append(4 * K_separation[-1])

        plt.figure(figsize=(10, 6))
        for I_step, K_step in zip(I_separation, K_separation):
            tetta_values, t_values, u = self.run_method_modified(I_step, K_step)
            i_point = int(0.38 / (0.5 * np.pi / I_step))
            u_0 = u[:, i_point]
            plt.plot(t_values, u_0, label=f'I={I_step}, K={K_step}')
        
        plt.xlabel('t')
        plt.ylabel('u(0, t)')
        plt.title('Сходимость разностного решения при tetta = 0.38')
        plt.legend()
        plt.grid(True)
        plt.show()
