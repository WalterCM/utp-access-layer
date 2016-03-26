from utp_access_layer.ual import UtpAccessLayer

driver_id = 'my_id'
utp = UtpAccessLayer()
utp.start_session(driver_id, 'nimbus')
utp.save_captcha(driver_id, driver_id + '.png')
captcha = input('Captcha?: ')
utp.login(driver_id, code, password, captcha)
classes = utp.get_classes(driver_id)
for class_name in classes:
    for key, value in class_name.items():
        print(key + ": " + value)
    print("");
utp.end_session(driver_id)