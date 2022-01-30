# PySimpleGUI27 : Using a FlexForm with multiple entry fields
# Prompting provided before multiple text entry boxes
# See printed results from form at last line of listing

import PySimpleGUI as sg
form = sg.FlexForm('Image-Hunter') 

layout =[sg.Text('What is your query?', text_color='blue')],[sg.InputText()],[sg.Submit(), sg.Cancel()]

window=sg.Window('Image-Hunter Interface 1.0', layout)

button,values=window.Read()

import image_miner as miner
miner.main(values[0])

quit()