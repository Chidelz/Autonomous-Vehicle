import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray
from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import Pose
import math

alpha = 0.5
beta = 1.0 - alpha



class odomNavigation(Node):

    def __init__(self):
        super().__init__('odom_navigation')
        self.subscriber = self.create_subscription(Odometry, 'odometry/filtered', self.pose_callback, 10)
        self.publisher = self.create_publisher(AckermannDriveStamped, 'ackermann_cmd', 10)
        self.waypoints = self.load_waypoints('path.txt')
        self.waypoint_index = 0

    def pose_callback(self, msg):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        linear_velocity = msg.twist.twist.linear
        angular_velocity = msg.twist.twist.angular
        
        print("Current Pose:", position,orientation,linear_velocity,angular_velocity)
        
        next_waypoint = self.waypoints[self.waypoint_index]
        distance_to_waypoint = self.calculate_distance(position, next_waypoint.position)
        
    def load_waypoints(self, file_path):
        waypoints = []
        with open(file_path, 'r') as file:
            for line in file:
                x, y, theta = map(float, line.strip().split())
                waypoints.append(Pose(position=Point(x,y,0), orientation=Quaternion(*quaternion_from_euler(0, 0, theta))))
        return waypoints
        
    def calculate_distance(self, position1, position2):
        dx = position1.x -position2.x
        dy = position1.y - position2.y
        return math.sqrt(dx**2 + dy**2)
        
    def calculate_steering_angle(self, position, orientation, waypoint):
        # Calculate the desired steering angle to reach the next waypoint
        # You can use the position, orientation, and waypoint data to calculate the desired steering angle
        # This is just a placeholder, you'll need to implement your own steering angle calculation
        return 0.0
        
    def publish_ackermann_cmd(self, velocity, acceleration, steering_angle):
        #Create an AckermannDriveStamped message
        drive_msg = AckermannDriveStamped()
        drive_msg.drive.speed = velocity
        drive_msg.drive.acceleration = acceleration
        drive_msg.drive.steering_angle = steering_angle

        # Publish the Ackermann drive command
        self.publisher.publish(drive_msg)
        
        
def main(args= None):
    rclpy.init(args=args)
    odom_navigation = odomNavigation()
    rclpy.spin(odom_navigation)
    odom_navigation.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
