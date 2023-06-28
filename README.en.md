# Question-answer telegram bot
## Изменить язык: [Русский](README.md)
***
A simple chat bot, which answers questions from database, provides links and sends files.
## [DEMO](README.demo.md)
## Commands:
- question (ask a new question - displays the start markup)

## Installation:
- create and activate a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate # for mac
source venv/Scripts/activate # for windows
```
- install dependencies:
```sh
pip install -r requirements.txt
```
- run project:
```sh
python3 main.py
```
- create .env file
- set environment's variables _(in .env)_:
**TELEBOT_TOKEN** - telegram API's key

## To add additional topics, subtopics, questions and answers:
**Edit questions_data.py file**

**1. In topic's tuple:**
- First element - topic's number
- Second element - topic's title

**2. In subtopic's tuple:**
- First element - topic's number
- Second element - subtopic's number
- Third element - subtopic's title

**3. In question's tuple:**
- First element - topic's number
- Second element - subtopic's number
- Third element - question's number
- Fourth element - question

**4. In answer's tuple:**
- First element - topic's number
- Second element - subtopic's number
- Third element - question's number
- Fourth element - a link, if required _(if there is a link - a link button will be added to an answer)_
- Fifth element - answer's text _(could be empty, will provide text from **config.py** if not filled)_
- Sixth element - document's name, wich should be send _(could be empty, if filled - sends document without text providing)_
- Seventh element - a list, wich contains topic and subtopic numbers, where user should be redirect after asking a question _(could be empty)_