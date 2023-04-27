import telebot

import config
import questions_data
from keyboard import topic_markup, subtopic_markup, question_markup, answer_markup, another_question

bot = telebot.TeleBot(config.TOKEN)

# storing info from questions_data, when bot starts
topics = []
subtopics = []
questions = []
answers = []

# classes for storing info from questions_data
class Topic():
    def __init__(self, topic):
        self.topic = int(topic[0])
        self.text = topic[1]

class Subtopic():
    def __init__(self, subtopic):
        self.topic = int(subtopic[0])
        self.subtopic = int(subtopic[1])
        self.text = subtopic[2]

class Question():
    def __init__(self, question):
        self.topic = int(question[0])
        self.subtopic = int(question[1])
        self.question = int(question[2])
        self.text = question[3]

class Answer():
    def __init__(self, answer):
        self.topic = int(answer[0])
        self.subtopic = int(answer[1])
        self.question = int(answer[2])
        self.url = answer[3]
        self.text = answer[4]
        self.document = answer[5]
        self.redirect = answer[6]

# extraction info from questions_data, and storing it
for topic in questions_data.topics:
    topics.append(Topic(topic))

for subtopic in questions_data.subtopics:
    subtopics.append(Subtopic(subtopic))

for question in questions_data.questions:
    questions.append(Question(question))

for answer in questions_data.answers:
    answers.append(Answer(answer))

@bot.message_handler(commands=['start'])
def start_message(message): 
    start_text = config.START_MESSAGE
    bot.send_message(message.chat.id, start_text, reply_markup=topic_markup(topics))

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    message_id = call.message.id
    chat_id = call.message.chat.id

    # open subtopic
    if 'topic' in call.data:
        topic = int(call.data.split('_')[1])
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=config.CHOOSE_SUBTOPIC)
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup=subtopic_markup(subtopics, topic)
                                      )
    
    # open questions
    elif 'sub' in call.data:
        call_data = call.data.split('_')
        topic = call_data[1]
        subtopic = int(call_data[2])

        # handling the 'back' button
        if topic == 'back':
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=config.CHOOSE_TOPIC)
            bot.edit_message_reply_markup(chat_id=chat_id, 
                                          message_id=message_id, 
                                          reply_markup = topic_markup(topics)
                                          )

        else:
            topic = int(topic)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=config.CHOOSE_QUESTION)
            bot.edit_message_reply_markup(chat_id=chat_id, 
                                          message_id=message_id, 
                                          reply_markup=question_markup(questions, topic, subtopic)
                                          )
    
    # providing answer
    elif 'question' in call.data:
        call_data = call.data.split('_')
        topic = call_data[1]
        subtopic = int(call_data[2])

        # handle the 'back' button
        if topic == 'back':
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=config.CHOOSE_SUBTOPIC)
            bot.edit_message_reply_markup(chat_id=chat_id, 
                                          message_id=message_id, 
                                          reply_markup=subtopic_markup(subtopics, subtopic)
                                          )
        
        # if we need to provide an answer
        else:
            topic = int(topic)
            question = int(call_data[3])
            for answer in answers:
                # extracting the answer we needed
                if answer.topic == topic and answer.subtopic == subtopic and answer.question == question:
                    text = answer.text
                    url = answer.url

                    # if there is a redirect to other part of navigation
                    if answer.redirect != '':
                        redirect_topic = int(answer.redirect[0])
                        redirect_subtopic = int(answer.redirect[1])

                        bot.edit_message_text(chat_id=chat_id, 
                                              message_id=message_id, 
                                              text=config.CHOOSE_QUESTION, 
                                              parse_mode='Markdown'
                                              )
                        
                        bot.edit_message_reply_markup(chat_id=chat_id, 
                                                      message_id=message_id, 
                                                      reply_markup=question_markup(questions, 
                                                                                   redirect_topic, 
                                                                                   redirect_subtopic)
                                                    )
                    
                    # if there is a document we need to send
                    elif answer.document != '':
                        with open(f'{answer.document}.docx', "rb") as f:
                            file_data = f.read()

                        bot.edit_message_text(chat_id=chat_id, 
                                              message_id=message_id, 
                                              text=config.DOCUMENT, 
                                              parse_mode='Markdown'
                                              )  
                          
                        bot.send_document(chat_id=chat_id, 
                                          document=file_data, 
                                          visible_file_name=f'{answer.document}.docx', 
                                          reply_markup=another_question(url)
                                          )
                        pass

                    else:
                        # if there is no text in answer - insert from config
                        if text == '':
                            text = config.NO_TEXT

                        document = False

                        # adding 'send document' button, if we have the url in answer
                        if url == config.document_url:
                            document = True

                        bot.edit_message_text(chat_id=chat_id, 
                                              message_id=message_id, 
                                              text=text, 
                                              parse_mode='Markdown'
                                              )
                        
                        bot.edit_message_reply_markup(chat_id=chat_id, 
                                                      message_id=message_id, 
                                                      reply_markup=answer_markup(url, topic, subtopic, document)
                                                      )
                    break
    
    elif 'answer' in call.data:
        call_data = call.data.split('_')
        # handle the 'back' button from provided answer
        if call_data[1] == 'back':
            topic = int(call_data[2])
            subtopic = int(call_data[3])

            bot.edit_message_text(chat_id=chat_id, 
                                  message_id=message_id, 
                                  text=config.CHOOSE_QUESTION
                                  )
            
            bot.edit_message_reply_markup(chat_id=chat_id, 
                                          message_id=message_id, 
                                          reply_markup=question_markup(questions, topic, subtopic)
                                          )

    # handle the 'contacts' button
    elif 'contacts' in call.data:
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.CONTACT
                              )
        
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = another_question()
                                      )
    
    # handle the 'ask another question' button
    elif 'another' in call.data:
        bot.send_message(chat_id, config.CHOOSE_TOPIC, reply_markup=topic_markup(topics))
    
    # sending document, when the 'send document' button hitted
    elif 'document' in call.data:
        with open(f'{config.document_name}.docx', "rb") as f:
            file_data = f.read()
        bot.send_document(chat_id=chat_id, 
                          document=file_data, 
                          visible_file_name=f'{config.document_name}.docx', 
                          reply_markup = another_question()
                          )

@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, config.CHOOSE_TOPIC, reply_markup=topic_markup(topics))

@bot.message_handler(commands=['question'])
def start_message(message):
    bot.send_message(message.chat.id, config.CHOOSE_TOPIC, reply_markup=topic_markup(topics))

while True:
    try:
        bot.polling()
    except:
        pass