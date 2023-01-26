# Importing Useful libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from cryptography.fernet import Fernet
import time
import os
import sys
import pathlib
import traceback
from cryptography.fernet import Fernet
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tktimepicker import AnalogPicker, AnalogThemes, constants
from datetime import date
import xml.etree.ElementTree as ET


'''
schtasks /query /TN autoPunchIn /FO LIST
SCHTASKS /DELETE /TN "autoPunchIn" /F
SCHTASKS /CREATE /TN "autoPunchIn" /TR "F:\Windowcmd\Python\punchin\output\punchin.exe" /SC WEEKLY /D SUN,MON,TUE,WED,THU,FRI /ST 12:24 /HRESULT
'''


        
print("Punch-in Process Started.....")
# with open('logs0.txt', 'w') as file:
#     file.writelines("Punch-in Process Started")

def generateKeys(companyCode,empCode,password,t):
    text = []
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(password.encode())

    text.append(str(key,encoding='utf-8')+"\n")
    text.append(str(encMessage,encoding='utf-8')+"\n")
    text.append(str(fernet.encrypt(empCode.encode()),encoding='utf-8')+"\n")
    text.append(str(fernet.encrypt(companyCode.encode()),encoding='utf-8')+"\n")
    text.append(str(fernet.encrypt(t.encode()),encoding='utf-8'))

    with open('key.txt', 'w') as file:
        file.writelines(text)

    return scheduledTask(t)

def scheduledTask(time):
    today = str(date.today())+"T"+time+":00"

    # parsing directly.
    tree = ET.parse('autoPunchIn.xml')
    root = tree.getroot()
    '''
    root = task

    root[0] = RegistrationInfo
    root[1] = Triggers

    root[0][0] = Date
    root[1][0] = CalendarTrigger

    root[1][0][0] = StartBoundary
    '''
    root[1][0][0].text = today
    tree.write('autoPunchIn.xml') 
    deleteTask = 'SCHTASKS /DELETE /TN "autoPunchIn" /F'
    createTask = 'SCHTASKS /CREATE /XML autoPunchIn.xml /TN "autoPunchIn"'
    #createTask = 'SCHTASKS /CREATE /TN "autoPunchIn" /TR "F:\Windowcmd\Python\punchin\output\punchin.exe" /SC WEEKLY /D SUN,MON,TUE,WED,THU,FRI /ST {}'.format(time)
    os.system(deleteTask)
    return os.system(createTask)

def on_closing():
    window.destroy()



def btn_clicked():
    companyCode = company_code.get()
    empCode = emp_code.get()
    password = password_entry.get()
    # output_path = output_path.strip()

    if not companyCode:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter companyCode.")
        return
    if not empCode:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter empCode.")
        return
    if not password:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Please enter password.")
        return

    t = time_lbl.cget("text")

    if generateKeys(companyCode.strip(),empCode.strip(),password.strip(),t) == 0:
        tk.messagebox.showinfo(
            "Success!", f"autoPunchin successfully registered for time: {t} Everyday.")
    else:
        tk.messagebox.showinfo(
            "Failure!", f"Not enough permissions, Please 'Run as Administrator'.")


def select_path():
    global output_path

    output_path = tk.filedialog.askdirectory()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, output_path)


def know_more_clicked(event):
    instructions = ("https://collegeek.com/")
    webbrowser.open_new_tab(instructions)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label

def core():
    companyCode = company_code.get()
    empCode = emp_code.get()
    password = password_entry.get()
    if not companyCode:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter companyCode.")
        return
    if not empCode:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter empCode.")
        return
    if not password:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Please enter password.")
        return

    before = time.time()
    #chrome_options = Options()
    #chrome_options.add_argument('--headless')
    companyCode = ""
    empCode = ""
    #os.system('cd F:\Windowcmd\Python\punchin')
    #self.scheduledTask(str("18:31"))

    lines = []
    with open('key.txt', 'r') as file:
        lines = file.readlines()
    fernet = Fernet(lines[0])
    password = fernet.decrypt(lines[1]).decode()
    companyCode = fernet.decrypt(lines[3]).decode()
    empCode = fernet.decrypt(lines[2]).decode()


    if os.path.exists('.wdm'):
        with open('.wdm/drivers.json', 'r') as file:
            text = file.read()
            text = text.split('"binary_path": ')[1]
            x = text.rfind('"')
            text = text[:x+1]
            text = pathlib.Path(text).as_posix()
            text = text[3:(len(text)-1)]
            text = os.path.normcase(text)
            driver = webdriver.Chrome(text)
    else:
        driver = webdriver.Chrome(ChromeDriverManager(path='.').install())
    #driver = webdriver.Chrome()
    # print(dir(driver)) # check all methods
    driver.get("https://portal.zinghr.com/2015/pages/authentication/login.aspx")
    # with open('logs1.txt', 'w') as file:
    #     file.writelines("driver getted")
    txtCompanyCode = driver.find_element('id','txtCompanyCode')  # Don't Use find_elements that will return list and turn into error
    txtCompanyCode.clear()
    time.sleep(2)
    txtCompanyCode.send_keys(str(companyCode))
    time.sleep(2)
    
    txtEmpCode = driver.find_element('id','txtEmpCode')
    txtEmpCode.clear()
    time.sleep(2)
    txtEmpCode.send_keys(str(empCode))
    time.sleep(2)
    
    txtPassword = driver.find_element('id','txtPassword')
    txtPassword.clear()
    time.sleep(2)
    txtPassword.send_keys(str(password))
    time.sleep(2)

    driver.find_element('xpath','//*[@id="login-box"]/div/div/div[1]/div[2]/div[7]/button').click()
    time.sleep(4)
    
    driver.delete_all_cookies()
    # Closing driver automatically
    driver.close()
    after = time.time()

    print("Closing Browser............\n")
    # Printing Summary of Program
    print("Browser Closed")
    print("============Summary=============")
    print(f"Total time taken : {((after - before)/60)} Minutes")

    n = len(sys.argv)
    if n>1 and sys.argv[1]=='start':
        exit()

def updateTime(time,top):
    time_lbl.configure(text="{}:{}".format(*time)) # remove 3rd flower bracket in case of 24 hrs time
    top.destroy()

def get_time():

    top = tk.Toplevel(window)
    
    time_picker = AnalogPicker(top, type=constants.HOURS24)
    time_picker.pack(expand=True, fill="both")

    theme = AnalogThemes(time_picker)
    theme.setDracula()
    # theme.setNavyBlue()
    # theme.setPurple()
    ok_btn = tk.Button(top, text="OK",
    font=("Arial-BoldMT", int(9.0)),bd=0, bg="#F6F7F9", fg="#515486", highlightthickness=0, command=lambda: updateTime(time_picker.time(),top))
    ok_btn.pack()

try:  

    # # Add tkdesigner to path
    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    # # Path to asset files for this GUI window.
    # ASSETS_PATH = Path(__file__).resolve().parent / "assets"

    # # Required in order to add data files to Windows executable
    # path = getattr(sys, '_MEIPASS', os.getcwd())
    # os.chdir(path)
    
    password = ""
    companyCode = ""
    empCode = ""
    timer = "10:30"
    try:
        lines = []
        with open('key.txt', 'r') as file:
            lines = file.readlines()
        fernet = Fernet(lines[0])
        password = fernet.decrypt(lines[1]).decode()
        empCode = fernet.decrypt(lines[2]).decode()
        companyCode = fernet.decrypt(lines[3]).decode()
        timer = fernet.decrypt(lines[4]).decode()
    except Exception as e:
        traceback.print_exc()
        pass

    window = tk.Tk()
    logo = tk.PhotoImage(file="assets/app_icon.png")
    window.call('wm', 'iconphoto', window._w, logo)
    window.title("PunchIn")

    window.geometry("862x519")
    window.configure(bg="#3A7FF6")
    canvas = tk.Canvas(
        window, bg="#3A7FF6", height=519, width=862,
        bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
    canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

    text_box_bg = tk.PhotoImage(file="assets/TextBox_Bg.png")
    company_code_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
    emp_code_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
    password_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)
   

    company_code = tk.Entry(bd=0, bg="#F6F7F9",fg="#000716",  highlightthickness=0)
    company_code.insert(0,companyCode)
    company_code.place(x=490.0, y=137+25, width=321.0, height=38)
    company_code.focus()

    emp_code = tk.Entry(bd=0, bg="#F6F7F9", fg="#000716",  highlightthickness=0)
    emp_code.insert(0,empCode)
    emp_code.place(x=490.0, y=218+25, width=321.0, height=38)

    password_entry = tk.Entry(bd=0, bg="#F6F7F9", fg="#000716", highlightthickness=0)
    password_entry.insert(0,password)
    password_entry.config(show="*")
    password_entry.place(x=490.0, y=299+25, width=321.0, height=38)

    path_picker_img = tk.PhotoImage(file="assets/path_picker.png")
    path_picker_button = tk.Button(
        image = path_picker_img,
        text = '',
        compound = 'center',
        fg = 'white',
        borderwidth = 0,
        highlightthickness = 0,
        command = select_path,
        relief = 'flat')

    # path_picker_button.place(x = 783, y = 319,width = 24,height = 22)

    canvas.create_text(
        490.0, 156.0, text="Company Code", fill="#515486",
        font=("Arial-BoldMT", int(8.0)), anchor="w")
    canvas.create_text(
        490.0, 234.5, text="Emp Code", fill="#515486",
        font=("Arial-BoldMT", int(8.0)), anchor="w")
    canvas.create_text(
        490.0, 315.5, text="Password",
        fill="#515486", font=("Arial-BoldMT", int(8.0)), anchor="w")
    canvas.create_text(
        646.5, 428.5, text="PunchIn",
        fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
    canvas.create_text(
        573.5, 88.0, text="Enter the details.",
        fill="#515486", font=("Arial-BoldMT", int(20.0)))

    title = tk.Label(
        text="Welcome to PunchIn", bg="#3A7FF6",
        fg="white", font=("Arial-BoldMT", int(20.0)))
    title.place(x=27.0, y=120.0)

    info_text = tk.Label(
        text="Punchin uses the selenium webdriver\n"
        "to connect with a browser, and schedules\n"
        "task using task scheduler\n"
        "for automation.\n\n"

        "Punchin GUI was created\n"
        "using standard Python interface Tkinter.",
        bg="#3A7FF6", fg="white", justify="left",
        font=("Georgia", int(16.0)))

    info_text.place(x=27.0, y=200.0)

    know_more = tk.Label(
        text="Click here for instructions",
        bg="#3A7FF6", fg="white", cursor="hand2")
    know_more.place(x=27, y=400)
    know_more.bind('<Button-1>', know_more_clicked)

    generate_btn_img = tk.PhotoImage(file="assets/generate.png")
    generate_btn = tk.Button(
        image=generate_btn_img, borderwidth=0, highlightthickness=0,
        command=btn_clicked)
    generate_btn.place(x=557, y=401, width=180, height=55)

    run_btn_img = tk.PhotoImage(file="assets/start40.png")
    run_btn = tk.Button(
        image=run_btn_img, borderwidth=0, highlightthickness=0,
        command=core, relief="flat")
    run_btn.place(x=783.5, y=70.0, width=30, height=30)

    time_lbl = tk.Label(window, font=("Arial-BoldMT", int(8.0)),
    text=timer,bd=0, bg="#F6F7F9", fg="#515486", highlightthickness=0)
    time_lbl.place(x=733.5, y=70.0, width=50.0, height=28)

    time_btn = tk.Button(window,text="Set Time",
    font=("Arial-BoldMT", int(9.0)),bd=0, bg="#F6F7F9", fg="#3A7FF6", highlightthickness=0, command=get_time)
    time_btn.place(x=683.5, y=70.0, width=50.0, height=28)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(False, False)
    # Arguments passed
    n = len(sys.argv)
    if n>1 and sys.argv[1]=='start':
        core()
    else:
        window.mainloop()

    

except Exception as e:
    traceback.print_exc()
    time.sleep(1)
    