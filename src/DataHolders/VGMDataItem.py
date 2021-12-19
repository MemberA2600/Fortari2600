class VGMDataItem:

    def __init__(self, line):
        line = line.replace("\t", " ")
        line = line.split(" ")
        newLine = []

        for item in line:
            if item != "":
                newLine.append(item)

        line = newLine

        self.dataBytes = []
        self.dataByteStrings = []
        self.command = ""
        self.extraData = ""

        last = 0
        for num in range(1,len(line)):
            try:

                self.dataBytes.append(int("0x"+line[num], 16))
                self.dataByteStrings.append(line[num])
                last = num
            except Exception as e:
                #print(str(e))
                break
        try:
            self.command = line[last+1].replace(":", "").lower()
            self.extraData = " ".join(line[last+2: len(line)])

        except:
            pass

        if "Wait:" in line:
            self.command = "wait"


