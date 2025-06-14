import numpy as np
import math
from data import BodyPart

def calculate_angle(pointA, pointB, pointC):
    """
    Calculate the angle between three points.
    
    Args:
        pointA: First point [x, y]
        pointB: Middle point (vertex) [x, y]
        pointC: End point [x, y]
    
    Returns:
        Angle in degrees
    """
    # Convert to numpy arrays for easier calculation
    a = np.array([pointA.x, pointA.y])
    b = np.array([pointB.x, pointB.y])
    c = np.array([pointC.x, pointC.y])
    
    # Calculate vectors
    ba = a - b
    bc = c - b
    
    # Calculate dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    
    # Handle numerical errors to keep cosine_angle between -1 and 1
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    # Calculate angle in degrees
    angle = np.arccos(cosine_angle) * 180 / np.pi
    
    return angle

def extract_angles_from_person(person):
    """
    Extract important angles for yoga pose detection from a Person object.
    
    Args:
        person: A Person object containing keypoints from MoveNet.
    
    Returns:
        Dictionary of angles
    """
    # Dictionary to store keypoints by body part for easier access
    keypoints_dict = {keypoint.body_part: keypoint for keypoint in person.keypoints}

    angles = {}
    confidence_threshold = 0.2  # Ensure keypoints have sufficient confidence
    
    # Define the angles we want to calculate (joint triplets)
    angle_definitions = [
        {'name': 'left_elbow', 'points': [BodyPart.LEFT_SHOULDER, BodyPart.LEFT_ELBOW, BodyPart.LEFT_WRIST]},
        {'name': 'right_elbow', 'points': [BodyPart.RIGHT_SHOULDER, BodyPart.RIGHT_ELBOW, BodyPart.RIGHT_WRIST]},
        {'name': 'left_shoulder', 'points': [BodyPart.LEFT_ELBOW, BodyPart.LEFT_SHOULDER, BodyPart.LEFT_HIP]},
        {'name': 'right_shoulder', 'points': [BodyPart.RIGHT_ELBOW, BodyPart.RIGHT_SHOULDER, BodyPart.RIGHT_HIP]},
        {'name': 'left_hip', 'points': [BodyPart.LEFT_SHOULDER, BodyPart.LEFT_HIP, BodyPart.LEFT_KNEE]},
        {'name': 'right_hip', 'points': [BodyPart.RIGHT_SHOULDER, BodyPart.RIGHT_HIP, BodyPart.RIGHT_KNEE]},
        {'name': 'left_knee', 'points': [BodyPart.LEFT_HIP, BodyPart.LEFT_KNEE, BodyPart.LEFT_ANKLE]},
        {'name': 'right_knee', 'points': [BodyPart.RIGHT_HIP, BodyPart.RIGHT_KNEE, BodyPart.RIGHT_ANKLE]}
    ]
    
    # Calculate each angle if all required keypoints exist with good confidence
    for angle_def in angle_definitions:
        name = angle_def['name']
        points = angle_def['points']
        
        if all(point in keypoints_dict and keypoints_dict[point].score >= confidence_threshold for point in points):
            angles[name] = calculate_angle(
                keypoints_dict[points[0]].coordinate,
                keypoints_dict[points[1]].coordinate,
                keypoints_dict[points[2]].coordinate
            )
        else:
            angles[name] = 0  # Default to 0 if keypoints are missing

    # ✅ **Corrected Neck Angle Calculation**
    if (
        BodyPart.LEFT_SHOULDER in keypoints_dict and keypoints_dict[BodyPart.LEFT_SHOULDER].score >= confidence_threshold and
        BodyPart.RIGHT_SHOULDER in keypoints_dict and keypoints_dict[BodyPart.RIGHT_SHOULDER].score >= confidence_threshold
    ):
        # Calculate midpoint of shoulders as the neck reference
        left_shoulder = keypoints_dict[BodyPart.LEFT_SHOULDER].coordinate
        right_shoulder = keypoints_dict[BodyPart.RIGHT_SHOULDER].coordinate
        
        # Create a virtual midpoint class
        class VirtualPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        neck_midpoint = VirtualPoint(
            (left_shoulder.x + right_shoulder.x) / 2,
            (left_shoulder.y + right_shoulder.y) / 2
        )
        
        # Compute the neck angle
        angles['neck'] = calculate_angle(
            left_shoulder,
            neck_midpoint,  # Neck reference point
            right_shoulder
        )
    else:
        angles['neck'] = 0  # Default if keypoints are missing

    return angles