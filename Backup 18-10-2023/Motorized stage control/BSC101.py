"""
pythonnet_template
==================

An example written to show control of a BSC101 stepper motor controller.
"""
import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

def main():
    """The main entry point for the application"""

    # Uncomment this line if you are using
    # SimulationManager.Instance.InitializeSimulations()

    try:

        DeviceManagerCLI.BuildDeviceList()

        # create new device
        serial_no = "70335874"  # Replace this line with your device's serial number
        serial_no_device1="70335875"
        serial_no_device2="70335876"
        serial_no_device3="70335877"

        # Connect, begin polling, and enable
        device = BenchtopStepperMotor.CreateBenchtopStepperMotor(serial_no)
        
        device.Connect(serial_no)
        time.sleep(0.25)
        # device1.Connect(serial_no_device1)
        # time.sleep(0.25)
        # device2.Connect(serial_no_device2)
        # time.sleep(0.25)
        # device3.Connect(serial_no_device3)
        # time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

        # For benchtop devices, get the channel
        channel1 = device.GetChannel(1)
        channel2 = device.GetChannel(2)
        channel3 = device.GetChannel(3)
        
        # Ensure that the device settings have been initialized
        if not channel1.IsSettingsInitialized():
            channel1.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert channel1.IsSettingsInitialized() is True
        if not channel2.IsSettingsInitialized():
             channel2.WaitForSettingsInitialized(10000)  # 10 second timeout
             assert channel2.IsSettingsInitialized() is True
        if not channel3.IsSettingsInitialized():
              channel3.WaitForSettingsInitialized(10000)  # 10 second timeout
              assert channel3.IsSettingsInitialized() is True
              
            

        # Start polling and enable
        channel1.StartPolling(250)  #250ms polling rate
        time.sleep(0.25)
        channel2.StartPolling(250)
        time.sleep(0.25)
        channel3.StartPolling(250)
        time.sleep(0.25)
        channel1.EnableDevice()
        time.sleep(0.25)
        channel2.EnableDevice()
        time.sleep(0.25)
        channel3.EnableDevice()
        time.sleep(0.25) # Wait for device to enable

        # Get Device Information and display description
        device1_info = channel1.GetDeviceInfo()
        print(device1_info.Description)
        device2_info = channel2.GetDeviceInfo()
        print(device2_info.Description)
        device3_info = channel3.GetDeviceInfo()
        print(device3_info.Description)

        # Load any configuration settings needed by the controller/stage
        channel_config = channel1.LoadMotorConfiguration(device1.DeviceID)
        chan_settings = channel1.MotorDeviceSettings

        channel1.GetSettings(chan_settings)

        channel_config.DeviceSettingsName = 'Benchtop Stepper Motor Controller'

        channel_config.UpdateCurrentConfiguration()

        channel.SetSettings(chan_settings, True, False)

        # Get parameters related to homing/zeroing/other

        # Home or Zero the device (if a motor/piezo)
        print("Homing Motor")
        channel1.Home(60000)
        print("Done")
        
        print("Homing Motor")
        channel2.Home(60000)
        print("Done")
        
        print("Homing Motor")
        channel3.Home(60000)
        print("Done")
        
        # Move the device to a new position
        channel1.SetMoveRelativeDistance(Decimal(2.0))
        print("Done")
        
        print("Moving 10 times")
        for i in range(10):
            channel1.MoveRelative(10000)
            time.sleep(5)
        print("Done")

        # Stop Polling and Disconnect
        channel.StopPolling()
        device.Disconnect()

    except Exception as e:
        # this can be bad practice: It sometimes obscures the error source
        print(e)

    # Uncomment this line if you are using Simulations
    SimulationManager.Instance.UninitializeSimulations()
    ...


if __name__ == "__main__":
    main()