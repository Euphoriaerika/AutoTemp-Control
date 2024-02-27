import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definition of the left Z-function
def z1_function(x, a, b):
    return np.where(x <= a, 1, np.where(x < b, 1 - (x - a) / (b - a), 0))

# Definition of the right Z-function
def z2_function(x, a, b):
    return np.where(x <= a, 0, np.where(x < b, (x - a) / (b - a), 1))

def calculation_tap(input, show=False):
    # Definition of x1 values range
    x1_values = np.linspace(-90, 90, 181)

    # Computation of z1 function values
    z1_values = z1_function(x1_values, -72, -36)

    if show:
        # Plotting the graph of the left function
        plt.figure(figsize=(8, 5))
        plt.plot(x1_values, z1_values, "b", linewidth=1.5)
        plt.title("Zeta1 Function")
        plt.xlabel("x")
        plt.ylabel("z(x)")
        plt.grid(True)
        plt.show()

    # Definition of x2 values range
    x2_values = np.linspace(-90, 90, 181)

    # Computation of z2 function values
    z2_values = z2_function(x2_values, 36, 72)

    if show:
        # Plotting the graph of the right function
        plt.figure(figsize=(8, 5))
        plt.plot(x2_values, z2_values, "b", linewidth=1.5)
        plt.title("Zeta2 Function")
        plt.xlabel("x")
        plt.ylabel("z(x)")
        plt.grid(True)
        plt.show()

    # Definition of input variables
    temperature = ctrl.Antecedent(np.arange(0, 101, 1), "temperature")

    # Definition of x3 values range
    x3_values = np.linspace(0, 100, 101)

    # Definition of fuzzy sets and their membership functions
    temperature["cold"] = z1_function(x3_values, 10, 30)
    temperature["cool"] = fuzz.trimf(temperature.universe, [20, 35, 50])
    temperature["medium"] = fuzz.trimf(temperature.universe, [40, 50, 60])
    temperature["not very hot"] = fuzz.trimf(temperature.universe, [50, 60, 70])
    temperature["hot"] = z2_function(x3_values, 60, 70)

    # Definition of output variable
    tap = ctrl.Consequent(np.arange(-90, 91, 1), "tap")

    # Definition of membership functions for the tap
    tap["large angle to the left"] = z1_function(x1_values, -72, -36)
    tap["slight angle to the left"] = fuzz.trimf(tap.universe, [-54, -27, 0])
    tap["OK"] = fuzz.trimf(tap.universe, [-18, 0, 18])
    tap["slight angle to the right"] = fuzz.trimf(tap.universe, [0, 27, 54])
    tap["large angle to the right"] = z2_function(x2_values, 36, 72)

    # Definition of rules
    rule1 = ctrl.Rule(temperature["hot"], tap["large angle to the right"])
    rule2 = ctrl.Rule(temperature["not very hot"], tap["slight angle to the right"])
    rule3 = ctrl.Rule(temperature["medium"], tap["OK"])
    rule4 = ctrl.Rule(temperature["cool"], tap["slight angle to the left"])
    rule5 = ctrl.Rule(temperature["cold"], tap["large angle to the left"])

    # Creation of the control system
    tap_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    tap_system = ctrl.ControlSystemSimulation(tap_ctrl)

    # Setting the temperature value (from 0 to 100)
    tap_system.input["temperature"] = input

    # Computing the output value
    tap_system.compute()

    if show:
        # Displaying the result
        print("Water Tap:", tap_system.output["tap"])

    return tap_system.output["tap"]
