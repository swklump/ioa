import pyautogui as pg
i = 0
while i < 3600:
    pg.moveTo(500,500)
    pg.sleep(15)
    i += 1
    pg.moveTo(200, 200)
    pg.sleep(15)
    pg.press('c')