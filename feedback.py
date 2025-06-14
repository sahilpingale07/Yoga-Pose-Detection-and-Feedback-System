# feedback.py

def feedback_adhomukhasvanasana(angles):
    """
    Feedback for Adhomukhasvanasana (Downward-Facing Dog).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: List with a single feedback instruction or 'Perfect pose!'
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    highlighted_keypoints = set()

    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)
    left_hip = angles.get('left_hip', 0)
    right_hip = angles.get('right_hip', 0)
    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)

    # Shoulder angle: ideally open between 110°–130° (arms aligned with spine)
    if not (110 <= left_shoulder <= 130):
        deviation = abs(120 - left_shoulder)
        message = "Relax left shoulder and lengthen spine."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (110 <= right_shoulder <= 130):
        deviation = abs(120 - right_shoulder)
        message = "Relax right shoulder and lengthen spine."
        feedback_items.append((message, 'right_shoulder', deviation))

    # Hips: should be high (angle at hip around 90°)
    if not (70 <= left_hip <= 90):
        deviation = abs(90 - left_hip)
        message = "Push your hips up and back."
        feedback_items.append((message, 'left_hip', deviation))

    if not (70 <= right_hip <= 90):
        deviation = abs(90 - right_hip)
        message = "Push your hips up and back."
        feedback_items.append((message, 'right_hip', deviation))
    
    # Knees: ideally straight (angle 170°–180°)
    if not (170 <= left_knee <= 180):
        deviation = abs(175 - left_knee)
        message = "Try to straighten your left leg."
        feedback_items.append((message, 'left_knee', deviation))
        
    if not (170 <= right_knee <= 180):
        deviation = abs(175 - right_knee)
        message = "Try to straighten your right leg."
        feedback_items.append((message, 'right_knee', deviation))

    # Perfect pose check
    if not feedback_items:
        return ["Perfect pose!"], set()

    # Take top feedback by deviation
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    feedback_messages = [top_item[0]]
    highlighted_keypoints = {top_item[1]}

    return feedback_messages, highlighted_keypoints

def feedback_virabhadrasana(angles):
    """
    Feedback for Virabhadrasana (Warrior Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: Single feedback instruction.
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    highlighted_keypoints = set()

    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)
    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)

    # Legs (front and back)
    if not (85 <= left_knee <= 95):
        deviation = abs(90 - left_knee)
        message = "Bend your left knee to form a right angle." if left_knee < 85 else "Don't extend your left leg too much."
        feedback_items.append((message, 'left_knee', deviation))

    if not (170 <= right_knee <= 180):
        deviation = abs(175 - right_knee)
        message = "Keep your back leg straight and strong."
        feedback_items.append((message, 'right_knee', deviation))

    # Arms (shoulder extension)
    if not (160 <= left_shoulder <= 180):
        deviation = abs(170 - left_shoulder)
        message = "Stretch your left arm fully in line with your shoulders."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (160 <= right_shoulder <= 180):
        deviation = abs(170 - right_shoulder)
        message = "Stretch your right arm fully in line with your shoulders."
        feedback_items.append((message, 'right_shoulder', deviation))

    # Sort and select top feedback based on max deviation
    if not feedback_items:
        return [], set()

    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    return [top_item[0]], {top_item[1]}

def feedback_bhujangasana(angles):
    """
    Feedback for Bhujangasana (Cobra Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: Single feedback instruction.
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    highlighted_keypoints = set()

    left_elbow = angles.get('left_elbow', 0)
    right_elbow = angles.get('right_elbow', 0)
    neck = angles.get('neck', 0)  # Simulating spinal extension
    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)

    # Arms (elbows)
    if not (150 <= left_elbow <= 170):
        deviation = abs(160 - left_elbow)
        message = "Straighten your left arm to lift your upper body."
        feedback_items.append((message, 'left_elbow', deviation))

    if not (150 <= right_elbow <= 170):
        deviation = abs(160 - right_elbow)
        message = "Straighten your right arm to lift your upper body."
        feedback_items.append((message, 'right_elbow', deviation))

    # Spine (using neck angle)
    if not (160 <= neck <= 180):
        deviation = abs(170 - neck)
        message = "Arch your spine and lift your chest higher."
        feedback_items.append((message, 'neck', deviation))

    # Legs (knees should be straight)
    if not (170 <= left_knee <= 180):
        deviation = abs(175 - left_knee)
        message = "Keep your left leg extended and firm on the mat."
        feedback_items.append((message, 'left_knee', deviation))

    if not (170 <= right_knee <= 180):
        deviation = abs(175 - right_knee)
        message = "Keep your right leg extended and firm on the mat."
        feedback_items.append((message, 'right_knee', deviation))

    # Prioritize top 1 feedback
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    return [top_item[0]], {top_item[1]}


def feedback_trikonasana(angles):
    """
    Feedback for Trikonasana (Triangle Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: Single feedback instruction.
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    highlighted_keypoints = set()

    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)
    left_hip = angles.get('left_hip', 0)
    right_hip = angles.get('right_hip', 0)
    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)

    # Legs straight
    if not (170 <= left_knee <= 180):
        deviation = abs(175 - left_knee)
        message = "Straighten your left leg."
        feedback_items.append((message, 'left_knee', deviation))

    if not (170 <= right_knee <= 180):
        deviation = abs(175 - right_knee)
        message = "Straighten your right leg."
        feedback_items.append((message, 'right_knee', deviation))

    # Hips: rotation and leg distance (angle between hips)
    if not (140 <= left_hip <= 160):
        deviation = abs(150 - left_hip)
        message = "Rotate your left hip more to open the body."
        feedback_items.append((message, 'left_hip', deviation))

    if not (140 <= right_hip <= 160):
        deviation = abs(150 - right_hip)
        message = "Rotate your right hip more to open the body."
        feedback_items.append((message, 'right_hip', deviation))

    # Shoulders: arms should align vertically
    if not (160 <= left_shoulder <= 180):
        deviation = abs(170 - left_shoulder)
        message = "Raise your left arm straight above your shoulder."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (160 <= right_shoulder <= 180):
        deviation = abs(170 - right_shoulder)
        message = "Align your right arm vertically with the lower one."
        feedback_items.append((message, 'right_shoulder', deviation))

    # Sort and return top 1 feedback only
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    return [top_item[0]], {top_item[1]}

def feedback_vrksasana(angles):
    """
    Feedback for Vrksasana (Tree Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: Single feedback instruction (highest priority).
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    leg_items = []
    arm_items = []
    highlighted_keypoints = set()

    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)
    left_elbow = angles.get('left_elbow', 0)
    right_elbow = angles.get('right_elbow', 0)
    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)

    # ----- LEG FEEDBACK -----
    if not (170 <= left_knee <= 180):
        deviation = abs(175 - left_knee)
        leg_items.append(("Keep your left leg strong and straight.", 'left_knee', deviation))

    if not (170 <= right_knee <= 180):
        deviation = abs(175 - right_knee)
        leg_items.append(("Keep your right leg strong and straight.", 'right_knee', deviation))

    if not (80 <= left_knee <= 100) and not (170 <= left_knee <= 180):
        deviation = abs(90 - left_knee)
        leg_items.append(("Lift your left foot to bend knee properly.", 'left_knee', deviation))

    if not (80 <= right_knee <= 100) and not (170 <= right_knee <= 180):
        deviation = abs(90 - right_knee)
        leg_items.append(("Lift your right foot to bend knee properly.", 'right_knee', deviation))

    # ----- ARM FEEDBACK -----
    if not (160 <= left_elbow <= 180):
        deviation = abs(170 - left_elbow)
        arm_items.append(("Straighten your left arm upward.", 'left_elbow', deviation))

    if not (160 <= right_elbow <= 180):
        deviation = abs(170 - right_elbow)
        arm_items.append(("Straighten your right arm upward.", 'right_elbow', deviation))

    if not (150 <= left_shoulder <= 180):
        deviation = abs(165 - left_shoulder)
        arm_items.append(("Raise your left arm to align with shoulder.", 'left_shoulder', deviation))

    if not (150 <= right_shoulder <= 180):
        deviation = abs(165 - right_shoulder)
        arm_items.append(("Raise your right arm to align with shoulder.", 'right_shoulder', deviation))

    if left_shoulder < 90 and right_shoulder < 90:
        deviation = abs(90 - (left_shoulder + right_shoulder) / 2)
        arm_items.append(("Raise your both arms and form Namaste overhead.", 'left_shoulder', deviation))

    # Combine legs first (priority), then arms
    feedback_items = leg_items + arm_items

    if not feedback_items:
        return [], set()

    # Sort and return top feedback item
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    return [top_item[0]], {top_item[1]}


def feedback_utkatasana(angles):
    """
    Feedback for Utkatasana (Chair Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: Single feedback instruction.
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []

    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)
    left_hip = angles.get('left_hip', 0)
    right_hip = angles.get('right_hip', 0)
    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)

    # Arms Overhead (shoulders)
    if not (150 <= left_shoulder <= 180):
        deviation = abs(165 - left_shoulder)
        message = "Raise your left arm fully overhead."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (150 <= right_shoulder <= 180):
        deviation = abs(165 - right_shoulder)
        message = "Raise your right arm fully overhead."
        feedback_items.append((message, 'right_shoulder', deviation))

    # Straight Back (torso alignment via shoulders)
    if not (140 <= left_shoulder <= 160):
        deviation = abs(150 - left_shoulder)
        message = "Keep your back straighter; avoid leaning forward."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (140 <= right_shoulder <= 160):
        deviation = abs(150 - right_shoulder)
        message = "Keep your back straighter; avoid leaning forward."
        feedback_items.append((message, 'right_shoulder', deviation))

    # Leg Bending (knees)
    if not (90 <= left_knee <= 110):
        deviation = abs(100 - left_knee)
        message = "Bend your left knee to sit deeper."
        feedback_items.append((message, 'left_knee', deviation))

    if not (90 <= right_knee <= 110):
        deviation = abs(100 - right_knee)
        message = "Bend your right knee to sit deeper."
        feedback_items.append((message, 'right_knee', deviation))

    # Leg Bending (hips)
    if not (100 <= left_hip <= 120):
        deviation = abs(110 - left_hip)
        message = "Lower your hips more."
        feedback_items.append((message, 'left_hip', deviation))

    if not (100 <= right_hip <= 120):
        deviation = abs(110 - right_hip)
        message = "Lower your hips more."
        feedback_items.append((message, 'right_hip', deviation))

    # Return only the most important feedback
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    return [top_item[0]], {top_item[1]}


def feedback_natarajasana(angles):
    """
    Feedback for Natarajasana (Dancer Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: Single feedback instruction.
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []

    neck = angles.get('neck', 0)
    back_leg_knee = angles.get('right_knee', 0)  # assuming right leg is lifted
    standing_leg_knee = angles.get('left_knee', 0)
    arm_angle = angles.get('left_shoulder', 0)  # assuming left arm is extended forward

    # 1. Back Arch via neck
    if not (20 <= neck <= 40):
        deviation = abs(30 - neck)
        message = "Arch your back more to deepen the pose." if neck < 20 else "Reduce the arch in your back slightly."
        feedback_items.append((message, 'neck', deviation))

    # 2. Leg Bending (lifted leg, e.g., right knee)
    if not (130 <= back_leg_knee <= 160):
        deviation = abs(145 - back_leg_knee)
        message = "Bend your lifted leg more to bring your foot closer to your head." if back_leg_knee < 130 else "Ease off the leg stretch slightly."
        feedback_items.append((message, 'right_knee', deviation))

    # 3. Arm Straightness (arm extended forward)
    if not (160 <= arm_angle <= 180):
        deviation = abs(170 - arm_angle)
        message = "Straighten your arm fully forward to balance the pose."
        feedback_items.append((message, 'left_shoulder', deviation))

    # 4. Standing leg should be straight
    if not (170 <= standing_leg_knee <= 180):
        deviation = abs(175 - standing_leg_knee)
        message = "Keep your standing leg straighter for better stability."
        feedback_items.append((message, 'left_knee', deviation))

    # Sort and select most deviated feedback
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_item = feedback_items[0]

    return [top_item[0]], {top_item[1]}


def feedback_ardhamatsyendrasana(angles):
    """
    Feedback for Ardhamatsyendrasana (Half Lord of the Fishes Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: List of feedback instructions (max 3).
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []

    neck = angles.get('neck', 0)
    left_hip = angles.get('left_hip', 0)
    right_hip = angles.get('right_hip', 0)
    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)
    left_elbow = angles.get('left_elbow', 0)
    right_elbow = angles.get('right_elbow', 0)
    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)

    # 1. Hip rotation check
    if not (70 <= left_hip <= 110):
        deviation = abs(90 - left_hip)
        message = "Rotate your hip slightly more to support the twist." if left_hip < 70 else "Relax the hip to avoid over-twisting."
        feedback_items.append((message, 'left_hip', deviation))
    
    if not (70 <= right_hip <= 110):
        deviation = abs(90 - right_hip)
        message = "Rotate your hip slightly more to support the twist." if right_hip < 70 else "Relax the hip to avoid over-twisting."
        feedback_items.append((message, 'right_hip', deviation))

    # 2. Arm raised and placed on opposite knee (assume left hand over right knee)
    if not (70 <= left_elbow <= 110):
        deviation = abs(90 - left_elbow)
        message = "Raise your left arm and press it against your right knee to deepen the twist."
        feedback_items.append((message, 'left_elbow', deviation))

    # 3. Bent knee check
    if not (50 <= right_knee <= 90):
        deviation = abs(70 - right_knee)
        message = "Bend your right knee properly to ground the foot beside your thigh."
        feedback_items.append((message, 'right_knee', deviation))

    # 4. Shoulder alignment (for spinal twist)
    if not (30 <= left_shoulder <= 60):
        deviation = abs(45 - left_shoulder)
        message = "Twist your torso more from the waist to align your shoulders."
        feedback_items.append((message, 'left_shoulder', deviation))

    # 5. Neck rotation
    if not (40 <= neck <= 60):
        deviation = abs(50 - neck)
        message = "Gently turn your head to follow the direction of the twist."
        feedback_items.append((message, 'neck', deviation))

    # Sort and select top 3 feedbacks based on deviation
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_items = feedback_items[:1]

    # Extract messages and keypoints
    feedback_messages = [item[0] for item in top_items]
    highlighted_keypoints = set(item[1] for item in top_items)

    return feedback_messages, highlighted_keypoints

def feedback_kumbhakasana(angles):
    """
    Feedback for Kumbhakasana (Plank Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: List of feedback instructions (max 3).
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    highlighted_keypoints = set()

    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)
    left_hip = angles.get('left_hip', 0)
    right_hip = angles.get('right_hip', 0)
    left_elbow = angles.get('left_elbow', 0)
    right_elbow = angles.get('right_elbow', 0)
    neck = angles.get('neck', 0)  # New angle for head/neck alignment

    # --- ARM STRAIGHTNESS ---
    if not (170 <= left_elbow <= 180):
        deviation = abs(175 - left_elbow)
        message = "Keep your left arm straight and avoid locking the elbow."
        feedback_items.append((message, 'left_elbow', deviation))

    if not (170 <= right_elbow <= 180):
        deviation = abs(175 - right_elbow)
        message = "Keep your right arm straight and avoid locking the elbow."
        feedback_items.append((message, 'right_elbow', deviation))

    # --- SHOULDER ALIGNMENT ---
    if not (160 <= left_shoulder <= 180):
        deviation = abs(170 - left_shoulder)
        message = "Stack your left shoulder over the wrist and engage the core."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (160 <= right_shoulder <= 180):
        deviation = abs(170 - right_shoulder)
        message = "Stack your right shoulder over the wrist and engage the core."
        feedback_items.append((message, 'right_shoulder', deviation))

    # --- BACK STRAIGHTNESS (HIPS) ---
    if not (165 <= left_hip <= 180):
        deviation = abs(172 - left_hip)
        message = "Keep your back flat — don’t let your hips drop or lift too high."
        feedback_items.append((message, 'left_hip', deviation))

    if not (165 <= right_hip <= 180):
        deviation = abs(172 - right_hip)
        message = "Keep your back flat — engage glutes and core to align hips."
        feedback_items.append((message, 'right_hip', deviation))

    # --- NECK ALIGNMENT (HEAD) ---
    if not (160 <= neck <= 180):
        deviation = abs(170 - neck)
        message = "Keep your neck in line with your spine — avoid looking up or dropping your head."
        feedback_items.append((message, 'neck', deviation))

    # Sort by deviation and take top 3
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_items = feedback_items[:1]

    # Extract messages and keypoints
    feedback_messages = [item[0] for item in top_items]
    highlighted_keypoints = set(item[1] for item in top_items)

    return feedback_messages, highlighted_keypoints


def feedback_utkatakonasana(angles):
    """
    Feedback for Utkatakonasana (Goddess Pose).
    angles: Dictionary containing key angles.
    Returns:
        - feedback_messages: List of feedback instructions (max 3).
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_items = []
    highlighted_keypoints = set()

    left_knee = angles.get('left_knee', 0)
    right_knee = angles.get('right_knee', 0)
    left_hip = angles.get('left_hip', 0)
    right_hip = angles.get('right_hip', 0)
    left_shoulder = angles.get('left_shoulder', 0)
    right_shoulder = angles.get('right_shoulder', 0)
    left_elbow = angles.get('left_elbow', 0)
    right_elbow = angles.get('right_elbow', 0)

    # --- KNEE BENDING ---
    if not (85 <= left_knee <= 100):
        deviation = abs(92 - left_knee)
        message = "Bend your left knee more to reach a right angle." if left_knee < 85 else "Slightly straighten your left knee to form 90 degrees."
        feedback_items.append((message, 'left_knee', deviation))

    if not (85 <= right_knee <= 100):
        deviation = abs(92 - right_knee)
        message = "Bend your right knee more to reach a right angle." if right_knee < 85 else "Slightly straighten your right knee to form 90 degrees."
        feedback_items.append((message, 'right_knee', deviation))

    # --- HIP POSITION (SINKING DOWN) ---
    if not (95 <= left_hip <= 115):
        deviation = abs(105 - left_hip)
        message = "Sink your hips lower for a deeper squat." if left_hip < 95 else "Lift your hips slightly to avoid over-sinking."
        feedback_items.append((message, 'left_hip', deviation))

    if not (95 <= right_hip <= 115):
        deviation = abs(105 - right_hip)
        message = "Sink your hips lower for a deeper squat." if right_hip < 95 else "Lift your hips slightly to avoid over-sinking."
        feedback_items.append((message, 'right_hip', deviation))

    # --- SHOULDER POSITION (TORSO UPRIGHT) ---
    if not (165 <= left_shoulder <= 180):
        deviation = abs(172 - left_shoulder)
        message = "Keep your torso upright — avoid leaning forward."
        feedback_items.append((message, 'left_shoulder', deviation))

    if not (165 <= right_shoulder <= 180):
        deviation = abs(172 - right_shoulder)
        message = "Keep your torso upright — avoid leaning forward."
        feedback_items.append((message, 'right_shoulder', deviation))

    # --- ARMS RAISED & BENT AT ELBOW (Goddess style) ---
    if not (85 <= left_elbow <= 100):
        deviation = abs(92 - left_elbow)
        message = "Raise your left arm and bend it to form a right angle at the elbow."
        feedback_items.append((message, 'left_elbow', deviation))

    if not (85 <= right_elbow <= 100):
        deviation = abs(92 - right_elbow)
        message = "Raise your right arm and bend it to form a right angle at the elbow."
        feedback_items.append((message, 'right_elbow', deviation))

    # Sort by deviation and select top 3 issues
    feedback_items.sort(key=lambda x: x[2], reverse=True)
    top_items = feedback_items[:1]

    # Prepare results
    feedback_messages = [item[0] for item in top_items]
    highlighted_keypoints = set(item[1] for item in top_items)

    return feedback_messages, highlighted_keypoints

# Dictionary to map pose names to feedback functions
POSE_FEEDBACK_FUNCTIONS = {
    "Adhomukhasvanasana": feedback_adhomukhasvanasana,
    "Virabhadrasana": feedback_virabhadrasana,
    "Bhujangasana": feedback_bhujangasana,
    "Trikonasana": feedback_trikonasana,
    "Vrksasana": feedback_vrksasana,
    "Utkatasana": feedback_utkatasana,
    "Natarajasana": feedback_natarajasana,
    "Ardhamatsyendrasana": feedback_ardhamatsyendrasana,
    "Kumbhakasana": feedback_kumbhakasana,
    "Utkatakonasana": feedback_utkatakonasana,
}

def get_feedback(pose_name, angles):
    """
    Get feedback for a specific pose.
    pose_name: Name of the pose.
    angles: Dictionary of key angles.
    Returns:
        - feedback_messages: List of feedback instructions (max 3).
        - highlighted_keypoints: Set of keypoints to highlight.
    """
    feedback_function = POSE_FEEDBACK_FUNCTIONS.get(pose_name)
    if feedback_function:
        return feedback_function(angles)
    else:
        return ["No feedback available for this pose."], set()