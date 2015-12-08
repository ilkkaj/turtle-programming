# -*- coding: utf-8 -*-
from Tkinter import *
from tkColorChooser import askcolor
from turtle import *
from Settings import *
import tkMessageBox, traceback, os, turtle, re, platform, math, sys, StringIO, contextlib, tkFileDialog

def get_color():
    """
    Opens the color picker dialog and assigns three variables to the chosen colors
    Colors are in RGB scale
    """
    global text, LAN
    color = askcolor()[0]
    if color is not None:
        text.insert(END, LAN.RED + ' = ' + str(color[0]) + '\n')
        text.insert(END, LAN.GREEN + ' = ' + str(color[1]) + '\n')
        text.insert(END, BLUE + ' = ' + str(color[2]) + '\n')
    else:
        pass
    

def get_prev():
    """
    Sets previously created script to the text widget if exists
    """
    global prev_arr, text, cur_index
    if (len(prev_arr) > 0 and cur_index > 0):
        text.delete('1.0', END)
        cur_index -= 1
        text.insert(0.0, prev_arr[cur_index])
    else:
        pass

def get_next():
    """
    Sets the followign script to the text widget if exists
    """
    global prev_arr, text, cur_index
    if (len(prev_arr) > 0 and cur_index < len(prev_arr) - 1):
        text.delete('1.0', END)
        cur_index += 1
        text.insert(0.0, prev_arr[cur_index])
    else:
        pass

def generate_code(turtle_code):
    """
    Generates Python code from the given param, checks for hazardous functions
    @type turtle_code: string
    @param turtle_code: turtle drawing script
    @rtype: string
    @return: equivalent Python code

    """
    global cur_difficulty, LAN
    update_previous(turtle_code)
    if cur_difficulty == 1:
        text = LAN.re_lev_one(turtle_code)
    elif cur_difficulty == 2:
        text = LAN.re_lev_two(turtle_code)
    elif cur_difficulty == 3:
        text = LAN.re_lev_three(turtle_code)
    elif cur_difficulty == 4:
        text = LAN.re_lev_four(turtle_code)
    else:
        text = LAN.re_lev_five(turtle_code)
    return text

def update_previous(code):
    """
    Updates previously inserted turtle drawing code
    @type code: string
    @param code: turtle drawing code
    """
    global prev_arr, cur_index
    prev_arr.append(code)
    cur_index = len(prev_arr) - 1

def is_empty(str):
    """
    Checks if a string contains only white spaces or is empty
    @type str: string
    @param str: string to check
    """
    return True if str.strip() == '' else False # --> if str.strip() == '': return True           else: return False

def append_python_code():
    """
    Gets a turtle drawing code from the text widget and sets the equivalent Python code to a new window
    """
    global text, root, LAN
    if is_empty(text.get('1.0', END)):
        return 
    code_text = text.get('1.0', END)
    code_text = generate_code(code_text)
    toplevel = Toplevel()
    toplevel.title(LAN.TITLE_CODE)
    toplevel_text = Text(toplevel)
    toplevel_text.insert(0.0, code_text)
    toplevel_text.insert(END, 'turtle.mainloop()')
    toplevel_text.insert(0.0, 'import turtle\ns = turtle.Screen()\nt = turtle.Turtle()\ns.colormode(255)\n')
    toplevel_text.pack(expand = 1)
    icon = PhotoImage(file = os.path.join('res', 'turtle.gif'))
    toplevel.tk.call('wm', 'iconphoto', toplevel._w, icon)
    menubar = Menu(toplevel)
    menubar.add_command(label = LAN.COPY_CODE, command = copy_code(src = toplevel_text))
    toplevel.config(menu = menubar)
    toplevel.focus_set()

def is_hazard(code):
    """
    Checks if string contains hazardous function calls
    @type code: string
    @param code: program code to check
    """
    return True if re.search('remove|rmdir|rmtree|rename|move|open|file|import|turtle|tk|screen', code.lower()) is not None else False

@contextlib.contextmanager
def stdoutIO(stdout = None):
    '''
    Usage:

    with stdoutIO() as s:
        exec(code)
    s.getvalue()

    redirects exec's stdout to console (print() for instance), can then be used in turtle screen...
    '''
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def highlight_line(from_line, to_line):
    '''
    Highlights line or lines in text widget
    @type from_line: int
    @type to_line: int
    @param from_line: line where highlight begins
    @param to_line: line were highlight goes
    '''
    global text
    text.tag_configure("current_line", background = "#FFF806")
    text.tag_remove("current_line", 1.0, "end")
    text.tag_add("current_line", str(from_line) + ".0", str(to_line) + '.0')

def split_into_blocks(txt):
    '''
    Splits given text into blocks by indents
    @type txt: string
    @param txt: string to split into blocks
    @return: block array
    '''
    txt = txt.encode('utf8')
    temp_arr = txt.split('\n')
    arr = []
    indent_arr = []
    flag = False
    for i, item in enumerate(temp_arr):
        leading_spaces = len(item) - len(item.lstrip())
        if leading_spaces == 0 and ('for i in range(' in item or 'if ' in item):
            if flag == True:
                temp = '\n'.join(indent_arr)
                arr.append(temp)
                indent_arr = []
            indent_arr.append(item)
        elif leading_spaces == 1 and flag == False: # first indent
            flag = True
            indent_arr.append(item)
        elif flag == True and leading_spaces != 0:
            indent_arr.append(item)
        elif leading_spaces == 0 and flag == True:
            flag = False
            temp = '\n'.join(indent_arr)
            arr.append(temp)
            arr.append(item)
            indent_arr = []
        elif leading_spaces == 0 and flag == False:
            arr.append(item)
    if len(indent_arr) > 0:
        arr.append('\n'.join(indent_arr))
    return arr

def run_code(debug = False):
    """
    Executes string as a Python code from the text widget
    """
    global text, s, LAN, show_flow, t
    t.reset() # reset canvas
    code_text = text.get('1.0', END)
    code = generate_code(code_text)
    from_line = to_line = None
    try:
        if is_hazard(code) == False:
            if is_empty(code) == False:
                if show_flow.get() == 0 and debug == False:
                    arr = split_into_blocks(code)
                    from_line = 0
                    to_line = 1
                    for i, item in enumerate(arr):
                        block_size = len(item.split('\n'))
                        if block_size == 1:
                            from_line += 1
                            to_line += 1
                            exec(item)
                        else:
                            from_line += 1
                            to_line += block_size
                            exec(item)
                            from_line += block_size - 1
                else:
                    from time import sleep
                    arr = split_into_blocks(code)
                    from_line = 0
                    to_line = 1
                    for i, item in enumerate(arr):
                        if item != '':
                            block_size = len(item.split('\n'))
                            if block_size == 1:
                                from_line += 1
                                to_line += 1
                                highlight_line(from_line, to_line)
                                sleep(0.5)
                                te = item.encode('utf-8')
                                exec(te)
                            else:
                                from_line += 1
                                to_line += block_size
                                highlight_line(from_line, to_line)
                                sleep(0.5)
                                te = item.encode('utf-8')
                                exec(te)
                                from_line += block_size - 1
                    sleep(3)
                    text.tag_remove("current_line", 1.0, "end")
        else:
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_HAZARD)
    except Exception as e: # try to show a non-generic error message
        print str(e)
        if isinstance(e, IndentationError):
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_INDENTATION)
            highlight_line(from_line, to_line)
        elif isinstance(e, TypeError):
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_BRACKETS)
            highlight_line(from_line, to_line)
        elif isinstance(e, NameError):
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_NAME)
            highlight_line(from_line, to_line)
        elif isinstance(e, SyntaxError):
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_SYNTAX)
            highlight_line(from_line, to_line)
        elif isinstance(e, turtle.TurtleGraphicsError):
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_TURTLE)
            highlight_line(from_line, to_line)
        elif isinstance(e, AttributeError):
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_NAME)
            highlight_line(from_line, to_line)
        else:
            print traceback.format_exc()

def on_close_root():
    """
    Handles the closing operation of the root window 
    """
    global root
    root.destroy()

def copy_code(src = None):
    """
    Copies the string from the text widget to the clipboard
    @type src: text widget
    @param src: source of the copy, if None, copy from the root widget
    """
    global text, root
    code_text = text.get('1.0', END) if src == None else src.get('1.0', END)
    root.clipboard_clear()
    root.clipboard_append(code_text)

def paste_code():
    """
    Pastes the code from the clipboard to the root text widget
    """
    global root, text
    try:
        update_previous(text.get('1.0', END))
        text.insert(INSERT, root.clipboard_get().strip())
    except Exception as e:
        pass

def remove_code():
    """
    Clears the text widget, still saving the string to array
    """
    global text
    update_previous(text.get('1.0', END))
    text.delete('1.0', END)

def get_selected(event):
    '''
    Gets the double clicked item from the command list
    '''
    global text
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    if value != '':
        text.insert(END, value.split('-')[0].strip() + '\n')
        syn()

def syn(event = None):
    '''
    For syntax highlighting
    '''
    global text, LAN
    text.tag_remove("current_line", '1.0', END)
    text.tag_remove("tagname","1.0", END)
    first = "1.0"
    count = IntVar()
    while True:
        first = text.search(LAN.HIGH_WORDS, first, END, count = count, regexp = True)
        if not first:
            break
        last = first + "+" + str(count.get()) + "c"
        text.tag_add("tagname", first, last)
        text.tag_config("tagname", foreground = "#A51029")
        first = last
    __syn_brackets(text, LAN)

def __syn_brackets(text, LAN):
    text.tag_remove("brack","1.0", END)
    first = '1.0'
    count = IntVar()
    while True:
        first = text.search(r'\(([^)]+)\)|\(\)', first, END, count = count, regexp = True)
        if not first:
            return
        last = first + '+' + str(count.get()) + 'c'
        text.tag_add('brack', first, last)
        text.tag_config('brack', foreground = '#56B290')
        first = last

def display():
    """
    Creates the command text widget from the param and creates an empty input text widget
    @type data: string
    @param data: a string of commands 
    """
    global text, help, root, LAN
    help = Listbox(root)
    help.bind('<Double-Button-1>', get_selected)
    text = Text(root)
    txt_scrollbar = Scrollbar(root)
    help_scrollbar = Scrollbar(root)
    txt_scrollbar.config(command = text.yview)
    help_scrollbar.config(command = help.yview)
    text.config(yscrollcommand = txt_scrollbar.set)
    help.config(yscrollcommand = help_scrollbar.set)
    txt_scrollbar.pack(side = 'left', fill = 'y', expand = 0)
    help_scrollbar.pack(side = 'right', fill = 'y', expand = 0)
    arr = LAN.COMMANDS_LEV_ONE.split('\n')
    for i, item in enumerate(arr):
        help.insert(i, item)
        if i % 2 != 0:
            help.itemconfig(i, { 'bg': '#EEEEEE' })
        else:
            help.itemconfig(i, { 'bg': '#D5E0FF' })
    text.insert(0.0, LAN.START_TXT)
    help.pack(side = RIGHT, fill = BOTH, expand = 1)
    text.pack(side = RIGHT, fill = 'x', expand = 1)

'''
Below are the handlers for scaffolding
'''
def easy():
    global help, cur_difficulty, menubar, LAN
    filemenu.entryconfig(LAN.COLOR_MAPS, state = 'disabled')
    cur_difficulty = 1
    help.delete(0, END)
    arr = LAN.COMMANDS_LEV_ONE.split('\n')
    for i, item in enumerate(arr):
        help.insert(i, item)
        if i % 2 != 0:
            help.itemconfig(i, { 'bg': '#EEEEEE' })
        else:
            help.itemconfig(i, { 'bg': '#D5E0FF' })
    
def normal_easy():
    global help, cur_difficulty, menubar, LAN
    filemenu.entryconfig(LAN.COLOR_MAPS, state = 'disabled')
    cur_difficulty = 2
    help.delete(0, END)
    arr = LAN.COMMANDS_LEV_TWO.split('\n')
    for i, item in enumerate(arr):
        help.insert(i, item)
        if i % 2 != 0:
            help.itemconfig(i, { 'bg': '#EEEEEE' })
        else:
            help.itemconfig(i, { 'bg': '#D5E0FF' })


def normal():
    global help, cur_difficulty, menubar, LAN
    filemenu.entryconfig(LAN.COLOR_MAPS, state = 'normal')
    cur_difficulty = 3
    help.delete(0, END)
    arr = LAN.COMMANDS_LEV_THREE.split('\n')
    for i, item in enumerate(arr):
        help.insert(i, item)
        if i % 2 != 0:
            help.itemconfig(i, { 'bg': '#EEEEEE' })
        else:
            help.itemconfig(i, { 'bg': '#D5E0FF' })

def normal_hard():
    global help, cur_difficulty, menubar, LAN
    filemenu.entryconfig(LAN.COLOR_MAPS, state = 'normal')
    cur_difficulty = 4
    help.delete(0, END)
    arr = LAN.COMMANDS_LEV_FOUR.split('\n')
    for i, item in enumerate(arr):
        help.insert(i, item)
        if i % 2 != 0:
            help.itemconfig(i, { 'bg': '#EEEEEE' })
        else:
            help.itemconfig(i, { 'bg': '#D5E0FF' })

def advanced():
    global help, cur_difficulty, menubar, LAN
    filemenu.entryconfig(LAN.COLOR_MAPS, state = 'normal')
    cur_difficulty = 5
    help.delete(0, END)
    arr = LAN.COMMANDS_LEV_FIVE.split('\n')
    for i, item in enumerate(arr):
        help.insert(i, item)
        if i % 2 != 0:
            help.itemconfig(i, { 'bg': '#EEEEEE' })
        else:
            help.itemconfig(i, { 'bg': '#D5E0FF' })
'''
end scaffolding
'''

'''
Draws the coordinates, positions etc
'''
def refresher():
    global root, canvas_compass, t
    canvas_compass.delete('all')
    angle = t.heading()
    angle = math.radians(angle)
    x = int(50 * math.cos(angle))
    y = int(50 * math.sin(angle))
    if x >= 0:
        x += 50
    elif x < 0:
        x = 50 - abs(x)
    if y == 0:
        y = 50
    elif y > 0:
        y = 50 - abs(y)
    elif y < 0:
        y += 150
    canvas_compass.create_line(50, 0, 50, 100)
    canvas_compass.create_line(0, 50, 100, 50)
    x_pos = canvas_compass.create_text(120, 60, anchor = 'nw')
    y_pos = canvas_compass.create_text(120, 80, anchor = 'nw')
    canvas_compass.itemconfig(x_pos, text = 'x: ' + str('%.1f' % t.pos()[0]))
    canvas_compass.itemconfig(y_pos, text = 'y: ' + str('%.1f' % t.pos()[1]))
    canvas_compass.insert(x_pos, 4, '')
    canvas_compass.insert(y_pos, 4, '')
    id_0 = canvas_compass.create_text(90, 35, anchor = 'nw')
    id_90 = canvas_compass.create_text(30, 4, anchor = 'nw')
    id_180 = canvas_compass.create_text(10, 54, anchor = 'nw')
    id_270 = canvas_compass.create_text(55, 85, anchor = 'nw')
    canvas_compass.itemconfig(id_0, text = '0')
    canvas_compass.itemconfig(id_90, text = '90')
    canvas_compass.itemconfig(id_180, text = '180')
    canvas_compass.itemconfig(id_270, text = '270')
    canvas_compass.insert(id_0, 4, '')
    canvas_compass.insert(id_90, 4, '')
    canvas_compass.insert(id_180, 4, '')
    canvas_compass.insert(id_270, 4, '')
    canvas_compass.create_oval(x - 1, y - 1, x + 1, y + 1, fill = 'red')
    canvas_compass.create_line(x, y, 50, 50, fill = 'red', dash = (4, 4))
    root.after(500, refresher)

'''
Saves code to xml file
'''
def save_code():
    global text, cur_difficulty, LAN
    code = text.get('1.0', END).lower()
    temp = code.split('\n')
    for i, item in enumerate(temp):
        li = item
        index = li.find('#')
        if index > -1:
            li = li[:index] + '<comment>' + li[index + 1:] + '</comment>'
            temp[i] = li
    arr = []
    for i in temp:
        temp_str = i#re.sub("\\s+(?=[^()]*\\))", "", i)
        temp_arr = temp_str.split(' ')
        for j, item in enumerate(temp_arr):
            if j == len(temp_arr) - 1:
                arr.append(item + '<n>')
            else:
                arr.append(item)
    script_arr = []
    script_arr.append('<begin_script>')
    script_arr.append('<difficulty=' + str(cur_difficulty) + '>')
    indent = 0
    for i, item in enumerate(arr):
        leading_spaces = len(item) - len(item.lstrip())
        if leading_spaces > indent:
            indent = leading_spaces
        elif leading_spaces < indent:
            indent = leading_spaces
        for j in range(indent):
            script_arr.append('<indent>')
        if item.endswith('<n>'):
            script_arr.append(item.strip())
        else:
            script_arr.append(item.strip() + '<s>')
    script_arr.append('<end_script>')
    code_str = ''.join(script_arr)
    f = tkFileDialog.asksaveasfile(mode = 'w', defaultextension = ".xml")
    if f is None:
        return
    f.write(code_str.encode('utf8'))
    f.close()
    tkMessageBox.showinfo(LAN.SAVED_TITLE, LAN.SAVED_CONTENT)

'''
Opens a code from the xml file
'''
def open_code():
    global text, LAN, cur_difficulty
    from tkFileDialog import askopenfilename
    filename = askopenfilename()
    content = None
    if filename.strip() != '':
        with open(filename) as f:
            content = f.readlines()
        f.close()
    if content is not None:
        parsed_code = parse_code(content)
        if parsed_code is None:
            tkMessageBox.showerror(LAN.GENERIC_ERROR, LAN.ERROR_PARSE)
            return  
        text.delete('1.0', END)
        text.insert(0.0, parsed_code)
        syn()
        if cur_difficulty == 1:
            easy()
        elif cur_difficulty == 2:
            normal_easy()
        elif cur_difficulty == 3:
            normal()
        elif cur_difficulty == 4:
            normal_hard()
        else:
            advanced()

'''
Parses xml format to python drawing format
'''
def parse_code(arr):
    global cur_difficulty
    code_str = ''.join(arr)
    temp = code_str.find('<difficulty=')
    nu = temp + len('<difficulty=')
    cur_difficulty = int(code_str[nu])
    code_str = code_str[:temp] + code_str[nu + 2:]
    start = code_str.find('<begin_script>')
    end = code_str.find('<end_script>')
    if start == 0 and end > 0:
        code_str = code_str[len('<begin_script>'):end]
        import string
        code_str = string.replace(code_str, '<comment>', '#')
        code_str = string.replace(code_str, '</comment>', '')
        code_str = string.replace(code_str, '<s>', ' ')
        code_str = string.replace(code_str, '<indent>', '\t')
        code_str = string.replace(code_str, '<n>', '\n')
    else:
        return None
    return code_str

'''
Changes the language of the program during the runtime
'''
def lan(param):
    global LAN, help, menubar, editmenu, pref_menu, filemenu, levelmenu, cur_difficulty, text
    code = text.get('1.0', END)
    text.delete('1.0', END)
    code = generate_code(code)
    prev_lan = LAN
    LAN = param
    menubar.entryconfig(prev_lan.PREF, label = LAN.PREF)
    pref_menu.entryconfig(prev_lan.EN, label = LAN.EN)
    pref_menu.entryconfig(prev_lan.FI, label = LAN.FI)
    menubar.entryconfig(prev_lan.EDIT, label = LAN.EDIT)
    editmenu.entryconfig(prev_lan.COPY, label = LAN.COPY)
    editmenu.entryconfig(prev_lan.PASTE, label = LAN.PASTE)
    editmenu.entryconfig(prev_lan.CLEAR, label = LAN.CLEAR)
    editmenu.entryconfig(prev_lan.PREV, label = LAN.PREV)
    editmenu.entryconfig(prev_lan.NEXT, label = LAN.NEXT)
    filemenu.entryconfig(prev_lan.SAVE, label = LAN.SAVE)
    filemenu.entryconfig(prev_lan.OPEN, label = LAN.OPEN)
    menubar.entryconfig(prev_lan.OS_X_FILE, label = LAN.OS_X_FILE)
    filemenu.entryconfig(prev_lan.DRAW, label = LAN.DRAW)
    filemenu.entryconfig(prev_lan.COLOR_MAPS, label = LAN.COLOR_MAPS)
    filemenu.entryconfig(prev_lan.SHOW_CODE, label = LAN.SHOW_CODE)
    menubar.entryconfig(prev_lan.COMMANDS, label = LAN.COMMANDS)
    levelmenu.entryconfig(prev_lan.NOVICE, label = LAN.NOVICE)
    levelmenu.entryconfig(prev_lan.ADVANCED_BEGINNER, label = LAN.ADVANCED_BEGINNER)
    levelmenu.entryconfig(prev_lan.COMPETENT, label = LAN.COMPETENT)
    levelmenu.entryconfig(prev_lan.PROFICIENT, label = LAN.PROFICIENT)
    levelmenu.entryconfig(prev_lan.EXPERT, label = LAN.EXPERT)
    if cur_difficulty == 1:
        easy()
    elif cur_difficulty == 2:
        normal_easy()
    elif cur_difficulty == 3:
        normal()
    elif cur_difficulty == 4:
        normal_hard()
    else:
        advanced()
    code = LAN.from_python_to_turtle(code)
    text.insert(0.0, code)
    syn()


'''
------------    Global variables    ------------
'''
cur_difficulty = 1

prev_arr = []
cur_index = 0

root = Tk()
root.geometry(str(root.winfo_screenwidth()) + 'x' + str(root.winfo_screenheight()))
LAN = FI_LAN # USE THIS TO SET DEFAULT LANGUAGE LAN = EN_LAN FOR INSTANCE
root.title(LAN.TITLE_ROOT)

img = os.path.join('res', 'turtle.gif')
icon = PhotoImage(file = img)

canvas_compass = Canvas(root, width = 200, height = 100)
canvas_compass.pack(side = TOP)
canvas_compass.configure(background = 'white')

help = text = None    

cv = turtle.Canvas(root)
cv.pack(expand = 1, fill = BOTH)

s = turtle.TurtleScreen(cv)
s.colormode(255)

s.addshape(img)

t = turtle.RawTurtle(s)
t.shape(img)
t.pensize(1)
t.width(1)
t.ondrag(t.goto)
display()
menubar = Menu(root)

editmenu = Menu(menubar, tearoff = 0)
editmenu.add_command(label = LAN.COPY, command = copy_code)
editmenu.add_command(label = LAN.PASTE, command = paste_code)
editmenu.add_command(label = LAN.CLEAR, command = remove_code)
editmenu.add_command(label = LAN.PREV, command = get_prev)
editmenu.add_command(label = LAN.NEXT, command = get_next)

pref_menu = Menu(menubar, tearoff = 0)
pref_menu.add_command(label = LAN.EN, command = lambda: lan(EN_LAN))
pref_menu.add_command(label = LAN.FI, command = lambda: lan(FI_LAN))
pref_menu.add_separator()
show_flow = IntVar()
pref_menu.add_checkbutton(label = LAN.SHOW_FLOW, onvalue = 1, offvalue = 0, variable  = show_flow)


filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = LAN.DRAW, command = run_code)
filemenu.add_command(label = LAN.COLOR_MAPS, command = get_color)
filemenu.entryconfig(LAN.COLOR_MAPS, state = 'disabled')
filemenu.add_command(label = LAN.SHOW_CODE, command = append_python_code)
filemenu.add_separator()
filemenu.add_command(label = LAN.SAVE, command = save_code)
filemenu.add_command(label = LAN.OPEN, command = open_code)
menubar.add_cascade(label = LAN.OS_X_FILE, menu = filemenu)
menubar.add_cascade(label = LAN.EDIT, menu = editmenu)
menubar.add_cascade(label = LAN.PREF, menu = pref_menu)

levelmenu = Menu(menubar, tearoff = 0)
levelmenu.add_command(label = LAN.NOVICE, command = easy)
levelmenu.add_command(label = LAN.ADVANCED_BEGINNER, command = normal_easy)
levelmenu.add_command(label = LAN.COMPETENT, command = normal)
levelmenu.add_command(label = LAN.PROFICIENT, command = normal_hard)
levelmenu.add_command(label = LAN.EXPERT, command = advanced)

menubar.add_cascade(label = LAN.COMMANDS, menu = levelmenu)

root.config(menu = menubar)

root.protocol('WM_DELETE_WINDOW', on_close_root)

root.tk.call('wm', 'iconphoto', root._w, icon)
refresher()
root.bind("<Key>", syn)
root.mainloop() 