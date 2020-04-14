#!/usr/bin/env python
# encoding: utf-8   #要打中文時加這行
import rospy
import sys
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ContactsState
class Gripper:
    def __init__(self): 
        self.publisher_rate=100
        self.m_finger_joint1='/mobile_dual_arm/m_joint1_position_controller/command'
        self.m_finger_joint2='/mobile_dual_arm/m_joint2_position_controller/command'
        self.m_finger_joint3='/mobile_dual_arm/m_joint3_position_controller/command'

        self.l_finger_joint1='/mobile_dual_arm/l_joint1_position_controller/command'
        self.l_finger_joint2='/mobile_dual_arm/l_joint2_position_controller/command'
        self.l_finger_joint3='/mobile_dual_arm/l_joint3_position_controller/command'

        self.r_finger_joint1='/mobile_dual_arm/r_joint1_position_controller/command'
        self.r_finger_joint2='/mobile_dual_arm/r_joint2_position_controller/command'
        self.r_finger_joint3='/mobile_dual_arm/r_joint3_position_controller/command'

        self.l_finger_joint='/mobile_dual_arm/l_finger_joint_position_controller/command'
        self.r_finger_joint='/mobile_dual_arm/r_finger_joint_position_controller/command'

        rospy.init_node('gripper_control',anonymous=False) #初始化node    anonymous=True  在node名稱後加入亂碼    避免相同名稱的node踢掉彼此
        self.l_Link3_bumper=False
        self.r_Link3_bumper=False
    # def command_convert(self):
    #     direction=float(sys.argv[1])
    #     return direction
    
    def get_gripper_state(self,joint):
        joint_now=rospy.wait_for_message('/mobile_dual_arm/joint_states',JointState)
        joint=joint
        return joint_now.position[joint]

    def get_rotating_state(self):
        joint_now=rospy.wait_for_message('/mobile_dual_arm/joint_states',JointState)
        return joint_now.position[5]
    
    def get_bumper_state(self,Link_bumper):
        bumper_now=rospy.wait_for_message(Link_bumper,ContactsState,timeout=1)
        #rospy.loginfo('00000000000000000')
        #print(bumper_now.states)
        # for state in bumper_now.states:
        if not bumper_now.states:
            return False
        else:
            return True

###############################################
    def send_finger_one(self,one,direction):
        if one=='r':
            joint1=self.r_finger_joint1
            joint2=self.r_finger_joint2
            joint3=self.r_finger_joint3
            feed_back=16
        elif one=='l':
            joint1=self.l_finger_joint1
            joint2=self.l_finger_joint2
            joint3=self.l_finger_joint3
            feed_back=2
        elif one=='m':
            joint1=self.m_finger_joint1
            joint2=self.m_finger_joint2
            joint3=self.m_finger_joint3
            feed_back=13

        pub1=rospy.Publisher(joint1,Float64,queue_size=10)
        pub2=rospy.Publisher(joint2,Float64,queue_size=10)
        pub3=rospy.Publisher(joint3,Float64,queue_size=10)
        #pub:publish名稱   chatter:topic name  queue_size=緩衝區大小
        rate=rospy.Rate(self.publisher_rate)

        # direction=self.command_convert()

        if direction==1.0:
            rospy.loginfo('The gripper is closing')
            joint1_ang=self.get_gripper_state(feed_back)
            joint2_ang=self.get_gripper_state(feed_back+1)
            joint3_ang=self.get_gripper_state(feed_back+2)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            while joint1_ang>-1.221:

                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)
                rospy.sleep(0.01)
                joint1_ang=joint1_ang-0.01
                joint3_ang=joint3_ang+0.01
            while joint2_ang>-1.57:
                pub2.publish(joint2_ang)
                rospy.sleep(0.01)
                joint2_ang=joint2_ang-0.01
        elif direction==2.0:
            rospy.loginfo('The gripper is opening')
            joint1_ang=self.get_gripper_state(feed_back)
            joint2_ang=self.get_gripper_state(feed_back+1)
            joint3_ang=self.get_gripper_state(feed_back+2)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            
            while joint2_ang<0:
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)
                rospy.sleep(0.01)
                joint2_ang=joint2_ang+0.01
            while joint1_ang<0:
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)
                rospy.sleep(0.01)
                joint1_ang=joint1_ang+0.01
                joint3_ang=joint3_ang-0.01
###################################################
    def send_rotating_command(self,ang):
        pub4=rospy.Publisher(self.l_finger_joint,Float64,queue_size=10)
        pub5=rospy.Publisher(self.r_finger_joint,Float64,queue_size=10)
        #rate=rospy.Rate(self.publisher_rate)
        rate=rospy.Rate(100)
        roating_ang=self.get_rotating_state()
        rospy.loginfo('Rotating now =%.2f',roating_ang)
        if ang>roating_ang:
            while ang>roating_ang:
                pub4.publish(roating_ang)
                pub5.publish(roating_ang)
                rospy.sleep(0.01)
                roating_ang=roating_ang+0.02
            pub4.publish(ang)
            pub5.publish(ang)
        elif ang<roating_ang:
            while ang<roating_ang:
                pub4.publish(roating_ang)
                pub5.publish(roating_ang)
                rospy.sleep(0.01)
                roating_ang=roating_ang-0.02
            pub4.publish(ang)
            pub5.publish(ang)
        rospy.loginfo('End Rotating=%.2f',roating_ang)
        rospy.sleep(1.5)
####################################################################ALL
    def send_finger_all(self,direction):
        pub1=rospy.Publisher(self.r_finger_joint1,Float64,queue_size=10)
        pub2=rospy.Publisher(self.r_finger_joint2,Float64,queue_size=10)
        pub3=rospy.Publisher(self.r_finger_joint3,Float64,queue_size=10)
        pub4=rospy.Publisher(self.l_finger_joint1,Float64,queue_size=10)
        pub5=rospy.Publisher(self.l_finger_joint2,Float64,queue_size=10)
        pub6=rospy.Publisher(self.l_finger_joint3,Float64,queue_size=10)
        pub7=rospy.Publisher(self.m_finger_joint1,Float64,queue_size=10)
        pub8=rospy.Publisher(self.m_finger_joint2,Float64,queue_size=10)
        pub9=rospy.Publisher(self.m_finger_joint3,Float64,queue_size=10)
        #pub:publish名稱   chatter:topic name  queue_size=緩衝區大小
        rate=rospy.Rate(self.publisher_rate)

        if direction==1.0:
            rospy.loginfo('The gripper is closing')
            joint1_ang=self.get_gripper_state(2)
            joint2_ang=self.get_gripper_state(3)
            joint3_ang=self.get_gripper_state(4)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            while (joint1_ang>-1.221 and (self.l_Link3_bumper==False or self.r_Link3_bumper==False or self.m_Link3_bumper==False)):

                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)

                pub4.publish(joint1_ang)
                pub5.publish(joint2_ang)
                pub6.publish(joint3_ang)

                pub7.publish(joint1_ang)
                pub8.publish(joint2_ang)
                pub9.publish(joint3_ang)
                ###
                self.l_Link3_bumper=self.get_bumper_state('l_Link3_bumper')
                self.r_Link3_bumper=self.get_bumper_state('r_Link3_bumper')
                self.m_Link3_bumper=self.get_bumper_state('m_Link3_bumper')
                ###
                rospy.sleep(0.01)
                joint1_ang=joint1_ang-0.01
                joint3_ang=joint3_ang+0.01
            force_ang=joint3_ang
            for i in range(100):
                joint3_ang=joint3_ang-0.01
                pub3.publish(joint3_ang)
                pub6.publish(joint3_ang)
                pub9.publish(joint3_ang)
                rospy.sleep(0.01)
            while (joint2_ang>-1.57 and (self.l_Link3_bumper==False or self.r_Link3_bumper==False or self.m_Link3_bumper==False)):
                pub2.publish(joint2_ang)

                pub5.publish(joint2_ang)

                pub8.publish(joint2_ang)
                ###
                self.l_Link3_bumper=self.get_bumper_state('l_Link3_bumper')
                self.r_Link3_bumper=self.get_bumper_state('r_Link3_bumper')
                self.m_Link3_bumper=self.get_bumper_state('m_Link3_bumper')
                ###

                rospy.sleep(0.01)
                joint2_ang=joint2_ang-0.01
        elif direction==2.0:
            rospy.loginfo('The gripper is opening')
            joint1_ang=self.get_gripper_state(2)
            joint2_ang=self.get_gripper_state(3)
            joint3_ang=self.get_gripper_state(4)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            
            while joint2_ang<0:
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)

                pub4.publish(joint1_ang)
                pub5.publish(joint2_ang)
                pub6.publish(joint3_ang)

                pub7.publish(joint1_ang)
                pub8.publish(joint2_ang)
                pub9.publish(joint3_ang)
                
                rospy.sleep(0.01)
                joint2_ang=joint2_ang+0.01
            while joint1_ang<0:
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)

                pub4.publish(joint1_ang)
                pub5.publish(joint2_ang)
                pub6.publish(joint3_ang)

                pub7.publish(joint1_ang)
                pub8.publish(joint2_ang)
                pub9.publish(joint3_ang)

                rospy.sleep(0.01)
                joint1_ang=joint1_ang+0.01
                joint3_ang=joint3_ang-0.01
#######################################################2finger
    def send_finger_two(self,direction):
        pub1=rospy.Publisher(self.r_finger_joint1,Float64,queue_size=10)
        pub2=rospy.Publisher(self.r_finger_joint2,Float64,queue_size=10)
        pub3=rospy.Publisher(self.r_finger_joint3,Float64,queue_size=10)
        pub4=rospy.Publisher(self.l_finger_joint1,Float64,queue_size=10)
        pub5=rospy.Publisher(self.l_finger_joint2,Float64,queue_size=10)
        pub6=rospy.Publisher(self.l_finger_joint3,Float64,queue_size=10)

        #pub:publish名稱   chatter:topic name  queue_size=緩衝區大小
        rate=rospy.Rate(self.publisher_rate)

        if direction==1.0:
            rospy.loginfo('The gripper is closing')
            joint1_ang=self.get_gripper_state(2)
            joint2_ang=self.get_gripper_state(3)
            joint3_ang=self.get_gripper_state(4)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            while (joint1_ang>-1.221 and (self.l_Link3_bumper==False or self.r_Link3_bumper==False)):
               
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)

                pub4.publish(joint1_ang)
                pub5.publish(joint2_ang)
                pub6.publish(joint3_ang)

                ###
                self.l_Link3_bumper=self.get_bumper_state('l_Link3_bumper')
                self.r_Link3_bumper=self.get_bumper_state('r_Link3_bumper')
                ###
                
                rospy.sleep(0.01)
                joint1_ang=joint1_ang-0.01
                joint3_ang=joint3_ang+0.01
            
            ##############
           
            while (joint2_ang>-1.57 and (self.l_Link3_bumper==False or self.r_Link3_bumper==False)):
                print(self.l_Link3_bumper)
                print(self.r_Link3_bumper)
                pub2.publish(joint2_ang)

                pub5.publish(joint2_ang)
                
                ###
                self.l_Link3_bumper=self.get_bumper_state('l_Link3_bumper')
                self.r_Link3_bumper=self.get_bumper_state('r_Link3_bumper')
                ###

                rospy.sleep(0.01)
                joint2_ang=joint2_ang-0.01
        elif direction==2.0:
            rospy.loginfo('The gripper is opening')
            joint1_ang=self.get_gripper_state(2)
            joint2_ang=self.get_gripper_state(3)
            joint3_ang=self.get_gripper_state(4)
            rospy.loginfo('Joint angle now = [ %.2f %.2f %.2f ]' ,joint1_ang,joint2_ang,joint3_ang)
            
            while joint2_ang<0:
                ###
                self.get_bumper_state('l_Link3_bumper')
                ###
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)

                pub4.publish(joint1_ang)
                pub5.publish(joint2_ang)
                pub6.publish(joint3_ang)

                rospy.sleep(0.01)
                joint2_ang=joint2_ang+0.01
            while joint1_ang<0:
                ###
                self.get_bumper_state('l_Link3_bumper')
                ###
                pub1.publish(joint1_ang)
                pub2.publish(joint2_ang)
                pub3.publish(joint3_ang)

                pub4.publish(joint1_ang)
                pub5.publish(joint2_ang)
                pub6.publish(joint3_ang)

                rospy.sleep(0.01)
                joint1_ang=joint1_ang+0.01
                joint3_ang=joint3_ang-0.01
    def send_finger_reset(self):
        pub1=rospy.Publisher(self.r_finger_joint1,Float64,queue_size=10)
        pub2=rospy.Publisher(self.r_finger_joint2,Float64,queue_size=10)
        pub3=rospy.Publisher(self.r_finger_joint3,Float64,queue_size=10)
        pub4=rospy.Publisher(self.l_finger_joint1,Float64,queue_size=10)
        pub5=rospy.Publisher(self.l_finger_joint2,Float64,queue_size=10)
        pub6=rospy.Publisher(self.l_finger_joint3,Float64,queue_size=10)
        pub7=rospy.Publisher(self.m_finger_joint1,Float64,queue_size=10)
        pub8=rospy.Publisher(self.m_finger_joint2,Float64,queue_size=10)
        pub9=rospy.Publisher(self.m_finger_joint3,Float64,queue_size=10)
        #pub:publish名稱   chatter:topic name  queue_size=緩衝區大小
        rate=rospy.Rate(self.publisher_rate)

        pub1.publish(0)
        pub2.publish(0)
        pub3.publish(0)

        pub4.publish(0)
        pub5.publish(0)
        pub6.publish(0)

        pub7.publish(0)
        pub8.publish(0)
        pub9.publish(0)




if __name__=='__main__':
    try:
        a=Gripper()
        # a.send_finger_one('r',1)
        # a.send_finger_one('r',2)
        # a.send_finger_one('m',1)
        # a.send_finger_one('m',2)
        # a.send_finger_one('l',1)
        # a.send_finger_one('l',2)
        #a.send_rotating_command(0)
        a.send_finger_all(1)
        # a.send_finger_all(2)
        #a.send_rotating_command(1.57)
        #a.send_finger_two(1)
        #a.send_finger_two(1)
        #a.send_finger_one('m',2)
        #a.send_finger_two(2)
        #a.send_rotating_command(0)
        #a.send_rotating_command(1.57)
        # a.send_finger_two(2)
        # a.send_finger_one('m',2)
        # a.send_rotating_command(0)
        #a.send_rotating_command(1)
        rospy.loginfo('123')
    except  rospy.ROSInterruptException:
        rospy.loginfo('end')
        pass