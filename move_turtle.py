

# Run turtlesim by : rosrun turtlesim turtlesim_node

# To see what all topics are available in the turtlesim_node : rostopic list
# $ rostopic list

# /rosout
# /rosout_agg
# /turtle1/cmd_vel
# /turtle1/color_sensor
# /turtle1/pose

# To move the turtle inside the turtlesim application, publish the linear and angular velocity to the /turtle1/cmd_vel topic.
# To know the position of the robot, subscribe to /turtle1/pose topic 

#But we dont know the type of topic (eg. the type in "hello world" is string), so to get that use : rostopic type /turtle1/cmd_vel
# $rostopic type /turtle1/cmd_vel
# geometry_msgs/Twist

# This means that the /cmd_vel topic has the geometry_msgs/Twist message type, so we have to publish the same message type to this topic to
# move the robot.

# To see what all data is supported by geometry_msgs/Twist use : rosmsg show geometry_msgs/Twist

# $rosmsg show geometry_msgs/Twist
# geometry_msgs/Vector3 linear 
# 	float64 x
# 	float64 y
# 	float64 z
# geometry_msgs/Vector3 angular 
# 	float64 x
# 	float64 y
# 	float64 z

################################################################################################################################################

# To know the position of the robot, subscribe to "/turtle1/pose" topic 
# Lets see what is the type of "/turtle1/pose" and what kind of data does it have 

# $rostopic type /turtle1/pose
# turtlsim/Pose

# $rosmsg show turtlesim/Pose
# float32 x
# float32 y
# float32 z
# float32 theta
# float32 linear_velocity
# float32 angular_velocity

################################################################################################################################################
#!/usr/bin/env python
import rospy

#Importing Twist message: Used to send velocity to Turtlesim
from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

# To input linear and angular vel from console 
import sys 

# callback function for the subscriber. It is called everytime a subscriber recives a message. 
def pose_callback(pose):
	# print on console 
	rospy.loginfo("Robot X = %f : Y=%f : Z=%f\n",pose.x,pose.y,pose.theta)


#Function to move turtle: Linear and angular velocities are arguments
def move_turtle(lin_vel,ang_vel):

    rospy.init_node('move_turtle', anonymous=False)

    # The /turtle1/cmd_vel is the topic in which we have to send Twist messages
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
	
    
    # SYNATX : rospy.Subscriber("topic_name",message_type,callback funtion name)
    #Creating new subscriber: 
    # topic name= /turtle1/pose:
    # message_type = Pose
    # callback funtion name = pose_callback
    rospy.Subscriber('/turtle1/pose',Pose, pose_callback)


    rate = rospy.Rate(10) # 10hz
     
    # #Creating Twist message instance
    vel = Twist()

    while not rospy.is_shutdown():
        
	# Adding linear and angular velocity to the message
	vel.linear.x = lin_vel
	vel.linear.y = 0
	vel.linear.z = 0

	vel.angular.x = 0
	vel.angular.y = 0
	vel.angular.z = ang_vel

        rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)
        
	# Publishing Twist message
        pub.publish(vel)

        rate.sleep()

if __name__ == '__main__':
    try:
        move_turtle(float(sys.argv[1]),float(sys.argv[2]))
    except rospy.ROSInterruptException:
        pass
