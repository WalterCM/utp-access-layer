from utp_access_layer.ual import UtpAccessLayer

driver_id = 'my_id'
utp = UtpAccessLayer()
utp.start_session(driver_id, 'nimbus')
utp.save_captcha(driver_id, driver_id + '.png')
captcha = input('Captcha?: ')
utp.login(driver_id, '1130802', 'a16011992', captcha)
print('El usuario se llama ' + utp.get_user_firstname(driver_id))
utp.end_session(driver_id)