from experta import *


class WashingMachine(Fact):
    """Specific appliance: a washing machine."""
    pass


class Drum(Fact):
    unbalanced_load = Field(bool, default=False)
    additional_water = Field(bool, default=False)
    jerking = Field(bool, default=False)


class Door(Fact):
    closed = Field(bool, default=True)
    caught_laundry = Field(bool, default=False)
    water_leak = Field(bool, default=False)


class DetergentDrawer(Fact):
    too_much_detergent = Field(bool, default=False)
    fabric_softener_remaining = Field(bool, default=False)


class WaterOutlet(Fact):
    blocked = Field(bool, default=False)
    caught = Field(bool, default=False)
    jammed = Field(bool, default=False)
    connected_too_high = Field(bool, default=False)
    water_leak = Field(bool, default=False)
    damaged = Field(bool, default=False)
    connected_correctly = Field(bool, default=True)


class DrainPipe(Fact):
    blocked = Field(bool, default=False)
    caught = Field(bool, default=False)
    jammed = Field(bool, default=False)
    unapproved_extension = Field(bool, default=False)


class PowerCord(Fact):
    plugged_in = Field(bool, default=True)


class Button(Fact):
    """Represents a button on the control panel."""
    name = Field(str)
    flashing = Field(bool, default=False)


class Display(Fact):
    """Represents the display on the control panel."""
    errors = Field(list, default=[])
    on = Field(bool, default=True)


class Program(Fact):
    """Represents a washing program."""
    name = Field(str)
    supports_fabric_softener = Field(bool, default=False)


class WaterSystemRules:
    @Rule(AND(Display(errors=["E:30 / -80"]), OR(DrainPipe(blocked=True), WaterOutlet(blocked=True))))
    def clean_drainage(self):
        print("Fix: Clean the drain pipe and the water outlet hose.")
        self.declare(Display(errors=[]))
        self.declare(DrainPipe(blocked=False))
        self.declare(WaterOutlet(blocked=False))

    @Rule(AND(Display(errors=["E:30 / -80"]), OR(OR(DrainPipe(caught=True), DrainPipe(jammed=True)),
                                                 OR(WaterOutlet(caught=True), WaterOutlet(jammed=True)))))
    def remove_obstruction(self):
        print("Fix: Ensure that the drain pipe and water drain hose are not kinked or trapped.")
        self.declare(Display(errors=[]))
        self.declare(DrainPipe(caught=False))
        self.declare(DrainPipe(jammed=False))
        self.declare(WaterOutlet(caught=False))
        self.declare(WaterOutlet(jammed=False))

    @Rule(AND(Display(errors=["E:30 / -80"]), WaterOutlet(connected_too_high=True)))
    def lower_water_outlet(self):
        print("Fix: Install the water outlet hose at a maximum height of 1 metre.")
        self.declare(Display(errors=[]))
        self.declare(WaterOutlet(connected_too_high=False))

    @Rule(AND(Display(errors=["E:30 / -80"]), DrainPipe(unapproved_extension=True)))
    def remove_extension(self):
        print("Fix: Remove any unapproved extensions from the water hose. ")
        self.declare(Display(errors=[]))
        self.declare(DrainPipe(unapproved_extension=False))

    @Rule(WaterOutlet(water_leak=True, damaged=True))
    def replace_water_outlet(self):
        print("Fix: Replace the water outlet.")
        self.declare(WaterOutlet(water_leak=False, damaged=False))

    @Rule(WaterOutlet(water_leak=True, connected_correctly=False))
    def replace_drain_pipe(self):
        print("Fix: Connect the water outlet hose correctly.")
        self.declare(DrainPipe(blocked=False, connected_correctly=True))


class DoorRules:
    @Rule(Door(closed=False))
    def check_door(self):
        print("Fix: Close the door.")
        # doors_to_close = [f for f in self.facts.values() if isinstance(f, Door) and not f['closed']]
        # for door in doors_to_close:
        #     self.retract(door)
        self.declare(Door(closed=True))

    @Rule(Door(caught_laundry=True))
    def remove_caught_laundry(self):
        print("Fix: Remove any trapped laundry")
        self.declare(Door(caught_laundry=False))

    @Rule(Door(water_leak=True))
    def fix_water_leak(self):
        print("Fix: Clean the door and the seal.")
        self.declare(Door(water_leak=False))


class DetergentDrawerRules:
    @Rule(AND(Display(errors=["E:30/-20"]), DetergentDrawer(too_much_detergent=True)))
    def remove_excess_detergent(self):
        print("Fix: Reduce the amount of detergent for the next washing cycle with the same load.")
        self.declare(Display(errors=[]))
        self.declare(DetergentDrawer(too_much_detergent=False))

    @Rule(AND(DetergentDrawer(fabric_softener_remaining=True), Program(supports_fabric_softener=False)))
    def add_fabric_softener(self):
        print("Fix: Use a program that supports fabric softener.")
        self.declare(DetergentDrawer(fabric_softener_remaining=False))


class SemanticNetwork(WaterSystemRules, DoorRules, DetergentDrawerRules, KnowledgeEngine):
    @Rule(PowerCord(plugged_in=False))
    def plug_in_power_cord(self):
        print("Fix: Plug in the power cord.")
        self.declare(PowerCord(plugged_in=True))

    @Rule(AND(Display(on=False), Button(name="Start/Pause", flashing=True)))
    def energy_saving_mode(self):
        print("Fix: Energy saving mode is active. Press any button.")
        print("Confirmation: Display lights up again.")
        self.declare(Display(on=True))
        self.declare(Button(name="Start/Pause", flashing=False))

    @Rule(AND(Display(errors=["E:60 / -2B"]), Drum(unbalanced_load=True)))
    def redistribute_laundry(self):
        print("Fix: Distribute the laundry evenly in the drum.")
        self.declare(Display(errors=[]))
        self.declare(Drum(unbalanced_load=False))

    @Rule(AND(Display(errors=["E:30/-20"]), Drum(additional_water=True)))
    def remove_excess_water(self):
        print("Fix: Do not add any extra water to the appliance while it is operating.")
        self.declare(Display(errors=[]))
        self.declare(Drum(additional_water=False))

    @Rule(Drum(jerking=True))
    def motor_test(self):
        print("This is caused by an internal motor test. Not a fault – no action required.")


if __name__ == "__main__":
    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Door(closed=False))
    engine.declare(WaterOutlet(flow=True))
    engine.declare(Display(on=False))
    engine.declare(Button(name="Start/Pause", flashing=True))
    engine.declare(Display(errors=["E:30 / -80"]))
    engine.declare(DrainPipe(blocked=True))
    engine.declare(WaterOutlet(connected_too_high=True))
    engine.declare(Display(errors=["E:60 / -2B"]))
    engine.declare(Drum(unbalanced_load=True))

    engine.run()
