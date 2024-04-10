from PIL import Image

def quantize_line(image, line_index, max_colors):
    width, height = image.size
    pixels = image.load()
    colors = set()

    for x in range(width):
        color = pixels[x, line_index]
        colors.add(color)

    if len(colors) <= max_colors:
        return  # Already within color limit

    # Find the most common colors
    color_count = {}
    for color in colors:
        if color in color_count:
            color_count[color] += 1
        else:
            color_count[color] = 1

    sorted_colors = sorted(color_count, key=lambda c: color_count[c], reverse=True)
    selected_colors = sorted_colors[:max_colors]

    # Map other colors to nearest selected color
    for x in range(width):
        current_color = pixels[x, line_index]
        if current_color not in selected_colors:
            nearest_color = min(selected_colors, key=lambda c: sum((a-b)**2 for a, b in zip(c, current_color)))
            pixels[x, line_index] = nearest_color

def main(input_image_path, output_image_path, max_colors_per_line=4):
    # Open image
    image = Image.open(input_image_path)

    # Convert to RGB mode
    image = image.convert('RGB')

    # Iterate over each line and quantize colors
    width, height = image.size
    for y in range(height):
        quantize_line(image, y, max_colors_per_line)

    # Save the modified image
    image.save(output_image_path)

if __name__ == "__main__":
    input_image_path = "D:/PyCharm/P/toDelete/forTest51/f04e16664fef72c9de9325bc04a6616d.jpg"
    output_image_path = "D:/PyCharm/P/toDelete/forTest51/f04e16664fef72c9de9325bc04a6616d_.png"
    max_colors_per_line = 4
    main(input_image_path, output_image_path, max_colors_per_line)