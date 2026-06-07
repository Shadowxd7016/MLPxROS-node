import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
import joblib  # Required to load the .pkl file
import os

class RobotBrain(Node):
    def __init__(self):
        super().__init__('robot_brain_node')
        
        # 1. Load the model saved from Windows
        # Ensure the .pkl file is in the same directory as this script
        model_path = os.path.join(os.getcwd(), 'robot_model.pkl')
        self.model = joblib.load(model_path)
        self.get_logger().info('Neural Network loaded from Windows successfully!')

        # 2. ROS setup
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/ultrasonic_sensors',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        # 3. Extract sensor data (Assuming 4 sensors)
        # We put it in a 2D list: [[s1, s2]]
        sensor_data = [list(msg.data)]
        
        # 4. Predict
        # The pipeline automatically handles the scaling (StandardScaler)
        prediction = self.model.predict(sensor_data)[0]

        # 5. Map and Publish
        self.publish_velocity(prediction)

    def publish_velocity(self, action):
        cmd = Twist()
        # Mapping logic (Section 5.2)
        if action == "Move-Forward":
            cmd.linear.x = 0.3
        elif action == "Sharp-Right-Turn":
            cmd.angular.z = -1.0
        elif "Right" in action: # Slight Right
            cmd.linear.x = 0.2; cmd.angular.z = -0.3
        elif "Left" in action:  # Slight Left
            cmd.linear.x = 0.2; cmd.angular.z = 0.3
            
        self.publisher_.publish(cmd)

rclpy.init()
node = RobotBrain()
rclpy.spin(node)
rclpy.shutdown()
