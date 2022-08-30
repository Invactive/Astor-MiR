import PySimpleGUI as sg
import cv2
from win32api import GetSystemMetrics
import guli
import matplotlib.pyplot as plt
import schedule
import QR_codes
import figure_plot as fp
import login_data as ld
import requests
import keyboard
import time


AstorColour = "#009459"
inputWinWidth = 540
inputWinHeigth = 280

visuWinWidth = 1100
visuWinHeigth = 840
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'


def checkLoginData(values):
    if (values['MIR_IP'] == ld.MIR_IP and values['MIR_Auth'] == ld.MIR_Auth and
        values['DB_IP'] == ld.DB_Host_IP and values['DB_Username'] == ld.DB_user and
            values['Password'] == ld.DB_passwd and values['CAM_IP'] == ld.CAM_IP_Addr):
        guli.GuliVariable("MIR_IP").setValue(values['MIR_IP'])
        guli.GuliVariable("MIR_Auth").setValue(values['MIR_Auth'])
        guli.GuliVariable("DB_IP").setValue(values['DB_IP'])
        guli.GuliVariable("DB_Username").setValue(values['DB_Username'])
        guli.GuliVariable("Password").setValue(values['Password'])
        guli.GuliVariable("CAM_IP").setValue(values['CAM_IP'])
        return True
    else:
        return False


def flushButtonText(window):
    window['choose_btn'].update(" ")
    time.sleep(3)
    return schedule.CancelJob


def inputWindow():
    sg.theme_background_color(AstorColour)
    sg.theme_text_color("Black")

    # Define the window layout
    layout = [[sg.Push(background_color=AstorColour), sg.Text('Input Data Window', justification='center', font=('Helvetica', '20', 'bold'), auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
              [sg.Text('MIR Robot IP Address:',
                       background_color=AstorColour), sg.Input(key='MIR_IP')],
              [sg.Text('MIR Robot Authorization Code:',
                       background_color=AstorColour), sg.Input(key='MIR_Auth')],
              [sg.Text('Database IP Address:',
                       background_color=AstorColour), sg.Input(key='DB_IP')],
              [sg.Text('Database Username:', background_color=AstorColour),
               sg.Input(key='DB_Username')],
              [sg.Text('Database User Password: ', background_color=AstorColour), sg.InputText(
                  key='Password', password_char='*')],
              [sg.Text('Camera IP Address:', background_color=AstorColour),
               sg.Input(key='CAM_IP')],
              [sg.Button(button_color=(sg.theme_background_color(), sg.theme_background_color()),
               image_filename="src/btn_proceed.png", image_size=(84, 34), image_subsample=1, border_width=0, key='btn_proceed')]]

    # Create the Inputwindow and show it
    InputWindow = sg.Window('Input Window', layout,
                            location=((GetSystemMetrics(0)-inputWinWidth)/2,
                                      (GetSystemMetrics(1)-inputWinHeigth)/2-200),
                            finalize=True, element_justification='r', return_keyboard_events=False, keep_on_top=True)
    InputWindow['MIR_IP'].bind("<Return>", "_Enter")
    InputWindow['MIR_Auth'].bind("<Return>", "_Enter")
    InputWindow['DB_IP'].bind("<Return>", "_Enter")
    InputWindow['DB_Username'].bind("<Return>", "_Enter")
    InputWindow['Password'].bind("<Return>", "_Enter")
    InputWindow['CAM_IP'].bind("<Return>", "_Enter")

    return InputWindow


def visuWindow():
    sg.theme_background_color(AstorColour)
    sg.theme_text_color("Black")

    # Define the window layout
    col1_cam = [[sg.Push(background_color=AstorColour), sg.Text('Live Camera View', font='Helvetica 15', justification='center', auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
                [sg.Push(background_color=AstorColour), sg.Image(
                    filename='', key='camera', enable_events=True), sg.Push(background_color=AstorColour)],
                [sg.Push(background_color=AstorColour), sg.Text(" ", key='QRdet', font=('Helvetica', 20, 'bold'),
                                                                auto_size_text=True, text_color='red', background_color=AstorColour), sg.Push(background_color=AstorColour)]
                ]

    col2_status = [[sg.Push(background_color=AstorColour), sg.Text('Status Panel', justification='center', font='Helvetica 15', auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Text('Robot name:', background_color=AstorColour), sg.Text(str(guli.GuliVariable("robotName").get(
                   )), key='rbt', justification='center', font='Helvetica 10', auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Text('Battery percent:', background_color=AstorColour), sg.Text(str(guli.GuliVariable("battery").get(
                   )), key='batt', justification='center', font='Helvetica 10', auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Text('State:', background_color=AstorColour), sg.Text(str(guli.GuliVariable("state").get()), key='stt',
                                                                                                                    justification='center', font='Helvetica 10', auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Text('Mission:', background_color=AstorColour), sg.Text(str(guli.GuliVariable("mission").get(
                   )), key='mss', justification='center', font='Helvetica 10', auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Button(button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                                                     image_filename="src/btn_cp1.png", image_size=(122, 40), image_subsample=1, border_width=0, key="btn_cp1"), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Button(button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                                                     image_filename="src/btn_cp2.png", image_size=(122, 40), image_subsample=1, border_width=0, key="btn_cp2"), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Button(button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                                                     image_filename="src/btn_cp3.png", image_size=(122, 40), image_subsample=1, border_width=0, key="btn_cp3"), sg.Push(background_color=AstorColour)],
                   [sg.Push(background_color=AstorColour), sg.Text(" ", key='choose_btn', font=('Helvetica', 20, 'bold'),
                                                                   auto_size_text=True, text_color='red', background_color=AstorColour), sg.Push(background_color=AstorColour)]
                   ]

    layout = [[sg.Push(background_color=AstorColour), sg.Text('Control Panel', size=(80, 0), justification='center', font=('Helvetica', '20', 'bold'), auto_size_text=True, background_color=AstorColour), sg.Push(background_color=AstorColour)],
              [sg.Column(col1_cam, expand_x=True), sg.Column(col2_status, vertical_alignment='t', expand_x=True)], [sg.Canvas(key='fig_cv', expand_x=True, background_color=AstorColour)]]

    # Create the VisuWindow and show it
    VisuWindow = sg.Window('Camera Graph Status', layout, size=(visuWinWidth, visuWinHeigth),
                           location=((GetSystemMetrics(0)-visuWinWidth)/2,
                                     (GetSystemMetrics(1)-visuWinHeigth)/2),
                           finalize=True, force_toplevel=True, grab_anywhere=True, grab_anywhere_using_control=True, background_color=AstorColour)

    return VisuWindow


def popupWindow(message):
    sg.theme_text_color("Black")

    layout = [
        [sg.Push(background_color=AstorColour), sg.Text(
            message, background_color=AstorColour), sg.Push(background_color=AstorColour)],
        [sg.Push(background_color=AstorColour), sg.Button(button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                                          image_filename="src/btn_ok.png", image_size=(52, 34), image_subsample=1, border_width=0, key="btn_ok"), sg.Push(background_color=AstorColour)],
    ]
    PopupWindow = sg.Window('POPUP', layout, background_color=AstorColour,
                            return_keyboard_events=True, keep_on_top=True).finalize()

    while True:
        event, values = PopupWindow.read()

        if event == sg.WINDOW_CLOSED:
            guli.GuliVariable("exitInputWindow").setValue('1')
            guli.GuliVariable("winClosed").setValue('1')
            schedule.clear()
            break
        elif event == 'btn_ok':
            break
        elif (event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2)):
            keyboard.wait('enter')
            time.sleep(.1)
            break

    PopupWindow.close()


def main(sh_QR_Detected):
    inputWindow1 = inputWindow()
    visuWindow2 = None

    capFlag = True
    drawFlag = True

    while True:
        window, event, values = sg.read_all_windows(timeout=0)

        # Init when app opens
        try:
            if guli.GuliVariable("Init").get() and drawFlag:
                fp.draw_fig(visuWindow2)
                schedule.every(10).seconds.do(fp.draw_fig, window=visuWindow2)
                plt.figure(1)
                drawFlag = False
        except:
            pass

        # Windows recognition
        if window == inputWindow1:

            if event == sg.WIN_CLOSED:
                guli.GuliVariable("exitInputWindow").setValue('1')
                guli.GuliVariable("winClosed").setValue('1')
                schedule.clear()
                break
            # Enter pressed, input data appoved
            elif (event == "btn_proceed" and checkLoginData(values)):
                guli.GuliVariable("loggedIn").setValue('1')
                inputWindow1.close()
                popupWindow("Connected")
                visuWindow2 = visuWindow()
            elif (event == "MIR_IP" + "_Enter" and checkLoginData(values)):
                window['btn_proceed'].click()
            elif (event == "MIR_IP" + "_Enter" and checkLoginData(values) != True):
                popupWindow("Invalid input data")
            elif (event == "btn_proceed" and checkLoginData(values) != True):
                popupWindow("Invalid input data")

        if window == visuWindow2:
            # Init run once
            try:
                if capFlag:
                    cap = cv2.VideoCapture(ld.Cam_IP)
                    fp.drawBlankFig(window)
                    capFlag = False
            except:
                print("Camera init error")

            if event != sg.WIN_CLOSED:
                schedule.run_pending()

                # Camera handling
                try:
                    ret, frame = cap.read()
                    if cap.isOpened():
                        if ret:
                            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                            window['camera'].update(data=imgbytes)
                            QR_codes.detect_QR(frame, sh_QR_Detected)
                    else:
                        print("Cannot open camera")
                except:
                    print("Camera handling error")

                # QR Code data print
                try:
                    if sh_QR_Detected.value != "":
                        window['QRdet'].update(
                            f"{sh_QR_Detected.value} detected")
                    else:
                        window['QRdet'].update("")
                except:
                    print("QR code data print error")

                # Robot status
                try:
                    window['rbt'].update(
                        str(guli.GuliVariable("robotName").get()))
                    battery_full_str = str(guli.GuliVariable("battery").get())
                    window['batt'].update(battery_full_str[:5])
                    window['stt'].update(str(guli.GuliVariable("state").get()))
                    window['mss'].update(
                        str(guli.GuliVariable("mission").get()))
                except:
                    print("Robot status print error")

                if event == "btn_cp1":
                    changeReg = {"value": 1, "label": "QR_Code_Position"}
                    regPost = requests.put(
                        ld.MIR_host + "registers/3", json=changeReg, headers=ld.MIR_headers)
                    print("Collect_btn1 clicked")
                    window['choose_btn'].update("Btn 1 clicked")
                    schedule.every().second.do(flushButtonText, window=window)
                if event == "btn_cp2":
                    changeReg = {"value": 2, "label": "QR_Code_Position"}
                    regPost = requests.put(
                        ld.MIR_host + "registers/3", json=changeReg, headers=ld.MIR_headers)
                    print("Collect_btn2 clicked")
                    window['choose_btn'].update("Btn 2 clicked")
                    schedule.every().second.do(flushButtonText, window=window)
                if event == "btn_cp3":
                    changeReg = {"value": 3, "label": "QR_Code_Position"}
                    regPost = requests.put(
                        ld.MIR_host + "registers/3", json=changeReg, headers=ld.MIR_headers)
                    print("Collect_btn3 clicked")
                    window['choose_btn'].update("Btn 3 clicked")
                    schedule.every().second.do(flushButtonText, window=window)

            if event == sg.WIN_CLOSED:
                guli.GuliVariable("winClosed").setValue('1')
                guli.GuliVariable("exitInputWindow").setValue('1')
                schedule.clear()
                cap.release()
                break

    window.close()
