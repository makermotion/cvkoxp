from threading import Thread
from re import T
from ahk import AHK
import ctypes
import cv2, pytesseract
import win32gui
import time
from PIL import ImageGrab, Image
import numpy as np
import sys
from difflib import SequenceMatcher
import re

class Agent:
    def __init__(self):
        self.state = 'init'
        self.ahk = AHK()
        self.win = self.ahk.find_window(title=b'Knight OnLine Client') # Find the opened window        
        self.win.activate()        
        self.full_hp = None
        self.full_mp = None
        self.target_monster = False
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.window_info = {}
        win32gui.EnumWindows(self.set_window_coordinates, self.window_info)

    @staticmethod
    def get_screen(x1, y1, x2, y2):
            box = (x1, y1, x2, y2)
            screen = ImageGrab.grab(box)
            #print(screen.size)
            img = np.array(screen.getdata(), dtype=np.uint8).reshape((screen.size[1], screen.size[0], 3))
            return img

    def set_target(self):
        if self.state == 'init' or self.state == 'onhold' or self.state == 'toofar':
            self.ahk.key_press('z')
            if self.target_monster and self.state != 'toofar':
                self.start_attack()  
    
    def set_window_coordinates(self, hwnd, window_info):
            if win32gui.IsWindowVisible(hwnd):
                if 'Knight' in win32gui.GetWindowText(hwnd):
                    rect = win32gui.GetWindowRect(hwnd)
                    x = rect[0]
                    y = rect[1]
                    w = rect[2] - x
                    h = rect[3] - y
                    window_info['x'] = x
                    window_info['y'] = y
                    window_info['width'] = w
                    window_info['height'] = h
                    window_info['name'] = win32gui.GetWindowText(hwnd)
                    win32gui.SetForegroundWindow(hwnd)

    def check_target(self, monster):
        x1, y1, x2, y2 = self.window_info['x'], self.window_info['y'], self.window_info['width'], self.window_info['height']
        cut_w = x2 / 2
        cut_re  = 110 
        cut_h = y2 - 47 

        x1 = x1 + cut_w - cut_re
        x2 = x1 + (cut_re * 2)
        img = Agent.get_screen(x1, y1+10, x2, y2-cut_h)

        img = cv2.resize(img, (550, 150))

        img = cv2.copyMakeBorder(img, 10, 10, 0, 0, cv2.BORDER_CONSTANT, value=255)

        gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
        #Image.fromarray(gray).show()
        
        # Performing OTSU threshold
        
        ret, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
        
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        #Image.fromarray(thresh1).show()
        config = ('-l eng --oem 1 --psm 3')

        # pytessercat
        # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/tess4/tesseract.exe'
        text1 = pytesseract.image_to_string(thresh1, config=config).lower().strip()

        text2 = pytesseract.image_to_string(thresh2, config=config).lower().strip()

        assert type(monster) == str, "Not correct variable type for monster."
        #print('SIMILARITIES', SequenceMatcher(None, monster, text1).ratio(), SequenceMatcher(None, monster, text2).ratio())
        if SequenceMatcher(None, monster, text1).ratio() > .5 or SequenceMatcher(None, monster, text2).ratio() > .5: 
            self.target_monster = True
        else:
            self.state = 'onhold'


    def check_stats(self, stat_name):
        if stat_name == 'hp':
            x1, y1, x2, y2 = 124, 49, 196, 61
        if stat_name == 'mp':
            x1, y1, x2, y2 = 124, 71, 196, 81

        img = Agent.get_screen(x1, y1, x2, y2)
        img = cv2.resize(img, (350, 55))

        img = cv2.copyMakeBorder(img, 10, 10, 0, 0, cv2.BORDER_CONSTANT, value=255)

        gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)

        #Image.fromarray(gray).show()
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        #ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        
        #Image.fromarray(thresh1).show()
        config = ('-l eng --oem 1 --psm 3')

        # pytessercat
        
        text = pytesseract.image_to_string(thresh1, config=config)
        #print(f'{stat_name} TEXT RESULT: {text}')
        text = text.split('/')
        #print(f'before regex {text[0], text[1]} ')
        text[0] = re.findall('[0-9]+', text[0])
        text[1] = re.findall('[0-9]+', text[1])
        #print(f'{stat_name.upper()} ACTUAL 1: {text[0]}')
        #print(f'{stat_name.upper()} FULL 1: {text[1]}')
        return int(text[0][0]), int(text[1][0])

    def check_toofar(self):
        x1, y1, x2, y2 = 1532, 955, 1871, 977 

        img = Agent.get_screen(x1, y1, x2, y2)
        img = cv2.resize(img, (350, 55))

        #img = cv2.copyMakeBorder(img, 10, 10, 0, 0, cv2.BORDER_CONSTANT, value=255)

        gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)

        #Image.fromarray(gray).show()
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        #Image.fromarray(thresh1).show()
        config = ('-l eng --oem 1 --psm 3')

        # pytessercat       
        text = pytesseract.image_to_string(thresh1, config=config)
        #print(f'{stat_name} TEXT RESULT: {text}')

        if 'too far' in text.lower() and self.state != 'toofar':
            self.state = 'toofar'
            self.set_target()
        elif 'too far' in text.lower() and self.state == 'toofar':
            self.state = 'onhold'
            self.set_target()

    def spell_mana(self, act, shld, th):
        if act / shld < th:
            self.ahk.key_press('2')

    def spell_hp(self, act:int, shld:int, th:int):
        if act / shld < th:
            self.ahk.key_press('1')

    def start_attack(self):
        i = 0 
        while i < 3:
            self.ahk.key_press('9')
            time.sleep(.8)
            i += 1
           
        self.state = 'attacking'

    def attack(self, attack_type):
        #print(f'State = {self.state}')
        if self.state == 'attacking':
            act_hp, shld_hp = self.check_stats('hp')
            act_mp, shld_mp = self.check_stats('mp')
            self.spell_hp(act_hp, shld_hp, .35)
            self.spell_mana(act_mp, shld_mp, .1)
            self.ahk.key_press(attack_type)
        elif self.state == 'onhold' or self.state == 'init':
            self.set_target()

    def recurrent(self, key):
        self.ahk.key_press(key)
    
    def active_win(self):
        return self.ahk.active_window
    
    def verify(self):
        pass

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def cont_attack(stop, attack_type):
    while True:
        try:
            active_window = bot.active_win().title.decode('utf-8')
            if 'Knight OnLine Client' in str(active_window):
                time.sleep(.05)
                bot.attack(attack_type)
            if stop():
                break
        except Exception as e:
            print(e)

def check_target(monster, stop):
    while True:
        try:
            bot.check_toofar()
            bot.check_target(monster)
            if stop():
                break
        except Exception as e:
            print(e)

def reccurent_skills(key, stop, t=None):
    while True:
        try:
            active_window = bot.active_win().title.decode('utf-8')
            if 'Knight OnLine Client' in str(active_window):
                if t != None:
                    bot.recurrent(str(key))
                    time.sleep(t)
                else:
                    bot.recurrent(str(key))
        except Exception as e:
            print(e)
        if stop():
            break


if __name__  == '__main__':
    if is_admin():
        bot = Agent()

        def bot_control():
            while True:
                action = input('Aksiyon Gir:')

                if action == 'att start':
                    att_stop = False
                    ct_stop = False
                    cht_stop = False
                    monster = input('Select target monster: ')
                    attack_type = input('Select attack type: "skill number": ')
                    att = Thread(target=cont_attack, args= [lambda: att_stop, attack_type])
                    ct = Thread(target=check_target, args = [monster, lambda: ct_stop])
                    ct.start() 
                    att.start()
                if action == 'att stop':
                    att_stop = True
                    ct_stop = True
                    att.join()
                    ct.join()
                if action == 'lf start':
                    lf_stop = False
                    lf = Thread(target=reccurent_skills, args=[6, lambda: lf_stop])
                    lf.start()
                if action == 'lf stop':
                    lf_stop = True
                    lf.join()
                if action == 'wolf start':
                    wolf_stop = False
                    wolf = Thread(target=reccurent_skills, args=[8, lambda: wolf_stop, 121])
                    wolf.start()
                if action == 'wolf stop':
                    wolf_stop = True
                    wolf.join()
                if action == 'safety start':
                    safety_stop = False
                    safety = Thread(target=reccurent_skills, args=[7, lambda: safety_stop])
                    safety.start()
                if action == 'safety stop':
                    safety_stop = True
                    safety.join()
                
        bc = Thread(target=bot_control)
        bc.start()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
