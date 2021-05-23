class ColorItem:

    def __init__(self, line):
        line = line.split(",")
        self.red = int(line[0])
        self.blue= int(line[1])
        self.green = int(line[2])
        self.PAL = line[3]
        self.ValidName = line[4]