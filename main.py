#HMD HeadTracking to CSV
#req: pip install openvr

import msvcrt, csv
import time, socket
import PyOpenVRHMDTrackingLog

from ctypes import windll

# ------- def func -------

def kbHit():
    result = 0
    if msvcrt.kbhit():
        kb = ord(msvcrt.getch())
        if kb == 0x00:
            kb2 = ord(msvcrt.getch())
            if kb2 == 0x43: #F9
                result = 1
            if kb2 == 0x44: #F10
                result = 2
        if kb == 0x1B:      #ESC
            result = 3
    return result

# ------- main -------

print('HMD Vive Tracking to CSV')
print('  (C)WIZAPPLY CO.,LTD.')

try:
    svhl = PyOpenVRHMDTrackingLog.PyOpenVRHMDTrackingLog()
except Exception as e:
    print('Error: SteamVR Application launch failed!')
    exit()

csv_file_w = None
tracking_data_csv_path = './tracking_data.csv'

print('Tracking Start....')
print('[F9]Key: RESET ZERO POSE')
print('[F10]Key: Start&Stop SAVE DATA to CSV files')

#time
time_sta = time.time()

windll.winmm.timeBeginPeriod(1)
while True:
    if svhl.UpdatePose(6):
        #show
        position = svhl.GetPosition()
        rotation = svhl.GetRotation()
        curTime = time.time() - time_sta

        viewData = (round(curTime,4), position[0],position[1],position[2])
        #print(viewData) #debug
        if not csv_file_w is None and not csv_file_w.closed:
            dataf_w.writerow(viewData) #save

    res = kbHit()
    if res == 1:    #f9
        svhl.ResetZeroPose()
        print('RESET ZERO POSE')
    if res == 2:    #f10
        if csv_file_w is None or csv_file_w.closed:
            csv_file_w = open(tracking_data_csv_path, 'w', encoding='utf_8_sig', errors='', newline='')
            dataf_w = csv.writer(csv_file_w, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"', skipinitialspace=True)
            dataf_w.writerow(['Time(s)','PosX(m)','PosY(m)','PosZ(m)','RotX(deg)','RotY(deg)','RotZ(deg)'])
            print('START RECORD DATA TO CSV FILE. -> ./tracking_data.csv')
        else:
            csv_file_w.close()
            csv_file_w = None
            print('TRACKING DATA WAS RECORDED.')
    if res == 3:    #end
        break

    time.sleep(.01) #10ms

svhl.Close()
if not csv_file_w is None and not csv_file_w.closed:
    csv_file_w.close()
windll.winmm.timeEndPeriod(1)

print('FINISH TRACKER.')