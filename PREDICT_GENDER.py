"""
Created on Wed Oct  3 8:30:43 2018

@author: DANIEL ABAI
"""
#Extract male and female friends of diﬀerent Facebook users and build a table to hold them for data analysis. 
#Build a classiﬁcation model that will tell the gender of a Facebook user given the amount of male and female friends he has

from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import seaborn as sn

def names_scraper(email, password, user_id, User_name):
    chrome = webdriver.Chrome(r"C:\Users\PASTOR DAN\Documents\DAN THE GURU\PYTHONPROJECTS\chromedriver")
    chrome.get("http://facebook.com")
    chrome.find_element_by_id("email").send_keys(str(email))
    chrome.find_element_by_id("pass").send_keys(str(password))
    chrome.find_element_by_id("pass").send_keys(Keys.ENTER)
    # Get login cookies
    cookie = chrome.get_cookies()
    for i in cookie:
        chrome.add_cookie(i)
    chrome.get("https://web.facebook.com/search/"+str(user_id)+"/friends/intersect/males/intersect?_rdc=1&_rdr")
    # Get scroll height
    last_height = chrome.execute_script("return document.body.scrollHeight")
    M = []
    while True:
        # Scroll down to bottom
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load
        sleep(15)
        # Calculate new scroll height and compare with last scroll height
        new_height = chrome.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    male = chrome.find_elements_by_class_name("_32mo")
    # Exracting male names
    for i in male:
        name = i.text
        data = {"male_name": name}
        M.append(data)
    male_n = {"male": M}
    
    # List of female friends search
    chrome.get("https://web.facebook.com/search/"+str(user_id)+"/friends/intersect/females/intersect?_rdc=1&_rdr")
    # Get scroll height
    last_height = chrome.execute_script("return document.body.scrollHeight")
    F = []
    while True:
        # Scroll down to bottom
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load
        sleep(15)
        # Calculate new scroll height and compare with last scroll height
        new_height = chrome.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    female = chrome.find_elements_by_class_name("_32mo")
    # Exracting female names
    for i in female:
        name = i.text
        data = {"female_name": name}
        F.append(data)
    female_n = {"female": F}
    
    # Writing to file
    User = {str(User_name): [male_n, female_n]}
    user = json.dumps(user, indent=2)
    with open(str(User_name)+".json", "w") as f:
        f.write(user)

# Loading All The Extracted Files
with open(r"C:\Users\PASTOR DAN\Documents\DAN THE GURU\PYTHONPROJECTS\Abai.json", "r") as f:
    Abai = json.load(f)
with open(r"C:\Users\PASTOR DAN\Documents\DAN THE GURU\PYTHONPROJECTS\daniel.json", "r") as f:
    Daniel = json.load(f)
    

def build_class():
    dataset = {"User_name": ["Daniel","Abai","Esther","Joy","Goke","Tomi","Titi","Kemi","Ade","Julius"],
               "Male":[len(Daniel["Daniel"][0]["male"]), len(Abai["Abai"][0]["male"]), 2000, 1500, 2000,1500,500,1523,3520,789],
               "Female": [len(Daniel["Daniel"][1]["female"]),len(Abai["Abai"][1]["female"]),3000,3500,1000,4200,3230,2430,1500,200],
               "Gender":["M","M","F","F","M","F","F","F","M","M"]}
    dataset = pd.DataFrame.from_dict(dataset)
    
    # Using seaborn to Visualise the gender distribution
    sn.countplot(x="User_name", hue="Gender", data=dataset)
    
    # Getting Dummies for gender in dataset
    gender = pd.get_dummies(dataset["Gender"], drop_first=True)
    dataset= pd.concat([dataset, gender], axis=1)
    
    # removing Gender from dataset
    dataset.drop("Gender", axis=1, inplace=True)
    
    # Spliting data into sets
    x = dataset.drop(["User_name","M"], axis=1)
    y = dataset["M"]
    
    # spliting data into training sets and testing sets
    from sklearn.model_selection import train_test_split
    x_train, x_test,y_train,y_test = train_test_split(x,y, test_size=0.2, random_state=101)
    
#    # training with logistic regression
#    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
   # clf = LogisticRegression(random_state = 0)
    clf.fit(x_train, y_train)
    
    # predicting y_test
    y_pred = clf.predict(x_test)
    
    # Checking prediction accuracy
    from sklearn.metrics import classification_report
    print(classification_report(y_test, y_pred))
    
    print(clf.score(x,y))
    
    # predicting gender based on two values; munbers of male and female friends
    print(clf.predict([[521, 101121]]))
     
    
    
    



