#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
bumper_a = Bumper(brain.three_wire_port.a)
bumper_b = Bumper(brain.three_wire_port.b)
left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)

# Wait for rotation sensor to fully initialize
wait(30, MSEC)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))

# Set random seed 
initializeRandomSeed()

def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# Add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# Clear the console to make sure we don't have the REPL in the console
print("\033[2J")

# Define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# Control mode: 0 = linear, 1 = exponential
control_mode = 0

# Define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled, control_mode

    while True:
        if remote_control_code_enabled:
            # Get joystick positions
            axis3 = controller_1.axis3.position()
            axis1 = controller_1.axis1.position()
            
            # Apply control mode
            if control_mode == 1:  # Exponential control
                drivetrain_left_side_speed = (axis3 + axis1) ** 3 / 10000
                drivetrain_right_side_speed = (axis3 - axis1) ** 3 / 10000
            else:  # Linear control
                drivetrain_left_side_speed = axis3 + axis1
                drivetrain_right_side_speed = axis3 - axis1

            # Deadband logic for drivetrain
            if abs(drivetrain_left_side_speed) < 5:
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    left_drive_smart.stop()
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_l_needs_to_be_stopped_controller_1 = True

            if abs(drivetrain_right_side_speed) < 5:
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    right_drive_smart.stop()
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_r_needs_to_be_stopped_controller_1 = True

            # Set motor velocities
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)

        # Wait before repeating the process
        wait(20, MSEC)

# Define event handlers for A and B buttons
def onevent_button_a_pressed():
    global control_mode
    control_mode = 1  # Enable exponential control
    brain.screen.clear_screen()
    brain.screen.print("Exponential Mode Enabled")
    
def onevent_button_b_pressed():
    global control_mode
    control_mode = 0  # Enable linear control
    brain.screen.clear_screen()
    brain.screen.print("Linear Mode Enabled")

# Define variable for remote controller enable/disable
remote_control_code_enabled = True

# Register button event handlers
controller_1.buttonA.pressed(onevent_button_a_pressed)
controller_1.buttonB.pressed(onevent_button_b_pressed)

# Start the control loop
rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration
