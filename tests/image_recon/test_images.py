import unittest
import cv2
import os
import numpy as np
import sys


# Add the parent directory of 'bjcounter' to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir+"\\..\\")

# Now you can use relative imports as usual
from app.image_ai import read_image; 


class CardDetectionTest(unittest.TestCase):
    def setUp(self):
        # Load the card images from your directory
        cards_dir = os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images_new_approach')
        self.cards_images = []
        for filename in os.listdir(cards_dir):
            if filename.endswith(".png"):
                card_path = os.path.join(cards_dir, filename)
                card_gray = cv2.imread(card_path, cv2.IMREAD_GRAYSCALE)
                if card_gray is not None:
                    self.cards_images.append((card_gray, filename))
                else:
                    print(f"Error loading card image: {card_path}")

    def crop_image(self, image, x, y, width, height):
        return image[y:y+height, x:x+width]
    def test_card_detection(self):
        # Provide a sample filename for the image to be tested
        test_image_filename = os.path.join(os.getcwd(), 'tests', 'image_recon',  '1.png')  # Replace with the actual path
       
        #load Definitions        
        roi_definitions = read_image.GetRoiDefinitions(read_image.roi_configurations[2])


        # Load the test image
        test_image_bf = cv2.imread(test_image_filename)
        
        self.assertIsNotNone(test_image_bf, f"Error loading test image: {test_image_filename}")


        test_image = self.crop_image(test_image_bf,roi_definitions["roi_x_player"], roi_definitions["roi_y_player"]-13, roi_definitions["roi_width"], roi_definitions["roi_height"])               

        if len(test_image.shape) == 2 or (len(test_image.shape) == 3 and test_image.shape[2] == 1):
            # Image is already grayscale, no need to convert
            grayscale_image = test_image
        else:
            # Convert the color image to grayscale
            grayscale_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    
        print(grayscale_image)
        read_image.save_screenshots(grayscale_image);

        # Ensure that the test image has been loaded successfully        

        # Initialize lists to store matched cards
        found_cards = []
        found_cards_dealer = []

        # Iterate through each template and perform template matching
        for card_gray, card_name in self.cards_images:
            # Call the search_card function with the test image and template card image            
            
            found_card_player = read_image.search_card(grayscale_image, card_gray,card_name)
            read_image.add_card_if_not_exists(found_cards, found_card_player, True)

            found_card_dealer = read_image.search_card(grayscale_image, card_gray,card_name)
            read_image.add_card_if_not_exists(found_cards_dealer, found_card_dealer, False)

        # Perform your assertions here to validate the results
        # For example, you can assert that certain cards were found in the test image:
        expected_player_cards = ['7hblack.png']  # Replace with expected card names
        expected_dealer_cards = []  # Replace with expected card names


        player_card_names = [card_data["card"] for card_data in found_cards]
        dealer_card_names = [card_data["card"] for card_data in found_cards_dealer]

        for card_name in expected_player_cards:
            self.assertIn(card_name, player_card_names)

        for card_name in expected_dealer_cards:
            self.assertIn(card_name, dealer_card_names)

if __name__ == '__main__':
    unittest.main()
