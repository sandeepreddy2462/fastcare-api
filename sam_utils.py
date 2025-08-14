import cv2
import numpy as np
import torch
from segment_anything import sam_model_registry, SamPredictor


# -------------------------------
# 1. Load SAM model
# -------------------------------
sam_checkpoint = "model/sam_vit_b_01ec64.pth"  # Path to SAM weights
model_type = "vit_b"
device = "cuda" if torch.cuda.is_available() else "cpu"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)

# -------------------------------
# 2. Get best mask from ROI or image center
# -------------------------------
def get_max_contour(image_width, image_height, roi_points):
    roi_copy = np.array(roi_points, dtype=np.int32)

    if roi_copy.size > 0:
        cx = np.mean(roi_copy[:, 0])
        cy = np.mean(roi_copy[:, 1])
        input_point = np.array([[cx, cy]])
    else:
        input_point = np.array([[image_width // 2, image_height // 2]])

    input_label = np.array([1])

    masks, scores, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True
    )

    best_mask = masks[np.argmax(scores)]
    mask_uint8 = (best_mask * 255).astype(np.uint8)
    contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        return max_contour
    return None
    

# -------------------------------
# 4. Get Red, Yellow, Black pixel counts in contour
# -------------------------------
def get_wound_RYB_composition(image, contour):
    """
    Calculate Red, Yellow, Black percentage composition from wound region.
    Ensures mutually exclusive classification with priority:
    Black > Yellow > Red.
    """
    wound_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(wound_mask, [contour], -1, (255,), -1)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # HSV ranges
    lower_red1 = np.array([0, 100, 100], dtype=np.uint8)
    upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
    lower_red2 = np.array([160, 100, 100], dtype=np.uint8)
    upper_red2 = np.array([179, 255, 255], dtype=np.uint8)

    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([180, 150, 50], dtype=np.uint8)  # Reduced S for accuracy

    # Create masks
    mask_red = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # Apply wound mask
    mask_red = cv2.bitwise_and(mask_red, wound_mask)
    mask_yellow = cv2.bitwise_and(mask_yellow, wound_mask)
    mask_black = cv2.bitwise_and(mask_black, wound_mask)

    # Mutually exclusive classification: Black > Yellow > Red
    classification_map = np.zeros_like(wound_mask, dtype=np.uint8)
    classification_map[mask_black > 0] = 3
    classification_map[(mask_yellow > 0) & (classification_map == 0)] = 2
    classification_map[(mask_red > 0) & (classification_map == 0)] = 1

    total_pixels = np.count_nonzero(wound_mask)
    # if total_pixels == 0:
    #     return {"Red": 0.0, "Yellow": 0.0, "Black": 0.0}

    red_pixels = np.count_nonzero(classification_map == 1)
    yellow_pixels = np.count_nonzero(classification_map == 2)
    black_pixels = np.count_nonzero(classification_map == 3)

    return {
        "Red": round((red_pixels / total_pixels) * 100, 2),
        "Yellow": round((yellow_pixels / total_pixels) * 100, 2),
        "Black": round((black_pixels / total_pixels) * 100, 2)
    }

