#!/usr/bin/env python3

import math
import time

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node


class StartupInitialPose(Node):
    def __init__(self):
        super().__init__('startup_initial_pose')

        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw', 0.0)

        self._x = float(self.get_parameter('x').value)
        self._y = float(self.get_parameter('y').value)
        self._yaw = float(self.get_parameter('yaw').value)

        self._pub = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)

    def _wait_for_sim_time(self, timeout_sec: float = 20.0) -> bool:
        start = time.time()
        while rclpy.ok() and (time.time() - start) < timeout_sec:
            now_ns = self.get_clock().now().nanoseconds
            if now_ns > 0:
                return True
            rclpy.spin_once(self, timeout_sec=0.1)
        return False

    def _wait_for_subscriber(self, timeout_sec: float = 20.0) -> bool:
        start = time.time()
        while rclpy.ok() and (time.time() - start) < timeout_sec:
            if self._pub.get_subscription_count() > 0:
                return True
            rclpy.spin_once(self, timeout_sec=0.1)
        return False

    def publish_initial_pose(self):
        if not self._wait_for_sim_time():
            self.get_logger().warn('Sim time did not become active before timeout; publishing anyway.')

        if not self._wait_for_subscriber():
            self.get_logger().warn('No /initialpose subscribers detected before timeout; publishing anyway.')

        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.pose.pose.position.x = self._x
        msg.pose.pose.position.y = self._y
        msg.pose.pose.position.z = 0.0

        half_yaw = self._yaw / 2.0
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = math.sin(half_yaw)
        msg.pose.pose.orientation.w = math.cos(half_yaw)

        msg.pose.covariance = [
            0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942,
        ]

        # Use stamp=0 so AMCL resolves against latest available TF and avoids
        # startup-time extrapolation races.
        msg.header.stamp.sec = 0
        msg.header.stamp.nanosec = 0

        # Publish a few times to ensure AMCL receives the pose after startup churn.
        for _ in range(5):
            self._pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.2)

        self.get_logger().info('Published startup initial pose to /initialpose.')


def main():
    rclpy.init()
    node = StartupInitialPose()
    node.publish_initial_pose()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
