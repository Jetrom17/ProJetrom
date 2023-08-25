import PySimpleGUI as sg
import subprocess
import webbrowser

# Função para listar os pacotes
def listar_pacotes():
    try:
        output = subprocess.check_output(["adb", "shell", "pm", "list", "packages"])
        pacotes = [line.strip().decode("utf-8")[8:] for line in output.splitlines()]
        return pacotes
    except Exception as e:
        return [str(e)]

# Função para forçar a parada de um pacote
def forcar_parada(pacote):
    try:
        subprocess.check_output(["adb", "shell", "am", "force-stop", pacote])
        return "Pacote {} forçado a parar com sucesso.".format(pacote)
    except Exception as e:
        return "Erro ao forçar a parada do pacote {}: {}".format(pacote, str(e))

# Função para forçar a parada de todos os pacotes
def forcar_parada_todos():
    confirmacao = sg.popup_ok_cancel("Tem certeza de que deseja forçar a parada de todos os pacotes?")
    if confirmacao == "OK":
        pacotes = listar_pacotes()
        for pacote in pacotes:
            forcar_parada(pacote)
        sg.popup("Todos os pacotes foram forçados a parar.")

# Função para trim-caches com valor definido
def trim_caches(valor):
    try:
        subprocess.check_output(["adb", "shell", "pm", "trim-caches", valor])
        return "Caches limpos com sucesso (valor: {}).".format(valor)
    except Exception as e:
        return "Erro ao limpar caches: {}".format(str(e))

# Layout da interface gráfica
sg.theme("DarkGrey5")  # Escolha um tema que você preferir

icone = 'logo.png' # Defina o caminho para o arquivo de ícone

layout = [
    [sg.Text("Pesquisar por nome de pacote:")],
    [sg.InputText(key="-PESQUISA-"), sg.Button("Pesquisar")],
    [sg.Text("Selecione um pacote para forçar a parada:")],
    [sg.Listbox(values=[], size=(40, 30), key="-PACOTES-"), sg.Image(r'logo.png', size=(500, 500))],
    [sg.Text("Sobre o programa:"), sg.Text(" Link", text_color="blue", enable_events=True, key="-LINK-")],
    [sg.Button("Listar Pacotes"), sg.Button("Forçar Parada"), sg.Button("Forçar Parada em Todos"), sg.Button("Limpar caches 2GB"), sg.Button("Sair")]
]

# Janela da interface gráfica
window = sg.Window("ProJetrom", layout, icon=icone)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Sair":
        break
    elif event == "Listar Pacotes":
        pacotes = listar_pacotes()
        window["-PACOTES-"].update(pacotes)
    elif event == "Forçar Parada":
        selected_pacotes = values["-PACOTES-"]
        if selected_pacotes:
            pacote = selected_pacotes[0]
            resultado = forcar_parada(pacote)
            sg.popup(resultado)
    elif event == "Forçar Parada em Todos":
        forcar_parada_todos()
    elif event == "Pesquisar":
        pesquisa = values["-PESQUISA-"]
        pacotes = listar_pacotes()
        pacotes_filtrados = [pacote for pacote in pacotes if pesquisa.lower() in pacote.lower()]
        window["-PACOTES-"].update(pacotes_filtrados)
    elif event == "-LINK-":
        webbrowser.open("https://jeiel-miranda.pages.dev/ProJetrom")

window.close()
