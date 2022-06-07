
import os

chars = {"á": "a", "é": "e", "í": "i", "ó": "o", "ő": "o", "ü": "u", "ú": "u", "ű": "u", "ö": "o",
         "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ő": "O", "Ü": "U", "Ú": "U", "Ű": "U", "Ö": "O"
         }
for root, dirs, files in os.walk("E:/mp3"):
    for file in files:

        newName = file
        for c in chars.keys():
            if c in newName:
               newName = newName.replace(c, chars[c])

        if file != newName:
            filename     = root + "/" + file
            newFileName  = root + "/" + newName

            os.rename(filename, newFileName)
