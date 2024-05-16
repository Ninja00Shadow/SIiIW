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

    def is_ok(self):
        return not any([self.blocked, self.caught, self.jammed, self.connected_too_high, self.water_leak,
                        self.damaged]) and self.connected_correctly


class DrainPipe(Fact):
    blocked = Field(bool, default=False)
    caught = Field(bool, default=False)
    jammed = Field(bool, default=False)
    unapproved_extension = Field(bool, default=False)

    def is_ok(self):
        return not any([self.blocked, self.caught, self.jammed]) and not self.unapproved_extension


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


class SemanticNetwork(KnowledgeEngine):
    @Rule(AS.power_cord << PowerCord(plugged_in=False))
    def plug_in_power_cord(self, power_cord):
        print("Fix: Plug in the power cord.")
        self.modify(power_cord, plugged_in=True)

    @Rule(AS.display << Display(on=False), AS.button << Button(name="Start/Pause", flashing=True))
    def energy_saving_mode(self, display, button):
        print("Fix: Energy saving mode is active. Press any button.")
        self.modify(display, on=True)
        self.modify(button, flashing=False)

    @Rule(
        AS.display << Display(errors=MATCH.errors),
        TEST(lambda errors: "E:60 / -2B" in errors),
        AS.drum << Drum(unbalanced_load=True))
    def redistribute_laundry(self, display, errors, drum):
        print("Fix: Distribute the laundry evenly in the drum.")
        self.modify(display, errors=[e for e in errors if e != "E:60 / -2B"])
        self.modify(drum, unbalanced_load=False)

    @Rule(
        AS.display << Display(errors=MATCH.errors),
        TEST(lambda errors: "E:30/-20" in errors),
        OR(AS.drum << Drum(additional_water=True), AS.drawer << DetergentDrawer(too_much_detergent=True)))
    def remove_excess_water(self, display, errors, drum=None, drawer=None):
        if drum:
            print("Fix: Do not add any extra water to the appliance while it is operating.")
            self.modify(drum, additional_water=False)
        if drawer:
            print("Fix: Reduce the amount of detergent for the next washing cycle with the same load.")
            self.modify(drawer, too_much_detergent=False)

        self.modify(display, errors=[e for e in errors if e != "E:30/-20"])

    @Rule(AS.drum << Drum(jerking=True))
    def motor_test(self, drum):
        print("This is caused by an internal motor test. Not a fault – no action required.")
        self.modify(drum, jerking=False)

    @Rule(AND(
        AS.display << Display(errors=MATCH.errors),
        TEST(lambda errors: "E:30 / -80" in errors),
        OR(
            AS.pipe_blocked << DrainPipe(blocked=True),
            AS.hose_blocked << WaterOutlet(blocked=True),
            AS.pipe_caught << DrainPipe(caught=True),
            AS.pipe_jammed << DrainPipe(jammed=True),
            AS.hose_caught << WaterOutlet(caught=True),
            AS.hose_jammed << WaterOutlet(jammed=True),
            AS.outlet_high << WaterOutlet(connected_too_high=True),
            AS.pipe_extension << DrainPipe(unapproved_extension=True)
        )
    ))
    def handle_error_e30_80(self, pipe_blocked=None, hose_blocked=None,
                            pipe_caught=None, pipe_jammed=None, hose_caught=None,
                            hose_jammed=None, outlet_high=None, pipe_extension=None):
        if pipe_blocked:
            print("Fix: Clean the drain pipe.")
            self.modify(pipe_blocked, blocked=False)

        if hose_blocked:
            print("Fix: Clean the water outlet hose.")
            self.modify(hose_blocked, blocked=False)

        if pipe_caught or pipe_jammed:
            print("Fix: Ensure that the drain pipe is not kinked or trapped.")
            if pipe_caught:
                self.modify(pipe_caught, caught=False)
            if pipe_jammed:
                self.modify(pipe_jammed, jammed=False)

        if hose_caught or hose_jammed:
            print("Fix: Ensure that the water outlet hose is not kinked or trapped.")
            if hose_caught:
                self.modify(hose_caught, caught=False)
            if hose_jammed:
                self.modify(hose_jammed, jammed=False)

        if outlet_high:
            print("Fix: Install the water outlet hose at a maximum height of 1 metre.")
            self.modify(outlet_high, connected_too_high=False)

        if pipe_extension:
            print("Fix: Remove any unapproved extensions from the water hose.")
            self.modify(pipe_extension, unapproved_extension=False)

    @Rule(
        AS.display << Display(errors=MATCH.errors),
        TEST(lambda errors: "E:30 / -80" in errors),
        WaterOutlet(blocked=False, caught=False, jammed=False, connected_too_high=False, water_leak=False,
                    damaged=False, connected_correctly=True),
        DrainPipe(blocked=False, caught=False, jammed=False, unapproved_extension=False),
    )
    def remove_error_e30_80(self, display, errors):
        errors = [e for e in errors if e != "E:30 / -80"]
        self.modify(display, errors=errors)

    @Rule(OR(AS.outlet << WaterOutlet(water_leak=True, damaged=True),
             AS.outlet << WaterOutlet(water_leak=True, connected_correctly=False)))
    def replace_water_outlet(self, outlet):
        if outlet["damaged"]:
            print("Fix: Replace the water outlet.")
            self.modify(outlet, water_leak=False, damaged=False)
        else:
            print("Fix: Connect the water outlet hose correctly.")
            self.modify(outlet, water_leak=False, connected_correctly=True)

    @Rule(AS.door << Door(closed=False))
    def check_door(self, door):
        print("Fix: Close the door.")
        self.modify(door, closed=True)

    @Rule(AS.door << Door(caught_laundry=True))
    def remove_caught_laundry(self, door):
        print("Fix: Remove any trapped laundry")
        self.modify(door, caught_laundry=False)

    @Rule(AS.door << Door(water_leak=True))
    def fix_water_leak(self, door):
        print("Fix: Clean the door and the seal.")
        self.modify(door, water_leak=False)

    @Rule(AS.drawer << DetergentDrawer(fabric_softener_remaining=True),
          AS.prog << Program(supports_fabric_softener=False))
    def add_fabric_softener(self, drawer, prog):
        print("Fix: Use a program that supports fabric softener.")
        self.modify(drawer, fabric_softener_remaining=False)
        self.modify(prog, supports_fabric_softener=True)

    @Rule(
        Drum(unbalanced_load=False, additional_water=False, jerking=False),
        Door(closed=True, caught_laundry=False, water_leak=False),
        DetergentDrawer(too_much_detergent=False, fabric_softener_remaining=False),
        WaterOutlet(blocked=False, caught=False, jammed=False, connected_too_high=False, water_leak=False,
                    damaged=False, connected_correctly=True),
        DrainPipe(blocked=False, caught=False, jammed=False, unapproved_extension=False),
        PowerCord(plugged_in=True),
        Button(flashing=False),
        Display(on=True, errors=[]),
    )
    def no_errors(self):
        print("Everything is working fine.")


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
