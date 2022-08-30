import qrcode
import cv2
import requests
import login_data as ld


def create_default_QR_codes():
    qr1 = qrcode.QRCode(version=1, box_size=10, border=5)
    data = "WallQR1_Poznan"
    qr1.add_data(data)
    qr1.make(fit=True)
    img = qr1.make_image(fill="black", back_color="white")
    img.save("qrCodes/WallQR1_Poznan.png")

    qr2 = qrcode.QRCode(version=1, box_size=10, border=5)
    data = "WallQR2_Poznan"
    qr2.add_data(data)
    qr2.make(fit=True)
    img = qr2.make_image(fill="black", back_color="white")
    img.save("qrCodes/WallQR2_Poznan.png")

    qr3 = qrcode.QRCode(version=1, box_size=10, border=5)
    data = "StairsQR3_Poznan"
    qr3.add_data(data)
    qr3.make(fit=True)
    img = qr3.make_image(fill="black", back_color="white")
    img.save("qrCodes/StairsQR3_Poznan.png")

    print("3 default QR codes created.")


def detect_QR(frame, sh_QR_Detected):
    try:
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(frame)
        if frame is not None:
            if data:
                if data == "WallQR1_Poznan":
                    sh_QR_Detected.value = "Item1"
                    changeReg = {"value": 1, "label": "QR_Code_Number"}
                    requests.put(ld.MIR_host + "registers/2",
                                 json=changeReg, headers=ld.MIR_headers)
                    # qr_data = sh_QR_Detected.value
                    # print(qr_data, "detected")
                elif data == "WallQR2_Poznan":
                    sh_QR_Detected.value = "Item2"
                    changeReg = {"value": 2, "label": "QR_Code_Number"}
                    requests.put(url=ld.MIR_host + "registers/2",
                                 json=changeReg, headers=ld.MIR_headers)
                    # qr_data = sh_QR_Detected.value
                    # print(qr_data, "detected")
                elif data == "StairsQR3_Poznan":
                    sh_QR_Detected.value = "Item3"
                    changeReg = {"value": 3, "label": "QR_Code_Number"}
                    requests.put(url=ld.MIR_host + "registers/2",
                                 json=changeReg, headers=ld.MIR_headers)
                    # qr_data = sh_QR_Detected.value
                    # print(qr_data, "detected")
                else:
                    sh_QR_Detected.value = "Unknown"
            else:
                sh_QR_Detected.value = ""
    except:
        pass
