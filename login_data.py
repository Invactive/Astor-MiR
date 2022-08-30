# Fill DB_Host_IP, DB_user, DB_passwd, MIR_IP, MIR_Auth and CAM_IP_Addr to log in


# Data to connect with MySQL database
DB_Host_IP = "TO BE COMPLETED"
DB_user = "TO BE COMPLETED"
DB_passwd = "TO BE COMPLETED"


# Initial connection with MIR
MIR_IP = 'TO BE COMPLETED'
MIR_host = 'http://' + MIR_IP + '/api/v2.0.0/'
MIR_headers = {}
MIR_Auth = 'TO BE COMPLETED'
MIR_headers['Content-Type'] = 'application/json'
MIR_headers['Authorization'] = MIR_Auth


# Data to connect with ESP32-CAM
CAM_IP_Addr = 'TO BE COMPLETED'
Cam_IP = 'http://' + CAM_IP_Addr + ':81/stream'
