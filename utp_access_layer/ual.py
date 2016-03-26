from selenium import webdriver
from PIL import Image
from utp_access_layer.config import services, urls, xpaths

class UtpAccessLayer:
    drivers = {}
    def __init__(self):
        print('Starting the Utp Access Layer')

    def start_session(self, driver_id, service):
        print('Starting a session')

        if service not in services:
            print("That service doesn't exist")
            return -1

        if driver_id in self.drivers:
            if self.drivers[driver_id]['active']:
                print("The driver is in use")
                return -1

        driver = {}
        
        driver['instance'] = webdriver.PhantomJS()
        driver['active'] = True
        driver['service'] = service

        self.drivers[driver_id] = driver

        url = urls[service + '_login']
        self.target(driver_id, url)

    def end_session(self, driver_id):
        print('Ending the session')
        driver = self.get_driver(driver_id)
        driver['instance'].close()
        self.drivers.pop(driver_id, None)

    def get_driver(self, name):
        if name in self.drivers:
            return self.drivers[name]
        else:
            print("The driver doesn't exist")
            return -1

    def target(self, driver_id, url):
        driver = self.get_driver(driver_id)
        if driver['instance'].current_url != url:
            print('The urls are different')
            driver['instance'].get(url)

    def get_captcha(self, driver_id):
        if not driver_id in self.drivers:
            print('A session has not been started')
            return -1

        driver = self.get_driver(driver_id)

        print('Getting the captcha of service ' + driver['service'] +'.')
        xpath = xpaths[driver['service'] + '_img']
        
        
        driver['instance'].save_screenshot(driver_id + '.png')
        img = driver['instance'].find_element_by_xpath(xpath)
        loc = img.location

        image = Image.open(driver_id + '.png')

        left = int(loc['x'])
        top = int(loc['y'])
        right = left + 220
        bottom = top + 80

        box = (left, top, right, bottom)

        captcha = image.crop(box)

        return captcha

    def save_captcha(self, driver_id, path):
        captcha = self.get_captcha(driver_id)
        captcha.save(path)

    def login(self, driver_id, user, password, captcha=''):
        if not driver_id in self.drivers:
            print('A session has not been started')
            return -1

        driver = self.get_driver(driver_id)

        print('Logging in with user ' + user + ', and captcha ' 
            + captcha)

        service = driver['service']
        instance = driver['instance']

        user_xpath = xpaths[service + '_user']
        password_xpath = xpaths[service + '_password']
        captcha_xpath = xpaths[service + '_captcha']
        submit_xpath = xpaths[service + '_submit']

        user_input = instance.find_element_by_xpath(user_xpath)
        passowrd_input = instance.find_element_by_xpath(password_xpath)
        captcha_input = instance.find_element_by_xpath(captcha_xpath)

        user_input.clear()
        passowrd_input.clear()
        captcha_input.clear()

        user_input.send_keys(user)
        passowrd_input.send_keys(password)
        captcha_input.send_keys(captcha)

        instance.find_element_by_xpath(submit_xpath).click()

    def get_user_firstname(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        print("Getting real user's firstname")
        url = urls['nimbus_profile']
        xpath = xpaths['user_firstname']

        self.target(driver_id, url)
        firstname = driver['instance'].find_element_by_xpath(xpath).get_attribute('value')

        return firstname

    def get_user_lastname(self):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        print("Getting real user's lastname")
        url = urls['nimbus_profile']
        xpath = xpaths['user_lastname']

        self.target(driver_id, url)
        lastname = driver['instance'].find_element_by_xpath(xpath).get_attribute('value')

        return lastname

    def get_classes(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the whole classes of the session')

        class_ids = self.get_class_ids(driver_id)
        course_ids = self.get_course_ids(driver_id)
        course_names = self.get_course_names(driver_id)
        class_turns = self.get_class_turns(driver_id)
        class_sections = self.get_class_sections(driver_id)
        course_terms = self.get_course_terms(driver_id)
        class_modes = self.get_class_modes(driver_id)

        classes = []
        for i in range(len(class_ids)):
            class_info = {}
            class_info["class_id"] = class_ids[i]
            class_info["course_id"] = course_ids[i]
            class_info["course_name"] = course_names[i]
            class_info["class_turn"] = class_turns[i]
            class_info["class_section"] = class_sections[i]
            class_info["course_term"] = course_terms[i]
            class_info["class_mode"] = class_modes[i]

            classes.append(class_info)
            
        print('Getting all the classes')
        return classes

    def get_class_ids(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the class ids of the session')

        class_ids = []
        elements = driver['instance'].find_elements_by_xpath(xpaths['class_ids'])

        for e in elements:
            class_ids.append(e.text)

        return class_ids

    def get_course_names(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the course names of the session')

        course_names = []
        elements = driver['instance'].find_elements_by_xpath(xpaths['course_names'])

        for e in elements:
            course_names.append(e.text)

        return course_names

    def get_course_ids(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the course ids of the session')

        course_ids = []
        elements = driver['instance'].find_elements_by_xpath(xpaths['course_ids'])

        for e in elements:
            course_ids.append(e.text[7:11])

        return course_ids

    def get_class_turns(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the class turns of the session')

        class_turns = []
        elements = driver['instance'].find_elements_by_xpath(xpaths['class_turns'])

        for e in elements:
            class_turns.append(e.text[20:21])

        return class_turns

    def get_course_terms(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the course terms of the session')

        course_terms = []
        elements = driver['instance'].find_elements_by_xpath(xpaths['course_terms'])

        for e in elements:
            course_terms.append(e.text[30:32])

        return course_terms

    def get_class_sections(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the class sections of the session')

        class_sections = []
        elements = driver['instance'].find_elements_by_xpath(xpaths['class_sections'])

        for e in elements:
            class_sections.append(e.text[43:45])

        return class_sections

    def get_class_modes(self, driver_id):
        driver = self.get_driver(driver_id)
        if not driver['service'] == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(driver_id, url)

        print('Getting the class modes of the session')

        class_modes = []
        elements = driver['instance']   .find_elements_by_xpath(xpaths['class_modes'])

        for e in elements:
            class_modes.append(e.text[58:70])

        return class_modes
