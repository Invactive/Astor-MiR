import database as user_db
import multiprocessing
import app
import schedulers as sch
import guli
import QR_codes
from ctypes import c_wchar_p


if __name__ == '__main__':
    QR_codes.create_default_QR_codes()
    manager = multiprocessing.Manager()
    sh_QR_Detected = multiprocessing.Array(c_wchar_p, "")
    app = multiprocessing.Process(
        name="app", target=app.main, args=(sh_QR_Detected,))
    app.start()
    while True:
        try:
            if guli.GuliVariable("loggedIn").get():
                print("Logged In")
                db, cursor = user_db.createDatabase(guli.GuliVariable("DB_IP").get(),
                                                    guli.GuliVariable(
                                                        "DB_Username").get(),
                                                    guli.GuliVariable("Password").get())
                initLoad = multiprocessing.Process(name="initLoad", target=user_db.initLoad,
                                                   args=[guli.GuliVariable("DB_IP").get(),
                                                         guli.GuliVariable(
                                                             "DB_Username").get(),
                                                         guli.GuliVariable("Password").get()])
                dbScheduler = multiprocessing.Process(name="get_save", target=sch.dbScheduler,
                                                      args=[guli.GuliVariable("DB_IP").get(),
                                                            guli.GuliVariable(
                                                                "DB_Username").get(),
                                                            guli.GuliVariable("Password").get()])
                initLoad.start()
                dbScheduler.start()
                break
            if guli.GuliVariable("exitInputWindow").get():
                break
        except:
            pass
