import cv2


def draw_angle(image, angle, center):
    height, width = image.shape[0:2]
    # Ellipse parameters
    radius = 50
    axes = (radius, radius)
    angle_1 = 0
    startAngle = angle
    endAngle = 0
    thickness = 2
    cv2.ellipse(image, center, axes, angle_1, startAngle, endAngle, (255, 0, 255), thickness)