from ctypes import *

class LibCaller:

    def __init__(self, loader):
        self.__loader = loader

    def callTiaPoly(self, AUDV, AUDC, AUDF):


        TIA = cdll.LoadLibrary("libTiaPoly")
        buffer = create_string_buffer(44100)

        cAUDV = c_int(AUDV)
        cAUDC = c_int(AUDC)
        cAUDF = c_int(AUDF)

        TIA.createTone(buffer, cAUDV, cAUDC, cAUDF)

        print(buffer.value.decode(), sizeof(buffer))


    def __loadDLL(self, name):
        tempDLL = None

        try:
            tempDLL = cdll.LoadLibrary(name+".dll")
        except:
            try:
                tempDLL = ("src/Libs/"+name+".dll")
            except:
                pass

        return(tempDLL)

if __name__ == "__main__":
    L = LibCaller(None)
    L.callTiaPoly(8, 4, 4)