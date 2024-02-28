listOfStates = {}

for portNum in range(0, 2):
    ports     = ["SWCHA", "SWCHB"]
    nameAlter = ["joyPorts", "switches"]

    portRegister = ports[portNum]
    portName     = "port" + str(portNum)

    specialAlias =  {"11111111": ["noDirectionPressed", "noSwitchPressed"]}
    

    for bitVal in range(0, 256):
        bitValBin = bin(bitVal).replace("0b", "")
        bitValBin = ("0" * (8-len(bitValBin)) + bitValBin)

        bitValHex = hex(bitVal).replace("0x", "").upper()
        if len(bitValHex) == 1: bitValHex = "0" + bitValHex

        portSubName = portName + "_" + bitValBin
        aliasList   = [portName + "_" + str(bitVal), portName + "_" + bitValHex,
                       nameAlter[portNum] + "_" + bitValBin,
                       nameAlter[portNum] + "_" + str(bitVal),
                       nameAlter[portNum] + "_" + bitValHex
                       ]

        if bitValBin in specialAlias:
           if specialAlias[bitValBin][portNum] != None:
              aliasList.append(portName           + "_" + specialAlias[bitValBin][portNum])
              aliasList.append(nameAlter[portNum] + "_" + specialAlias[bitValBin][portNum])



        listOfStates[portSubName] = [aliasList, portRegister, "11111111", bitValBin]

for joyPortNum in range(0, 2):
    portName = "joyPort" + str(joyPortNum)
    bitMasks = ["11110000", "00001111"]

    for bitVal in range(0, 16):
        bitValBin = bin(bitVal).replace("0b", "")
        bitValBin = ("0" * (4 - len(bitValBin)) + bitValBin)

        bitValHex = hex(bitVal).replace("0x", "").upper()

        portSubName = portName + "_" + bitValBin
        aliasList = [portName + "_" + str(bitVal), portName + "_" + bitValHex
                     ]

        listOfStates[portSubName] = [aliasList, "SWCHA", bitMasks[joyPortNum], bitValBin]


for key in listOfStates:
    print(key + "=[" + " ".join(listOfStates[key][0]) + "]," + listOfStates[key][1] + "," + listOfStates[key][2] + "," + listOfStates[key][3] + "\n")

