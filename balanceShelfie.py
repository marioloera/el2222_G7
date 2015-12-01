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
def updateAngle(angle,dt):
        # Fill in here

        angleAcce,angleGyro=initialAngle()
        #angleGyro=gyro()

        newAngle=0.98*(angle+angleGyro*dt)+0.02*(angleAcce)

	return newAngle

x=1
#angle gyro
def gyro():
    poll_interval = imu.IMUGetPollInterval()
    prom1 = 0
    prom2 = 0
    prom3 = 0
    for n in range(0,x) :
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
    angle = math.degrees(math.atan2(prom3/x,prom2/x))-90
    return angle


def initialAngle():
    poll_interval = imu.IMUGetPollInterval()
    prom1 = 0
    prom2 = 0
    prom3 = 0
    while True:
        if imu.IMURead():
            data = imu.getIMUData()
            gyroData = data["gyro"]
            accelData = data["accel"]
            dat1 = accelData[0]
            dat2 = accelData[1]
            dat3 = accelData[2]
            prom1 = dat1 + prom1
            prom2 = dat2 + prom2
            prom3 = dat3 + prom3
            time.sleep(poll_interval*1.0/1000.0)
            angle = math.degrees(math.atan2(prom3/x,prom2/x))-90
            return angle, math.degrees(gyroData[0])

#Initialize pins in motorcontroller script
speed=0.000
motors.set_speed(speed)

#Call calibration here
calibration.calibrateSensors(500,imu)

#time
initT=time.time()

# Initialize PWM to 0 
# Define previous time as time now
y=1
currentAngle=0
angleAcce=0
print "calculation home angle"
for n in range(0,y):
    angleAcce,angleGyro=initialAngle()
    currentAngle=currentAngle+angleAcce
currentAngle=currentAngle/y
controlAngle=currentAngle
print str(controlAngle)
error=0
kp=5
ki=kp/5
kd=0.000
dt=0.001
I_term=0
minAng=0
maxAng=0
# Wait for key to enter balancing mode
raw_input("------------PRESS ENTER WHEN READY TO START CONTROL LOOP------------")

try:
        while True:
            currT=time.time()
            dt=currT-initT
            initT=currT
            currentAngle=updateAngle(currentAngle,dt)
            print str(currentAngle)
            if currentAngle<minAng:
                minAng=currentAngle
            if currentAngle>maxAng:
                maxAng=currentAngle
            currentAngle0=currentAngle
            if abs(currentAngle0)<1.5:
                currentAngle0=0
            error=currentAngle-controlAngle
            P_term=kp*error
            #I_term=(ki*error)+I_term
            #D_term=kd*dt
            u=P_term#+I_term
            print "angle= "+str(currentAngle)+ " u:   " + str(u) +" e: "+str(error) 
            motors.set_speed(u)
#        # Fill in here

except KeyboardInterrupt:
	pass
# Stop PWM signals
print "max= "+str(maxAng) +" min="+str(minAng)
GPIO.cleanup()
