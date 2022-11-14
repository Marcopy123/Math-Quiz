from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from sympy import *
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

driver = webdriver.Firefox()

url = 'https://moodle.reginaassumpta.qc.ca/mod/quiz/view.php?id=24721'

driver.get(url)

with open('Credentials.txt', 'r') as file:
    credentials = file.readlines()
    username = credentials[0]
    password = credentials[1]


time.sleep(2)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "username").send_keys(username)
time.sleep(2)
driver.find_element(By.ID, 'loginbtn').click()

driver.find_element(
    By.XPATH, "//div[@id='page-content']/div/section/div[2]/div[1]/div[1]/div[1]/form[1]/button[1]").click()

time.sleep(1)
driver.find_element(By.ID, 'id_submitbutton').click()
time.sleep(0.5)

delay = 0.2
listOfEquations = []

for i in range(1, 21):
    time.sleep(delay)
    equation = driver.find_element(
        By.XPATH, f"//form[@id='responseform']/div[1]/div[{i}]/div[2]/div[1]/span[1]/p[1]/span[1]/span[1]/script[1]").get_attribute('innerHTML')
    print("og equation" + equation)
    equation = equation.strip()
    equation = equation.replace('\\xa', '')
    equation = equation.replace('\;000','000')
    # equation = re.sub("\\\\;000", "", equation)
    equation = equation.replace('&nbsp;', '')
    print(equation)
    listOfEquations.append(str(equation))

cleanSolutions = []
n = symbols('n')
for equationOfMath in listOfEquations:
    equationOfMath = equationOfMath.replace("^", "**")
    equationOfMath = equationOfMath.split('=')
    eq1 = sympify(equationOfMath[0])
    eq2 = sympify(equationOfMath[1])
    eqn = Eq(eq1, eq2)
    sol = solve(eqn)
    cleanSolutions.append(sol[0])

print(cleanSolutions)

for i in range(1,21):
    button = driver.find_element(By.XPATH, f"//form[@id='responseform'][1]/div[1]/div[{i}]/div[2]/div[1]/span[1]/p[2]/span[1]/span[2]/input[1]").send_keys(str(cleanSolutions[i-1]))

driver.find_element(By.XPATH, f"//input[@id='mod_quiz-next-nav']").click()
driver.find_element(By.XPATH, f"//section[@id='region-main'][1]/div[2]/div[5]/div[1]/div[1]/form[1]/button[1]").click()

