import PySimpleGUI as sg
import os.path

file_name = 'Untitled.txt'
diffs = False
prev_version = ''



def wipe_doc():
	window['DOC'].update('')
	return 'Untitled.txt', False, ''

def save_menu(doc):
	global file_name, diffs, prev_version
	save_screen = [	[sg.Text('Filename:'), sg.Input(key='FNAME', size=15), sg.Text('.txt', pad=((0,5),(5,5))), sg.Button('Save')]]

	window = sg.Window('Save...', save_screen, font=('any', 15), modal=True)

	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED:
			break
		if event == 'Save':
			if values['FNAME'] != '':
				if values['FNAME'].find('.') != -1 or values['FNAME'].find(' ') != -1:
					sg.popup('File name cannot contain \'.\' or spaces.', title='Caution', font=('any', 15))
				else:
					file_name = values['FNAME'] + '.txt'
					if os.path.exists(file_name):
						if sg.popup_ok_cancel(f'The file {file_name} already exists. Overwrite?', title='Caution', font=('any', 15)) == 'OK':
							with open(file_name, 'w', encoding='utf-8') as file:
								file.write(doc)
							diffs = False
							prev_version = doc
					else:
						with open(file_name, 'w', encoding='utf-8') as file:
							file.write(doc)
							diffs = False
							prev_version = doc
			if not diffs:
				break



	window.close()

def open_menu():
	global file_name, diffs, prev_version
	conf = False
	content = ''

	load_screen = [ [sg.Text('File to open:'), sg.Input('', size=15, key='OPEN'), sg.Button('Open')]]

	event, values = sg.Window('Open...', load_screen, font=('any', 15)).read(close=True)
	if event == sg.WIN_CLOSED:
		return None
	if event == 'Open':
		if diffs:
			conf = sg.popup_ok_cancel(f'{file_name} has unsaved changes. Open anyway?', title='Caution', font=('any', 15))
		if not diffs or conf == 'OK':
			target = values['OPEN']
			if target.find('.txt') == -1:
				target += '.txt'
			try:
				with open(target, 'r') as file:
					content = file.read()
					file_name = target
					diffs = False
					prev_version = content
				return content
			except FileNotFoundError:
				sg.popup(f'{target} does not exist.', title='Error', font=('any', 15))



menu_buttons = [	['&File', ['&New', '&Save', 'Save As...', '&Open', '&Customize', 'E&xit']]
						]

main_screen = [	[sg.Menu(menu_buttons, pad=(200,1), font=('any', 10))],
			[sg.Multiline('', size=(60,30), pad=20, key='DOC', enable_events=True)]	]

window = sg.Window('TextPad - Untitled.txt', main_screen, font=('any', 15), enable_close_attempted_event=True)

while True:
	event, values = window.read()
	if event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit'):
		if diffs:
			choice, _ = sg.Window('Caution', [[sg.T(f'Do you want to save changes to {file_name}?')], [sg.Button('Save',s=10), sg.Button('Don\'t Save', s=10), sg.Button('Cancel', s=10)]], modal=True, font=('any', 15), element_justification='center').read(close=True)
			if choice == 'Save':
				if file_name != 'Untitled.txt':
					with open(file_name, 'w', encoding='utf-8') as file:
						file.write(values['DOC'])
						prev_version = values['DOC']
						diffs = False
						window.set_title('TextPad - ' + file_name)
				else:
					save_menu(values['DOC'])
					if values['DOC'] != prev_version:
						window.set_title('TextPad - ' + file_name +'*')
						diffs = True
					else:
						window.set_title('TextPad - ' + file_name)
						diffs = False
				if not diffs:
					break
			elif choice == 'Don\'t Save':
				break
			else:
				pass
		else:
			break			

	if event == 'DOC':
		if values['DOC'] != prev_version:
			window.set_title('TextPad - ' + file_name +'*')
			diffs = True
		else:
			window.set_title('TextPad - ' + file_name)
			diffs = False
	if event == 'New':
		if diffs:
			choice, _ = sg.Window('Caution', [[sg.T(f'Do you want to save changes to {file_name}?')], [sg.Button('Save',s=10), sg.Button('Don\'t Save', s=10), sg.Button('Cancel', s=10)]], modal=True, font=('any', 15), element_justification='center').read(close=True)
			if choice == 'Save':
				if file_name != 'Untitled.txt':
					with open(file_name, 'w', encoding='utf-8') as file:
						file.write(values['DOC'])
						prev_version = values['DOC']
						diffs = False
						window.set_title('TextPad - ' + file_name)
				else:
					save_menu(values['DOC'])
					if values['DOC'] != prev_version:
						window.set_title('TextPad - ' + file_name +'*')
						diffs = True
					else:
						window.set_title('TextPad - ' + file_name)
						diffs = False
				if not diffs:
					file_name, diffs, prev_version = wipe_doc()
			elif choice == 'Don\'t Save':
				file_name, diffs, prev_version = wipe_doc()
			else:
				pass

	if event == 'Save':
		if file_name != 'Untitled.txt':
			with open(file_name, 'w', encoding='utf-8') as file:
				file.write(values['DOC'])
				prev_version = values['DOC']
				diffs = False
				window.set_title('TextPad - ' + file_name)
		else:
			save_menu(values['DOC'])
			if values['DOC'] != prev_version:
				window.set_title('TextPad - ' + file_name +'*')
				diffs = True
			else:
				window.set_title('TextPad - ' + file_name)
				diffs = False
	if event == 'Save As...':
		save_menu(values['DOC'])
	if event == 'Open':
		new_content = open_menu()
		if new_content:
			window['DOC'].update(new_content)
			prev_version = new_content
			diffs = False 
			window.set_title('TextPad - ' + file_name)

window.close()