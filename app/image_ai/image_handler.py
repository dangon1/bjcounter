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

def take_screenshot():   
    # Capture the screen
    # screenshot = pyautogui.screenshot()            

    #screenshot2 = pyautogui.screenshot(region=(0, 0,800,600))        
    #screenshot2 = np.array(screenshot2)
    #screenshot2_g = cv2.cvtColor(screenshot2, cv2.COLOR_BGR2GRAY)
    #image_handler.save_screenshots(screenshot2);    
    #image_handler.save_screenshots(screenshot2_g);     

    # Change this to select the desired configuration        
    roi_definitions = configuration.roi_definitions(configuration.ResolutionConfiguration.RESOLUTION_800_600);
    
    screenshot = pyautogui.screenshot(region=(roi_definitions["roi_x_player"], roi_definitions["roi_y_player"], roi_definitions["roi_width"], roi_definitions["roi_height"]))            
    screenshot = np.array(screenshot)                     

    #image_handler.save_screenshots(screenshot);
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    #image_handler.save_screenshots(screenshot_gray);
        
    screenshot_dealer = pyautogui.screenshot(region=(roi_definitions["roi_x_dealer"], roi_definitions["roi_y_dealer"], roi_definitions["roi_width"], roi_definitions["roi_height"]))
    screenshot_dealer = np.array(screenshot_dealer)
    screenshot_dealer_gray = cv2.cvtColor(screenshot_dealer, cv2.COLOR_BGR2GRAY)
    
    return screenshot_gray,screenshot_dealer_gray
            
            