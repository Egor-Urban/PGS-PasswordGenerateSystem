import random
import subprocess
import os

#GLOBAL VARIABLES
modeALL = "m.cmd"

clear = lambda: os.system('cls')


def mode1():
    print("Простой режим генерации")

def mode2():
    print("Продвинутый режим генерации")




def main():
    clear()
    while True:
        print("PGS - Password Generate System [ver: 0.0.567]")
        print("Версия для CMD[текущая] - команда 'm.cmd' (Для перехода в PowerShell версию - команда 'm.pShell', для перехода в граф. режим - команда 'm.gui') для смены локализации - приписка '.eng' после любой из команд смены режима")
        print()
        print(f"Генератор паролей [{modeALL}]")
        print("1 - простая генерация / 2 - продвинутая генерация")
        modeGlobal = input(">> ")
        if modeGlobal == '1':
            mode1()
        elif modeGlobal == '2':
            mode2()
        elif modeGlobal == "m.pShell":
            clear()
            print("Выбран режим совместимости с PowerShell")
            print()
            continue
        elif modeGlobal == "m.cmd":
            clear()
            print("Выбран режим совместимости с PowerShell")
            print()
            continue
        elif modeGlobal == "m.gui":
            clear()
            print("Выбран режим совместимости с Графическим интерфейсом")
            print()
            #ЗАПУСК GUI Версии программы, выход из этой после запуска
            continue # ВРЕМЕННО
        else:
            clear()
            print("!ERROR! [code:1] {modeGlobal in main()} ==> Извините, но этот режим либо отсутствует, либо пока недоступен")



if __name__ == "__main__":
    main()