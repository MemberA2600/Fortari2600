class Executor:

    def __init__(self, loader):
        self.__loader = loader
        self.proc = None

    def killByForce(self, program):
        import subprocess
        self.proc = subprocess.call('taskkill /IM /F "'+program+'.exe"', creationflags=0x08000000)

    def execute(self, program, args, hide):
        import subprocess
        from os import getcwd
        programPath = getcwd()+"/applications/"+program.lower()+"/"+program+".exe"

        if hide == True:
            self.proc = subprocess.call('"'  + programPath + '" ' + " ".join(args), creationflags=0x08000000)
            #subprocess.Popen('"'  + programPath + '" ' + " ".join(args), creationflags=0x08000000)
        else:
            from subprocess import check_output, check_call
            print(check_output('"'  + programPath + '" ' + " ".join(args)))

    def __executeFortran(self, module, program, hide):
        import subprocess
        import sys
        from os.path import abspath, exists

        programPath = "fortranApps/"+module+"/"+program+".exe"
        path = abspath(programPath)

        if hide == True:
            subprocess.call('"' + programPath+'"')
        else:
            from subprocess import check_output, check_call
            print(check_output('"' + programPath+'" '))

        #subprocess.check_call('"' + path+'"', stdout=sys.stdout, stderr=subprocess.STDOUT)


        """
        from os import getcwd
        from os.path import abspath, exists
        import ctypes

        path = abspath("fortranApps/"+module+"/"+program+".dll")
        print(path)
        print(exists(path))
        print(path)
        fortran = ctypes.CDLL(path)
        fortran.run()
        """

    def __addSourceToFortran(self, module, input):
        if type(input) == str:
            file = open("temp/Input.txt", "w")
            file.write(input)
            file.close()
        elif type(input) == dict:
            for key in input:
                if type(key) == int:
                    outKey = str(key)
                    if len(outKey) == 1:
                        outKey = "0" + outKey
                else:
                    outKey = str(key)
                file = open("temp/Input"+outKey+".txt", "w")
                if type(input[key]) == list:
                    output = "\n".join(input[key])
                else:
                    output = input[key]

                file.write(output)
                file.close()

    def __addArgsToFortran(self, module, args):
        if type(args) == list:
            file = open("temp/Args.txt", "w")
            file.write(" ".join(args))
            file.close()
        else:
            file = open("temp/Args.txt", "w")
            file.write(args)
            file.close()

    def __getFortranResults(self, module, program, deleteOutPut):
        import os
        if os.path.exists("temp/Output.txt"):
            file = open("temp/Output.txt", "r")
            t = file.read()
            file.close()

            if deleteOutPut == True:
                os.remove("temp/Output.txt")
            else:
                os.rename("temp/Output.txt", "temp/"+program+"_SavedOut.txt")
            return (t)
        else:
            result = {}
            for n in range(0, 99):
                try:
                    n = str(n)
                    if len(n) == 1:
                        n = "0" + n
                    file = open("temp/Output" + n + ".txt", "r")
                    t = file.read()
                    file.close()
                    result[n] = t.split("\n")
                    if deleteOutPut == True:
                        os.remove("temp/Output" + n + ".txt")
                    else:
                        os.rename("temp/Output" + n + ".txt", "temp/"+program+"_SavedOut" + n + ".txt")
                except Exception as e:
                    pass

        try:
            if deleteOutPut == True:
                os.remove("temp/Input.txt")
            else:
                os.rename("temp/Input.txt", "temp/"+program+"_SavedIn.txt")
        except:
            pass
        try:
            if deleteOutPut == True:
                os.remove("temp/Args.txt")
            else:
                os.rename("temp/Args.txt", "temp/"+program+"_SavedArgs.txt")
        except:
            pass

        for n in range(0, 99):
            try:
                n = str(n)
                if len(n) == 1:
                    n = "0" + n
                if deleteOutPut == True:
                    os.remove("temp/Input" + n + ".txt")
                else:
                    os.rename("temp/Input" + n + ".txt", "temp/"+program+"_SavedIn" + n + ".txt")

            except:
                pass

        return(result)


    def callFortran(self, module, program, input, args, hide, deleteOutPut):
        self.__addSourceToFortran(module, input)
        if args != [] and args!= None:
            self.__addArgsToFortran(module, args)
        self.__executeFortran(module, program, hide)
        return(self.__getFortranResults(module, program, deleteOutPut))