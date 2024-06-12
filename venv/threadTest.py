def looper(level, loopNum, num):
    if level > 9: return

    level  += 1
    num[0] += 1

    for x in range(0, loopNum):
        looper(level, loopNum, num)

def loopThread(counter, loopNum, num):
    counter[0] += 1
    for x in range(0, loopNum):
        num[0] += 1
        looper(1, loopNum, num)
    counter[0] -= 1


if __name__ == "__main__":
    from datetime import datetime
    from threading import Thread
    from time import sleep

    timeNow = datetime.now()
    loopNum = 3
    num = [0]

    for x in range(0, loopNum):
        looper(0, loopNum, num)

    print("normal", (datetime.now() - timeNow).total_seconds(), num[0])
    timeNow = datetime.now()

    counter = [0]
    num     = [0]

    for x in range(0, loopNum):
        t = Thread(target=loopThread, args=[counter, loopNum, num])
        t.daemon = True
        t.start()

    while (counter[0] > 0): sleep(0.000001)
    print("threaded", (datetime.now() - timeNow).total_seconds(), num[0])
