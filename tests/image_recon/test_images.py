import unittest
import cv2
import os
import sys
import re

# Add the parent directory of 'bjcounter' to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print(parent_dir)
sys.path.append(parent_dir)

parent_dir2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','app','image_ai'))
print(parent_dir2)
sys.path.append(parent_dir2)

# Now you can use relative imports as usual
from app.image_ai import configuration
from app.image_ai import image_handler
from app.image_ai import read_image

class CardDetectionTest(unittest.TestCase):
    
    def setUp(self):
        # Load the card images from your directory        
        self.cards_images = image_handler.load_cards(configuration.PathDefinition.TEST)
        self.resolution_configuration = configuration.ResolutionConfiguration.RESOLUTION_800_600;
        self.treshhold = configuration.roi_definitions(self.resolution_configuration)["treshhold"];     
        
    def test_card_detection(self):        
        ##Format of file in folder as p_{cardNumber}{cardType}_d_{cardNumber}{cardType}

              # Test scenario for a entire folder        
        folder_path = os.path.abspath(os.path.join(parent_dir, 'tests', 'image_recon','800x600'))        
        self.card_detection_from_folder(folder_path)        
        
        
        # Test scenario for expecific image
        testpath = os.path.abspath(os.path.join(parent_dir, 'tests', 'image_recon','800x600' , 'p_3h_d_2d.png'))
        expected_player_cards,expected_dealer_cards = self.expected_cards_from_filename(testpath)
        self.card_detection_for_image(testpath, expected_player_cards, expected_dealer_cards)

  
        # Test scenario forcing expected results
        testpath = os.path.abspath(os.path.join(parent_dir, 'tests', 'image_recon','800x600' , 'p_3h_d_2d.png'))        
        self.card_detection_for_image(testpath, ['3h'], ['2d'])
        
        ##to-do: assert the treshhold on every test
        ##to-do: assert the treshhold difference between clubs and spades                     

    def expected_cards_from_filename(self,image_file):                
        
        file_name = os.path.basename(image_file)
        file_name_without_extension = os.path.splitext(file_name)[0]  # Remove the file extension
         
        #p_{cardNumber}{cardType}_d_{cardNumber}{cardType}
        card_match = re.search(r'p_((([JQKAjqka]{1}|[0-9]{1,2})[hdscHDSC])*)_?d_((([JQKAjqka]{1}|[0-9]{1,2})[hdscHDSC])*)', file_name_without_extension)
            
        player_match = card_match.group(1)
        dealer_match = card_match.group(4)
        
        expected_player_cards = re.findall(r'(?:(?:\d{1,2}|[JQKAjqka])[hdscHDSC])', player_match) if player_match else []
        expected_dealer_cards = re.findall(r'(?:(?:\d{1,2}|[JQKAjqka])[hdscHDSC])', dealer_match) if dealer_match else []
        
        
        return expected_player_cards,expected_dealer_cards
    
    def card_detection_from_folder(self,folder_dir):        
        for filename in os.listdir(folder_dir):
            full_file_name = os.path.abspath(os.path.join(folder_dir,filename))
            expected_player_cards,expected_dealer_cards = self.expected_cards_from_filename(full_file_name)
            self.   card_detection_for_image(full_file_name, expected_player_cards, expected_dealer_cards)

    # Define a function to test card detection for a given image and expected cards
    def card_detection_for_image(self,test_image_filename, expected_player_cards, expected_dealer_cards):
        # Load the test image            
        grayscale_image_player, grayscale_image_dealer = image_handler.image_test_from_file(test_image_filename, self.resolution_configuration)
            
        # Initialize lists to store matched cards
        found_cards = []
        found_cards_dealer = []

        # Iterate through each template and perform template matching
        for card_gray, card_name in self.cards_images:
            found_card_player = read_image.search_card(grayscale_image_player, card_gray, card_name,self.treshhold)
            read_image.add_card_if_not_exists(found_cards, found_card_player, True)

            found_card_dealer = read_image.search_card(grayscale_image_dealer, card_gray, card_name,self.treshhold)
            read_image.add_card_if_not_exists(found_cards_dealer, found_card_dealer, False)

        # Perform your assertions here to validate the results
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
