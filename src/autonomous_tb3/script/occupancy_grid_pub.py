#! /usr/bin/env python3

# Node for publishing the OccupancyGrid Messages.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
# Additional Imports
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Header
import numpy as np


class Occupancy_Grid_Publisher(Node):

    def __init__(self):
        super().__init__('occupancy_grid_pub_node')
        self.publisher_ = self.create_publisher(OccupancyGrid, 'occupancy_grid_map', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        
    def timer_callback(self):
        # Initialising the publisher message which is of OccupancyGrid datatype.
        msg = OccupancyGrid()   
        
        # the header attribute of the message consists of a std_msgs/msg/Header type data. 
        msg.header = Header()  # Initailizing 
         
        # the 'std_msgs/msg/Header header' attribute consists of 2 propertise - 'builtin_interfaces/Time stamp' and 'string frame_id'.
        msg.header.stamp = self.get_clock().now().to_msg()   # current time
        msg.header.frame_id = 'map_frame'   # think of it as the name given to our map
             
        msg.info.resolution = 1.0
        msg.info.width = 3      # Our grid map will have 3 boxes on the x-axis direction 
        msg.info.height = 3     # Our grid map will have 3 boxes on the y-axis direction 
        # Below 3 values represents the origin position of our map (pose).
        msg.info.origin.position.x = 0.0
        msg.info.origin.position.y = 0.0
        msg.info.origin.position.z = 0.0
        
        # the 'data' attribute id the message, dictates which boxes of the grid are gonna be occupied and which boxes are gonna be un-occupied.
        msg.data = np.array([0,1,1,0,1,1,1,1,0], dtype=np.int8).tolist()
 
        
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    occupancy_grid_publisher = Occupancy_Grid_Publisher()
    print('Publishing Map...')
    rclpy.spin(occupancy_grid_publisher)
    occupancy_grid_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
  