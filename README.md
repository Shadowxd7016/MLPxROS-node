# Autonomous Wall-Following Robot Brain (ROS 2 & Machine Learning)

An intelligent wall-following navigation system designed for ROS 2 (Robot Operating System). The system leverages an offline-trained Multi-Layer Perceptron (MLP) Neural Network model exported as a scikit-learn Pipeline (`robot_model.pkl`) inside the submission archive `i242589_abdulrafey_A3.zip`. It consumes real-time ultrasonic distance readings, infers high-level control strategies, and converts them into precise differential drive actuation commands (`/cmd_vel`).

---

## 🚀 Key Features
- **Machine Learning Driven Control**: Implements an MLP Neural Network classifier with high diagnostic accuracy (99.5% train, 99.8% test) to decide the best steering action.
- **End-to-End Inference Pipeline**: The loaded binary contains an integral `StandardScaler` to clean and scale incoming data inputs on-the-fly safely before feeding them into the network.
- **ROS 2 Integration**: Lightweight, fully asynchronous ROS 2 node executing within standard event loops.
- **Deterministic Dynamic Mapping**: Maps symbolic classifications into safe linear and angular velocity vectors (`geometry_msgs/msg/Twist`).

---

## 🏗 Node Architecture & Mechanics

The node initializes under the identifier `robot_brain_node` and operates over standard publisher/subscriber paradigms:

+-----------------------------------------+
  |        /ultrasonic_sensors              |
  |   (std_msgs/msg/Float32MultiArray)      |
  +--------------------+--------------------+
                       |
                       v [Real-Time Sensor Streams]
  +--------------------+--------------------+
  |             RobotBrain Node             |
  |                                         |
  | 1. Extract raw distance array           |
  | 2. Standardize & scale inputs           |
  | 3. Run model inference (`.predict()`)   |
  | 4. Velocity mapping strategy            |
  +--------------------+--------------------+
                       |
                       v [High-Frequency Twist Output]
  +--------------------+--------------------+
  |                 /cmd_vel                |
  |          (geometry_msgs/msg/Twist)      |
  +-----------------------------------------+

### Data Pipeline Details
1. **Subscribed Topic**: `/ultrasonic_sensors` (`std_msgs/msg/Float32MultiArray`) receives structured float arrays corresponding to spatial distance boundaries (e.g., `front_distance`, `left_distance`).
2. **Inference Loop**: Data is unpacked into a 2D matrix layout (`[[front, left, ...]]`), scaled through the pipeline, and categorized into distinct target states.
3. **Published Topic**: `/cmd_vel` (`geometry_msgs/msg/Twist`) updates motor drive controllers at a 10Hz queue depth boundary.

### Action Mapping Profiles
The inferred behavior classes are translated into the following motor profiles:

| Predicted Action Class | Linear Velocity (`x`) | Angular Velocity (`z`) | Intended Robot Movement |
| :--- | :---: | :---: | :--- |
| `"Move-Forward"` | `0.3 m/s` | `0.0 rad/s` | Stable straight cruise away from obstacles. |
| `"Sharp-Right-Turn"` | `0.0 m/s` | `-1.0 rad/s` | Instant dynamic pivot to avoid direct collision. |
| `Contains "Right"` | `0.2 m/s` | `-0.3 rad/s` | Soft corrections to track walls smoothly. |
| `Contains "Left"` | `0.2 m/s` | `0.3 rad/s` | Smooth defensive angling adjustment. |

---

## 🛠 Prerequisites & Dependencies

Before running this script, ensure you have a properly configured ROS 2 environment along with the essential data-science libraries:

```bash
# Update package paths and install Python dependencies
pip install scikit-learn joblib pandas numpy
