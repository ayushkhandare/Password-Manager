import string #for ascii letters and digits
import random #for smhfrandom password generation
import base64 #for base64 encoding and decoding
import os #for deleting unrequired files and hiding certain others
import UI #User Interface


def pwd_gen(length, special, digits, toggle):
    pwd= [] #temporary var to store password
    #Entire character set
    chars = "".join(string.ascii_letters) #all aplhabets upper and lower
    if digits: #toggle for digits
        chars = chars.join(string.digits) #add digits to character set
        pwd.append(random.choice(string.digits)) #choose one random digit
    if special: #toggle for special characters
        chars = chars.join("!@#$%^&*?_") #add special characters to character set
        pwd.append(random.choice("!@#$%^&*?_")) #choose one random special character
    pwd.append(random.choice(string.ascii_uppercase)) #picking one lowercase letter
    pwd.append(random.choice(string.ascii_lowercase)) #picking one uppercase letter
    
    #Making random password
    for i in range(length-toggle): #picking the rest of the password
        pwd.append(random.choice(chars))
    #Shuffling password    
    pwd_shuff = "" #temporary var to store scrambled password
    for i in range(length):
        n = random.randint(0,length-i)-1 #randomly pick one index
        pwd_shuff += pwd[n] #add the character at that index
        del(pwd[n]) #delete that index
    return pwd_shuff


def parameters():
    #Exception Handling format 
    while True:
        toggle = 0 #a variable to set characterset
        try:
            #Toggle for special characters
            special, digits, length = UI.parameters_UI() #get requirements for password
            if special: #if user wants special characters
                toggle += 1 #increase types of characters used by 1
            if digits: #if user wants digits
                toggle += 1 #increase types of characters used by 1
            length = int(length) #to check if length is an integer
            if length > 20: #if length is greater than 20
                UI.alert_UI("Length cannot be greater than 20!") 
                continue #restarts loop
            if length <= toggle+2: #is length is less than minimum length to cover all character types
                UI.alert_UI(f"Length should be greater than {toggle+2}!")
                continue #restarts loop
        except ValueError: #if anything other than an integer is input
            UI.alert_UI("Please Enter an Integer value!")
            continue #restarts loop
        break #if everything is correct
    return length, special, digits, toggle


def pwd_maker():
    while True:
        length, special, digits, toggle = parameters() #taking password criteria
        password = pwd_gen(length, special, digits, toggle+2) #generating password
        caption = UI.pwd_maker_UI(password) #get caption and display password
        if type(caption) == str: #if caption is entered
            if caption.find(":") != -1: #if ":" in caption
                UI.alert_UI("':' is an Invalid Input!")
                continue #since ":" can break display as it uses .split(":")
            break #correct caption
    final_password = f"{caption} : {password}" #save format
    final_password = encrypt(final_password) #encryption
    os.system("attrib -h random_passwords.txt")
    with open(f"random_passwords.txt","a") as f:
        f.write(f"{final_password}\n") #storing excrpyted password
    os.system("attrib +h random_passwords.txt")


def pwd_display(): #displaying passwords
    try:
        caption, password = [], [] #temporary lists
        with open("random_passwords.txt","r") as f:
            for line in f.readlines(): #taking single line from file
                line = line.replace("\n","") #to avoid errors
                line = decrypt(line) 
                contents = line.split(":") #split with respect to ":"
                caption.append(contents[0]) #before ":" = username
                password.append(contents[1]) #after ":" = password
        UI.pwd_display_UI(caption, password) #display
    except FileNotFoundError: #if not passwords were created thusfar
        UI.alert_UI("No passwords were created!")


def encrypt(string_sample): #base64 encryprion
    string_bytes = string_sample.encode("ascii") #convert string into its ascii value
    base64_bytes = base64.b64encode(string_bytes) #convert ascii value into base64 binary
    base64_string = base64_bytes.decode("ascii") #convert base64 binary back into encoded ascii
    return base64_string #return encoded base64


def decrypt(base64_string): #base64 decryption
    base64_bytes = base64_string.encode("ascii") #convert encoded ascii into base64 binary
    string_bytes = base64.b64decode(base64_bytes) #convert base64 binary into ascii value
    string_sample = string_bytes.decode("ascii") #convert ascii value into string
    return string_sample #return decoded string


def master():
    try:
        with open("master.txt","r") as f:
            master = [] #temporary list
            for line in f.readlines():
                master.append(decrypt(line)) #adds lines of master.txt in master list
            try:
                username = master[0].replace("\n","") #retrieves username
                master_password = master[1].replace("\n","") #and password
            except IndexError: #incase master file contents were deleted
                os.remove("random_passwords.txt")
                os.remove("master.txt")
                quit() 
            try:
                input_username, input_password = UI.master_UI() #take input credentials
            except NameError: #if user closes window without any inputs
                UI.alert_UI("Have a good day!")
                quit()
            if master_password == input_password and username == input_username: #valid credentials
                return False, username #stop loop
            else: #input password is not the same as master
                UI.alert_UI("Incorrect Credentials!")
                return True, username #reloop

    except FileNotFoundError:
        with open("master.txt","w") as f: #on first boot/ master file was deleted
            username, master_password = UI.master_UI()
            f.write(f"{encrypt(username)}\n") #write username
            f.write(encrypt(master_password)) #write password
            os.system("attrib +h master.txt") #hides master file
            if os.path.exists("random_passwords.txt"): #incase master file was deleted
                os.remove("random_passwords.txt") #passwords will be deleted 
        return False, username #reloop
        

run = True #variable to control while loop
while run:
    run, username = master() #run master until correct credentials are entered

while True: #loop until program is closed

    u = UI.display_UI() #call display 
    if u == 0: #if window was closed without any inputs
        UI.alert_UI("Have a good day!")
        quit()
    if u==1: #create new password
        pwd_maker()
    elif u==2: #display saved passwords
        pwd_display()
    elif u==3: #save and exit
        UI.alert_UI("Have a good day!")
        quit()
