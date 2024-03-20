def moving(start, end, baseSpeed):
    startX = start[0]
    startY = start[1]

    endX   = end[0]
    endY   = end[1]

    dirX   = 0
    dirY   = 0

    if endX > startX:
       distanceX = endX - startX
    else:
       distanceX = startX - endX
       dirX      = 1

    if endY > startY:
       distanceY = endY - startY
    else:
       distanceY = startY - endY
       dirY      = 1

    speedX = 1
    speedY = 1

    if distanceX > distanceY:
       speedX = distanceX / distanceY
    else:
       speedY = distanceY / distanceX

    speedX *= speed
    speedY *= speed

    currentX = startX
    currentY = startY

    print(speedX, speedY)

    xDone = False
    yDone = False

    while xDone == False and yDone == False:
        if xDone == False:
            if dirX:
               currentX -= speedX
               if round(currentX) <= endX: xDone = True

            else:
               currentX += speedX
               if round(currentX) >= endX: xDone = True

        if yDone == False:
            if dirY:
                currentY -= speedY
                if round(currentY) <= endY: xDone = True

            else:
                currentY += speedY
                if round(currentY) >= endY: yDone = True

            if round(currentY) == endY: yDone = True

        if (currentY < 0 or currentY > 255) or (currentX < 0 or currentX > 255): raise ValueError

        print(currentX, currentY)

from random import randint

for number in range(0, 10000):
    startX = randint(0, 255)
    startY = randint(0, 255)
    endX   = randint(0, 255)
    endY   = randint(0, 255)
    speed  = randint(1, 5)

    print("--" + str(startX) + "-" + str(startY) + "*" + str(endX) + "-" + str(endY) + "*" + str(speed) + "--------")
    moving([startX,startY], [endX, endY], speed)