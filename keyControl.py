from control import key_press, SC_DOWN, SC_UP,SC_RIGHT,SC_LEFT, key_down
def control_car(func):
    key_down(SC_UP)
    cof = func // 3300
    speed = func // 3000
    if func > 0:
        key_press(SC_RIGHT, interval=abs(cof))
        key_press(SC_LEFT, interval=abs(cof)//2)
        if func > 250:
            key_press(SC_DOWN, interval=abs(speed))

    else:
        key_press(SC_LEFT,interval=abs(cof))
        key_press(SC_RIGHT, interval=abs(cof) // 2)
        if func < -250:
            key_press(SC_DOWN, interval=abs(speed))