import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# Визначення Z-функції
def z1_fuction(x, a, b):
    return np.where(x <= a, 1, np.where(x < b, 1 - (x - a) / (b - a), 0))


# Визначення області значень x
x1_values = np.linspace(-90, 90, 181)

# Обчислення значень функції z(x)
z1_values = z1_fuction(x1_values, -72, -36)

# Побудова графіку
plt.figure(figsize=(8, 5))
plt.plot(x1_values, z1_values, "b", linewidth=1.5)
plt.title("Zeta1 Fuction")
plt.xlabel("x")
plt.ylabel("z(x)")
plt.grid(True)
plt.show()


# Визначення Z-функції
def z2_function(x, a, b):
    return np.where(x <= a, 0, np.where(x < b, (x - a) / (b - a), 1))


# Визначення області значень x
x2_values = np.linspace(-90, 90, 181)

# Обчислення значень функції z(x)
z2_values = z2_function(x2_values, 36, 72)

# Побудова графіку
plt.figure(figsize=(8, 5))
plt.plot(x2_values, z2_values, "b", linewidth=1.5)
plt.title("Zeta2 Fuction")
plt.xlabel("x")
plt.ylabel("z(x)")
plt.grid(True)
plt.show()

# Визначення змінних вхідних
temperature = ctrl.Antecedent(np.arange(0, 101, 1), "temperature")

# Визначення області значень х
x3_values = np.linspace(0, 100, 101)

# Визначення нечітких множин та їх функцій належності
temperature["cold"] = z1_fuction(x3_values, 10, 30)
temperature["cool"] = fuzz.trimf(temperature.universe, [20, 35, 50])
temperature["medium"] = fuzz.trimf(temperature.universe, [40, 50, 60])
temperature["not very hot"] = fuzz.trimf(temperature.universe, [50, 60, 70])
temperature["hot"] = z2_function(x3_values, 60, 70)

# Визначення вихідної змінної
tap = ctrl.Consequent(np.arange(-90, 91, 1), "tap")

# Визначення функції належності для крана
tap["large angle to the left"] = z1_fuction(x1_values, -72, -36)
tap["slight angle to the left"] = fuzz.trimf(tap.universe, [-54, -27, 0])
tap["OK"] = fuzz.trimf(tap.universe, [-18, 0, 18])
tap["slight angle to the right"] = fuzz.trimf(tap.universe, [0, 27, 54])
tap["large angle to the right"] = z2_function(x2_values, 36, 72)

# Визначення правил
rule1 = ctrl.Rule(temperature["hot"], tap["large angle to the right"])
rule2 = ctrl.Rule(temperature["not very hot"], tap["slight angle to the right"])
rule3 = ctrl.Rule(temperature["medium"], tap["OK"])
rule4 = ctrl.Rule(temperature["cool"], tap["slight angle to the left"])
rule5 = ctrl.Rule(temperature["cold"], tap["large angle to the left"])

# Створення системи керування
tap_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
tap_system = ctrl.ControlSystemSimulation(tap_ctrl)

# Встановлення значення температури (від 0 до 100)
tap_system.input["temperature"] = 50

# Обчислення вихідного значення
tap_system.compute()

# Виведення результату
print("Water Tap:", tap_system.output["tap"])



