from PIL import Image
from tkinter import Tk, filedialog

Tk().withdraw()

file_path = filedialog.askopenfilename(
    title="Select BMP file",
    filetypes=[("Bitmap images", "*.bmp")]
)
if not file_path:
    print("No file selected.")
    exit()

# Load the image as grayscale
img = Image.open(file_path).convert("L")

# Convert to list of strings
rows = []
for y in range(img.height):
    row_str = ""
    for x in range(img.width):
        val = img.getpixel((x, y))
        row_str += "1" if val == 255 else "0"
    rows.append(row_str)

numOfCols = img.width // 8
datas     = []

for colNum in range(0, numOfCols):
    string = "\t_align\t" + str(img.height) +"\n" + "#NAME#_" + str(colNum) + "\n"

    for rowNum in range(img.height - 1, -1, -1):
        linePart = rows[rowNum][colNum * 8 : (colNum + 1) * 8]
        string  += "\tBYTE\t#%" + linePart + '\n'

    datas.append(string)

for item in datas:
    print(item)