import time
import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup

def get_html():
    return requests.get("https://dolarhoy.com/")

def get_all_dolars():
    """ Obtains all anchors (<a>) that contains dollars data. """
    html = get_html()
    soup = BeautifulSoup(html.text, 'html.parser')
    dollars = soup.find_all('a', class_='title') #All dolars have an <a> tag with a href atributte.

    return dollars, soup

def filter_data(dollars_a, soup):
    """ Filters the anchors to get only the ones that belongs to "Dolar Blue" and "Dolar Turista". """
    dollars_a = list(filter(lambda dollar: dollar['href'] in ["/cotizaciondolarblue", "/cotizaciondolarturista"], dollars_a)) #filter only the ones i want
    dollars = []
    dollars.append(dollars_a[0].parent) # I skip position 1 because "Dolar Blue" appears twice.
    dollars.append(dollars_a[2].parent) # Obtain its parents because i want to get the values tags.

    return dollars

def get_dolars_data(dollars):
    """ Returns a dictionary that contains all the info about the two types of dollars. """
    dollars_data = []
    for dollar in dollars:
        compra = dollar.find('div', class_='compra').contents
        venta = dollar.find('div', class_='venta').contents

        try:
            buy_value = compra[1].text
        except:
            buy_value = None

        dollars_data.append(
            {
                'title': dollar.find('a', class_='title').text,
                'buy_value': buy_value,
                'sell_value': venta[1].text,
            }
        )

    return dollars_data

def create_window(dollars_data):
    """ Show the main GUI """
    sg.theme("Green")
    
    frames = [
        [
            [sg.Text("Compra", font=("Arial", 12, 'bold'), text_color='white'), sg.Text("Venta",  font=('Arial', 12, 'bold'), text_color='white')],
            [sg.Text(dollar_data['buy_value'], font=("Arial", 10, 'bold'), text_color='white'), sg.Text(dollar_data['sell_value'], font=("Arial", 10, 'bold'), text_color='white', pad=((30, 0), (0, 0)))],
        ]
            if dollar_data['buy_value'] else
        [
            [sg.Text("Venta",  font=('Arial', 12, 'bold'), text_color='white')],
            [sg.Text(dollar_data['sell_value'], font=("Arial", 10, 'bold'), text_color='white')],
        ]
            for dollar_data in dollars_data
    ]


    layout = [
            [sg.Frame(dollars_data[0]['title'], font=("Helvetica", 12, 'bold'), title_color= "white", layout=frames[0],title_location='n', element_justification= "c")],
            [sg.Frame(dollars_data[1]['title'], font=("Helvetica", 12, 'bold'), title_color= "white", layout=frames[1],title_location='n', element_justification= "c")],
    ]

    window = sg.Window("Dólar Hoy", layout, grab_anywhere=True, element_justification='c')
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break

def no_connection_window():
    sg.theme("Green")

    frame = [
        [sg.Text('Ha ocurrido un problema al intentar conectarse al servidor', pad=(10, 10), font=("Arial", 10, 'bold'), text_color='white')],
        [sg.Text('Por favor, revise el estado de su red', pad=(0, 10), font=("Arial", 10, 'bold'), text_color='white')],
    ]
    
    layout = [
            [sg.Frame('Problemas de conexión', font=("Helvetica", 12, 'bold'), title_color= "white", layout=frame, title_location='n', element_justification= "c")],
    ]

    window = sg.Window("Dólar Hoy", layout, grab_anywhere=True, element_justification='c')
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break

def main():
    try:
        dollars, soup = get_all_dolars()
    except requests.ConnectionError:
        no_connection_window()
    else:
        dollars = filter_data(dollars, soup)
        dollars_data = get_dolars_data(dollars)
        create_window(dollars_data)

if __name__ == '__main__':
    main()