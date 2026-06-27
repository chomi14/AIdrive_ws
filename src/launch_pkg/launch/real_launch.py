import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # ---------------------------------------------------------
    # [설정] 본인의 경로에 맞게 이 변수들을 수정하세요
    # ---------------------------------------------------------
    BASE_PATH = '/home/autolab/Autonomous-Driving-AI-SW-Design/src'
    
    # 1. 비디오 파일 경로 (파일이 존재하는지 꼭 확인!)
    VIDEO_FILE = os.path.join(BASE_PATH, 'camera_perception_pkg/camera_perception_pkg/lib/Collected_Datasets/driving_simulation.mp4')
    
    # 2. YOLO 모델 파일 경로 (.pt 파일 위치)
    YOLO_MODEL_FILE = os.path.join(BASE_PATH, 'camera_perception_pkg/camera_perception_pkg/models/best.pt') 
    
    # ---------------------------------------------------------

    image_publisher = Node(
        package='camera_perception_pkg',
        executable='image_publisher_node',
        name='image_publisher_node',
        output='screen',
        parameters=[{
            'data_source': 'video', 
            'video_path': VIDEO_FILE,
            'timer': 0.03
        }]
    )

    yolov8_detector = Node(
        package='camera_perception_pkg',
        executable='yolov8_node',
        name='yolov8_node',
        output='screen',
        parameters=[{
            'model': YOLO_MODEL_FILE,
            'device': 'cpu', 
            'enable': True
        }]
    )

    lane_extractor = Node(
        package='camera_perception_pkg',
        executable='lane_info_extractor_node',
        name='lane_info_extractor_node',
        output='screen',
        parameters=[{'show_image': True}]
    )

    traffic_light_detector = Node(
        package='camera_perception_pkg',
        executable='traffic_light_detector_node',
        name='traffic_light_detector_node',
        output='screen'
    )

    lidar_publisher = Node(
        package='lidar_perception_pkg',
        executable='lidar_publisher_node',
        name='lidar_publisher_node',
        output='screen',
        parameters=[{'lidar_port': '/dev/ttyUSB0'}] # [주의] 포트 번호 확인 필요
    )

    lidar_processor = Node(
        package='lidar_perception_pkg',
        executable='lidar_processor_node',
        name='lidar_processor_node',
        output='screen'
    )

    lidar_obstacle_detector = Node(
        package='lidar_perception_pkg',
        executable='lidar_obstacle_detector_node',
        name='lidar_obstacle_detector_node',
        output='screen'
    )

    path_planner = Node(
        package='decision_making_pkg',
        executable='path_planner_node',
        name='path_planner_node',
        output='screen'
    )

    motion_planner = Node(
        package='decision_making_pkg',
        executable='motion_planner_node',
        name='motion_planner_node',
        output='screen',
        parameters=[{'timer': 0.1}]
    )

    serial_sender = Node(
        package='serial_communication_pkg',
        executable='serial_sender_node',
        name='serial_sender_node',
        output='screen',
        parameters=[{
            'port': '/dev/ttyACM0', # [주의] 포트 번호 확인 필요
            'baudrate': 115200,
            'sub_topic': 'topic_control_signal'
        }]
    )

    yolov8_visualizer = Node(
        package='debug_pkg',
        executable='yolov8_visualize_node',
        name='yolov8_visualize_node',
        output='screen'
    )

    path_visualizer = Node(
        package='debug_pkg',
        executable='path_visualizer_node',
        name='path_visualizer_node',
        output='screen'
    )

    return LaunchDescription([
        image_publisher,
        yolov8_detector,
        lane_extractor,
        traffic_light_detector,
        lidar_publisher,
        lidar_processor,
        lidar_obstacle_detector,
        path_planner,
        motion_planner,
        serial_sender,
        yolov8_visualizer,
        path_visualizer
    ])
