import tkinter as tk
from tkinter import ttk
from analytic import HeatEquationSolver


class HeatEquationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование теплового уравнения")
        self.initialize_main_menu()

    def initialize_main_menu(self):
        """Инициализация главного меню выбора графиков."""
        self.clear_window()

        label = tk.Label(self.root, text="Выберите тип графика:", font=("Arial", 14))
        label.pack(pady=10)

        btn_temp_evolution = tk.Button(self.root, text="Динамика процесса при фиксированных углах",
                                       command=self.setup_temp_evolution_window)
        btn_temp_evolution.pack(pady=5)

        btn_temp_distribution = tk.Button(self.root, text="Динамика процесса при фиксированных моментах времени",
                                           command=self.setup_temp_distribution_window)
        btn_temp_distribution.pack(pady=5)

        btn_convergence = tk.Button(self.root, text="Сходимость решения",
                                     command=self.setup_convergence_window)
        btn_convergence.pack(pady=5)

    def setup_temp_evolution_window(self):
        """Окно настройки параметров для графика изменения температуры во времени."""
        self.initialize_input_window("Динамика процесса при фиксированных углах",
                                     self.plot_temp_evolution)

    def setup_temp_distribution_window(self):
        """Окно настройки параметров для графика изменения температуры по углу."""
        self.initialize_input_window("Динамика процесса при фиксированных моментах времени",
                                     self.plot_temp_distribution)

    def setup_convergence_window(self):
        """Окно выбора типа графика для сходимости решения."""
        self.clear_window()

        label = tk.Label(self.root, text="Выберите тип сходимости:", font=("Arial", 14))
        label.pack(pady=10)

        btn_convergence_tetta = tk.Button(self.root, text="Сходимость при t = 74.9",
                                          command=self.plot_convergence_tetta_zero)
        btn_convergence_tetta.pack(pady=5)

        btn_convergence_t = tk.Button(self.root, text="Сходимость при θ = 0.38",
                                      command=self.plot_convergence_t_zero)
        btn_convergence_t.pack(pady=5)

        btn_back = tk.Button(self.root, text="Назад", command=self.initialize_main_menu)
        btn_back.pack(pady=20)

    def initialize_input_window(self, title, plot_function):
        """Создание окна ввода параметров."""
        self.clear_window()

        label = tk.Label(self.root, text=title, font=("Arial", 14))
        label.pack(pady=10)

        # Поля ввода параметров
        self.create_input_field("Радиус (R):", "6", 0)
        self.create_input_field("Коэффициент теплопроводности (koeff):", "0.59", 1)
        self.create_input_field("Удельная теплоёмкость (c):", "1.65", 2)
        self.create_input_field("Время моделирования (T):", "100", 3)
        self.create_input_field("Узлы по θ (I):", "100", 4)
        self.create_input_field("Узлы по времени (K):", "400", 5)

        btn_plot = tk.Button(self.root, text="Построить график", command=plot_function)
        btn_plot.pack(pady=10)

        btn_back = tk.Button(self.root, text="Назад", command=self.initialize_main_menu)
        btn_back.pack(pady=20)

    def create_input_field(self, label_text, default_value, row):
        """Создание поля ввода."""
        label = tk.Label(self.root, text=label_text)
        label.pack()
        entry = tk.Entry(self.root)
        entry.insert(0, default_value)
        entry.pack()
        setattr(self, f"entry_{row}", entry)

    def get_parameters(self):
        """Получение параметров от пользователя."""
        R = float(self.entry_0.get())
        koeff = float(self.entry_1.get())
        c = float(self.entry_2.get())
        T = float(self.entry_3.get())
        I = int(self.entry_4.get())
        K = int(self.entry_5.get())
        return R, koeff, c, T, I, K

    def clear_window(self):
        """Очистка текущего окна."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def plot_temp_evolution(self):
        """Построение графика изменения температуры во времени."""
        R, koeff, c, T, I, K = self.get_parameters()
        solver = HeatEquationSolver(R, koeff, c, T)
        tetta_values, t_values, u = solver.run_method_modified(I, K)
        solver.plot_temperature_evolution(tetta_values, t_values, u)

    def plot_temp_distribution(self):
        """Построение графика изменения температуры по углу."""
        R, koeff, c, T, I, K = self.get_parameters()
        solver = HeatEquationSolver(R, koeff, c, T)
        tetta_values, t_values, u = solver.run_method_modified(I, K)
        solver.plot_temperature_distribution(tetta_values, t_values, u)

    def plot_convergence_tetta_zero(self):
        """Построение графика сходимости при t = 74.9."""
        R, koeff, c, T = 6, 0.59, 1.65, 100  # Статические параметры
        solver = HeatEquationSolver(R, koeff, c, T)
        solver.plot_convergence_tetta_zero()

    def plot_convergence_t_zero(self):
        """Построение графика сходимости при θ = 0.38."""
        R, koeff, c, T = 6, 0.59, 1.65, 100  # Статические параметры
        solver = HeatEquationSolver(R, koeff, c, T)
        solver.plot_convergence_t_zero()


if __name__ == "__main__":
    root = tk.Tk()
    app = HeatEquationGUI(root)
    root.mainloop()
