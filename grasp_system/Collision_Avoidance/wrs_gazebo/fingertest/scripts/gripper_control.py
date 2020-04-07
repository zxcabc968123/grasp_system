#!/usr/bin/env python
# encoding: utf-8   #要打中文時加這行
import rospy
import sys
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
class Gripper:
    def __init__(self): 
        self.publisher_rate=50
        self.finger_joint1='/fingertest/m_joint1_position_controller/command'
        self.finger_joint2='/fingertest/m_joint2_position_controller/command'
        self.finger_joint3='/fingertest/m_joint3_position_controller/command'

        rospy.init_node('gripper_control',anonymous=False) #初始化node    anonymous=True  在node名稱後加入亂碼    避免相同名稱的node踢掉彼此

    def command_convert(self):
        direction=float(sys.argv[1])
        return direction
    
    def get_gripper_state(self,joint):
        joint_now=rospy.wait_for_message('/fingertest/joint_states',JointState)
        joint=joint-1
        return joint_now.position[joint]

    def send_gripper_command(self):
        pub1=rospy.Publisher(self.finger_joint1,Float64,queue_size=10)
        pub2=rospy.Publisher(self.finger_joint2,Float64,queue_size=10)
        pub3=rospy.Publisher(self.finger_joint3,Float64,queue_size=10)
        #pub:publish名稱   chatter:topic name  queue_size=緩衝區大小
        rate=rospy.Rate(self.publisher_rate)

        direction=self.command_convert()

        if direction==1.0:
            rospy.loginfo('The gripper is closing')
            joint1_ang=self.get_gripper_state(4)
            joint2_ang=self.get_gripper_state(5)
            joint3_ang=self.get_gripper_state(6)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            while joint1_ang>-1.221:

                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)
                rospy.sleep(0.03)
                joint1_ang=joint1_ang-0.01
                joint3_ang=joint3_ang+0.01
            while joint2_ang>-1.57:
                pub2.publish(joint2_ang)
                rospy.sleep(0.03)
                joint2_ang=joint2_ang-0.01
        elif direction==2.0:
            rospy.loginfo('The gripper is opening')
            joint1_ang=self.get_gripper_state(4)
            joint2_ang=self.get_gripper_state(5)
            joint3_ang=self.get_gripper_state(6)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            
            while joint2_ang<0:
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)
                rospy.sleep(0.03)
                joint2_ang=joint2_ang+0.01
            while joint1_ang<0:
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)
                rospy.sleep(0.03)
                joint1_ang=joint1_ang+0.01
                joint3_ang=joint3_ang-0.01



        
if __name__=='__main__':
    try:
        a=Gripper()
        a.send_gripper_command()
    except  rospy.ROSInterruptException:
        rospy.loginfo('end')
        pass