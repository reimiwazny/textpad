import PySimpleGUI as sg
from ntpath import basename

file_name = 'Untitled'
short_name = 'Untitled'
diffs = False
prev_version = ''
font_size = 15


def wipe_doc():
	window['DOC'].update('')
	return 'Untitled', False, ''


menu_buttons = [	['&File', ['&New', '&Save', 'Save As...', '&Open', 'E&xit']],
					['Format', ['Justify']]	]

main_screen = [	[sg.Menu(menu_buttons, pad=(200,1), font=('any', 10))],
			[sg.Multiline('', size=(100,30), pad=20, key='DOC', enable_events=True)]	]

window = sg.Window('TextPad - Untitled.txt', main_screen, font=('any', 15), enable_close_attempted_event=True, return_keyboard_events=True, finalize=True)

window.bind('<Control_L><s>', key='CTRL-S')
window.bind('<Control_L><S>', key='CTRL-SHIFT-S')
window.bind('<Control_L><n>', key='CTRL-N')
window.bind('<Control_L><o>', key='CTRL-O')

while True:
	event, values = window.read()
	if event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit'):
		if diffs:
			choice, _ = sg.Window('Caution', [[sg.T(f'Do you want to save changes to {file_name}?')], [sg.Button('Save',s=10), sg.Button('Don\'t Save', s=10), sg.Button('Cancel', s=10)]], modal=True, font=('any', 15), element_justification='center').read(close=True)
			if choice == 'Save':
				if file_name != 'Untitled':
					with open(file_name, 'w', encoding='utf-8') as file:
						file.write(values['DOC'])
						prev_version = values['DOC']
						diffs = False
				else:
					if f_name := sg.popup_get_file('',no_window=True,save_as=True,file_types=(("Text Files", ".txt"),("ALL Files", ". *"))):
						with open(f_name, 'w', encoding='utf-8') as file:
							file.write(values['DOC'])
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
			window.set_title('TextPad - ' + short_name +'*')
			diffs = True
		else:
			window.set_title('TextPad - ' + short_name)
			diffs = False
	if event in ('New', 'CTRL-N'):
		if diffs:
			choice, _ = sg.Window('Caution', [[sg.T(f'Do you want to save changes to {file_name}?')], [sg.Button('Save',s=10), sg.Button('Don\'t Save', s=10), sg.Button('Cancel', s=10)]], modal=True, font=('any', 15), element_justification='center').read(close=True)
			if choice == 'Save':
				if file_name != 'Untitled.txt':
					with open(file_name, 'w', encoding='utf-8') as file:
						file.write(values['DOC'])
						prev_version = values['DOC']
						diffs = False
						short_name = basename(file_name)
						window.set_title('TextPad - ' + short_name)
				else:
					if f_name := sg.popup_get_file('',no_window=True,save_as=True,file_types=(("Text Files", ".txt"),("ALL Files", ". *"))):
						with open(f_name, 'w', encoding='utf-8') as file:
							file.write(values['DOC'])
							prev_version = values['DOC']
							diffs = False
							file_name = f_name
							short_name = basename(file_name)
							window.set_title('TextPad - ' + short_name)
				if not diffs:
					file_name, diffs, prev_version = wipe_doc()
			elif choice == 'Don\'t Save':
				file_name, diffs, prev_version = wipe_doc()
			else:
				pass
		else:
			file_name, diffs, prev_version = wipe_doc()

	if event in ('Save', 'CTRL-S'):
		if file_name != 'Untitled':
			with open(file_name, 'w', encoding='utf-8') as file:
				file.write(values['DOC'])
				prev_version = values['DOC']
				diffs = False
				short_name = basename(file_name)
				window.set_title('TextPad - ' + short_name)
		else:
			if f_name := sg.popup_get_file('',no_window=True,save_as=True,file_types=(("Text Files", ".txt"),("ALL Files", ". *"))):
				with open(f_name, 'w', encoding='utf-8') as file:
					file.write(values['DOC'])
					prev_version = values['DOC']
					diffs = False
					file_name = f_name
					short_name = basename(file_name)
					window.set_title('TextPad - ' + short_name)

	if event in ('Save As...', 'CTRL-SHIFT-S'):
		if f_name := sg.popup_get_file('',no_window=True,save_as=True,file_types=(("Text Files", ".txt"),("ALL Files", ". *"))):
			with open(f_name, 'w', encoding='utf-8') as file:
				file.write(values['DOC'])
				prev_version = values['DOC']
				diffs = False
				file_name = f_name
				short_name = basename(file_name)
				window.set_title('TextPad - ' + short_name)

	if event in ('Open', 'CTRL-O'):
		if f_name := sg.popup_get_file('',no_window=True):
			if diffs:
				conf = sg.popup_ok_cancel(f'{file_name} has unsaved changes. Open anyway?', title='Caution', font=('any', 15))
			if not diffs or conf == 'OK':
				file_name = f_name
				with open(f_name, 'r') as file:
					window['DOC'].update(file.read())
					diffs = False
					prev_version = values['DOC']
					short_name = basename(file_name)
					window.set_title('TextPad - ' + short_name)

window.close()