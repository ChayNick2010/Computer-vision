from control import key_press, SC_DOWN, SC_UP,SC_RIGHT,SC_LEFT, key_down, SC_INSERT, SC_DELETE
def control_car(func):
    key_down(SC_UP)
    cof = func // 3300
    speed = func // 3000
    fast = 2
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

    if func < 20 and func > -20:
        key_press(SC_INSERT, interval=0.02)
        fast + 1
    if func > 50 and fast == (4, 5, 6, 7):
        key_press(SC_DELETE, interval=0.02)
        fast - 1
    if func < -50 and fast == (4, 5, 6, 7):
        key_press(SC_DELETE, interval=0.02)
        fast - 1