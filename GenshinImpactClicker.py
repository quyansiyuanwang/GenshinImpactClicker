import os
import sys
from time import sleep as t_slp
from typing import Final, Union

Digit = Union[int, float]

# ------------User settings------------
OPERATION_INTERVAL: Final[Digit] = 0.27  # 操作间隔
GET_POS_KEY: Final[str] = 'f6'  # 显示坐标
QUIT_WORLD_KEY: Final[str] = 'f7'  # F2并单击坐标位置
SET_TARGET_KEY: Final[str] = 'f8'  # 记录坐标
EXIT_KEY: Final[str] = 'f9'  # 退出
# -------------------------------------

PROJECT_PATH = os.path.split(os.path.abspath(__file__))[0]
EXE_PATH = os.path.dirname(sys.executable)
FILE_NAME = os.path.basename(__file__)

if not os.path.exists(f'{PROJECT_PATH}\\temp_run.bat'):
    with open(f'{PROJECT_PATH}\\temp_run.bat', 'w', encoding='utf-8') as f:
        f.write(
            '@echo off&&cls\n'
            '>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"\n'
            'if \'%errorlevel%\' NEQ \'0\' (goto UACPrompt) else (goto UACAdmin)\n'
            ':UACPrompt\n'
            '%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)'
            '(window.close)&&exit\n'
            ':UACAdmin\n'
            f'start {EXE_PATH}\\python "%~dp0{FILE_NAME}"\n'
            'echo cold_starting...\n'
            'ping -n 2 127.0.0.1 >nul\n'
            'del /f /q %~dp0%~n0.bat'
        )

    os.system(f'start {PROJECT_PATH}\\temp_run.bat')
    exit(1)

try:
    import pyautogui
except ImportError:
    raise ImportError(f'Please install pyautogui under {EXE_PATH}')

try:
    import keyboard
except ImportError:
    raise ImportError(f'Please install pyautogui under {EXE_PATH}')

from pyautogui import Point

target_position: Point = Point(x=1, y=1)


def user_enter_monitor(
        sleep: Digit = 0.1,
        delay: Digit = 0
):
    t_slp(delay)

    while True:
        try:
            if (key_event := keyboard.read_event()).event_type == keyboard.KEY_DOWN:
                return key_event.name
        except KeyboardInterrupt:
            pass

        t_slp(sleep)


def clicker():
    global target_position
    while True:
        pressed = user_enter_monitor()

        if pressed == GET_POS_KEY:
            init_position = pyautogui.position()
            print('Mouse cur pos:', init_position)

        elif pressed == QUIT_WORLD_KEY:
            pyautogui.press('f2')
            t_slp(OPERATION_INTERVAL)
            pyautogui.click(target_position, button='left')

        elif pressed == SET_TARGET_KEY:
            target_position = pyautogui.position()
            print('Set target pos:', target_position)

        elif pressed == EXIT_KEY:
            break

        else:
            pass


def main():
    clicker()


if __name__ == '__main__':
    main()
    os.system('pause')
