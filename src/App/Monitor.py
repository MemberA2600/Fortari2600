class Monitor():

    def __init__(self, ):

        from ctypes import windll as windll

        user32 = windll.user32
        self.__screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


    def get_screensize(self):
        return(self.__screensize)