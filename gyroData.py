import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import getopt

import sys, getopt

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

if __name__ == "__main__":
   main(sys.argv[1:])


file=open('gyroData1.txt','w')
SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed");
    sys.exit(1)
else:
    print("IMU Init Succeeded");

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

try:
  while True:
    if imu.IMURead():
      data = imu.getIMUData()
      gyroData = data["gyro"]
      print("x: %f y: %f z: %f" % (gyroData[0], gyroData[1], gyroData[2]))
      file.write(str(180*gyroData[0]/3.1416)+" ")
      file.write(str(180*gyroData[1]/3.1416)+" ")
      file.write(str(180*gyroData[2]/3.1416)+"\n")
      time.sleep(poll_interval*1.0/1000.0)
except KeyboardInterrupt:
  pass
file.close()

