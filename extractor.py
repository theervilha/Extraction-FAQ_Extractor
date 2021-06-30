import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException

driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.get("https://www.bb.com.br/pbb/pagina-inicial/perguntas-frequentes#/")

def acceptCookies():
    while True:
        try:
            driver.find_element_by_css_selector(".btn.btn-azul.botao-ok-avCookies").click()
            break
        except:
            pass

acceptCookies()

data = {}
counter = 1
for i in range(91):
    answersElem = driver.find_elements_by_css_selector('.titulo-pergunta.ng-binding') 
    while answersElem == []:
        answersElem = driver.find_elements_by_css_selector('.titulo-pergunta.ng-binding')     
    responsesElem = driver.find_elements_by_xpath('//p[@ng-bind-html="faq.resposta"]')

    for i, answer in enumerate(answersElem):
        try:
            answer.click()
        except ElementClickInterceptedException:
            windowHeight = driver.execute_script('return document.body.scrollHeight')
            while windowHeight != 0:
                driver.execute_script("scroll(0, 0);")
                counter += 1
                if counter == 50:
                    break
            counter = 1
            answer.click()

        response = responsesElem[i].text
        data[answer.text] = response

    while True:
        try:
            driver.find_element_by_xpath('//span[@ng-click="proximo()"]').click()
            break
        except:
            pass

    driver.execute_script("scroll(0, 0);")

data = {answer: response.lower() for answer, response in data.items() if len(response.split()) <= 500}
dfData = {
    'answers': list(data.keys()),
    'responses': list(data.values()),
}
dfWithAnswers = pd.DataFrame(dfData)
dfWithAnswers.to_csv('bb-with-answers.csv', index=False, encoding='utf-8', sep=';')

dataOnlyAnswers = {
    'index_name': 'bb',
    'items': dfData['responses'],
}
dfOnlyAnswers = pd.DataFrame(dataOnlyAnswers)
dfOnlyAnswers.to_csv('bb-only-answers.csv', index=False, encoding='utf-8', sep=';')