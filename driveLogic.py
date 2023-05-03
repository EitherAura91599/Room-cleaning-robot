"""
This program is the backend of the driving program for the robot. This includes all of the functions needed to simply drive around and navigate to specific locations.
There are multiple functions and muntiple options in each of those functions. The robot is able to turn with either a relative or an absolute bearing, meaning that it
will never be confused about which direction it is going. This also includes specialty turning functions with adjustable wheel base turning methods.

Each function also returns the result, which allows for advanced debugging and program integration.

This program was originally written by Alex McMinn and Parker Pulfer for the LEGO Mindstorms EV3 robot, and has been adjusted to be more useful for the room cleaning robot

Copyright 2020 Alex McMinn and Parker Pulfer
Copyright 2023 Alex McMinn
"""

##############
# In Python, any libraries that are used to interface with an enternal function (i.e. the robot) are defined and imported here:
##############

from time import sleep

##############
# Initialize the robot's motors and functions.
##############
def drive_base_init(): # This function initializes the robot and makes sure that it works properly
    left_motor = Motor(Port.B, Direction.CLOCKWISE)
    right_motor = Motor(Port.C, Direction.CLOCKWISE)
    robot = DriveBase(left_motor, right_motor, 87.5, 90) # Define the drive base, which defines the width between the wheels and the size of the wheels to help with math later
    robot.settings(150, 50, 50, 25) # Initialize other settings

    return robot

def calc_right_distance(want, current):
    distance = 0
    ring = current
    while ring != want:
        if ring == 361:
            ring = -1
        distance = distance + 1
        ring = ring + 1
        # print('  calc_right_distance ring ' + str(ring) + ' want ' + str(want))
    return distance


###############
# These functions travel a distance on a given bearing and then return the new bearing if it has deviated from the original
# Given a position on the compass, return new position on compass after traveling a distance. This helps to correct for any deviation while driving.
# current- the current position on the compass
# distance- how many degrees to move on the compass
# return- this returns the new compass position
###############
def travel_left_distance(current, distance):
    traveled = 0
    gyro_value = current
    while traveled < distance:
        traveled = traveled + 1
        gyro_value = gyro_value -1
        print('  travel_left_distance ring_value ' + str(ring_value) + ' traveled ' + str(traveled))
    return gyro_value

def travel_right_distance(current, distance):
    traveled = 0
    ring_value = current
    while traveled < distance:
        traveled = traveled + 1
        ring_value = ring_value + 1
        # print('  travel_right_distance ring_value ' + str(ring_value) + ' traveled ' + str(traveled))
    return ring_value


###############
# Calculate the turning distace using a ring (tank drive) method.
# Determine the # of degrees between the current and wanted position
# want- the new compass position
# current- the current position on the compass
###############
def calc_left_distance(want, current):
    distance = 0
    ring = current
    while ring < want:
        if ring == 0:
            ring = 360
        distance = distance + 1
        ring = ring - 1
        print('  calc_left_distance ring ' + str(ring) + ' want ' + str(want))
    return distance


#################
# THE MASTER TURN FUNCTION
# Turns to a specific given compass heading using the best available method. Given a bearing, it also decides whether to turn left or right to maximize efficiency
# degrees - 0 - 359
# NOTE: gyro_sensor.angle() can be positive or negative integer
#################
def turn(robot, gyro_sensor, desired_degrees):
    current_gyro_value = gyro_sensor.angle()
    # get current gyro degrees
    start_gyro_compass_value = current_gyro_value % 360
    print('  turn current ' + str(gyro_sensor.angle()) + ' desired ' + str(desired_degrees) + ' compass heading ' + str(start_gyro_compass_value))
    # turn right or left?
    right_distance = calc_right_distance(desired_degrees, start_gyro_compass_value)
    left_distance = calc_left_distance(desired_degrees, start_gyro_compass_value)
    steering_speed_fast = 50
    steering_speed_slow = 10
    if gyro_sensor.angle() < 0:
        # Set the actual current DEGREES to 360 minus whatever the gyro is at. This means that at any negative number can work in the equation.
        current_degrees = 360 + gyro_sensor.angle()
    else:
        current_degrees = gyro_sensor.angle()
    if right_distance > left_distance:
        # go left
        print('  left turn distance ' + str(left_distance))
        new_gyro_value = travel_left_distance(current_gyro_value, left_distance)
        robot.drive(0, steering_speed_fast)
        while gyro_sensor.angle() > new_gyro_value:
            #print(str(gyro_sensor.angle() % 360))
            wait(1)
        robot.drive(0, 0)
        robot.drive(0, steering_speed_slow)
        while gyro_sensor.angle() > new_gyro_value:
            #print(str(gyro_sensor.angle()))
            wait(1)
        robot.drive(0, 0)
        print('  left turn desired ' + str(new_gyro_value) + ' actual ' + str(gyro_sensor.angle()))
    else:
        # go right
        print('  right turn distance ' + str(right_distance))
        new_gyro_value = travel_right_distance(current_gyro_value, right_distance)
        robot.drive(0, steering_speed_fast)
        while gyro_sensor.angle() < new_gyro_value:
            wait(1)
        robot.drive(0, 0)
        
        robot.drive(0, steering_speed_slow)
        while gyro_sensor.angle() < new_gyro_value:
            wait(1)
        robot.drive(0, 0)
        print('  right turn desired ' + str(new_gyro_value) + ' actual ' + str(gyro_sensor.angle()))


################
# Specific turning functions
# These functions allow for customized control over the all turning methods. These speeds are adjustable, making it useful for select functions
# For most turns, the master turn function will suffice
################
def turn_right(robot, gyro_sensor, want): # Turns the robot right with adjustable speeds and angles
    rough_turn = want - 10
    steering = -45
    steering_slow = -8
    robot.drive(0, steering)
    while gyro_sensor.angle() < rough_turn:
        wait(1)
    robot.drive(0, 0)
    robot.drive(0, steering_slow)
    while gyro_sensor.angle() < want:
        wait(1)
    robot.drive(0, 0)
    print(str(gyro_sensor.angle()))

def turn_left(robot, gyro_sensor, want): # Turns the robot lefs with adjustable speeds and angles
    rough_turn = want + 10
    steering = 45
    steering_slow = 8
    robot.drive(0, steering)
    while gyro_sensor.angle() > rough_turn:
        wait(1)
    robot.drive(0, 0)
    robot.drive(0, steering_slow)
    while gyro_sensor.angle() > want:
        wait(1)
    robot.drive(0, 0)
    print(str(gyro_sensor.angle()))
    
def turn_left_slow(robot, gyro_sensor, want): # A slower, more precise way to turn the robot left
    steering_slow = 8
    robot.drive(0, steering_slow)
    while gyro_sensor.angle() > want:
        wait(1)
    robot.drive(0, 0)
    print(str(gyro_sensor.angle()))

def turn_right_slow(robot, gyro_sensor, want): # A slower, more precise way to turn the robot right
    steering_slow = -8
    robot.drive(0, steering_slow)
    while gyro_sensor.angle() < want:
        wait(1)
    robot.drive(0, 0)
    print(str(gyro_sensor.angle()))

def turn(robot, gyro_sensor, want): # An automatic function that calculates the best turn function of the 4 above to use for any given angle input
    gyro_sensor.reset_angle(0)
    if want > 10:
        turn_right(robot, gyro_sensor, want)
    
    if want < -10:
        turn_left(robot, gyro_sensor, want)
    
    else:
        if want > 0:
            if want < 11:
                turn_right_slow(robot, gyro_sensor, want)

        if want < 0:
            if want > -11:
                turn_left_slow(robot, gyro_sensor, want)

def straight(robot, gyro_sensor, distance, speed): # An accurate way to drive the robot straight. It uses the gyroscopic sensor to correct any errors greater then about a degree
    gyro_sensor.reset_angle(0)
    driven_distance = robot.distance() - robot.distance()
    robot.drive(speed, 0)
    while driven_distance < distance:
        wait(1)
        print(str(robot.angle()))
        if gyro_sensor.angle() != 0:
            turn_distance = gyro_sensor.angle() * -1
            robot.drive(1, turn_distance)
            while gyro_sensor.angle() != 0:
                wait(1)
        else:
            pass


##########
# Main
# In a typical program, this would be where the action actually happens. The entire code above is split into "functions," which make it very easy to call a specific function.
# This program does not use the main section because it is designed to be imported into another program that uses any of these functions above.
# However, it order to make sure that there are no errors in the program, I've added a Hello World line to prove that the program works properly on a defined level.
##########
print("Hello world!")    # If all else fails, at least say hello to the world first!