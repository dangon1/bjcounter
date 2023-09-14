import cv2
import numpy as np
import pyautogui

# Load the template image
import os
# print("Current Directory:", os.getcwd())

# Load all card images from the folder into an array
cards_dir = os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images')
cards_images = []

for filename in os.listdir(cards_dir):
    if filename.endswith(".png"):
        card_path = os.path.join(cards_dir, filename)
        card_gray = cv2.imread(card_path, cv2.IMREAD_GRAYSCALE)
        if card_gray is not None:
            cards_images.append((card_gray, filename))
        else:
            print(f"Error loading card image: {card_path}")

if not cards_images:
    print("No valid card images found.")

else:

    # while True:
    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Captured Screenshot", screenshot_gray)
    cv2.waitKey(0)  # Wait for a key press to close the window

    found_templates = []  # List to store matched templates

    # Iterate through each template and perform template matching
    for card_gray, template_name in cards_images:
        res = cv2.matchTemplate(screenshot_gray, card_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust the threshold as needed
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            print(f"Found card '{template_name}' at pixel coordinates (x={max_loc[0]}, y={max_loc[1]})")
            found_templates.append(template_name)
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                # Draw a rectangle around the matched area
                w, h = card_gray.shape[::-1]
                cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    if found_templates:
        print("Matched cards:", ", ".join(found_templates))
    else:
        print("No cards found on the screen.")

    # Display the captured screen with matches (optional)
    cv2.imshow("Screen", screenshot)


    # Display the captured screen with matches
    cv2.imshow("Screen", screenshot)
    cv2.waitKey(0)  # Wait for a key press to close the window


    # Exit when 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        print("quit")
        # break

    cv2.destroyAllWindows()