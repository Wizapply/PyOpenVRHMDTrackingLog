#PyOpenVRHMDTrackingLog class
# -*- coding: utf-8 -*-
import openvr
import numpy as np

# ------- main -------

class PyOpenVRHMDTrackingLog:

    GET_DEVICE_NUM = 5
    LOGGER_DEVCICE = openvr.k_unTrackedDeviceIndex_Hmd

    def __init__(self):
        self.Status = False
        self.ZeroAbsolute_tk_pose = np.identity(4)
        self.Absolute_tk_pose_np = self.ZeroAbsolute_tk_pose
        self.Position = (0, 0, 0)
        self.Rotation = (0, 0, 0)

        try:
            openvr.init(openvr.VRApplication_Background)
        except Exception:
            raise Exception('Error: SteamVR launch failed!')
        
        self.Status = True

    def _toRotationAngles(self, matrix, rd):
        theta1 = np.arctan(-matrix[1, 2] / matrix[2, 2])
        theta2 = np.arctan(matrix[0, 3] * np.cos(theta1) / matrix[2, 2])
        theta3 = np.arctan(-matrix[0,1] / matrix[0, 0])

        theta1 = round(theta1 * 180 / np.pi, rd)
        theta2 = round(theta2 * 180 / np.pi, rd)
        theta3 = round(theta3 * 180 / np.pi, rd)

        return (theta1, theta2, theta3)

    def _toPosition(self, matrix, rd):
        p1 = round(matrix[0, 3], rd)    #X
        p2 = round(matrix[1, 3], rd)    #Y
        p3 = round(matrix[2, 3], rd)    #Z

        return (p1, p2, p3)

    def UpdatePose(self, rd):
        if not self.Status:
            return False

        all_poses = openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, self.GET_DEVICE_NUM)
        if len(all_poses) < 1:
            return False
    
        tracker_pose = all_poses[self.LOGGER_DEVCICE]
        if tracker_pose.eTrackingResult == openvr.TrackingResult_Running_OK and tracker_pose.bDeviceIsConnected == True:
            absolute_tk_pose = tracker_pose.mDeviceToAbsoluteTracking
            absolute_tk_pose3 = [0.0, 0.0, 0.0, 1.0]
            self.Absolute_tk_pose_np = np.matrix([absolute_tk_pose[0], absolute_tk_pose[1], absolute_tk_pose[2], absolute_tk_pose3])
        
            absolute_tk_pose_np_dot = np.dot(self.Absolute_tk_pose_np, self.ZeroAbsolute_tk_pose)
            self.Position = self._toPosition(absolute_tk_pose_np_dot, rd)
            self.Rotation = self._toRotationAngles(absolute_tk_pose_np_dot, rd)

            return True

        return False

    def ResetZeroPose(self):
        if not self.Status:
            return False
        self.ZeroAbsolute_tk_pose = np.linalg.inv(self.Absolute_tk_pose_np)
        return True
    
    def GetPosition(self):
        return self.Position

    def GetRotation(self):
        return self.Rotation

    def Close(self):
        if not self.Status:
            return

        openvr.shutdown()