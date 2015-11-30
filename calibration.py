import math
import time

def calibrateSensors(n, imu):
	cal_check = raw_input("Press y to calibrate, any other key to continue without calibrating\n")
	if cal_check == "y":
        	gyroSum = 0
        	print("-----Sensor calibration has begun-----")
        	for i in range(n):
                	if imu.IMURead():
                        	gyroData = imu.getIMUData()["gyro"]
                        	gyroSum += math.degrees(gyroData[0])
                        	time.sleep(0.01)
        	gyroBias = gyroSum/n
        	print("Gyroscope bias",gyroBias)
        	print("-----Sensor calibration has finished-----")
	else:
		print("You chose not to calibrate")
                print("Gyroscope bias",0)
	       	gyroBias = 0

        return gyroBias
