'''
Менеджер паролей
Разработчик: Журбан Е.
Версия: 0.2.2058 [pre.beta]
Разработано в России
Язык: Pyton
Локализация: Русская
                          '''

#IMPORTS
import random as r
import string
import os
import time as t
from colorama import init
init()
from colorama import Fore as bc, Back, Style
import shutil
from cryptography.fernet import Fernet
import base64


#GLOBAL MACROSES
wh = bc.WHITE
cy = bc.CYAN
gr = bc.GREEN
rd = bc.RED
ltyo = bc.LIGHTYELLOW_EX
ltbl = bc.LIGHTBLUE_EX




clear = lambda: os.system('cls')

#GLOBAL VARIABLES
CRYPTOINIT = "crypto.init"
mainKey = b'G1MwrvMBW5xXj4PB2MxsAqFCdj_7iALFHvCZhGAI0JM=' #!!!!!СДЕЛАТЬ МЕХАНИЗМ ДЛЯ ГЕНЕРАЦИИ!!!!!
MAIN_FOLDER = "PasswordData"

#FUNCTIONS
def readFile(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("code:8")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def checkConcretFolderInDir(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)

    return os.path.exists(folder_path) and os.path.isdir(folder_path)


def checkFolders(directory_path):
    folders = []
    try:
        # Получаем список всех файлов и папок в указанной директории
        files_and_folders = os.listdir(directory_path)

        # Фильтруем только папки
        folders = [folder for folder in files_and_folders if os.path.isdir(os.path.join(directory_path, folder))]

        if not folders:
            return False

        # Объединяем имена папок через запятую и возвращаем как строку
        return ', '.join(folders)
    except FileNotFoundError:
        return f"|{rd}ERROR{wh}| [code:{gr}4{wh}] (checkFolders) {ltyo}==>{wh} Указанная директория не найдена."
    except PermissionError:
        return f"|{rd}ERROR{wh}| [code:{gr}5{wh}] [{rd}FATAL{wh}] (checkFolders) {ltyo}==>{wh} Нет доступа к директории"
    except Exception as e:
        return f"|{rd}ERROR{wh}| [code:{gr}0{wh}] (checkFolders) {ltyo}==>{wh} {e}"

def checkFoldersONLYLIST(directory_path):
    folders = []
    # Получаем список всех файлов и папок в указанной директории
    files_and_folders = os.listdir(directory_path)

    # Фильтруем только папки
    folders = [folder for folder in files_and_folders if os.path.isdir(os.path.join(directory_path, folder))]

    return  folders

def delDir(path):
    try:
        shutil.rmtree(path)
        print(f"Директория {path} успешно удалена.")
    except Exception as e:
        print(f"Произошла ошибка при удалении директории {path}: {e}")

def checkFileInDirectory(directory_path, file_name):
    dFsecurity = False
    # Получаем список файлов в указанной директории
    files = os.listdir(directory_path)

    # Проверяем, есть ли указанный файл в списке файлов
    if file_name in files:
        print(f"|{gr}ШИФР{wh}| Библиотека '{cy}{file_name}{wh}' содержит дополнительную степень шифрования'.")
        dFsecurity = True
        return dFsecurity
    else:
        dFsecurity = False
        return dFsecurity


def listFileInDir(directory_path):
    try:
        # Получаем список файлов в указанной директории и преобразуем его в строку, разделяя запятой
        files = [file for file in os.listdir(directory_path) if file not in ["Description.txt", "core.imp"]]


        files_str = [file.replace(".psw", "").replace(".init", "").replace(".imp", "").replace(".txt", "") for file in files]

        return files

    except FileNotFoundError:
        print(f"|{rd}ОШИБКА{wh}| [code:{gr}4{wh}] (listFileInDir/FileNotFoundError) [{rd}FATAL{wh}] {ltyo}==>{wh} Директория не найдена!")
        return None

def packFolder(folder_path):
    # Создаем zip-архив
    shutil.make_archive(folder_path, 'zip', folder_path)

    # Удаляем оригинальную папку
    shutil.rmtree(folder_path)

    # Получаем имя архива без расширения
    zip_name = f"{folder_path}.zip"

    # Переименовываем архив, убирая расширение .zip
    os.rename(zip_name, folder_path)
    print(f'|{gr}ГОТОВО {ltbl}-> {gr}АРХИВАЦИЯ{wh}|')

def unpackFolder(archive_path):
    # Переименовываем архив, добавляя расширение .zip
    os.rename(archive_path, f"{archive_path}.zip")

    # Распаковываем архив в ту же папку
    shutil.unpack_archive(f"{archive_path}.zip", extract_dir=archive_path)

    # Удаляем архив
    os.remove(f"{archive_path}.zip")

    print(f'|{gr}ГОТОВО {ltbl}-> {gr}РАСПАКОВКА{wh}|')

def createNewDirectory(directory_path, folder_name):
    # Полный путь к новой папке
    new_folder_path = os.path.join(directory_path, folder_name)

    # Проверяем, существует ли папка
    if not os.path.exists(new_folder_path):
        # Создаем новую папку
        os.makedirs(new_folder_path)
        print(f'|{gr}ГОТОВО {ltbl}-> {gr}ГЕНЕРАЦИЯ СЛУЖЕБНЫХ ФАЙЛОВ{wh}|')
    else:
        print(f"|{rd}ОШИБКА{wh}| [code:{gr}1{wh}] (createNewDirectory/os.makedirs()) {ltyo}==>{wh} Библиотека с таким именем уже существует!")

def writeToFile(directory_path, file_name, data):
    # Полный путь к новому файлу
    file_path = os.path.join(directory_path, file_name)

    # Открываем файл в режиме записи
    with open(file_path, 'w') as file:
        # Записываем данные в файл
        file.write(data)
        print(f'|{gr}ГОТОВО {ltbl}-> {gr}ЗАПИСЬ{wh}|')

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def decode_base64_key(base64_key):
    # Декодируем base64-строку и возвращаем 32 байта (256 бит)
    try:
        decoded_key = base64.urlsafe_b64decode(base64_key + '=' * (4 - len(base64_key) % 4))
        if len(decoded_key) != 32:
            raise ValueError(f"|{rd}ERROR{wh}| Длина ключа должна быть 32 байта.")
        return decoded_key
    except Exception as e:
        raise ValueError(f"|{rd}ERROR{wh}| Некорректная base64-строка ключа.") from e

def tablOfLibsPaswd(directory, file_list):
    for file_name in file_list:
        full_path = os.path.join(directory, file_name)
        try:
            with open(full_path, 'r') as file:
                file_content = file.readline().strip()
                print(f'| {file_name:<20} {file_content}')
        except FileNotFoundError:
            print(f'{file_name:<20} File not found')
        except Exception as e:
            print(f'{file_name:<20} Error: {str(e)}')

def createLibFN():    #Всё ок
    clear()
    while True:
        print("|===================================|")
        print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
        print("|===================================|")
        print()
        libName = input(f"|{bc.CYAN}ВВОД{bc.WHITE}| Введите имя для библиотеки: ")
        file_path = os.path.join(MAIN_FOLDER, libName)
        if os.path.isfile(file_path):
            print(f"|{bc.RED}ERROR{bc.WHITE}| Такая библиотека уже существует!")
            t.sleep(1)
            clear()
            continue
        else:
            print(f"| {gr}ОК{wh} | Название {libName} допустимо")
            t.sleep(1.1)
            clear()
            print("|===================================|")
            print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
            print("|===================================|")
            print()
            opisCreateChoice = input(f"|{cy}ВВОД{wh}| Создать описание для библиотеки?({gr}y{wh}/{rd}n{wh}): ")
            if opisCreateChoice == "y" or opisCreateChoice == "Y":
                clear()
                print("|===================================|")
                print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
                print("|===================================|")
                print()
                opis = input(f"|{cy}ВВОД{wh}| Введите описание для этой библиотеки: ")
                clear()
            else:
                opis = " "
                clear()
            print("|===================================|")
            print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
            print("|===================================|")
            print()
            localKeyCreateChoice = input(f"|{cy}ВВОД{wh}| Подключить локальный ключ?({gr}y{wh}/{rd}n{wh}): ")
            if localKeyCreateChoice == "y" or localKeyCreateChoice == "Y":
                clear()
                print("|===================================|")
                print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
                print("|===================================|")
                print()
                localKey = Fernet.generate_key()
                print(f"|{gr}КЛЮЧ{wh}| Программа сгенерировала ключ для библиотеки: {localKey}")
                localKeyCreateChoice = True
                saveLocalKeyChoice = input(f"|{cy}ВВОД{wh}| Сохранить ключ в файл?({gr}y{wh}/{rd}n{wh}): ")
                if saveLocalKeyChoice == "y" or saveLocalKeyChoice == "Y":
                    clear()
                    print("|===================================|")
                    print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
                    print("|===================================|")
                    print()
                    saveLocalKeyFilePath = input(f"|{cy}ВВОД{wh}| Введите путь для сохранения: ")
                    clear()
                    saveLocalKeyChoice = True
                else:
                    clear()
                    saveLocalKeyChoice = False
                    saveLocalKeyFilePath = " "
            else:
                clear()
                localKey = " "
                localKeyCreateChoice = False
                saveLocalKeyChoice = False
                saveLocalKeyFilePath = " "

            clear()
            print(f"| {ltyo}Будет создана библиотека со следующими параметрами{wh} |")
            print()
            print(f"| Имя: {ltbl}{libName}{wh}")
            print(f"| Описание: {ltbl}{opis}{wh}")
            print(f"| Локальный ключ: {ltbl}{localKey}{wh}")
            print(f"| Путь к файлу ключа: {ltbl}{saveLocalKeyFilePath}{wh}")
            print()
            saveChoice = input(f"|{cy}ВВОД{wh}| Создать библиотеку с текущими параметрами?({gr}y{wh}/{rd}n{wh}): ")
            if saveChoice == "y" or saveChoice == "Y":
                clear()
                print("|===================================|")
                print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
                print("|===================================|")
                print()
                print(f"|{gr}ПРОЦЕСС{wh}| Создание файловой системы библиотеки")
                createNewDirectory(MAIN_FOLDER, libName)
                if localKeyCreateChoice == True:
                    createNewDirectory(f"{MAIN_FOLDER}/{libName}", f"{libName}PRIVATE")
                    writeToFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", "core.imp  ", "!DO NOT DELETE!")
                    writeToFile(f"{MAIN_FOLDER}/{libName}", "crypto.init", "!THISE LIB IS ENCRYPTED!")
                    writeToFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", "Description.txt", opis)
                    packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                    encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                    localKey = str(localKey)
                    if saveLocalKeyChoice == True:
                        writeToFile(saveLocalKeyFilePath, f"key({libName}).txt", localKey)
                    packFolder(f"{MAIN_FOLDER}/{libName}")
                    encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                elif localKeyCreateChoice == False:
                    createNewDirectory(f"{MAIN_FOLDER}", libName)
                    writeToFile(f"{MAIN_FOLDER}/{libName}", "core.imp  ", "!DO NOT DELETE!")
                    writeToFile(f"{MAIN_FOLDER}/{libName}", "Description.txt", opis)
                    packFolder(f"{MAIN_FOLDER}/{libName}")
                    encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                print(f"|{gr}УСПЕШНО ЗАВЕРШЕНО{wh}|")
                 
                t.sleep(1)
                clear()
                print("|===================================|")
                print(f"|    {ltyo}CРЕДСТВО СОЗДАНИЯ БИБЛИОТЕК{wh}    |")
                print("|===================================|")
                print()
                print(f"|      {cy}МЕНЮ ДЕЙСТВИЙ{wh}     |")
                print(f"| {gr}1{wh} - Главное меню       |")
                print(f"| {gr}2{wh} - Перезапуск функции |")
                print(f"| {gr}3{wh} - Выход из программы |")
                print()
                choiceModeReturn1 = input(f"|{cy}ВВОД{wh}| >> ")
                if choiceModeReturn1 == "1":
                     
                    clear()
                    main()
                elif choiceModeReturn1 == "2":
                     
                    clear()
                    continue
                elif choiceModeReturn1 == "3":
                     
                    exit()
            elif saveChoice == "n" or saveChoice == "N":
                 
                clear()
                continue
            elif saveChoice == "01":
                 
                main()

def addNewPassw():
    while True:
        clear()
        print("|===============================|")
        print(f"|    {ltyo}CРЕДСТВО ЗАПИСИ ПАРОЛЕЙ{wh}    |")
        print("|===============================|")
        print()
        listLibs = listFileInDir(MAIN_FOLDER)
        listLibs_str = ", ".join(listLibs).replace("'", "").replace("[", "").replace("]", "")
        if listLibs:
            print()
            chosenLib = input(f"|{cy}ВВОД{wh}| Выберите библиотеку для записи({listLibs_str}): ")
            libName = chosenLib

            if chosenLib in listLibs:
                print(f"| {gr}ОК{wh} | Библиотека {cy}{libName}{wh} инициализирована")
                t.sleep(1.1)
                decrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                try:
                    # Распаковываем архив и удаляем его
                    unpackFolder(f"{MAIN_FOLDER}/{libName}")
                except Exception as e:
                    print(f'Произошла ошибка: {str(e)}')
                t.sleep(1)

                if checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == True:
                    clear()
                    print("|===============================|")
                    print(f"|    {ltyo}CРЕДСТВО ЗАПИСИ ПАРОЛЕЙ{wh}    |")
                    print("|===============================|")
                    print()
                    localKey = input(f"|{cy}ВВОД{wh}| Введите приватный ключ для этой библиотеки: ")
                    localKey = localKey.encode('utf-8')
                    decrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                    unpackFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                    print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                    while True:
                        clear()
                        print("|===============================|")
                        print(f"|    {ltyo}CРЕДСТВО ЗАПИСИ ПАРОЛЕЙ{wh}    |")
                        print("|===============================|")
                        print()
                        serviseName = input(f"|{cy}ВВОД{wh}| Введите имя сервиса, пароль которого требуеся сохранить: ")
                        newPassword = input(f"|{cy}ВВОД{wh}| Введите пароль({gr}1{wh} - Сгенерировать простой пароль / {gr}2{wh} - Сгенерировать продвинутый пароль): ")
                        if newPassword == "1":
                            newPassword = genSimplePasswdS(20)
                            print(f"| {gr}ОК{wh} | Сгенерированный пароль: {cy}{newPassword}{wh}")
                            t.sleep(1)
                        writeToFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", f"{serviseName}.psw", newPassword)
                        print(f"| {gr}ОК{wh} | Пароль сохранён")
                        t.sleep(1.2)
                        clear()
                        print(f"|                {cy}МЕНЮ ДЕЙСТВИЙ{wh}               |")
                        print(f"| {gr}1{wh} - Записать новый пароль в эту библиотеку |")
                        print(f"| {gr}2{wh} - Записать новый пароль в др. библиотеку |")
                        print(f"| {gr}3{wh} - Главное меню                           |")
                        print(f"| {gr}4{wh} - Выход из программы                     |")
                        choiceModeLocal1 = input(f"|{cy}ВВОД{wh}| >> ")
                        if choiceModeLocal1 == "1":
                            clear()
                            continue
                        elif choiceModeLocal1 == "2":
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            addNewPassw()
                        elif choiceModeLocal1 == "3":
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            main()
                        elif choiceModeLocal1 == "4":
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            exit()
                        else:
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                elif checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == False:
                    while True:
                        clear()
                        print("|===============================|")
                        print(f"|    {ltyo}CРЕДСТВО ЗАПИСИ ПАРОЛЕЙ{wh}    |")
                        print("|===============================|")
                        print()
                        serviseName = input(f"|{cy}ВВОД{wh}| Введите имя сервиса, пароль которого требуеся сохранить: ")
                        newPassword = input(f"|{cy}ВВОД{wh}| Введите пароль({gr}1{wh} - Сгенерировать простой пароль / {gr}2{wh} - Сгенерировать продвинутый пароль): ")
                        if newPassword == "1":
                            newPassword = genSimplePasswdS(20)
                            print(f"| {gr}ОК{wh} | Сгенерированный пароль: {cy}{newPassword}{wh}")
                            t.sleep(1)
                        elif newPassword == "2":
                            newPassword = genHardPasswd(40)
                            print(f"| {gr}ОК{wh} | Сгенерированный пароль: {cy}{newPassword}{wh}")
                            t.sleep(1)
                        writeToFile(f"{MAIN_FOLDER}/{libName}", f"{serviseName}.psw", newPassword)
                        t.sleep(1.5)
                        clear()
                        print(f"| {gr}ОК{wh} | Пароль сохранён")
                        print(f"|                {cy}МЕНЮ ДЕЙСТВИЙ{wh}               |")
                        print(f"| {gr}1{wh} - Записать новый пароль в эту библиотеку |")
                        print(f"| {gr}2{wh} - Записать новый пароль в др. библиотеку |")
                        print(f"| {gr}3{wh} - Главное меню                           |")
                        print(f"| {gr}4{wh} - Выход из программы                     |")
                        choiceModeLocal1 = input(f"|{cy}ВВОД{wh}| >> ")
                        if choiceModeLocal1 == "1":
                            clear()
                            continue
                        elif choiceModeLocal1 == "2":
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            addNewPassw()
                        elif choiceModeLocal1 == "3":
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            main()
                        elif choiceModeLocal1 == "4":
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            exit()
                        else:
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                             
                            clear()
                            pass
                break

            else:
                print(f"|{rd}ОШИБКА{wh}| Библиотека {cy}{chosenLib}{wh} не существует")
                t.sleep(1.1)
                continue
        else:
            print(f"|{rd}ОШИБКА{wh}| [code:{gr}3{wh}] [{rd}FATAL{wh}] (addNewPassw/listLibs) {ltyo}==>{wh} Отсутствует служебный список")
            t.sleep(1.1)
            exit()

def readLibFN():
    while True:
        clear()
        print()
        print("|=========================================|")
        print(f"|         {ltyo}CРЕДСТВО ЧТЕНИЯ ПАРОЛЕЙ{wh}         |")
        print("|=========================================|")
        print()
        listLibs = listFileInDir(MAIN_FOLDER)
        if listLibs:
            print()
            listLibs_str = ", ".join(listLibs).replace("'", "").replace("[", "").replace("]", "")
            chosenLib = input(f"|{cy}ВВОД{wh}| Выберите библиотеку для записи({listLibs_str}): ")
            libName = chosenLib

            if chosenLib in listLibs:                                                                                   #https://mclo.gs/7LUMjS7
                print(f"| {gr}ОК{wh} | Библиотека {cy}{libName}{wh} инициализирована")
                t.sleep(1.1)
                decrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                try:
                    # Распаковываем архив и удаляем его
                    unpackFolder(f"{MAIN_FOLDER}/{libName}")
                except Exception as e:
                    print(f'Произошла ошибка: {str(e)}')
                t.sleep(1)

                if checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == True:
                    localKey = input(f"|{cy}ВВОД{wh}| Введите приватный ключ для этой библиотеки: ")
                    localKey = localKey.encode('utf-8')
                    decrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                    unpackFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                    print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                    while True:
                        clear()
                        print("|=========================================|")
                        print(f"|         {ltyo}CРЕДСТВО ЧТЕНИЯ ПАРОЛЕЙ{wh}         |")
                        print("|=========================================|")
                        print()
                        print(f'|{gr}FILE{wh}| Описание библиотеки: {readFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE/Description.txt")}')
                        print()
                        print("| Сервисы                              Пароли                   |")
                        #files_str = ", ".join(listFileInDir((f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE"))).replace("'", "").replace("[", "").replace("]", "")
                        files_list = listFileInDir((f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE"))
                        tablOfLibsPaswd(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", files_list)

                        t.sleep(1.3)
                        print()
                        print()
                        print(f"|       {cy}МЕНЮ ДЕЙСТВИЙ{wh}           |")
                        print(f"| {gr}1{wh} - Гл. Меню                  |")
                        print(f"| {gr}2{wh} - Читать другую библиотеку  |")
                        print(f"| {gr}3{wh} - Завершить программу       |")
                        choiceModeLocal3 = input(f"|{cy}ВВОД{wh}| >> ")
                        if choiceModeLocal3 == "1":
                            clear()
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                            clear()
                            main()
                        elif choiceModeLocal3 == "2":
                            clear()
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                            clear()
                            readLibFN()
                        elif choiceModeLocal3 == "3":
                            clear()
                            packFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                            clear()
                            exit()
                elif checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == False:
                    print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                    t.sleep(1.5)
                    clear()
                    while True:
                        clear()
                        print("|=========================================|")
                        print(f"|         {ltyo}CРЕДСТВО ЧТЕНИЯ ПАРОЛЕЙ{wh}         |")
                        print("|=========================================|")
                        print()
                        print(f'|{gr}FILE{wh}| Описание библиотеки: {readFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE/Description.txt")}')
                        print()
                        print(f"| {ltyo}Сервисы                              Пароли{wh}                   |")
                        #files_str = ", ".join(listFileInDir((f"{MAIN_FOLDER}/{libName}"))).replace("'","").replace("[", "").replace("]", "")
                        files_list = listFileInDir((f"{MAIN_FOLDER}/{libName}"))
                        tablOfLibsPaswd(f"{MAIN_FOLDER}/{libName}", files_list)

                        t.sleep(1.3)
                        print()
                        print()
                        print(f"|       {cy}МЕНЮ ДЕЙСТВИЙ{wh}           |")
                        print(f"| {gr}1{wh} - Гл. Меню                  |")
                        print(f"| {gr}2{wh} - Читать другую библиотеку  |")
                        print(f"| {gr}3{wh} - Завершить программу       |")
                        choiceModeLocal3 = input(f"|{cy}ВВОД{wh}| >> ")
                        if choiceModeLocal3 == "1":
                            clear()
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                            clear()
                            main()
                        elif choiceModeLocal3 == "2":
                            clear()
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                            clear()
                            readLibFN()
                        elif choiceModeLocal3 == "3":
                            clear()
                            packFolder(f"{MAIN_FOLDER}/{libName}")
                            encrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                            clear()
                            exit()
                        else:
                            clear()
                            continue

def delLibFN():
    print("Средство удаления библиотек")
    listLibs = listFileInDir(MAIN_FOLDER)
    if listLibs:
        print()
        listLibs_str = ", ".join(listLibs).replace("'", "").replace("[", "").replace("]", "")
        chosenLib = input(f"|{cy}ВВОД{wh}| Выберите библиотеку ({listLibs_str}): ")
        libName = chosenLib

        if chosenLib in listLibs:
            print(f"| {gr}ОК{wh} | Библиотека {cy}{libName}{wh} инициализирована")
            t.sleep(1.1)
            decrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
            try:
                # Распаковываем архив и удаляем его
                unpackFolder(f"{MAIN_FOLDER}/{libName}")
            except Exception as e:
                print(f'Произошла ошибка: {str(e)}')
            if checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == True:
                localKey = input(f"|{cy}ВВОД{wh}| Введите приватный ключ для этой библиотеки: ")
                localKey = localKey.encode('utf-8')
                decrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                unpackFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                delChoice = input("Удалить библиотеку? Восстановление не возможно (y/n): ")
                if delChoice == "y" or delChoice == "Y":
                    delDir(f"{MAIN_FOLDER}/{libName}")
                    print("Процедура завершена успешно")
                    t.sleep(1.5)
                    clear()
                    main()
                else:
                    print("Процедура отменена")
                    t.sleep(1.5)
                    clear()
                    main()
            elif checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == False:
                print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                delChoice = input("Удалить библиотеку? Восстановление не возможно (y/n): ")
                if delChoice == "y" or delChoice == "Y":
                    delDir(f"{MAIN_FOLDER}/{libName}")
                    print("Процедура завершена успешно")
                    t.sleep(1.5)
                    clear()
                    main()
                else:
                    print("Процедура отменена")
                    t.sleep(1.5)
                    clear()
                    main()

def restoreBadLib():
    ispr = False
    while ispr == False:
        if checkFolders(MAIN_FOLDER) == False:
            ispr = True
            print(f"| {gr}ОК{wh} | Ошибки отсутствуют")
            t.sleep(1)
            clear()
            return False
        else:
            ispr = False
            clear()
            print("|===================================|")
            print(f"|  {ltyo}CРЕДСТВО ВОССТАНОВЛЕНИЯ ПАРОЛЕЙ{wh}  |")
            print("|===================================|")
            print()
            print(f"| {ltyo}!!{wh} | Программа обнаружила вероятно повреждённые библиотеки: {checkFolders(MAIN_FOLDER)}")
            choiseRestore = input(f"|{cy}ВВОД{wh}| Исправить возможные повреждения?(y/n): ")
            if choiseRestore == "Y" or choiseRestore == "y":
                clear()
                try:
                    restoreList = checkFoldersONLYLIST(MAIN_FOLDER)
                    for badLib in restoreList:
                        clear()
                        print("|===================================|")
                        print(f"|  {ltyo}CРЕДСТВО ВОССТАНОВЛЕНИЯ ПАРОЛЕЙ{wh}  |")
                        print("|===================================|")
                        print()
                        print(f"| {gr}ОК{wh} | Библиотека инициализирована")
                        t.sleep(1.2)
                        clear()
                        print("|===================================|")
                        print(f"|  {ltyo}CРЕДСТВО ВОССТАНОВЛЕНИЯ ПАРОЛЕЙ{wh}  |")
                        print("|===================================|")
                        print()
                        if checkFileInDirectory(f"{MAIN_FOLDER}/{badLib}", CRYPTOINIT) == True and checkConcretFolderInDir(f"{MAIN_FOLDER}/{badLib}", f"{badLib}PRIVATE") == True:
                            localKey = input(f"|{cy}ВВОД{wh}| Введите ключ: ")
                            localKey = localKey.encode("utf-8")
                            packFolder(f"{MAIN_FOLDER}/{badLib}/{badLib}PRIVATE")
                            encrypt_file(f"{MAIN_FOLDER}/{badLib}/{badLib}PRIVATE", localKey)
                            packFolder(f"{MAIN_FOLDER}/{badLib}")
                            encrypt_file(f"{MAIN_FOLDER}/{badLib}", mainKey)
                            print(f"| {gr}ОК{wh} | Возможные проблемы исправлены")
                            ispr = True
                        elif checkFileInDirectory(f"{MAIN_FOLDER}/{badLib}", CRYPTOINIT) == False and checkFileInDirectory(f"{MAIN_FOLDER}/{badLib}", "core.imp") == True:
                            packFolder(f"{MAIN_FOLDER}/{badLib}")
                            encrypt_file(f"{MAIN_FOLDER}/{badLib}", mainKey)
                            print(f"| {gr}ОК{wh} | Возможные проблемы исправлены")
                            ispr = True

                        else:
                            print(f"|{rd}ERROR{wh}| [code:{gr}7{wh}] (restoreBadLib()) {ltyo}==>{wh} Данная библиотека не подлежит восстановлению.")
                            ispr = True

                        t.sleep(1.3)
                        clear()
                        print(f"| {gr}ОК{wh} | Возможные проблемы исправлены")
                        print("|===================================|")
                        print(f"|  {ltyo}CРЕДСТВО ВОССТАНОВЛЕНИЯ ПАРОЛЕЙ{wh}  |")
                        print("|===================================|")
                        print()
                        print(f"|       {cy}МЕНЮ ДЕЙСТВИЙ{wh}     |")
                        print(f"| {gr}1{wh} - Гл. Меню            |")
                        print(f"| {gr}2{wh} - Повторная проверка  |")
                        print(f"| {gr}3{wh} - Завершить программу |")
                        choiceModeLocal1 = input(f"|{cy}ВВОД{wh}| >> ")
                        if choiceModeLocal1 == "1":
                            clear()
                            main()
                        elif choiceModeLocal1 == "2":
                            clear()
                            continue
                        elif choiceModeLocal1 == "3":
                            exit()
                except 7:
                    print(f"|{rd}ERROR{wh}| [code:{gr}7{wh}] (restoreBadLib()) {ltyo}==>{wh} Данная библиотека не подлежит восстановлению.")
                    ispr = True
                    t.sleep(2)
                    clear()
                    main()
            elif choiseRestore == "N" or choiseRestore == "n":
                t.sleep(1.5)
                clear()
                main()
def genSimplePasswdS(length=20):    #simple system mode
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(r.choice(characters) for i in range(length))
    return password

def genSimplePasswd(length=20):
    while True:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(r.choice(characters) for i in range(length))
        clear()
        print("Сгенерированный пароль")
        print("|============================|")
        print(f"|    {ltyo}{password}{wh}    |")
        print("|============================|")
        print()
        print(f"|       {cy}МЕНЮ ДЕЙСТВИЙ{wh}        |")
        print(f"| {gr}1{wh} - Сгенерировать снова    |")
        print(f"| {gr}2{wh} - Главное меню           |")
        print(f"| {gr}3{wh} - Записать в библиотеку  |")
        print(f"| {gr}4{wh} - Завершить программу    |")
        choiceModeLocal2 = input(f"|{cy}ВВОД{wh}| >> ")
        if choiceModeLocal2 == "1":
            clear()
            continue
        elif choiceModeLocal2 == "2":
            clear()
            main()
        elif choiceModeLocal2 == "3":
            print("Средство записи паролей")
            listLibs = listFileInDir(MAIN_FOLDER)
            if listLibs:
                print()
                listLibs_str = ", ".join(listLibs).replace("'", "").replace("[", "").replace("]", "")
                chosenLib = input(f"|{cy}ВВОД{wh}| Выберите библиотеку ({listLibs_str}): ")
                libName = chosenLib

                if chosenLib in listLibs:
                    print(f"| {gr}ОК{wh} | Библиотека {cy}{libName}{wh} инициализирована")
                    t.sleep(1.1)
                    decrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                    try:
                        # Распаковываем архив и удаляем его
                        unpackFolder(f"{MAIN_FOLDER}/{libName}")
                    except Exception as e:
                        print(f'Произошла ошибка: {str(e)}')
                    if checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == True:
                        localKey = input(f"|{cy}ВВОД{wh}| Введите приватный ключ для этой библиотеки: ")
                        localKey = localKey.encode('utf-8')
                        decrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                        unpackFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                        print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                        while True:
                            serviseName = input(
                                f"|{cy}ВВОД{wh}| Введите имя сервиса, пароль которого требуеся сохранить: ")
                            newPassword = password
                            writeToFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", f"{serviseName}.psw", newPassword)
                            print(f"| {gr}ОК{wh} | Пароль сохранён")
                            t.sleep(2)
                            clear()
                            main()
                    elif checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == False:
                        while True:
                            serviseName = input(f"|{cy}ВВОД{wh}| Введите имя сервиса, пароль которого требуеся сохранить: ")
                            newPassword = password
                            writeToFile(f"{MAIN_FOLDER}/{libName}", f"{serviseName}.psw", newPassword)
                            print(f"| {gr}ОК{wh} | Пароль сохранён")
                            t.sleep(2)
                            clear()
                            main()
        elif choiceModeLocal2 == "4":
            exit()
        else:
            clear()
            continue

    return password

def genHardPasswd(length=40):
    while True:
        characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters + string.punctuation + string.digits
        password = ''.join(r.choice(characters) for i in range(length))
        clear()
        print("Сгенерированный пароль")
        print("|============================|")
        print(f"|    {ltyo}{password}{wh}    |")
        print("|============================|")
        print()
        print(f"|       {cy}МЕНЮ ДЕЙСТВИЙ{wh}        |")
        print(f"| {gr}1{wh} - Сгенерировать снова    |")
        print(f"| {gr}2{wh} - Главное меню           |")
        print(f"| {gr}3{wh} - Записать в библиотеку  |")
        print(f"| {gr}4{wh} - Завершить программу    |")
        choiceModeLocal2 = input(f"|{cy}ВВОД{wh}| >> ")
        if choiceModeLocal2 == "1":
            clear()
            continue
        elif choiceModeLocal2 == "2":
            clear()
            main()
        elif choiceModeLocal2 == "3":
            print("Средство записи паролей")
            listLibs = listFileInDir(MAIN_FOLDER)
            if listLibs:
                print()
                listLibs_str = ", ".join(listLibs).replace("'", "").replace("[", "").replace("]", "")
                chosenLib = input(f"|{cy}ВВОД{wh}| Выберите библиотеку ({listLibs_str}): ")
                libName = chosenLib

                if chosenLib in listLibs:
                    print(f"| {gr}ОК{wh} | Библиотека {cy}{libName}{wh} инициализирована")
                    t.sleep(1.1)
                    decrypt_file(f"{MAIN_FOLDER}/{libName}", mainKey)
                    try:
                        # Распаковываем архив и удаляем его
                        unpackFolder(f"{MAIN_FOLDER}/{libName}")
                    except Exception as e:
                        print(f'Произошла ошибка: {str(e)}')
                    if checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == True:
                        localKey = input(f"|{cy}ВВОД{wh}| Введите приватный ключ для этой библиотеки: ")
                        localKey = localKey.encode('utf-8')
                        decrypt_file(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", localKey)
                        unpackFolder(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE")
                        print(f"| {gr}ОК{wh} | Библиотека {libName} активирована, и готова к эксплуатации.")
                        while True:
                            serviseName = input(
                                f"|{cy}ВВОД{wh}| Введите имя сервиса, пароль которого требуеся сохранить: ")
                            newPassword = password
                            writeToFile(f"{MAIN_FOLDER}/{libName}/{libName}PRIVATE", f"{serviseName}.psw", newPassword)
                            print(f"| {gr}ОК{wh} | Пароль сохранён")
                            t.sleep(2)
                            clear()
                            main()
                    elif checkFileInDirectory(f"{MAIN_FOLDER}/{libName}", "crypto.init") == False:
                        while True:
                            serviseName = input(f"|{cy}ВВОД{wh}| Введите имя сервиса, пароль которого требуеся сохранить: ")
                            newPassword = password
                            writeToFile(f"{MAIN_FOLDER}/{libName}", f"{serviseName}.psw", newPassword)
                            print(f"| {gr}ОК{wh} | Пароль сохранён")
                            t.sleep(2)
                            clear()
                            main()
        elif choiceModeLocal2 == "4":
            exit()
        else:
            clear()
            continue

    return password

def genHardPasswdS(length=40):   #Системная функция, не для пользователя
    characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters + string.punctuation + string.digits
    password = ''.join(r.choice(characters) for i in range(length))
    return password



'''
Менеджер паролей
Разработчик: Журбан Е. 
Версия: 0.2.2046 [pre.beta]
Разработано в России
Язык: Pyton
Локализация: Русская
                          '''
def pasc():
    print("                              __======__                           ")
    print("           AMOGUS          ._/___       \__                       ")
    print("                           |     |      |  |                      ")
    print("                           |_____|         |                      ")
    print("                             |   ____   |==                      ")
    print("                             |  |    |  |                        ")
    print("                              --      --             SUS        ")
    t.sleep(1.5)
    exit()

#MAIN
def main():
    print(f"Менеджер паролей\n"
          "Разработчик: Журбан Е. \n"
          "Версия: 0.2.2058 [pre.beta]\n"
          "Разработано в России\n"
          "Язык: Pyton\n"
          "Локализация: Русская\n")
    t.sleep(1)
    clear()
    print("ver:0.2.2058 [pre.beta]")
    print(f"|{rd}DEBUG{wh}| Debug режим, не для широкого использования!")
    print("|================================|")
    print(f"|        {ltyo}МЕНЕДЖЕР ПАРОЛЕЙ{wh}        |")
    print("|================================|")
    print(f"| {gr}1{wh} - Создать библиотеку         |")
    print(f"| {gr}2{wh} - Записать пароль            |")
    print(f"| {gr}3{wh} - Прочесть пароль            |")
    print(f"| {gr}4{wh} - Восстановить библиотеку    |")
    print(f"| {gr}5{wh} - Удалить библиотеку         |")
    print(f"| {gr}6{wh} - Ген. Простой пароль        |")
    print(f"| {gr}7{wh} - Ген. Сложный пароль        |")
    choiceModeMain = input(f"|{cy}ВВОД{wh}| >> ")
    if choiceModeMain == "1":
        createLibFN()
    elif choiceModeMain == "2":
        addNewPassw()
    elif choiceModeMain == "3":
        readLibFN()
    elif choiceModeMain == "4":
        restoreBadLib()
        clear()
        main()
    elif choiceModeMain == "5":
        clear()
        delLibFN()
    elif choiceModeMain == "6":
        while True:
            print(genSimplePasswd(20))
            break
    elif choiceModeMain == "7":
        while True:
            print(genHardPasswd(40))
            break
    elif choiceModeMain == "#amogus":
        clear()
        pasc()



#START
if __name__ == "__main__":
    main()

