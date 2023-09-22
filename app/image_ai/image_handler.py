import cv2
import os
import uuid
import configuration
import pyautogui
import numpy as np

def load_cards(config_param):
    cards_images = []  # Create an empty list to store card images
        
    cards_dir = configuration.card_path_configuration(config_param)
    
    # Load all card images from the folder into an array
    for filename in os.listdir(cards_dir):
        if filename.endswith(".png"):
            card_path = os.path.join(cards_dir, filename)
            card_gray = cv2.imread(card_path, cv2.IMREAD_GRAYSCALE)
            if card_gray is not None:
                cards_images.append((card_gray, filename))
            else:
                print(f"Error loading card image: {card_path}")
    
    return cards_images  # Return the list of loaded card images


##Generates a unique file of a image in the root folder of the app
def save_screenshots(screenshot):
    # Generate unique filenames using UUID
    screenshot_filename = f"screenshot_{uuid.uuid4()}.png"    

    cv2.imwrite(screenshot_filename, screenshot)               

def take_screenshot(resolution_configuration):   
    # Capture the screen
    # screenshot = pyautogui.screenshot()            

    #Use this to print actual screen for testing purpuses
    #screenshot2 = pyautogui.screenshot(region=(0, 0,800,600))        
    #screenshot2 = np.array(screenshot2)
    #screenshot2_g = cv2.cvtColor(screenshot2, cv2.COLOR_BGR2GRAY)
    #save_screenshots(screenshot2);    
    #save_screenshots(screenshot2_g);     

    # Change this to select the desired configuration        
    roi_definitions = configuration.roi_definitions(resolution_configuration);
    
    screenshot = pyautogui.screenshot(region=(roi_definitions["roi_x_player"], roi_definitions["roi_y_player"], roi_definitions["roi_width"], roi_definitions["roi_height"]))            
    screenshot = np.array(screenshot)                     

    #save_screenshots(screenshot);
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    #save_screenshots(screenshot_gray);
        
    screenshot_dealer = pyautogui.screenshot(region=(roi_definitions["roi_x_dealer"], roi_definitions["roi_y_dealer"], roi_definitions["roi_width"], roi_definitions["roi_height"]))
    screenshot_dealer = np.array(screenshot_dealer)    
    #save_screenshots(screenshot_dealer);
    
    screenshot_dealer_gray = cv2.cvtColor(screenshot_dealer, cv2.COLOR_BGR2GRAY)    
    #save_screenshots(screenshot_dealer_gray);
    
    return screenshot_gray,screenshot_dealer_gray

def image_test_from_file(test_image_filename_url,resolution_configuration):
    #load Definitions        
    roi_definitions = configuration.roi_definitions(resolution_configuration);

    # Load the test image
    test_image_bf = cv2.imread(test_image_filename_url)
    
    

#    # Draw rectangles on the image to highlight player and dealer regions
#    color_player = (0, 255, 0)  # Green color
#    color_dealer = (0, 0, 255)  # Red color
#    thickness = 2  # Thickness of the rectangle
#
#    # Draw the player rectangle
#    cv2.rectangle(test_image_bf, (roi_definitions["roi_x_player"], roi_definitions["roi_y_player"]),
#                (roi_definitions["roi_x_player"] + roi_definitions["roi_width"], roi_definitions["roi_y_player"] + roi_definitions["roi_height"]), color_player, thickness)
#
#    # Draw the dealer rectangle
#    cv2.rectangle(test_image_bf, (roi_definitions["roi_x_dealer"], roi_definitions["roi_y_dealer"]),
#                  (roi_definitions["roi_x_dealer"] + roi_definitions["roi_width"], roi_definitions["roi_y_dealer"] + roi_definitions["roi_height"]), color_dealer, thickness)
#

#    save_screenshots(test_image_bf);
        
    #player
    player_test_image = crop_image(test_image_bf,roi_definitions["roi_x_player"], roi_definitions["roi_y_player"], roi_definitions["roi_width"], roi_definitions["roi_height"])               
    player_greyscale_image = image_to_greyscale(player_test_image);
    
    #dealer
    dealer_test_image = crop_image(test_image_bf,roi_definitions["roi_x_dealer"], roi_definitions["roi_y_dealer"], roi_definitions["roi_width"], roi_definitions["roi_height"])               
    dealer_greyscale_image = image_to_greyscale(dealer_test_image);
     
    ##use this to get the print and generate the card
    #save_screenshots(player_greyscale_image);
    #save_screenshots(dealer_greyscale_image);

    return player_greyscale_image,dealer_greyscale_image;

def crop_image(image, x, y, width, height):
    return image[y:y+height, x:x+width]
        
        
def image_to_greyscale(image):
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        # Image is already grayscale, no need to convert
        grayscale_image = image
    else:
        # Convert the color image to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)           
    return grayscale_image        
       
                