import PySimpleGUI as sg
from ntpath import basename

file_name = 'Untitled'  #Path to the file to save as.
short_name = 'Untitled' #Filename of the file, without path
saved = False  			#True if the file has been saved to/loaded from disk
diffs = False			#True if the document contents differ from the most recently saved contents
prev_version = ''		#Contains the most recently saved version of file


def wipe_doc():
	'''Clears the contents of the document and returns a filename of
	'Untitled', a value of False for the diffs variable, and an empty
	string for the contents of previous_version. '''
	window['DOC'].update('')
	return 'Untitled', False, ''

def save_menu(doc, diffs, is_saved, previous, file_name, save_as=False):
	'''Saves the current document to file. Requires the following arguments:

	doc: String. The content of the document to be saved.

	diffs: Boolean. True if the current contents of the document differ from
	the most recently saved contents.

	is_saved: Boolean. True if the document has been saved to file previously,
	including documents opened from file.

	previous: String. The most recently saved contents of the document.

	file_name: String. The name of the file as previously saved. If the file
	has not been saved previously, this value is ignored(set as 'Untitled',
	but not used.)'

	save_as: Boolean. Set as True when the user selects the 'Save As' menu
	option, otherwise False. '''
	if is_saved and not save_as:
		with open(file_name, 'w', encoding='utf-8') as file:
			file.write(doc)
			previous = doc
			diffs = False
			is_saved=True
			return diffs, is_saved, previous, file_name
	else:
		if f_name := sg.popup_get_file('',no_window=True,save_as=True,file_types=(("Text Files", ".txt"),("ALL Files", ". *"))):
			file_name = f_name
			with open(f_name, 'w', encoding='utf-8') as file:
				file.write(values['DOC'])
				diffs = False
				is_saved=True
				return diffs, is_saved, previous, file_name
		else:
			return diffs, is_saved, previous, file_name


menu_buttons = [	['&File', ['&New                       Ctrl+N',
 							   '&Save                      Ctrl+S',
 							   'Save As...       Ctrl+Shift+S', 
 							   '&Open                     Ctrl+O', 
 							   'E&xit']],
				]

main_screen = [	[sg.Menu(menu_buttons, pad=(200,1), font=('any', 10))],
			[sg.Multiline('', size=(100,30), pad=20, key='DOC', enable_events=True, justification='left')]	]

window = sg.Window('TextPad - Untitled.txt', main_screen, font=('any', 15), enable_close_attempted_event=True, return_keyboard_events=True, finalize=True)

window.bind('<Control_L><s>', key='CTRL-S')
window.bind('<Control_L><S>', key='CTRL-SHIFT-S')
window.bind('<Control_L><n>', key='CTRL-N')
window.bind('<Control_L><o>', key='CTRL-O')

while True:
	event, values = window.read()
	if event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit'): #If the user has unsaved changes, give the choice to save
		if diffs:										   #on attempted program exit.
			choice, _ = sg.Window('Caution', [[sg.T(f'Do you want to save changes to {file_name}?')], [sg.Button('Save',s=10), sg.Button('Don\'t Save', s=10), sg.Button('Cancel', s=10)]], modal=True, font=('any', 15), element_justification='center').read(close=True)
			if choice == 'Save':
				diffs, saved, prev_version, file_name = save_menu(values['DOC'], diffs, saved, prev_version, file_name)
				if not diffs:
					break
			elif choice == 'Don\'t Save':
				break
			else:
				pass
		else:
			break			
	if event == 'DOC': #On entering text, check if the current document differs from the last saved version
		if values['DOC'] != prev_version:
			window.set_title('TextPad - ' + short_name +'*')
			diffs = True
		else:
			window.set_title('TextPad - ' + short_name)
			diffs = False
	if event in ('New                       Ctrl+N', 'CTRL-N'):
		if diffs:
			choice, _ = sg.Window('Caution', [[sg.T(f'Do you want to save changes to {file_name}?')], [sg.Button('Save',s=10), sg.Button('Don\'t Save', s=10), sg.Button('Cancel', s=10)]], modal=True, font=('any', 15), element_justification='center').read(close=True)
			if choice == 'Save':
				diffs, saved, prev_version, file_name = save_menu(values['DOC'], diffs, saved, prev_version, file_name)
				if not diffs:
					file_name, diffs, prev_version = wipe_doc()
					short_name = basename(file_name)
					window.set_title('TextPad - ' + short_name)
			elif choice == 'Don\'t Save':
				file_name, diffs, prev_version = wipe_doc()
				saved=False
				short_name = basename(file_name)
				window.set_title('TextPad - ' + short_name)				
			else:
				pass
		else:
			file_name, diffs, prev_version = wipe_doc()
			saved=False
			short_name = basename(file_name)
			window.set_title('TextPad - ' + short_name)

	if event in ('Save                      Ctrl+S', 'CTRL-S'):
		diffs, saved, prev_version, file_name = save_menu(values['DOC'], diffs, saved, prev_version, file_name)
		if not diffs:
			short_name = basename(file_name)
			window.set_title('TextPad - ' + short_name)		
	if event in ('Save As...       Ctrl+Shift+S', 'CTRL-SHIFT-S'):
		diffs, saved, prev_version, file_name = save_menu(values['DOC'], diffs, saved, prev_version, file_name, save_as=True)
		if not diffs:
			short_name = basename(file_name)
			window.set_title('TextPad - ' + short_name)		
	if event in ('Open                     Ctrl+O', 'CTRL-O'):
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
					saved=True

window.close()