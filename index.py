import time
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait 
from urllib.parse import urlparse, parse_qs
import undetected_chromedriver as uc
import autoit 
import pyautogui
import pytesseract
from PIL import Image
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import numpy as np
from planilhasleitura import nomeEmpresas, nomeMetodo, strings_sao_parecidas, puxarCnpj
from anticaptchaofficial.hcaptchaproxyless import *
# Configura o serviço do ChromeDriver


# Configurar o resolvedor de hCaptcha

    
empresas = nomeEmpresas()
metodos = nomeMetodo()
pxacnpj = puxarCnpj()

for empresa, metodo, cnpj in zip(empresas, metodos, pxacnpj):
        certificado = empresa
        if metodo == 'Orlando':
            certificado = 'FRANCISCO ORLANDO SILVEIRA PEREIRA'
            
        service = Service(ChromeDriverManager().install())

        # Inicia o navegador
        driver = uc.Chrome(service=service)
        driver.implicitly_wait(10)
        
    
        # Abre uma página da web
        driver.get("https://cav.receita.fazenda.gov.br/autenticacao/login")
        
            
        time.sleep(5)
        autoit.send("{f11}")
        time.sleep(1)
       
        gov = driver.find_element(By.XPATH, '//*[@id="login-dados-certificado"]/p[2]/input')
        driver.execute_script("arguments[0].click();", gov)
        time.sleep(5)
        
        
        certificadoDigital = driver.find_element(By.XPATH, '//*[@id="login-certificate"]')
        driver.execute_script("arguments[0].click();", certificadoDigital)
        #captcha  aqui
        
        print('Captcha')
        time.sleep(5)
        
        
         
        screenshot = pyautogui.screenshot(region=(625, 26, 400, 30))  # Ajuste as coordenadas
        screenshot.save("cert.png")
        textoCert = pytesseract.image_to_string(Image.open("cert.png"))
        print(textoCert)
        
        if textoCert != 'Selecione um certificado\n':
        # Verifique se o iframe do captcha está presente
            captcha_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='hcaptcha']"))
            )

            # Se o iframe for encontrado, resolva o captcha
            if captcha_iframe:
                print("Captcha detectado, iniciando solução...")
                time.sleep(5)
                # Localize o iframe do hCaptcha
                # Localize o iframe do hCaptcha
                script_element = driver.find_element(By.XPATH, '//*[@id="loginData"]/script[2]')
                inner_html = script_element.get_attribute("innerHTML")
                
                # Use uma expressão regular para encontrar a sitekey
                match = re.search(r'sitekey:\s*"([a-zA-Z0-9-]+)"', inner_html)
                if match:
                    site_key = match.group(1)
                    print("Site Key encontrada:", site_key)
                else:
                    print("Site Key não encontrada no script.")
                # Configurar o resolvedor de hCaptcha
                solver = hCaptchaProxyless()
                solver.set_verbose(1)
                solver.set_key("e6151c3f9b60917d81333ea30f5ca6f6")
                solver.set_website_url(driver.current_url)
                solver.set_website_key(site_key)

                # tell API that Hcaptcha is invisible
                #solver.set_is_invisible(1)

                # tell API that Hcaptcha is Enterprise
                #solver.set_is_enterprise(1)

                # set here parameters like rqdata, sentry, apiEndpoint, endpoint, reportapi, assethost, imghost
                #solver.set_enterprise_payload({
                #    "rqdata": "rq data value from target website",
                #    "sentry": True
                #})

                # Specify softId to earn 10% commission with your app.
                # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
                solver.set_soft_id(0)

                g_response = solver.solve_and_return_solution()
                print('G-response:', g_response)
                try:
                    # Localize e mude para o iframe que contém o hCaptcha
                    iframe = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='hcaptcha']"))
                    )
                    driver.switch_to.frame(iframe)

                    # Espere até que o textarea esteja presente e defina seu valor
                    textarea = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="h-captcha-response-0l8o8vyy9am"]'))
                    )
                    print('achouuuuuuu')
                    textarea.send_keys(g_response)

                    # Volte ao contexto padrão da página
                    driver.switch_to.default_content()

                    # Submeta o formulário
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "button-submit"))  # Ajuste o seletor conforme necessário
                    )
                    submit_button.click()

                except Exception as e:
                    print("Erro ao injetar ou submeter a resposta do captcha:", e)
                
                if g_response != 0:
                    print("g-response: "+g_response)
                    print("user-agent, use it to post the form: ", solver.get_user_agent())
                    print("respkey, if any: ", solver.get_respkey())
                else:
                    print("task finished with error "+solver.error_code)
        else:
            print('Sem Captcha')
            
            
        time.sleep(5)
        while True:
            screenshot = pyautogui.screenshot(region=(610, 120, 290, 200))  # Ajuste as coordenadas
            screenshot.save("captura.png")

            # Usa OCR para extrair o texto da imagem
            texto = pytesseract.image_to_string(Image.open("captura.png"))
            time.sleep(2)
            lines = [linha.strip() for linha in texto.split('\n') if linha.strip()]
            print("Texto capturado:", lines)

            
            testeA1 = strings_sao_parecidas(lines[0], certificado)
            testeA2 = strings_sao_parecidas(lines[1], certificado)
            testeA3 = strings_sao_parecidas(lines[2], certificado)
            autoit.send("{DOWN}") 
            
            time.sleep(1)

            screenshot = pyautogui.screenshot(region=(610, 120, 290, 200))  # Ajuste as coordenadas
            screenshot.save("captura.png")
            texto = pytesseract.image_to_string(Image.open("captura.png"))
            
            time.sleep(2)
            
            lines = [linha.strip() for linha in texto.split('\n') if linha.strip()]
            print("Texto capturado:", lines)

            testeB1 = strings_sao_parecidas(lines[0], certificado)
            testeB2 = strings_sao_parecidas(lines[1], certificado)
            testeB3 = strings_sao_parecidas(lines[2], certificado)
            autoit.send("{DOWN}") 
            
            time.sleep(1)
            
            screenshot = pyautogui.screenshot(region=(610, 120, 290, 200))  # Ajuste as coordenadas
            screenshot.save("captura.png")
            texto = pytesseract.image_to_string(Image.open("captura.png"))
            
            time.sleep(2)

            lines = [linha.strip() for linha in texto.split('\n') if linha.strip()]
            print("Texto capturado:", lines)
            testeC1 = strings_sao_parecidas(lines[0], certificado)
            testeC2 = strings_sao_parecidas(lines[1], certificado)
            testeC3 = strings_sao_parecidas(lines[2], certificado)
            
            if(testeA3 == True & testeB2 == True & testeC1 == True):
                autoit.send("{UP}") 
                autoit.send("{UP}") 
                autoit.send("{ENTER}") 

                
                break
            
            elif(testeA1 == True & testeB1 == True & testeC1 == True):
                autoit.send("{UP}") 
                autoit.send("{UP}") 
                autoit.send("{ENTER}") 

                
                break
            
            elif(testeA2 == True & testeB2 == True & testeC2 == True):
                autoit.send("{UP}") 
                autoit.send("{ENTER}") 

                
                break
            
            elif(testeB3 == True & testeC2 == True):
                autoit.send("{UP}") 
                autoit.send("{ENTER}") 

                
                break
            
            elif(testeA3 == True & testeB3 == True & testeC3 == True):
                autoit.send("{ENTER}") 

                
                break
            
            elif(testeA3 == False & testeB3 == False & testeC3 == True):
                autoit.send("{ENTER}") 

                
                break
            
            elif(testeA3 == False & testeB3 == True & testeC3 == True):
                autoit.send("{ENTER}") 

                
                break
            else:
                print('Continua rodando')
                
                
            print(testeA1,testeA2,testeA3)
            print(testeB1,testeB2,testeB3)
            print(testeC1,testeC2,testeC3)
        
            
        
        time.sleep(7)
        
        perfilAltera = driver.find_element(By.XPATH, '//*[@id="btnPerfil"]')
        driver.execute_script("arguments[0].click();", perfilAltera)
        time.sleep(9)
        input_element = driver.find_element(By.ID, "txtNIPapel2")  

        # Limpe qualquer texto existente (opcional)
        input_element.clear()

        # Insira o texto desejado
        texto_desejado = np.int64(cnpj)
        texto_desejadoCVT = str(texto_desejado)

        input_element.send_keys(texto_desejadoCVT)
        
        time.sleep(7)
        submit = driver.find_element(By.XPATH, '//*[@id="formPJ"]/input[4]')
        driver.execute_script("arguments[0].click();", submit)
        
        WebDriverWait(driver, 300).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-widget-overlay')) 
        )
        declaracao = driver.find_element(By.XPATH, '//*[@id="btn214"]/a')
        driver.execute_script("arguments[0].click();", declaracao)
        time.sleep(1)
        
        dctf = driver.find_element(By.XPATH, '//*[@id="containerServicos214"]/div[2]/ul/li[1]/a')
        driver.execute_script("arguments[0].click();", dctf)
        
        time.sleep(2) 
            #captcha  aqui
        print('clica olho')
        olho = driver.find_element(By.XPATH, '//*[@id="ctl00_cphConteudo_tabelaListagemDctf_GridViewDctfs_ctl02_lbkVisualizarDctf"]')
        driver.execute_script("arguments[0].click();", olho)
        
        time.sleep(100)
        driver.quit()
        
       