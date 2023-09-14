from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tb_settings import TB_USERPATH, TB_DRIVER

# 0) устанавливаем опции Telegram
def prepare_webdriver():
    try:
        s = Service(ChromeDriverManager().install())
        bot_driver = webdriver.Chrome(service=s)
        bot_driver.maximize_window()

        print("Загрузка драйвера выполнена успешно!)")
        return bot_driver
    except:
        print("Загрузка драйвера не выполнена!(")
        return False

# 1) открываем Telegram
def load_webdriver(web_driver, file_cookies):
    try:
        #handle_current = web_driver.current_window_handle
        #if (handle_current is not None) and (handle_current is handle_chrome):
        #    web_driver.switch_to.window(handle_current)
        #else:
        web_driver.get("https://webogram.ru/")
            #handle_chrome = web_driver.current_window_handle
        tb_cookies = web_driver.get_cookies()
        print(tb_cookies)
        with open(file_cookies, "r") as openfile:
            tb_cookies = json.load(openfile)
    except IOError:
        print("Файл tb_cookies.json пока не существует")
    try:
        # запоминаем файл с куками
        json_object = json.dumps(tb_cookies)
        with open(file_cookies, "w") as outfile:
            outfile.write(json_object)
        print("Файл с настройками успешно сохранен!)")
        return True
    except:
        print("Файл с настройками не сохранен!(")
        return False

# 2) получаем число чатов
def get_num_chats(tbot, timetowait, freq):
    for num in range(1, int(timetowait/freq)):
        try:
            time.sleep(freq)
            row_count = tbot.find_element_by_xpath('{}').get_attribute("aria-rowcount")
            if row_count:
                pass
        except:
            print("Чаты пока не найдены!")
            row_count = 0
    print("Найдено число чатов: ", row_count)
    return int(row_count)

# 3) отправляем сообщения адресату
def send_to_chat(tbot, name, msg):
    chat_elem = ""
    try:
        row_count = tbot.find_element_by_xpath('{}').get_attribute("aria-rowcount")
        for num in range(1, int(row_count)+1):
            try:
                param_contact = "/span"
                if name == "tbot_log":
                    param_contact = ""
                params = '{}'.\
                format(num, param_contact, name)
                #print("params=\n", params)
                chat_elem = tbot.find_element_by_xpath(params)
            except NoSuchElementException:
                #print("NoSuchElementException: Чат № {} не существует!".format(num))
                pass
    except IOError:
        #print("IOError: Чат № {} не соответствует имени в поиске!".format(num))
        return -102
    if chat_elem:
        print("Чат найден!)")
        chat_elem.click()
    else:
        print("Завершение функции отправки сообщения в чат, т.к. чат не найден!(")
        return -103
    input_elem = tbot.find_element_by_xpath('{}')
    if input_elem:
        print("Строка ввода обнаружена")
        input_elem.send_keys(msg)
    else:
        print("Строка ввода не найдена")
        return -104
    output_elem = tbot.find_element_by_xpath('{}')
    if output_elem:
        output_elem.click()
        print("Cообщение успешно отправлено!)")
    else:
        print("Сообщение не отправлено!(")
        return -105
    return 0 # нормальное завершение функции

# 4) ждем ответного сообщения
def wait_reply(tbot, row_count, chat_name, time_wait, freq_wait):
    for num in range(1, int(time_wait/freq_wait)):
        # 4.0) шаг по времени
        time.sleep(freq_wait)
        # 4.1) номер контакта
        number = get_num_by_contactname(tbot, row_count, chat_name)
        # 4.2) флаг нового сообщения
        flag_new = is_new_message(tbot, number)
        if flag_new:
        # 4.3) получение текста ответного сообщения
            str_last = get_last_unread_message(tbot, number)
            return str_last
    return -401

# 4.1) получаем номер контакта по имени
def get_num_by_contactname(tbot, row_count, contact_name):
    for num in range(1, int(row_count)+1):
        try:
            str = '{}'.\
                format(num, contact_name)
            #print(str)
            elem = tbot.find_element_by_xpath(str)
            if elem:
                #print("Чат {} соответствует имени {}".format(num, contact_name))
                return num
        except:
            #print("Чат {} не соответствует имени {}".format(num, contact_name))
            row_count = 0
    return -1

# 4.2) выясняем, есть ли новое сообщение для данного контакта
def is_new_message(tbot, number):
    msg = ""
    try:
        tbot.find_element_by_xpath(
            '{}'.
                format(number))
        print("Есть новое сообщение для чата №{}!".format(number))
        return True
    except:
        print("Нет нового сообщения для чата {}!(".format(number))
        return False

# 4.3) пытаемся получить последнее непрочитанное сообщение
def get_last_unread_message(tbot, number):
    try:
        msg = tbot.find_element_by_xpath(
            ''.
                format(number)).text
        print("Получение новое сообщение для чата №{}:\n{}".format(number, msg))
    except:
        print("Нового сообщения для чата {} не получено!".format(number))
        msg = -402
    return msg

# основной цикл выполнения данных
def SendMessage(contact_name, time_wait, msg_question):
    try:
        #### пользовательские данные ####
        # флаг значений приложения
        _flag_chrome = -1001
        # хэндл окна хрома (изначально пустой)
        _handle_chrome = None
        # хэндл драйвера
        print("Инициализация драйвера Chrome")
        _tbot_driver = prepare_webdriver()
        if not _tbot_driver:
            _flag_chrome = -1002
            return _flag_chrome

        # 1) открываем Telegram (если не получилось, приложение также завершаем)
        if not load_webdriver(_tbot_driver, "tb_cookies.json"):
            _flag_chrome = -1003
            return _flag_chrome
        # 2) получаем число чатов (если не получилось за 20 секунд, вызывая 1 раз в секунду, - завершаем приложение)
        time4load = 20
        freq4load = 1
        num_chats = get_num_chats(_tbot_driver, time4load, freq4load)
        if num_chats < 0:
            _flag_chrome = -1004
            return _flag_chrome
        # 3) отправляем сообщения адресату (если не отправилось, завершаем приложение)
        # time_wait = 60 # время ожидания, что сообщение отправлено
        freq_wait = 2 # частота проверки того, что сообщение отправлено
        # contact_name = "+7 999 999 99 99" - имя или номер: то, как называется чат
        is_send = send_to_chat(_tbot_driver, contact_name, msg_question)
        if (is_send < 0):
            _flag_chrome = -1005
            return _flag_chrome
        # 4) переключаемся на "нейтральное" окно статуса (если не получилось, - завершаем приложение)
        # ждем ответного сообщения 60 секунд c частотой раз в 2 секунды
        if send_to_chat(_tbot_driver, "tbot_log", "Служебное сообщение") == 0:
            _flag_chrome = -1006
            return _flag_chrome
        str_reply = wait_reply(_tbot_driver, num_chats, contact_name, time_wait, freq_wait)
        _flag_chrome = 0 # нормальное завершение функции
        return str_reply
    finally:
        _tbot_driver.quit()
        print("_flag_chrome = ", _flag_chrome)
        print("Драйвер браузера Chrome и связанные соединения успешно закрыты!!")
if __name__=="__main__":
    prepare_webdriver()
