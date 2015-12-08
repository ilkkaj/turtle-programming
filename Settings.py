# -*- coding: utf-8 -*-
import re
import locale

class EN_LAN(object):

	COMMANDS_LEV_ONE = """right(x)   - x: turn to the right in degrees
left(x)   - x: turn to the left in degrees
forward(x)   - x: the amount of the distance ahead
backward(x)  - x: the amount of the distance backwards
say('x')     - x: a word or a sentence, which turtle says
reset()      - clears the picture"""

	COMMANDS_LEV_TWO = COMMANDS_LEV_ONE + """
speed(x)  - x: 0, 10, 6, 3, 1 (from the fastest to the slowest)
size(x)   - x: a line thickness"""

	COMMANDS_LEV_THREE = COMMANDS_LEV_TWO + """
color(red, green, blue)    - x: the color of the line
up()   - raise the pen up
down()   - drop the pen down
red = x   - x: a number from 0 to 255
green = x   - x: a number from 0 to 255
blue = x   - x: a number from 0 to 255"""

	COMMANDS_LEV_FOUR = COMMANDS_LEV_THREE + """
repeat(x)  - x: a number of repetitions, repeatable lines must be indented"""
	
	COMMANDS_LEV_FIVE =  COMMANDS_LEV_FOUR + """
if(x OPERATOR y)   - x: a number, y: a number (conditional lines must be indented), OPERATOR:
                    < - (x less than y)
                    > - (x greater than y)
                    == - (x equals y)
position_x()   - tells the the number of x coordinate of the turtle
position_y()   - tells the the number of y coordinate of the turtle"""
	HIGH_WORDS = r'forward|backward|right|left|speed|size|color|up|down|repeat|if|position_x|position_y|FORWARD|BACKWARD|RIGHT|LEFT|SPEED|SIZE|COLOR|UP|DOWN|REPEAT|IF|POSITION_X|POSITION_Y|say|SAY|reset|RESET'

	@staticmethod
	def re_lev_one(text):
		text = text.lower()
		text = re.sub(r"right(.*)", r"t.right\1", text)
		text = re.sub(r"left(.*)", r"t.left\1", text)
		text = re.sub(r"forward(.*)", r"t.forward\1", text)
		text = re.sub(r"backward(.*)", r"t.backward\1", text)
		text = re.sub(r"say\((.*)\)", r"t.write(\1, True, align='center')", text)
		text = re.sub(r"reset\(\)", r"s.reset()", text)
		return text
	
	@staticmethod
	def re_lev_two(text):
		text = EN_LAN.re_lev_one(text)
		text = re.sub(r"speed(.*)", r"t.speed\1", text)
		text = re.sub(r"size(.*)", r"t.pensize\1", text)
		return text

	@staticmethod
	def re_lev_three(text):
		text = EN_LAN.re_lev_two(text)
		text = re.sub(r"color(.*)", r"t.pencolor\1", text)
		text = re.sub(r"down(.*)", r"t.pendown\1", text)
		text = re.sub(r"up(.*)", r"t.penup\1", text)
		return text

	@staticmethod
	def re_lev_four(text):
		text = EN_LAN.re_lev_three(text)
		text = re.sub(r"repeat(.*)", r"for i in range\1:", text)
		return text

	@staticmethod
	def re_lev_five(text):
		text = EN_LAN.re_lev_four(text)
		text = re.sub(r"if\((.*)\)", r"if \1:", text)
		text = re.sub(r"position_x\(\)", r"t.pos()[0]", text)
		text = re.sub(r"position_y\(\)", r"t.pos()[1]", text)
		return text

	@staticmethod
	def from_python_to_turtle(code):
		code = code.lower()
		code = re.sub(r"t.right(.*)", r"right\1", code)
		code = re.sub(r"t.left(.*)", r"left\1", code)
		code = re.sub(r"t.forward(.*)", r"forward\1", code)
		code = re.sub(r"t.backward(.*)", r"backward\1", code)
		code = re.sub(r"t.speed(.*)", r"speed\1", code)
		code = re.sub(r"t.pensize(.*)", r"size\1", code)
		code = re.sub(r"t.pencolor(.*)", r"color\1", code)
		code = re.sub(r"t.pendown(.*)", r"down\1", code)
		code = re.sub(r"t.penup(.*)", r"up\1", code)
		code = re.sub(r"for i in range(.*):", r"repeat\1", code)
		code = re.sub(r"if (.*):", r"if(\1)", code)
		code = re.sub(r"t.pos\(\)\[0\]", r"position_x()", code)
		code = re.sub(r"t.pos\(\)\[1\]", r"position_y()", code)
		return code

	START_TXT = '# INSERT YOUR CODE HERE\n'
	RED = 'red'
	GREEN = 'green'
	BLUE = 'blue'

	SHOW_FLOW = 'Show program flow'

	PREF = 'Preferences'
	EN = 'English'
	FI = 'Finnish'

	SAVED_TITLE = 'Info'
	SAVED_CONTENT = 'Script saved'

	SAVE = 'Save'
	OPEN = 'Open'

	EDIT = 'Edit'
	DRAW = 'Draw'
	COLOR_MAPS = 'Color maps'
	SHOW_CODE = 'Show Python code'
	COPY = 'Copy'
	PASTE = 'Paste'
	CLEAR = 'Clear'
	NEXT = 'Next'
	PREV = 'Previous'
	COMMANDS = 'Controls'
	NOVICE = 'Novice'
	ADVANCED_BEGINNER = 'Advanced beginner'
	COMPETENT = 'Competent'
	PROFICIENT = 'Proficient'
	EXPERT = 'Expert'

	GENERIC_ERROR = 'Error'

	ERROR_HAZARD = 'Your code contains hazardous system calls'
	ERROR_INDENTATION = 'Please, check the indentations'
	ERROR_BRACKETS = 'Please, check the brackets'
	ERROR_NAME = 'Please, check the spelling'
	ERROR_SYNTAX = 'Please, check the spelling!!!'
	ERROR_TURTLE = 'Please ensure that the given drawing values are positive numbers'
	ERROR_PARSE = 'File is not in valid Turtle drawing form'

	TITLE_ROOT = 'Turtle drawing'

	TITLE_CODE = 'Python code'
	COPY_CODE = 'Copy to clipboard'

	OS_X_FILE = 'File'


class FI_LAN(object):

	COMMANDS_LEV_ONE = u"""oikea(x)   - x: Käännös oikealle asteissa (luku)
vasen(x)   - x: Käännös vasemmalle asteissa (luku)
eteen(x)   - x: Matkan määrä eteen päin
taakse(x)  - x: Matkan määrä taaksen päin
sano('x')    - x: sana tai lause, jonka kilpikonna sanoo
tyhjennä()   - tyhjentää ruudun"""
	
	COMMANDS_LEV_TWO = COMMANDS_LEV_ONE + u"""
nopeus(x)  - x: 0, 10, 6, 3, 1 (nopeimmasta hitainpaan)
koko(x)   - x: viivan paksuus"""

	COMMANDS_LEV_THREE = COMMANDS_LEV_TWO + u"""
väri(punainen, vihreä, sininen)    - x: Viivan väri
nosta()   - Nosta kynä ylös
laske()   - Laske kynä alas
punainen = x   - x: Luku väliltä 0 - 255
vihreä = x   - x: Luku väliltä 0 - 255
sininen = x   - x: Luku väliltä 0 - 255"""

	COMMANDS_LEV_FOUR = COMMANDS_LEV_THREE + u"""
toista(x)  - x: Toistojen määrä, toistettavat rivit sisennetään"""

	COMMANDS_LEV_FIVE =  COMMANDS_LEV_FOUR + u"""
jos(x VERTAILU y)   - x: luku, y: luku, halutut rivit sisennetään, VERTAILU:
                                      < (x on pienempi kuin y)
                                      > (x on suurempi kuin y)
                                      == (x on yhtä juuri kuin y)
paikka_x()   - kilpikonnan x-koordinaatti
paikka_y()   - kilpikonnan y-koordinaatti"""
	HIGH_WORDS = ur'vasen|eteen|oikea|taakse|nopeus|koko|väri|nosta|laske|toista|jos|paikka_x|paikka_y|VASEN|ETEEN|OIKEA|TAAKSE|NOPEUS|KOKO|VÄRI|NOSTA|LASKE|TOISTA|JOS|PAIKKA_X|PAIKKA_Y|sano|SANO|tyhjennä|TYHJENNÄ'
	
	@staticmethod
	def re_lev_one(text):
		text = text.lower()
		text = re.sub(r"oikea(.*)", r"t.right\1", text)
		text = re.sub(r"vasen(.*)", r"t.left\1", text)
		text = re.sub(r"eteen(.*)", r"t.forward\1", text)
		text = re.sub(r"taakse(.*)", r"t.backward\1", text)
		text = re.sub(r"sano\((.*)\)", r"t.write(\1, True, align='center')", text)
		text = re.sub(ur"tyhjennä\(\)", r"s.reset()", text)
		return text

	@staticmethod
	def re_lev_two(text):
		text = FI_LAN.re_lev_one(text)
		text = re.sub(r"nopeus(.*)", r"t.speed\1", text)
		text = re.sub(r"koko(.*)", r"t.pensize\1", text)
		return text

	@staticmethod
	def re_lev_three(text):
		text = FI_LAN.re_lev_two(text)
		text = re.sub(ur"vihreä", r"vihrea", text)
		text = re.sub(ur"väri(.*)", r"t.pencolor\1", text)
		text = re.sub(r"laske(.*)", r"t.pendown\1", text)
		text = re.sub(r"nosta(.*)", r"t.penup\1", text)
		return text

	@staticmethod
	def re_lev_four(text):
		text = FI_LAN.re_lev_three(text)
		text = re.sub(r"toista(.*)", r"for i in range\1:", text)
		return text

	@staticmethod
	def re_lev_five(text):
		text = FI_LAN.re_lev_four(text)
		text = re.sub(r"jos\((.*)\)", r"if \1:", text)
		text = re.sub(r"paikka_x\(\)", r"t.pos()[0]", text)
		text = re.sub(r"paikka_y\(\)", r"t.pos()[1]", text)
		return text

	@staticmethod
	def from_python_to_turtle(code):
		code = code.lower()
		code = re.sub(r"t.right(.*)", r"oikea\1", code)
		code = re.sub(r"t.left(.*)", r"vasen\1", code)
		code = re.sub(r"t.forward(.*)", r"eteen\1", code)
		code = re.sub(r"t.backward(.*)", r"taakse\1", code)
		code = re.sub(r"t.speed(.*)", r"nopeus\1", code)
		code = re.sub(r"t.pensize(.*)", r"koko\1", code)
		code = re.sub(r"t.pencolor(.*)", ur"väri\1", code)
		code = re.sub(r"t.pendown(.*)", r"laske\1", code)
		code = re.sub(r"t.penup(.*)", r"nosta\1", code)
		code = re.sub(r"for i in range(.*):", r"toista\1", code)
		code = re.sub(r"if (.*):", r"jos(\1)", code)
		code = re.sub(r"t.pos\(\)\[0\]", r"paikka_x()", code)
		code = re.sub(r"t.pos\(\)\[1\]", r"paikka_y()", code)
		return code

	START_TXT = '# OHJELMASI:\n'
	RED = 'punainen'
	GREEN = u'vihreä'
	BLUE = 'sininen'

	PREF = 'Asetukset'
	EN = 'Englanti'
	FI = 'Suomi'

	SAVED_TITLE = 'Ilmoitus'
	SAVED_CONTENT = 'Ohjelma tallennettu'

	SAVE = 'Tallenna'
	OPEN = 'Avaa'

	EDIT = 'Muokkaa'
	DRAW = u'Piirrä'
	COLOR_MAPS = u'Värikartat'
	SHOW_CODE = u'Näytä Python-koodi'
	COPY = 'Kopioi'
	PASTE = u'Liitä'
	CLEAR = u'Tyhjennä'
	NEXT = 'Seuraava'
	PREV = 'Edellinen'
	COMMANDS = 'Näytä'
	NOVICE = 'Aloittelija'
	ADVANCED_BEGINNER = 'Kokenut aloittelija'
	COMPETENT = 'Kokenut'
	PROFICIENT = 'Taitava'
	EXPERT = 'Mestari'

	GENERIC_ERROR = 'Virhe'

	ERROR_HAZARD = u'Ohjelmasi sisältää vahingollisia kutsuja'
	ERROR_INDENTATION = 'Tarkista sisennyket'
	ERROR_BRACKETS = 'Tarkista sulut'
	ERROR_NAME = 'Tarkista oikeinkirjoitus'
	ERROR_SYNTAX = 'Tarkista oikeinkirjoitus!!!'
	ERROR_TURTLE = u'Piirtämiseen annetut arvot eivät ole positiivisia kokonaislukuja'
	ERROR_PARSE = u'Tiedosto ei ole oikeassa Turtle drawing -muodossa'

	TITLE_ROOT = 'Kilpikonnailua'
	SHOW_FLOW = 'Näytä ohjelmavuo'
	TITLE_CODE = 'Python-koodi'
	COPY_CODE = 'Kopio leikepöydälle'

	OS_X_FILE = 'Tiedosto'
