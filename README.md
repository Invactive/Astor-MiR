# Astor-MiR

Intralogistics demo project implemented during apprenticeship in ASTOR Poznan 2022.

# Project tasks

:heavy_check_mark: - MiR REST API queries used to get data from robot and manipulate with PLC registers

:heavy_check_mark: - MySQL read/write data from robot, PHPMyAdmin web tool

:heavy_check_mark: - Window app with live camera view, current informations about robot state, buttons responsible for calling robot to particular place and battery percentage graph refreshed every 30 seconds

:heavy_check_mark: - QR codes recognition combined with robot manipulation (MiR moves to a point according to QR code data)

:x: - Check connection with MySQL database, ESP32CAM and MiR100 robot (to implement)

# Project components

- MiR 100 - cooperative mobile robot (AMR - Autonomous Mobile Robot) with a load capacity of up to 100 kg:
	
	<img src="screenshots/mir100.png" width="475" height="317">

- Desktop aplication made using PySimpleGUI:

	![App_window1](screenshots/Window1.png)

	<img src="screenshots/Window2.png" width="510" height="407">

- MySQL database with Apache server and PHPMyAdmin tool:

	<img src="screenshots/phpmyadmin.png" width="641" height="225">

- ESP32CAM - microcontroller module with WiFi connection and camera:

	<img src="screenshots/esp32cam.png">

# Demonstration video

[Youtube video](https://youtu.be/8ByWWWsOIjM)

# How to use (tutorial in Polish)

Poradnik uruchomienia aplikacji w języku polskim na systemie Windows znajduje się w pliku "Poradnik - Aplikacja MiR.pdf".
