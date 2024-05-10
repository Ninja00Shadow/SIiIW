from experta import *


class Appliance(Fact):
    """Represents an appliance."""
    pass


class Component(Fact):
    """Represents a component of an appliance."""
    pass


class WashingMachine(Appliance):
    """Specific appliance: a washing machine."""
    pass


class Drum(Component):
    """Specific component: the drum of the washing machine."""
    pass


class MaintenanceFlap(Component):
    """Specific component: the maintenance flap for the drain pump"""
    pass


class Door(Component):
    """Specific component: the door of the washing machine"""
    pass


class DetergentDrawer(Component):
    """Specific component: the detergent drawer"""
    pass


class WaterOutlet(Component):
    """Specific component: the water outlet hose"""
    pass


class DrainPipe(Component):
    """Specific component: the drain pipe"""
    pass


class PowerCord(Component):
    """Specific component: the power cord"""
    pass


class TransitBolts(Component):
    """Specific component: the transit bolts"""
    pass


class ControlPanel(Component):
    """Specific component: the control panel"""
    pass


class Button(Fact):
    """Represents a button on the control panel."""
    name = Field(str)


# class DisplayItem(Fact):
#     """Represents an item on the display."""
#
#     def __init__(self, name, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.name = name


class Display(Fact):
    """Represents the display on the control panel."""
    items = Field(list, default=[])


class SemanticNetwork(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield WashingMachine(model="BOSCH WGG154ZSPL")

    @Rule(NOT(Door(closed=True)))
    def check_door(self):
        print("Ensure the washing machine door is properly closed.")

    @Rule(NOT(WaterOutlet(flow=True)))
    def check_water_inlet(self):
        print("Check the water inlet hose for blockages or kinks.")

    @Rule(AND(Display(items=[], off=True), Button(name="Start/Pause", flashing=True)))
    def energy_saving_mode(self):
        print("Fix: Energy saving mode is active. Press any button.")
        print("Confirmation: Display lights up again.")

    @Rule(AND(Display(items=["E:30 / -80"]), OR(DrainPipe(blocked=True), WaterOutlet(blocked=True))))
    def clean_drainage(self):
        print("Fix: Clean the drain pipe and the water outlet hose.")

    @Rule(AND(Display(items=["E:30 / -80"]), OR(OR(DrainPipe(caught=True), DrainPipe(jammed=True)),
                                                OR(WaterOutlet(caught=True), WaterOutlet(jammed=True)))))
    def remove_obstruction(self):
        print("Fix: Ensure that the drain pipe and water drain hose are not kinked or trapped.")

    @Rule(AND(Display(items=["E:30 / -80"]), WaterOutlet(connected_too_high=True)))
    def lower_water_outlet(self):
        print("Fix: Install the water outlet hose at a maximum height of 1 metre.")

    @Rule(AND(Display(items=["E:30 / -80"]), DrainPipe(unapproved_extension=True)))
    def remove_extension(self):
        print("Fix: Remove any unapproved extensions from the water hose. ")

    @Rule(AND(Display(items=["E:60 / -2B"]), Drum(unbalanced_load=True)))
    def redistribute_laundry(self):
        print("Fix: Distribute the laundry evenly in the drum.")


if __name__ == "__main__":
    engine = SemanticNetwork()

    engine.reset()

    # engine.declare(Door(closed=False))
    # engine.declare(WaterOutlet(flow=False))

    engine.declare(Door(closed=True))
    engine.declare(WaterOutlet(flow=True))
    # engine.declare(Display(items=[], off=True))
    # engine.declare(Button(name="Start/Pause", flashing=True))
    engine.declare(Display(items=["E:30 / -80"]))
    # engine.declare(DrainPipe(blocked=True))
    engine.declare(WaterOutlet(connected_too_high=True))

    engine.run()
