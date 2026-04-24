#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_maze = get_package_share_directory('autonomous_tb3')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    launch_file_dir = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'), 'launch')

    maze_world = os.path.join(pkg_maze, 'worlds', 'maze_model.world')
    maze_map = os.path.join(pkg_maze, 'config', 'maze_model', 'maze_world_map.yaml')
    nav2_params = os.path.join(pkg_maze, 'config', 'tb3_nav_params.yaml')
    rviz_config = os.path.join(pkg_maze, 'config', 'tb3_nav.rviz')
    gazebo_model_path = os.pathsep.join([
        os.path.join(pkg_maze, 'worlds'),
        os.path.expanduser('~/.gazebo/models'),
        os.environ.get('GAZEBO_MODEL_PATH', '')
    ])

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    use_gui = LaunchConfiguration('use_gui', default='true')
    use_rviz = LaunchConfiguration('use_rviz', default='true')
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    extra_gazebo_args = LaunchConfiguration(
        'extra_gazebo_args',
        default='')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_node',
        arguments=['-d', rviz_config],
        additional_env={
            'LIBGL_ALWAYS_SOFTWARE': '1',
            'MESA_GL_VERSION_OVERRIDE': '3.3',
        },
        output='screen',
        condition=IfCondition(use_rviz),
    )

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': maze_map,
            'params_file': nav2_params,
            'use_sim_time': use_sim_time,
            'autostart': 'true',
            'use_localization': 'True',
            'slam': 'False',
        }.items(),
    )

    delayed_initial_pose = TimerAction(
        period=45.0,
        actions=[
            Node(
                package='autonomous_tb3',
                executable='startup_initial_pose.py',
                name='startup_initial_pose',
                parameters=[{
                    'use_sim_time': True,
                    'x': 0.0,
                    'y': 0.0,
                    'yaw': 0.0,
                }],
                output='screen',
            ),
        ],
    )

    delayed_spawn = TimerAction(
        period=15.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')),
                launch_arguments={
                    'x_pose': x_pose,
                    'y_pose': y_pose
                }.items()
            ),
        ],
    )

    delayed_navigation = TimerAction(
        period=35.0,
        actions=[
            nav2_bringup,
        ],
    )

    delayed_rviz = TimerAction(
        period=42.0,
        actions=[
            rviz_node,
        ],
    )

    return LaunchDescription([
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'waffle'),
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', gazebo_model_path),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
            launch_arguments={
                'world': maze_world,
                'extra_gazebo_args': extra_gazebo_args
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')),
            condition=IfCondition(use_gui)
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')),
            launch_arguments={'use_sim_time': use_sim_time}.items()
        ),
        # Start Gazebo first, then spawn robot, then bring up Nav2/RViz.
        delayed_spawn,
        delayed_navigation,
        delayed_rviz,
        delayed_initial_pose,
    ])