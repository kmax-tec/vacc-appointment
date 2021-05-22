from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


#Selenium Tool in order to get Appointment at Vaccination Center, specified for Sachsen
#Needed Python and Selenium
#guid-numbers of the elements need to be checked regularly

#LoginPart

#Personal Information
regnr="A...."#Aktenzeichen
passwd="PWD" #Enter Passwd

#Options For Finetuning of the Gecko Driver
coptions = Options()
#coptions.binary_location ='/usr/lib/chromium/chromedriver'
#coptions.add_argument('--no-sandbox')
#coptions.add_argument("--headless")

#options.set_preference("browser.download.folderList",2)
#options.set_preference("browser.download.manager.showWhenStarting", False)
#options.set_preference("browser.download.dir","/Data")
#options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")

#Specify Location of the Webdriver
driver = webdriver.Chrome(executable_path=r"/home/...chromedriver")

#start page for login
driver.get("https://sachsen.impfterminvergabe.de/civ.public/start.html?oe=00.00.IM&mode=cc&cc_key=IOAktion")

#could be longer in case server is busy
delay = 2000 # seconds

#Go to LoginSite
try:
    myElem = WebDriverWait(driver, delay,poll_frequency=3).until(EC.presence_of_element_located((By.ID, 'gwt-uid-3')))
    print ("Login Success!")
except TimeoutException:
    print ("Login Loading took too much time!")

nbr = driver.find_element_by_id("gwt-uid-3") #field for Aktenzeichen
nbr.send_keys(regnr)
code = driver.find_element_by_id("gwt-uid-5") #field for password
code.send_keys(passwd)

button=driver.find_element_by_id("WorkflowButton-4212") #continue
button.click()

#wait till page with Impfcenter is loaded
try:
    myElem = WebDriverWait(driver, delay,poll_frequency=3).until(EC.presence_of_element_located((By.ID, 'gwt-uid-9')))
    print ("Appointment Selection is ready!")
except TimeoutException:
    print ("Appointment Selection took too much time!")

#Select Interest for an Appointment
radio_app = driver.find_element_by_css_selector("label[for='gwt-uid-9']") #Button for Impftermin vereinbaren
radio_app.click()


cont_butt = driver.find_element_by_id("WorkflowButton-4212") #continue
cont_butt.click()

driver.implicitly_wait(5)


ref = driver.find_element_by_css_selector("span.select2-selection") #activate element, to load selection list
ref.click()

select2 = Select(driver.find_element_by_xpath("//select"))
select2.select_by_value("LZ01") #select Impfzenter from list - LZ Leipzig

#continue
cont_butt= driver.find_element_by_id("WorkflowButton-4212")
cont_butt.click()

#Appointment Part, search for appointment

#Search for appointment, if not success, return to previous page and try again
count=0
while True:

        #wait till back button can be pushed
        WebDriverWait(driver, delay, poll_frequency=3).until(EC.element_to_be_clickable((By.ID, "WorkflowButton-4255")))
        print ("Page for Appointment is ready!")
        # info = driver.find_element_by_tag_name("body")
        # print(info.text)

        try:
            #look for text, that no appointment could be found
            myElem = WebDriverWait(driver, delay, poll_frequency=3).until(EC.presence_of_element_located((By.CLASS_NAME, 'sjf-step-intro')))
            nope = driver.find_element_by_class_name("sjf-step-intro")
            error = "Aufgrund der aktuellen Auslastung der Impfzentren und der verfügbaren Impfstoffmenge können wir Ihnen leider keinen Termin anbieten. Bitte versuchen Sie es in ein paar Tagen erneut."

            #if the error text was not found, the request was successful
            if nope.text != error or nope.is_displayed() != True:
                break #Appointment was found

            count +=1 #raise counter
            print("Failed try",count)
            back = driver.find_element_by_id("WorkflowButton-4255")
            back.click() #go to previous page
            WebDriverWait(driver, delay, poll_frequency=3).until(EC.element_to_be_clickable((By.ID, "WorkflowButton-4212")))
            cont_butt.click() #new try for finding an appointment
        except:
            print("Timed Out for Waiting of InfoBox")


print("Found Appointment Successfully")
