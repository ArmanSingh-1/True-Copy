import torch
import torchvision.models.vgg
# Patch for CRAFT Text Detector
if not hasattr(torchvision.models.vgg, 'model_urls'):
    torchvision.models.vgg.model_urls = {
        'vgg16_bn': 'https://download.pytorch.org/models/vgg16_bn-6c64b313.pth'
    }

from craft_text_detector import Craft

# Initialize CRAFT Text Detection Engine
def initialize_text_detection_engine() -> Craft:
    use_cuda = False 
    return Craft(
        output_dir=None,
        crop_type="box",
        cuda=use_cuda
    )

# Merge Nearby or Overlapping Bounding Boxes
def merge_nearby_overlapping_regions(dialogue_regions: list[dict], pixel_distance: int = 45) -> list[dict]:
    while True:
        new_merges = False
        merged_regions = []

        while dialogue_regions:
            current = dialogue_regions.pop(0)
            merged_this_iteration = False

            for i, other in enumerate(merged_regions):
                # Check if regions overlap or are close enough to merge
                if not (current['x'] > other['x'] + other['width'] + pixel_distance or
                        current['x'] + current['width'] < other['x'] - pixel_distance or
                        current['y'] > other['y'] + other['height'] + pixel_distance or
                        current['y'] + current['height'] < other['y'] - pixel_distance):
                    
                    # Calculate the bounding box of the merged region
                    min_x = min(current['x'], other['x'])
                    min_y = min(current['y'], other['y'])
                    max_x = max(current['x'] + current['width'], other['x'] + other['width'])
                    max_y = max(current['y'] + current['height'], other['y'] + other['height'])
                    
                    # Update merged region
                    merged_regions[i] = {
                        'x': min_x, 
                        'y': min_y, 
                        'width': max_x - min_x, 
                        'height': max_y - min_y
                    }

                    new_merges = True
                    merged_this_iteration = True
                    break

            if not merged_this_iteration:
                merged_regions.append(current)

        dialogue_regions = merged_regions
        if not new_merges:
            break

    return dialogue_regions

# Main pipeline function to segment image regions
def segment_dialogue_regions(input_image_path: str, craft_engine: Craft) -> list[dict]:
    prediction = craft_engine.detect_text(input_image_path)
    boxes = prediction.get("boxes", [])
    
    raw_regions = []
    
    # Extract coordinates and calculate region dimensions
    for box in boxes:
        x_coords = [point[0] for point in box]
        y_coords = [point[1] for point in box]
        
        # Append region to list
        raw_regions.append({
            "x": int(min(x_coords)),
            "y": int(min(y_coords)),
            "width": int(max(x_coords) - min(x_coords)),
            "height": int(max(y_coords) - min(y_coords))
        })
        
    # Merge close regions
    merged_regions = merge_nearby_overlapping_regions(raw_regions, pixel_distance=45)
    return merged_regions