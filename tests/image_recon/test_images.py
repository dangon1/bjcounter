import unittest
import cv2
import os
#import numpy as np
import sys

# Add the parent directory of 'bjcounter' to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print(parent_dir)
sys.path.append(parent_dir)

parent_dir2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','app','image_ai'))
print(parent_dir2)
sys.path.append(parent_dir2)

# Now you can use relative imports as usual
from app.image_ai import configuration; 
from app.image_ai import image_handler; 
from app.image_ai import read_image; 

class CardDetectionTest(unittest.TestCase):
    
    def setUp(self):
        # Load the card images from your directory        

        self.cards_images = image_handler.load_cards(configuration.PathDefinition.TEST);
        
    def test_card_detection(self):


        # Provide a sample filename for the image to be tested
        player_test_image_filename = os.path.abspath(os.path.join(parent_dir, 'tests', 'image_recon','800x600' , 'image1B.png'))  # Replace with the actual path             
        
        #get the cut of the apporpriated configured size for player and dealer cards
        grayscale_image_player,grayscale_image_dealer = image_handler.image_test_from_file(player_test_image_filename,configuration.ResolutionConfiguration.RESOLUTION_800_600);          
    
        print(grayscale_image_dealer)
        image_handler.save_screenshots(grayscale_image_dealer);

        # Ensure that the test image has been loaded successfully        

        # Initialize lists to store matched cards
        found_cards = []
        found_cards_dealer = []

        # Iterate through each template and perform template matching
        for card_gray, card_name in self.cards_images:
            # Call the search_card function with the test image and template card image            
            
            found_card_player = read_image.search_card(grayscale_image_player, card_gray,card_name)
            read_image.add_card_if_not_exists(found_cards, found_card_player, True)

            found_card_dealer = read_image.search_card(grayscale_image_dealer, card_gray,card_name)            
            read_image.add_card_if_not_exists(found_cards_dealer, found_card_dealer, False)

        # Perform your assertions here to validate the results
        # For example, you can assert that certain cards were found in the test image:
        expected_player_cards = ['kcBlack.png','KcColour.png' ]  # Replace with expected card names
        expected_dealer_cards = []  # Replace with expected card names


        player_card_names = [card_data["card"] for card_data in found_cards]
        dealer_card_names = [card_data["card"] for card_data in found_cards_dealer]

        # Check that ONLY the expected player cards were found
        for card_name in expected_player_cards:
            self.assertIn(card_name, player_card_names)
        for card_name in player_card_names:
            self.assertIn(card_name, expected_player_cards)

        # Check that ONLY the expected dealer cards were found
        for card_name in expected_dealer_cards:
            self.assertIn(card_name, dealer_card_names)
        for card_name in dealer_card_names:
            self.assertIn(card_name, expected_dealer_cards)

if __name__ == '__main__':
    unittest.main()
