import cv2
import numpy as np
import pyautogui
import curses
import uuid

# Load the template image
import os
# print("Current Directory:", os.getcwd())

# Load all card images from the folder into an array
cards_dir = os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images_large_screen_h_small')
cards_images = []
found_cards = []  # List to store matched cards
found_cards_dealer = []  # List to store matched cards
attempt_counter = 1 ##counter of mismatch
last_message_is_not_found = False

roi_configurations = ["LARGE SCREEN", "SMALL SCREEN", "ALTERNATIVE MONITOR"]




for filename in os.listdir(cards_dir):
    if filename.endswith(".png"):
        card_path = os.path.join(cards_dir, filename)
        card_gray = cv2.imread(card_path, cv2.IMREAD_GRAYSCALE)
        if card_gray is not None:
            cards_images.append((card_gray, filename))
        else:
            print(f"Error loading card image: {card_path}")

def print_no_cards_message():
    global last_message_is_not_found
    if last_message_is_not_found == True:
        print('\r' + f"No valid card images found (Attempt {attempt_counter})", end="")        
    else :  
        print(f"No valid card images found (Attempt {attempt_counter})")   
        last_message_is_not_found = True;

def search_card(screenshot, card , card_name):
    #cv2.imshow("Captured Screenshot", screenshot)
    #cv2.waitKey(0)  # Wait for a key press to close the window

    # Checking dealer cards
    res = cv2.matchTemplate(screenshot, card, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    threshold = 0.97 # Adjust the threshold as needed    
    card_name_pos = {}
    if max_val >= threshold:
        # print(f"Found card '{card_name}' at pixel coordinates (x={max_loc[0]}, y={max_loc[1]})")
        card_name_pos["card"] = card_name
        card_name_pos["pos_x"] = max_loc[0]
        card_name_pos["pos_y"] = max_loc[1]
    #    print(f"Treshhold: {max_val} card: {card_name}" )
    #else:        
    #    #if (max_val >= 0.70):
    #    print(f"Treshhold: {max_val} card: {card_name}" )

        # loc = np.where(res >= threshold)
        # for pt in zip(*loc[::-1]):
        #     # Draw a rectangle around the matched area
        #     w, h = card_gray.shape[::-1]
        #     cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    return card_name_pos

def add_card_if_not_exists(found_cards, found_card, is_player):
    if found_card:
        # if found_card not in found_cards:
            # Offset previous cards
            # if is_player:
            #     for previous_card in found_cards:
            #         previous_card["pos_x"] -= 8
            # else:
            #     if len(found_cards) > 1:
            #         for previous_card in found_cards:
            #             previous_card["pos_x"] -= 8
        # if still not found is indeed a new card 
        if found_card not in found_cards:
            found_cards.append(found_card)

def save_screenshots(screenshot):
    # Generate unique filenames using UUID
    screenshot_filename = f"screenshot_{uuid.uuid4()}.png"    

    cv2.imwrite(screenshot_filename, screenshot)    
            
# Define the region of interest (ROI) coordinates
def GetRoiDefinitions(configuration):
    if configuration == "LARGE SCREEN": #currently
        return {
            "roi_x_player": 1750,
            "roi_y_player": 900,
            "roi_x_dealer": 1450,
            "roi_y_dealer": 650,
            "roi_width": 400,
            "roi_height": 50
        }
    elif configuration == "SMALL SCREEN":
        return {
            "roi_x_player": 1250,
            "roi_y_player": 650,
            "roi_x_dealer": 1100,
            "roi_y_dealer": 480,
            "roi_width": 400,
            "roi_height": 100
        }
    elif configuration == "ALTERNATIVE MONITOR": 
        return {
            "roi_x_player": 960,
            "roi_y_player": 778,
            "roi_x_dealer": 943,
            "roi_y_dealer": 603,
            "roi_width": 400,
            "roi_height": 50
        }
    else:
        raise ValueError("Invalid configuration type")

if not cards_images:        
    print_no_cards_message()
    attempt_counter += 1

else:

    if __name__ == '__main__':                   
        attempt_counter = 0
        # Change this to select the desired configuration
        chosen_configuration = roi_configurations[0]  
        roi_definitions = GetRoiDefinitions(chosen_configuration)

        while True:
            # Capture the screen
            # screenshot = pyautogui.screenshot()            
            
            screenshot = pyautogui.screenshot(region=(roi_definitions["roi_x_player"], roi_definitions["roi_y_player"], roi_definitions["roi_width"], roi_definitions["roi_height"]))
            screenshot = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
            screenshot_dealer = pyautogui.screenshot(region=(roi_definitions["roi_x_dealer"], roi_definitions["roi_y_dealer"], roi_definitions["roi_width"], roi_definitions["roi_height"]))
            screenshot_dealer = np.array(screenshot_dealer)
            screenshot_dealer_gray = cv2.cvtColor(screenshot_dealer, cv2.COLOR_BGR2GRAY)
       
            # Iterate through each template and perform template matching
            for card_gray, card_name in cards_images:
                #cv2.imshow("Card to match", card_gray)
                #cv2.waitKey(0)
            
                # Checking player cards
                found_card = search_card(screenshot_gray, card_gray , card_name)
                add_card_if_not_exists(found_cards, found_card, True)
                # if found_card != {} and found_card not in found_cards:
                #     found_cards.append(found_card)

                # Checking dealer cards
                found_card = search_card(screenshot_dealer_gray, card_gray , card_name)
                add_card_if_not_exists(found_cards_dealer, found_card, False)
                # if found_card != {} and found_card not in found_cards:
                #     found_cards.update(found_card)

            if found_cards:
                print("PLAYER:")
                card_values = [{card_data["card"]} for card_data in found_cards]
                print(card_values)
                last_message_is_not_found = False
                attempt_counter = 0
            if found_cards_dealer:
                print("DEALER:")
                card_values = [{card_data["card"]} for card_data in found_cards_dealer]
                print(card_values)
                last_message_is_not_found = False
                attempt_counter = 0
            else:                
                print_no_cards_message()
                attempt_counter += 1

            # Display the captured screen with matches
            #cv2.imshow("Screen", screenshot)            
            #cv2.imshow("Screen2", screenshot_dealer)
            #cv2.waitKey(0)  # Wait for a key press to close the window            
             
            #save_screenshots(screenshot);                      

            # Exit when 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                print("quit")
                break

        cv2.destroyAllWindows()