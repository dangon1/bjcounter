import unittest
import cv2
import os
import numpy as np
import sys


# Add the parent directory of 'bjcounter' to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir+"\\..\\")

# Now you can use relative imports as usual
from app.image_ai.read_image import search_card; 
from app.image_ai.read_image import add_card_if_not_exists;

class CardDetectionTest(unittest.TestCase):
    def setUp(self):
        # Load the card images from your directory
        cards_dir = os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images_large_screen_h_small')
        self.cards_images = []
        for filename in os.listdir(cards_dir):
            if filename.endswith(".png"):
                card_path = os.path.join(cards_dir, filename)
                card_gray = cv2.imread(card_path, cv2.IMREAD_GRAYSCALE)
                if card_gray is not None:
                    self.cards_images.append((card_gray, filename))
                else:
                    print(f"Error loading card image: {card_path}")

    def test_card_detection(self):
        # Provide a sample filename for the image to be tested
        test_image_filename = os.path.join(os.getcwd(), 'tests', 'image_recon',  '1.png')  # Replace with the actual path

        # Load the test image
        test_image = cv2.imread(test_image_filename, cv2.IMREAD_GRAYSCALE)

        # Ensure that the test image has been loaded successfully
        self.assertIsNotNone(test_image, f"Error loading test image: {test_image_filename}")

        # Initialize lists to store matched cards
        found_cards = []
        found_cards_dealer = []

        # Iterate through each template and perform template matching
        for card_gray, card_name in self.cards_images:
            # Call the search_card function with the test image and template card image            
            
            found_card_player = search_card(test_image, card_gray,card_name)
            add_card_if_not_exists(found_cards, found_card_player, True)

            found_card_dealer = search_card(test_image, card_gray,card_name)
            add_card_if_not_exists(found_cards_dealer, found_card_dealer, False)

        # Perform your assertions here to validate the results
        # For example, you can assert that certain cards were found in the test image:
        expected_player_cards = ['card1.png', 'card2.png']  # Replace with expected card names
        expected_dealer_cards = ['card3.png', 'card4.png']  # Replace with expected card names

        player_card_names = [card_data["card"] for card_data in found_cards]
        dealer_card_names = [card_data["card"] for card_data in found_cards_dealer]

        for card_name in expected_player_cards:
            self.assertIn(card_name, player_card_names)

        for card_name in expected_dealer_cards:
            self.assertIn(card_name, dealer_card_names)

if __name__ == '__main__':
    unittest.main()
