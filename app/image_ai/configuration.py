import enum
import os

class ResolutionConfiguration(enum.Enum):
    LARGE_SCREEN = 1
    SMALL_SCREEN = 2
    ALTERNATIVE_MONITOR = 3
    RESOLUTION_800_600 = 4

# Define the region of interest (ROI) coordinates
def roi_definitions(resolution_enum):   
    if str(resolution_enum) == str(ResolutionConfiguration.LARGE_SCREEN):
        return {
            "roi_x_player": 1750,
            "roi_y_player": 900,
            "roi_x_dealer": 1450,
            "roi_y_dealer": 650,
            "roi_width": 400,
            "roi_height": 50
        }
    elif str(resolution_enum) == str(ResolutionConfiguration.SMALL_SCREEN):
        return {
            "roi_x_player": 1250,
            "roi_y_player": 650,
            "roi_x_dealer": 1100,
            "roi_y_dealer": 480,
            "roi_width": 400,
            "roi_height": 100
        }
    elif str(resolution_enum) == str(ResolutionConfiguration.ALTERNATIVE_MONITOR): 
        return {
            "roi_x_player": 960,
            "roi_y_player": 778,
            "roi_x_dealer": 943,
            "roi_y_dealer": 603,
            "roi_width": 400,
            "roi_height": 31
        }
    elif str(resolution_enum) == str(ResolutionConfiguration.RESOLUTION_800_600):
        return {
            "roi_x_player": 393,
            "roi_y_player": 446,
            "roi_x_dealer": 390,
            "roi_y_dealer": 373,
            "roi_width": 400,
            "roi_height": 31
        }
    else:
        raise ValueError("Invalid configuration type")

class PathDefinition(enum.Enum):
    PRODUCTION = 1
    TEST = 2    

def card_path_configuration(config):
    if str(config) == str(PathDefinition.PRODUCTION):
        return os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images_800x600')
    elif str(config) == str(PathDefinition.TEST):
        return os.path.join(os.getcwd(), 'app', 'image_ai', 'card_images_800x600')    
    else:
        raise ValueError("Invalid configuration")
