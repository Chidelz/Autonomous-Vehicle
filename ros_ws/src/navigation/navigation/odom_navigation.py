import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray
from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import Pose, Quaternion, Point
import math

class odomNavigation(Node):

    def __init__(self):
        super().__init__('odom_navigation')
        self.subscriber = self.create_subscription(Odometry, 'odometry/filtered', self.pose_callback, 10)
        self.publisher = self.create_publisher(AckermannDriveStamped, 'ackermann_cmd', 10)
        self.waypoints = self.load_waypoints('/496/ros_ws/src/navigation/4_corners_waypoints.txt')
        self.waypoint_index = 0

    def pose_callback(self, msg):
        min_dist = 0.5 # minimum distance to waypoint in meters
        desired_velocity = 1.0
        acceleration = 1.0
        
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        linear_velocity = msg.twist.twist.linear
        angular_velocity = msg.twist.twist.angular
        
        #print("Current Pose:", position,orientation,linear_velocity,angular_velocity)
        
        # Compare current pose with the next waypoint
        next_waypoint = self.waypoints[self.waypoint_index]
        distance_to_waypoint = self.calculate_distance(position, next_waypoint.position)
        
        if distance_to_waypoint < min_dist:
            self.waypoint_index += 1
            if self.waypoint_index == len(self.waypoints):
                #reached final waypoint (start line), stop the robot
                self.publish_ackermann_cmd(0.0,0.0,0.0)
                return
                
        desired_steering_angle = self.calculate_steering_angle(position, orientation, next_waypoint)
        
        self.publish_ackermann_cmd(desired_velocity, acceleration, desired_steering_angle)
        
        
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
        #Note that this approach assumes that the orientation quaternion is in the form (x, y, z, w), where w is the scalar part, and (x, y, z) is the vector part
        
        # calculate the vector from the current position to the waypoint
        waypoint_vector = [waypoint.position.x - position.x, waypoint.position.y - position.y]
        
        # calculate the angle between the robot's heading and the waypoint vector
        robot_heading = 2 * math.atan2(orientation.z, orientation.w)
        waypoint_angle = math.atan2(waypoint_vector[1], waypoint_vector[0])
        angle_diff = waypoint_angle - robot_heading
        
        # normalize the angle difference to [-pi,pi]
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi
        
        # calculate the desired steering angle using the pure pursuit algorithm
        lookahead_distance = 1.0 # adjust this value as needed
        desired_steering_angle = math.atan2(2.0 * math.sin(angle_diff) * lookahead_distance, math.sqrt(1 + (2 * math.cos(angle_diff) * lookahead_distance)**2))
        
        return desired_steering_angle
        
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
