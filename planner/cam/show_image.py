import pygame
import numpy as np
import cv2

class ImageDisplayer:
    def __init__(self, display_width=800, display_height=600):
        """
        Initialize the pygame window for displaying images.
        
        Args:
            display_width (int): Width of the display window
            display_height (int): Height of the display window
        """
        pygame.init()
        
        self.display_width = display_width
        self.display_height = display_height
        
        # Create the display window
        self.screen = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Image Display")
        
        # Fill with black background initially
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
    
    def _resize_image_maintain_aspect(self, image):
        """
        Resize image to fit within display dimensions while maintaining aspect ratio.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Resized image
            tuple: (x_offset, y_offset) for centering the image
        """
        img_height, img_width = image.shape[:2]
        
        # Calculate scaling factor to fit image within display bounds
        scale_w = self.display_width / img_width
        scale_h = self.display_height / img_height
        scale = min(scale_w, scale_h)
        
        # Calculate new dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image
        resized_image = cv2.resize(image, (new_width, new_height))
        
        # Calculate offsets to center the image
        x_offset = (self.display_width - new_width) // 2
        y_offset = (self.display_height - new_height) // 2
        
        return resized_image, (x_offset, y_offset)
    
    def _convert_to_pygame_surface(self, image):
        """
        Convert numpy image to pygame surface.
        
        Args:
            image (numpy.ndarray): Input image (1 or 3 channels)
            
        Returns:
            pygame.Surface: Pygame surface ready for blitting
        """
        # Handle different image formats
        if len(image.shape) == 2:  # Grayscale (1 channel)
            # Convert grayscale to RGB
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif len(image.shape) == 3:
            if image.shape[2] == 1:  # Single channel with explicit dimension
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 3:  # RGB
                # Convert BGR to RGB if needed (OpenCV uses BGR by default)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif image.shape[2] == 4:  # RGBA
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        
        # Ensure image is in the correct format for pygame (uint8)
        if image.dtype != np.uint8:
            # Normalize to 0-255 range if not already
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        
        # Transpose for pygame (pygame expects (width, height, channels))
        image = np.transpose(image, (1, 0, 2))
        
        # Create pygame surface
        surface = pygame.surfarray.make_surface(image)
        
        return surface
    
    def update(self, image):
        """
        Update the display with a new image.
        
        Args:
            image (numpy.ndarray): New image to display (1 or 3 channels)
        """
        # Handle pygame events to prevent window from becoming unresponsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        # Clear the screen with black background
        self.screen.fill((0, 0, 0))
        
        # Resize image while maintaining aspect ratio
        resized_image, (x_offset, y_offset) = self._resize_image_maintain_aspect(image)
        
        # Convert to pygame surface
        surface = self._convert_to_pygame_surface(resized_image)
        
        # Blit the surface to the screen at the calculated offset
        self.screen.blit(surface, (x_offset, y_offset))
        
        # Update the display
        pygame.display.flip()
        
        return True
    
    def close(self):
        """
        Close the pygame window and quit pygame.
        """
        pygame.quit()