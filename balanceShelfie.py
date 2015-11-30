import math
import sys
import RTIMU
import time
import RPi.GPIO as GPIO
#import cal_vals
import calibration
import motorcontroller as motors

#initialize PID controller constants


#Setting up I2C comunication with the IMU
SETTINGS_FILE = "RTIMU1"
s = RTIMU.Settings("RTIMU1")
imu = RTIMU.RTIMU(s)
if (not imu.IMUInit()):
        print("IMU Init Failed");
        sys.exit(1)
else:
        print("IMU Init succeeded")


#Angle update
def updateAngle(angle):
        # Fill in here

        angleAcce=initialAngle()
        angleGyro=gyro()

        newAngle=0.98*(angle+angleGyro*.001)+0.02*(angleAcce)

	return newAngle

#angle gyro
def gyro():
    poll_interval = imu.IMUGetPollInterval()
    prom1 = 0
    prom2 = 0
    prom3 = 0
    for n in range(1,500) :
        if imu.IMURead():
            data = imu.getIMUData()
            gyroData = data["gyro"]
            dat1 = gyroData[0]
            dat2 = gyroData[1]
            dat3 = gyroData[2]
            prom1 = dat1 + prom1
            prom2 = dat2 + prom2
            prom3 = dat3 + prom3
            time.sleep(poll_interval*1.0/1000.0)
    angle = math.degrees(math.atan2(prom2,prom1))
    return angle

#angle accel
def initialAngle():
    poll_interval = imu.IMUGetPollInterval()
    prom1 = 0
    prom2 = 0
    prom3 = 0
    for n in range(1,500) :
        if imu.IMURead():
            data = imu.getIMUData()
            accelData = data["accel"]
            dat1 = (accelData[0])
            dat2 = (accelData[1])
            dat3 = (accelData[2])
            prom1 = dat1 + prom1
            prom2 = dat2 + prom2
            prom3 = dat3 + prom3
            time.sleep(poll_interval*1.0/1000.0)
    angle = math.degrees(math.atan2(prom2,prom1))
    print angle
    return angle

#Initialize pins in motorcontroller script
speed=0.000
motors.set_speed(speed)

#Call calibration here
calibration.calibrateSensors(500,imu)

#time
initT=time.time()

# Wait for key to enter balancing mode
raw_input("------------PRESS ENTER WHEN READY TO START CONTROL LOOP------------")
# Initialize PWM to 0 
# Define previous time as time now

currentAngle=initialAngle()


try:
        while True:
            currT=time.time()
            dt=currT-initT
            initT=currT
            currentAngle=updateAngle(currentAngle)
#        # Fill in here
except KeyboardInterrupt:
	pass
# Stop PWM signals
GPIO.cleanup()
