import tensorflow as tf
import numpy as np
import joblib
from data import BodyPart
from angle_calculator import extract_angles_from_person

def get_center_point(landmarks, left_bodypart, right_bodypart):
    """Calculates the center point of the two given landmarks."""
    left = tf.gather(landmarks, left_bodypart.value, axis=0)
    right = tf.gather(landmarks, right_bodypart.value, axis=0)
    center = left * 0.5 + right * 0.5
    return center

def get_pose_size(landmarks, torso_size_multiplier=2.5):
    """Calculates pose size."""
    # Hips center
    hips_center = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)

    # Shoulders center
    shoulders_center = get_center_point(landmarks, BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER)

    # Torso size as the minimum body size
    torso_size = tf.linalg.norm(shoulders_center - hips_center)

    # Pose center
    pose_center_new = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)
    pose_center_new = tf.expand_dims(pose_center_new, axis=0)

    # Dist to pose center
    d = landmarks - pose_center_new
    # Max dist to pose center
    max_dist = tf.reduce_max(tf.linalg.norm(d, axis=1))

    # Normalize scale
    pose_size = tf.maximum(torso_size * torso_size_multiplier, max_dist)
    return pose_size

def normalize_pose_landmarks(landmarks):
    """Normalizes the landmarks translation by moving the pose center to (0,0) and scaling it to a constant pose size."""
    # Move landmarks so that the pose center becomes (0,0)
    pose_center = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)
    pose_center = tf.expand_dims(pose_center, axis=0)
    landmarks = landmarks - pose_center

    # Scale the landmarks to a constant pose size
    pose_size = get_pose_size(landmarks)
    landmarks /= pose_size
    return landmarks

def landmarks_to_embedding(landmarks):
    """Converts the input landmarks into a pose embedding."""
    # Normalize landmarks 2D
    landmarks = normalize_pose_landmarks(landmarks[:, :2])  # Use only (x, y), ignore score
    # Flatten the normalized landmark coordinates into a vector
    embedding = tf.reshape(landmarks, (-1,))
    return embedding

def extract_angle_features(pose):
    """
    Extract raw angle features from a Person object.
    
    Args:
        pose: A Person object from MoveNet.
    
    Returns:
        numpy.ndarray: Raw angle features array with shape (1, num_angles)
    """
    # Skip processing if pose is None or doesn't have keypoints
    if pose is None or not hasattr(pose, 'keypoints'):
        # Return zeros array with the expected shape for angles
        return np.zeros((1, 9))  # 9 angles
    
    # Calculate angles
    angles = extract_angles_from_person(pose)
    
    # Convert angles dictionary to a list in a consistent order
    angle_features = [
        angles.get('left_elbow', 0),
        angles.get('right_elbow', 0),
        angles.get('left_shoulder', 0),
        angles.get('right_shoulder', 0),
        angles.get('left_hip', 0),
        angles.get('right_hip', 0),
        angles.get('left_knee', 0),
        angles.get('right_knee', 0),
        angles.get('neck', 0)
    ]
    
    # Convert to numpy array and reshape for model input
    return np.array(angle_features).reshape(1, -1)

def extract_normalized_keypoints(pose):
    """
    Extract and normalize keypoint features from a Person object.
    
    Args:
        pose: A Person object from MoveNet.
    
    Returns:
        numpy.ndarray: Normalized keypoint features array with shape (1, 34)
    """
    # Skip processing if pose is None or doesn't have keypoints
    if pose is None or not hasattr(pose, 'keypoints'):
        # Return zeros array with the expected shape for normalized keypoints
        return np.zeros((1, 34))  # 17 keypoints * 2 (x,y) after normalization
    
    # Extract raw keypoints from the pose
    keypoint_coords = []
    for keypoint in pose.keypoints:
        x = keypoint.coordinate.x
        y = keypoint.coordinate.y
        score = keypoint.score
        keypoint_coords.append([x, y, score])
    
    # Convert to numpy array and reshape to [17, 3]
    keypoints = np.array(keypoint_coords)
    
    # Convert to tensor for normalization
    keypoints_tensor = tf.convert_to_tensor(keypoints, dtype=tf.float32)
    
    # Use landmarks_to_embedding to normalize keypoints
    # This uses the same normalization as in the training code
    normalized_keypoints = landmarks_to_embedding(keypoints_tensor).numpy()
    
    # Reshape for model input (batch size of 1)
    return normalized_keypoints.reshape(1, -1)

def preprocess_for_prediction(pose, angle_scaler_path='./pose_models/angle_scaler.joblib'):
    """
    Preprocess a Person object to get model inputs.
    
    Args:
        pose: A Person object from MoveNet.
        angle_scaler_path: Path to the saved StandardScaler for angles
    
    Returns:
        tuple: (normalized_keypoints, scaled_angles) - Two numpy arrays ready for model input
    """
    # Load the angle scaler
    angle_scaler = joblib.load(angle_scaler_path)
    
    # Get normalized keypoints (shape: [1, 34])
    keypoints_input = extract_normalized_keypoints(pose)
    
    # Get raw angle features
    raw_angles = extract_angle_features(pose)
    
    # Scale angle features using the same scaler as during training
    scaled_angles = angle_scaler.transform(raw_angles)
    
    return keypoints_input, scaled_angles, raw_angles