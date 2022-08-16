#HMD HeadTracking to CSV
# -*- coding: utf-8 -*-
import msvcrt, csv
import time
import PyOpenVRHMDTrackingLog

from ctypes import windll

# ------- def func -------

def kbHit():
    result = 0
    if msvcrt.kbhit():
        kb = ord(msvcrt.getch())
        if kb == 0x00:
            kb2 = ord(msvcrt.getch())
            if kb2 == 0x43:
                result = 1
        if kb == 0x1B:
            result = 2
    return result

# ------- main -------

print("HMD HeadTracking to CSV")
print("  (C)WIZAPPLY CO.,LTD.")

try:
    svhl = PyOpenVRHMDTrackingLog.PyOpenVRHMDTrackingLog()
except Exception as e:
    print("Error: SteamVR Application launch failed!")
    exit()

csv_file_w = open('./test_data.csv', 'w', encoding='utf_8_sig', errors='', newline='')
dataf_w = csv.writer(csv_file_w, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"', skipinitialspace=True)
dataf_w.writerow(['Time(s)','PosX(m)','PosY(m)','PosZ(m)','RotX(deg)','RotY(deg)','RotZ(deg)'])

print("Tracking Start....")
print("[F9]Key: RESET ZERO POSE")

#time
time_sta = time.time()

windll.winmm.timeBeginPeriod(1)
while True:
    if svhl.UpdatePose(5):
        #show
        position = svhl.GetPosition()
        rotation = svhl.GetRotation()
        curTime = (time.time() - time_sta, )

        viewData = round(curTime,4) + position + rotation
        print(viewData) #debug
        dataf_w.writerow(viewData) #save

    res = kbHit()
    if res == 1:
        svhl.ResetZeroPose()
        print("RESET ZERO POSE")
    if res == 2:
        break

    time.sleep(.01) #10ms

svhl.Close()
csv_file_w.close()
windll.winmm.timeEndPeriod(1)

print("FINISH: Save CSV")