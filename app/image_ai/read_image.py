import cv2
import numpy as np
import pyautogui

# Load the template image
import os
# print("Current Directory:", os.getcwd())

# Load all card images from the folder into an array
cards_dir = os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images_large_screen_h_small')
cards_images = []
found_cards = []  # List to store matched cards
found_cards_dealer = []  # List to store matched cards

for filename in os.listdir(cards_dir):
    if filename.endswith(".png"):
        card_path = os.path.join(cards_dir, filename)
        card_gray = cv2.imread(card_path, cv2.IMREAD_GRAYSCALE)
        if card_gray is not None:
            cards_images.append((card_gray, filename))
        else:
            print(f"Error loading card image: {card_path}")


def search_card(screenshot, card):
    # cv2.imshow("Captured Screenshot", screenshot)
    # cv2.waitKey(0)  # Wait for a key press to close the window

    # Checking dealer cards
    res = cv2.matchTemplate(screenshot, card, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    threshold = 0.97  # Adjust the threshold as needed
    card_name_pos = {}
    if max_val >= threshold:
        # print(f"Found card '{card_name}' at pixel coordinates (x={max_loc[0]}, y={max_loc[1]})")
        card_name_pos["card"] = card_name
        card_name_pos["pos_x"] = max_loc[0]
        card_name_pos["pos_y"] = max_loc[1]
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

if not cards_images:
    print("No valid card images found.")

else:

    # # Define the region of interest (ROI) coordinates
    # # SMALL SCREEN
    # roi_x_player = 1250  # X-coordinate of the top-left corner of the ROI
    # roi_y_player = 650  # Y-coordinate of the top-left corner of the ROI
    # roi_width = 400  # Width of the ROI
    # roi_height = 100  # Height of the ROI

    # roi_x_dealer = 1100  # X-coordinate of the top-left corner of the ROI
    # roi_y_dealer = 480  # Y-coordinate of the top-left corner of the ROI

    # Define the region of interest (ROI) coordinates
    # LARGE SCREEN
    roi_x_player = 1750  # X-coordinate of the top-left corner of the ROI
    roi_y_player = 900  # Y-coordinate of the top-left corner of the ROI
    roi_width = 400  # Width of the ROI
    roi_height = 50  # Height of the ROI

    roi_x_dealer = 1450  # X-coordinate of the top-left corner of the ROI
    roi_y_dealer = 650  # Y-coordinate of the top-left corner of the ROI

    while True:
        # Capture the screen
        # screenshot = pyautogui.screenshot()
        screenshot = pyautogui.screenshot(region=(roi_x_player, roi_y_player, roi_width, roi_height))
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        screenshot_dealer = pyautogui.screenshot(region=(roi_x_dealer, roi_y_dealer, roi_width, roi_height))
        screenshot_dealer = np.array(screenshot_dealer)
        screenshot_dealer_gray = cv2.cvtColor(screenshot_dealer, cv2.COLOR_BGR2GRAY)
       
        # Iterate through each template and perform template matching
        for card_gray, card_name in cards_images:
            # cv2.imshow("Card to match", card_gray)
            # cv2.waitKey(0)
            
            # Checking player cards
            found_card = search_card(screenshot_gray, card_gray)
            add_card_if_not_exists(found_cards, found_card, True)
            # if found_card != {} and found_card not in found_cards:
            #     found_cards.append(found_card)

            # Checking dealer cards
            found_card = search_card(screenshot_dealer_gray, card_gray)
            add_card_if_not_exists(found_cards_dealer, found_card, False)
            # if found_card != {} and found_card not in found_cards:
            #     found_cards.update(found_card)

        if found_cards:
            print("PLAYER:")
            card_values = [{card_data["card"]} for card_data in found_cards]
            print(card_values)
        if found_cards_dealer:
            print("DEALER:")
            card_values = [{card_data["card"]} for card_data in found_cards_dealer]
            print(card_values)
        else:
            print("No cards found on the screen.")

        # Display the captured screen with matches (optional)
        # cv2.imshow("Screen", screenshot)


        # Display the captured screen with matches
        # cv2.imshow("Screen", screenshot)
        # cv2.waitKey(0)  # Wait for a key press to close the window


        # Exit when 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            print("quit")
            break

    cv2.destroyAllWindows()