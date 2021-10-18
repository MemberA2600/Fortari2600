
def getData(holder, num):
    file = open(str(num)+".txt", "r")
    text = file.read()
    file.close()

    uuu = {}

    data = text.replace("\r","").split("\n")
    for line in data:
        line = line.split("=")
        uuu[int(line[0])] = float(line[1])

    return(uuu)

if __name__ == "__main__":
    freq = {}

    lineNum = 8
    maxi = 0

    limits = {}

    for num in (1, 4, 6, 12):
        freq[num] = {}
        freq[num] = getData(freq[num], num)

    for channel in freq.keys():
        for key in freq[channel].keys():
            if freq[channel][key] > maxi:
                maxi = freq[channel][key]


    limits[0] = 0.0
    for num in range(1, lineNum):
        limits[num] = maxi / (lineNum**2) * num * 0.75

    result = {}

    for channel in (1, 4, 6, 12):
        result[channel] = {}
        for note in range(0,32):
            result[channel][note] = 0
            for num in range(1,8):

                if freq[channel][note] > limits[num]:
                    result[channel][note] = num
                else:
                    break

    text = "Music_Visuals_Data\n"
    for channel in (1,4,6,12):


        text+="Music_Visuals_Data_Channel_"+str(channel)+"\n"

        for note in range(0,32):
            text+="\tBYTE\t#"+str(7-(result[channel][note]))+"\n"

        text+"\n"
    print(text)

