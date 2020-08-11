import pyautogui as pygui 
import pydirect_test as pydirect 
import win32api, time, cv2, time




keyboard_keys=['a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']

def get_click_positions(button, clicks):
    button_vk={
        "left_click":0x01,
        "right_click":0x02
    }
    click_reference=win32api.GetKeyState(button_vk[button])
    positions_list=[]
    i=0 
    while True:
        click_status=win32api.GetKeyState(button_vk[button])
        if click_status != click_reference:
            click_reference=click_status
            if click_status<0 : # GetKeyState returns a negative value if the key is pressed
                x_, y_ = pygui.position()

                positions_list.append([x_,y_])
                i=i+1
                if i==clicks:
                    break

                    
        time.sleep(0.01)
        
    return positions_list



def execute_macro(instructions, ms_delay):
  
    for key, value in instructions:
        
        time.sleep(ms_delay)
        if key=="key_down":
            pydirect.keyDown(value)
            continue

        if key=="key_up" in instruction:
            pydirect.keyUp(value)
            continue

        if "click" in key:
            #process string into list, example: click:[[662, 625]]+ click:[[687, 662]] ---> [(662,625), (687,662)]
            click_list= [(int(x),int(y)) for x,y in  [part.replace("[", '').replace("]", '').split(',') for part in value.split('],') ]] 
            
            if "left" in key:
                for x, y in click_list:
                    pydirect.click(x,y)
                    time.sleep(ms_delay)

            elif "right" in key:
                for x, y in click_list:
                    pydirect.rightClick(x,y)
                    time.sleep(ms_delay)  
            continue

        if key=="press":
            pydirect.press(value)
            continue


        if key=="wait":
            time.sleep(int(value))
            continue

    





    #>>> pydirectinput.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
    #>>> pydirectinput.click() # Click the mouse at its current location.
    #>>> pydirectinput.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
    #>>> pydirectinput.move(None, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
    #>>> pydirectinput.doubleClick() # Double click the mouse at the
    #>>> pydirectinput.press('esc') # Simulate pressing the Escape key.
    #>>> pydirectinput.keyDown('shift')
    #>>> pydirectinput.keyUp('shift')


