from tb_chome_chats import SendMessage

# определяем ответы на вопросы
# 1) определяем ответ на 1й вопрос
def get_message_1_question(str_reply):
    tb_DICT_1 = {'1': 'Заказ можем доставить в выходные, устроит? Ответьте "да" или "нет"',
                 '2': 'Заказ можем доставить в будние дни, ОК? Ответьте "да" или "нет"',
                 '3': 'Заказ можем доставить в любой день, подойдет? Ответьте "да" или "нет"'}
    msg = tb_DICT_1.get(str_reply, 'Не получили ответа на вопрос!( Всего доброго.')
    return msg
# 2) определяем ответ на 2й вопрос (если получен ответ на 1й вопрос)
def get_message_2_question(str_reply):
    tb_DICT_2 = {'да': 'Отлично, привезем Ваш заказ! До встречи.',
                 'нет': 'Жаль, что отказываетесь. Всего доброго.'}
    msg = tb_DICT_2.get(str_reply, 'Не получили ответа на вопрос!( Уточните при следующем запросе.' )
    return msg

# ОСНОВНОЙ БЛОК ЧАТ-БОТА
time_wait = 20
contact_name = "+7 999 999-99-99"
msg_1_question = 'Вопрос 1: Напишите в ответ число 1, 2 или 3 (время ожидания {} секунд)'.format(time_wait)
msg_1_reply_num = SendMessage(contact_name, time_wait, msg_1_question)
msg_1_reply_str = get_message_1_question(msg_1_reply_num)
print('msg_1_reply_num: ', msg_1_reply_num, ' msg_1_reply_str:', msg_1_reply_str)
if msg_1_reply_num == '1' or msg_1_reply_num == '2' or msg_1_reply_num == '3':
    msg_2_question = 'Вопрос 2: ', msg_1_reply_str, 'Напишите в ответ "да" или "нет" (время ожидания {} секунд)'.\
        format(time_wait)
    msg_2_reply_num = SendMessage(contact_name, time_wait, msg_2_question)
    msg_2_reply_str = get_message_2_question(msg_2_reply_num)
    if msg_2_reply_num == 'да' or msg_2_reply_num == 'нет':
        SendMessage(contact_name, 0, msg_2_reply_str)
    else:
        SendMessage(contact_name, 0, msg_2_reply_str)
else:
    SendMessage(contact_name, 0, msg_1_reply_str)