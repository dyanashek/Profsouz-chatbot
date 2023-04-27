from telebot import types

# the keyboard with topics
def topic_markup(topics):
    keyboard = types.InlineKeyboardMarkup()

    for topic in topics:
        keyboard.add(types.InlineKeyboardButton(topic.text, callback_data = f'topic_{topic.topic}'))

    keyboard.add(types.InlineKeyboardButton('Юридическая помощь', url='https://sberfriend.sbrf.ru/sberfriend/#/application/D67D5357D4BD097CE053F7E9740A00EB?sberfriend.searchQuery=%D0%BF%D1%80%D0%BE%D1%84%D1%81%D0%BE%D1%8E%D0%B7'))
    keyboard.add(types.InlineKeyboardButton('Контакты', callback_data = 'contacts'))

    return keyboard

# the keyboard with subtopics
def subtopic_markup(subtopics, topic):
    keyboard = types.InlineKeyboardMarkup()

    for subtopic in subtopics:
        if subtopic.topic == topic:
            keyboard.add(types.InlineKeyboardButton(subtopic.text, callback_data = f'sub_{subtopic.topic}_{subtopic.subtopic}'))

    keyboard.add(types.InlineKeyboardButton('Контакты', callback_data = 'contacts'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'sub_back_0'))

    return keyboard

# the keyboard with questions
def question_markup(questions, topic, subtopic):
    keyboard = types.InlineKeyboardMarkup()

    for question in questions:
        if question.topic == topic and question.subtopic == subtopic:
            keyboard.add(types.InlineKeyboardButton(question.text, callback_data = f'question_{question.topic}_{question.subtopic}_{question.question}'))

    keyboard.add(types.InlineKeyboardButton('Контакты', callback_data = 'contacts'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = f'question_back_{topic}'))

    return keyboard

# the keyboard, which we adding when providing an answer (if it's not only a document)
def answer_markup(url, topic, subtopic, document):
    keyboard = types.InlineKeyboardMarkup()

    # if there is a url in the answer - adding url button
    if url != '':
        keyboard.add(types.InlineKeyboardButton('Перейти по ссылке', url=url))

    # if we need to provide additional document to the answer - adding 'send document' button
    if document is True:
        keyboard.add(types.InlineKeyboardButton('Заявление на мат. помощь', callback_data = 'document'))

    keyboard.add(types.InlineKeyboardButton('Контакты', callback_data = 'contacts'))
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = f'answer_back_{topic}_{subtopic}'))
    return keyboard

# the keyboard, which we adding, when sending document or contacts
def another_question(url=''):
    keyboard = types.InlineKeyboardMarkup()

    if url != '':
        keyboard.add(types.InlineKeyboardButton('Перейти по ссылке', url=url))

    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another'))
    return keyboard
