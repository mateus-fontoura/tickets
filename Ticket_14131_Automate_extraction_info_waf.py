import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configurar o driver do Chrome com o caminho correto do chromedriver
#chrome_driver_path = "C:\\Users\\Mateus\\Documents\\GitHub\\azion\\Tickets\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Acessar a home
driver.get("https://manager.azion.com")

try:
    # Esperar até que o campo de e-mail seja visível
    email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="e-mail:"]')))
    email_input.send_keys("seu.login@domain.com")

    # Clicar em "proceed"
    proceed_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="button-proceed"]')))
    proceed_button.click()

    # Esperar até que o campo de senha seja visível
    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    password_input.send_keys("SUAsenha_AQUI_123")

    # Clicar em "Sign In"
    sign_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="button-sign in"]')))
    sign_in_button.click()

    # Aguardar 2 segundos
    time.sleep(2)

    # Acessar a página específica
    # MODIFICAR AQUI PARA UMA URL Válida ( acessar o allowed rules que deseja e copiar)
    driver.get("https://manager.azion.com/account/XXX/waf/XXX/allowed_rules/?active_tab=allowed_rules")

    # Encontrar todos os elementos input dentro do XPath específico
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div/div[2]/form/div/table/tbody/input')))

    # Dentro do loop de extração dos IDs
    ids_list = []  # Lista vazia para armazenar os IDs
    for input_element in input_elements:
        value = input_element.get_attribute("value")
        ids_list.append(value)

    # Agora você tem todos os IDs armazenados na lista "ids_list"
    print(ids_list)

    # Loop para acessar as URLs com base nos IDs e extrair o conteúdo
    for id_number in ids_list:
        url = f"https://manager.azion.com/account/494/waf/1836/allowed_rules/{id_number}/edit/"
        driver.get(url)

        # Aguardar 2 segundos (opcional, se necessário esperar pela página carregar completamente)
        time.sleep(2)

        # Extrair o conteúdo da página
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')

        # Encontrar todos os elementos input, label e div dentro da página
        form_elements = soup.find_all(['input', 'label', 'div'])

        # Loop para acessar as informações dos campos do formulário
        for element in form_elements:
            if element.name == 'input':
                field_name = element.get('name')
                field_value = element.get('value')
                if field_name in ["Rule ID", "path", "description", "Match Zone", "application_name"]:
                    print(f"Name: {field_name}, Value: {field_value}")
                    print("--------------------------------------------------------")
            elif element.name == 'label':
                field_name = element.get_text(strip=True)
                if field_name in ["Rule ID", "path", "description", "Match Zone", "application_name"]:
                    field_value = element.find_next_sibling('div').get_text(strip=True)
                    print(f"Name: {field_name}, Value: {field_value}")
                    print("--------------------------------------------------------")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    # Fechar o navegador após a extração
    driver.quit()
