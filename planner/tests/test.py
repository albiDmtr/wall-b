import math

def calculate_focal_length(image_width_px, fov_degrees=120):
    """
    Calculate focal length in pixels from field of view
    
    Args:
        image_width_px: Width of the image in pixels
        fov_degrees: Horizontal field of view in degrees
    
    Returns:
        Focal length in pixels
    """
    # Convert FOV from degrees to radians
    fov_radians = math.radians(fov_degrees)
    
    # Calculate focal length
    focal_length_px = (image_width_px / 2) / math.tan(fov_radians / 2)
    
    return focal_length_px

# Example usage
image_width = 1280  # Your camera resolution width
focal_length = calculate_focal_length(image_width)
print(f"Focal length: {focal_length:.2f} pixels")