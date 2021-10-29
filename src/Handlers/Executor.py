class Executor:

    def __init__(self, loader):
        self.__loader = loader

    def exectuteSIDtoMIDI(self, path):
        import os
        tempMidi = os.getcwd() + "/temp/temp.mid"

        try:
            os.remove(os.getcwd() + "/temp/temp.mid")
        except:
            pass

        self.__execute("sid2midi", ['"'+path+'" ', '"'+tempMidi+'" '])
        return(tempMidi)

    def __execute(self, program, args):
        import subprocess
        programPath = "applications/"+program.upper()+"/"+program.lower()+".exe"
        subprocess.call('"' + programPath + '" ' + " ".join(args), creationflags=0x08000000)