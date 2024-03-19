# -----------------------------------------------------------------------------
# Copyright 2021 Bernd Pfrommer <bernd.pfrommer@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import os

from ament_index_python.packages import get_package_share_directory
import launch
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def launch_setup(context, *args, **kwargs):
    """Create composable node."""
    cam_0_name = LaunchConfig("camera_0_name")
    cam_0_str = cam_0_name.perform(context)
    cam_1_name = LaunchConfig("camera_1_name")
    cam_1_str = cam_1_name.perform(context)
    cam_2_name = LaunchConfig("camera_2_name")
    cam_2_str = cam_2_name.perform(context)
    cam_3_name = LaunchConfig("camera_3_name")
    cam_3_str = cam_3_name.perform(context)
    pkg_name = "metavision_driver"
    share_dir = get_package_share_directory(pkg_name)
    bias_config = os.path.join(share_dir, "config", "zrh01.bias")
    #
    # camera 0
    #
    cam_0 = ComposableNode(
        package="metavision_driver",
        plugin="metavision_driver::DriverROS2",
        name=cam_0_name,
        namespace="sensors",
        parameters=[
            {
                "use_multithreading": False,
                "bias_file": bias_config,
                "camerainfo_url": "",
                "frame_id": "cam_0",
                "serial": "00050500",
                "sync_mode": "primary",
                "num_secondary_nodes": 3,
                "trigger_in_mode": "external",
                "event_message_time_threshold": 1.0e-3,
                "save_raw_file": True,
            }
        ],
        remappings=[
            ("~/events", cam_0_str + "/events"),
            # must remap so primary listens to secondary's ready message
            #("~/ready", cam_1_str + "/ready"),
        ],
        extra_arguments=[{"use_intra_process_comms": True}],
    )
    #
    # camera 1
    #
    cam_1 = ComposableNode(
        package="metavision_driver",
        plugin="metavision_driver::DriverROS2",
        name=cam_1_name,
        namespace="sensors",
        parameters=[
            {
                "use_multithreading": False,
                "bias_file": bias_config,
                "camerainfo_url": "",
                "frame_id": "cam_1",
                "serial": "00050243",
                "sync_mode": "secondary",
                "secondary_node_nr": 0,
                "event_message_time_threshold": 1.0e-3,
                "save_raw_file": True,
            }
        ],
        remappings=[("~/events", cam_1_str + "/events"),
                    ("~/ready", cam_0_str + "/ready")],
        extra_arguments=[{"use_intra_process_comms": True}],
    )
    #
    # camera 2
    #
    cam_2 = ComposableNode(
        package="metavision_driver",
        plugin="metavision_driver::DriverROS2",
        name=cam_2_name,
        namespace="sensors",
        parameters=[
            {
                "use_multithreading": False,
                "bias_file": bias_config,
                "camerainfo_url": "",
                "frame_id": "cam_1",
                "serial": "00050242",
                "sync_mode": "secondary",
                "secondary_node_nr": 1,
                "event_message_time_threshold": 1.0e-3,
                "save_raw_file": True,
            }
        ],
        remappings=[("~/events", cam_2_str + "/events"),
                    ("~/ready", cam_0_str + "/ready")],
        extra_arguments=[{"use_intra_process_comms": True}],
    )
    #
    # camera 3
    #
    cam_3 = ComposableNode(
        package="metavision_driver",
        plugin="metavision_driver::DriverROS2",
        name=cam_3_name,
        namespace="sensors",
        parameters=[
            {
                "use_multithreading": False,
                "bias_file": bias_config,
                "camerainfo_url": "",
                "frame_id": "cam_1",
                "serial": "00050086",
                "sync_mode": "secondary",
                "secondary_node_nr": 2,
                "event_message_time_threshold": 1.0e-3,
                "save_raw_file": True,
            }
        ],
        remappings=[("~/events", cam_3_str + "/events"),
                    ("~/ready", cam_0_str + "/ready")],
        extra_arguments=[{"use_intra_process_comms": True}],
    )
    container = ComposableNodeContainer(
        name="metavision_driver_container",
        namespace="",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[cam_0, cam_1, cam_2, cam_3],
        #composable_node_descriptions=[cam_0],
        output="screen",
    )
    return [container]


def generate_launch_description():
    """Create composable node by calling opaque function."""
    return launch.LaunchDescription(
        [
            LaunchArg(
                "camera_0_name",
                default_value=["evs00050500"],
                description="camera name of camera 0",
            ),
            LaunchArg(
                "camera_1_name",
                default_value=["evs00050243"],
                description="camera name of camera 1",
            ),
            LaunchArg(
                "camera_2_name",
                default_value=["evs00050242"],
                description="camera name of camera 2",
            ),
            LaunchArg(
                "camera_3_name",
                default_value=["evs00050086"],
                description="camera name of camera 3",
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
