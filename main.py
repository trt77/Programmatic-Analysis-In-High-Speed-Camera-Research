import os
import cv2
import matplotlib.pyplot as plt
import seaborn as sns


def find_thickest_horizontal_bar(contours, image_width, margin=10):
    thickest_contour = None
    max_thickness = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w >= image_width - margin and h > max_thickness:
            thickest_contour = (x, y, w, h)
            max_thickness = h
    return thickest_contour


def process_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    thickest_horizontal_contour = find_thickest_horizontal_bar(contours, image.shape[1])

    if thickest_horizontal_contour:
        _, _, _, thickest_bar_height = thickest_horizontal_contour
        ratio = thickest_bar_height / image.shape[0]
    else:
        ratio = 0
    return ratio


def analyze_images_in_folder(folder_path):
    brightness_ratios = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            brightness_level = int(filename.split('.')[0])
            # Brightness is the namefile of the photograph
            image_path = os.path.join(folder_path, filename)
            ratio = process_image(image_path)
            brightness_ratios.append((brightness_level, ratio))

    brightness_ratios.sort(key=lambda x: x[0])

    # Plotting the graph
    brightness_levels = [x[0] for x in brightness_ratios]
    ratios = [x[1] for x in brightness_ratios]
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=brightness_levels, y=ratios)
    plt.xlabel('Brightness Setting (%)')
    plt.ylabel('Ratio of Thickest Black Bar Height to Picture Height')
    plt.title('Ratio vs Brightness Setting')
    plt.grid(True)
    plt.show()


# Path to the folder with the photographs taken with high-speed camera
folder_path = 'phone_images'
analyze_images_in_folder(folder_path)
