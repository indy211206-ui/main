month = int(input())
day = int(input())

if day >= 21 and month % 3 == 0:
    if month < 3 and month >= 1:
        print("winter")
    elif month >= 3 and month < 6:
        print("spring")
    elif month >= 6  and month < 8:
        print("summer")
    elif month >= 8 and month < 12:
        print("fall")
elif day < 21:
    if month < 4 and month >= 1:
        print("winter")
    elif month >= 4 and month < 7:
        print("spring")
    elif month >= 7 and month < 9:
        print("summer")
    elif month >= 9 and month < 12:
        print("fall")
