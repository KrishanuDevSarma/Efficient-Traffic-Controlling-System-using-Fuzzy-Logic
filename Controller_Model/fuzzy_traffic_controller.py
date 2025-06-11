# File: Codes/Model/fuzzy_traffic_controller.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os

from Codes.Dataset.traffic_dataset import predefined_traffic_inputs
from Codes.Utils.helpers import validate_input_range


class TrafficLightControl:
    """
    Class implementing a fuzzy logic-based traffic light control system.
    This system adjusts traffic light wait times based on the number of waiting and incoming vehicles.
    """

    def __init__(self):
        """Initialize the traffic light controller and build the fuzzy inference system."""
        self._setup_fuzzy_system()

    def _setup_fuzzy_system(self):
        """
        Set up fuzzy variables, membership functions, and rules for the traffic controller.
        This includes fuzzification, rule definition, and control system creation.
        """
        self.waiting_cars = ctrl.Antecedent(np.arange(0, 101, 1), 'waiting_cars')
        self.incoming_cars = ctrl.Antecedent(np.arange(0, 101, 1), 'incoming_cars')
        self.wait_time = ctrl.Consequent(np.arange(0, 161, 1), 'wait_time')

        self.waiting_cars.automf(names=['minimal', 'light', 'average', 'heavy', 'standstill'])
        self.incoming_cars.automf(names=['minimal', 'light', 'average', 'heavy', 'excess'])

        self.wait_time['short'] = fuzz.trimf(self.wait_time.universe, [0, 50, 75])
        self.wait_time['medium'] = fuzz.trimf(self.wait_time.universe, [50, 87, 125])
        self.wait_time['long'] = fuzz.trimf(self.wait_time.universe, [100, 150, 160])

        rules = [
            # Define fuzzy inference rules
            ctrl.Rule(self.waiting_cars['minimal'] | self.incoming_cars['minimal'], self.wait_time['short']),
            ctrl.Rule(self.waiting_cars['minimal'] | self.incoming_cars['light'], self.wait_time['short']),
            ctrl.Rule(self.waiting_cars['minimal'] | self.incoming_cars['average'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['minimal'] | self.incoming_cars['heavy'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['minimal'] | self.incoming_cars['excess'], self.wait_time['long']),

            ctrl.Rule(self.waiting_cars['light'] | self.incoming_cars['minimal'], self.wait_time['short']),
            ctrl.Rule(self.waiting_cars['light'] | self.incoming_cars['light'], self.wait_time['short']),
            ctrl.Rule(self.waiting_cars['light'] | self.incoming_cars['average'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['light'] | self.incoming_cars['heavy'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['light'] | self.incoming_cars['excess'], self.wait_time['long']),

            ctrl.Rule(self.waiting_cars['average'] | self.incoming_cars['minimal'], self.wait_time['short']),
            ctrl.Rule(self.waiting_cars['average'] | self.incoming_cars['light'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['average'] | self.incoming_cars['average'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['average'] | self.incoming_cars['heavy'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['average'] | self.incoming_cars['excess'], self.wait_time['long']),

            ctrl.Rule(self.waiting_cars['heavy'] | self.incoming_cars['minimal'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['heavy'] | self.incoming_cars['light'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['heavy'] | self.incoming_cars['average'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['heavy'] | self.incoming_cars['heavy'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['heavy'] | self.incoming_cars['excess'], self.wait_time['long']),

            ctrl.Rule(self.waiting_cars['standstill'] | self.incoming_cars['minimal'], self.wait_time['medium']),
            ctrl.Rule(self.waiting_cars['standstill'] | self.incoming_cars['light'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['standstill'] | self.incoming_cars['average'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['standstill'] | self.incoming_cars['heavy'], self.wait_time['long']),
            ctrl.Rule(self.waiting_cars['standstill'] | self.incoming_cars['excess'], self.wait_time['long'])
        ]

        # Initialize the fuzzy control system and simulator
        system = ctrl.ControlSystem(rules)
        self.simulation = ctrl.ControlSystemSimulation(system)

    def compute_wait_time(self, incoming, waiting, plot_output=False, filename_prefix="output"):
        """
        Compute the wait time using fuzzy logic for given traffic inputs.

        Parameters:
            incoming (float): Number of incoming cars (0-100)
            waiting (float): Number of waiting cars (0-100)
            plot_output (bool): Whether to save a graph of the fuzzy result
            filename_prefix (str): Prefix for the saved plot filename

        Returns:
            float: Computed wait time in seconds
        """
        validate_input_range(incoming, "Incoming Cars")
        validate_input_range(waiting, "Waiting Cars")

        self.simulation.input['waiting_cars'] = waiting
        self.simulation.input['incoming_cars'] = incoming
        self.simulation.compute()

        if plot_output:
            output_dir = "Results"
            os.makedirs(output_dir, exist_ok=True)
            plot_path = os.path.join(output_dir, f"{filename_prefix}_wait_time.png")
            self.wait_time.view(sim=self.simulation)
            plt.savefig(plot_path)
            plt.close()

        return self.simulation.output['wait_time']


def main():
    """
    Main program loop to interact with the user.
    Allows user to input values manually or test predefined traffic inputs.
    """
    controller = TrafficLightControl()

    print("\nTraffic Controller System Using Fuzzy Logic")
    print("1. Enter custom input")
    print("2. Use predefined test data")
    choice = input("Select an option (1/2): ")

    if choice == '1':
        incoming = float(input("Enter number of incoming cars (0-100): "))
        waiting = float(input("Enter number of waiting cars (0-100): "))
        result = controller.compute_wait_time(incoming, waiting, plot_output=True, filename_prefix="custom_input")
        print(f"\nComputed Wait Time: {result:.2f} seconds\n")

    elif choice == '2':
        print("\nRunning predefined test cases:\n")
        for i, (incoming, waiting) in enumerate(predefined_traffic_inputs):
            result = controller.compute_wait_time(incoming, waiting, plot_output=True, filename_prefix=f"case_{i+1}")
            print(f"Test Case {i+1}: Incoming = {incoming}, Waiting = {waiting} -> Wait Time = {result:.2f} sec")
    else:
        print("\nInvalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()
