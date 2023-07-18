from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pandas as pd

from credenciales import USER, PASS

import os



driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

##Función para hacer el login en el curso QA
def login():

    driver.get("http://localhost/course/view.php?id=2602")
    driver.maximize_window()

    title = driver.title

    #ingresar los datos de usuario
    driver.find_element(By.ID,"username").send_keys(USER)
    driver.find_element(By.ID,"password").send_keys(PASS)

    #hacer click en el botón acceder
    driver.find_element(By.ID,"loginbtn").click()

#seleccionar el modo de edición si este está desactivado
def editMode():
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="usernavigation"]/li/form/div')))

    if not element.is_selected():
        print(element.text)
        element.click()

#QA de formatos de curso
def formatQA():
    from selenium.webdriver.support.ui import Select
        
    wait = WebDriverWait(driver, 10)
    configbtn = wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@data-key="editsettings" and @title="Configuración"]')))
    configbtn.click()
    formatbtn = wait.until(EC.visibility_of_element_located((By.ID, 'id_courseformathdr')))
    formatbtn.click()
    menuopciones = wait.until(EC.visibility_of_element_located((By.ID, 'id_format')))
    menuopciones.click()
    
    selector = Select(menuopciones)
    opciones = selector.options
    
    df = []

    for opcion in opciones:
        
        df.append(str(opcion.get_attribute('value')))
        
    print(df)
        

    for i in range(0, (len(df))):
        opcion = df[i]
        
        print(opcion)
        
        selector = Select(menuopciones)
        selector.select_by_value(opcion)
        
        displaybtn = wait.until(EC.element_to_be_clickable((By.ID, 'id_saveanddisplay')))
        displaybtn.click()
        
        # screenshooter("formatos_de_curso", opcion)
        
        if(opcion == "singleactivity"):
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="course"]')))
            btn.click()
            
            configbtn = wait.until(EC.element_to_be_clickable((By.XPATH,  '//a[text()="Configuración"]')))
            configbtn.click()

        else:
            
            configbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="editsettings" and @title="Configuración"]')))
            configbtn.click()
        
        formatbtn = wait.until(EC.element_to_be_clickable((By.ID, 'id_courseformathdr')))
        formatbtn.click()
        
        menuopciones = wait.until(EC.element_to_be_clickable((By.ID, 'id_format')))
        # menuopciones.click()
        
        if(i == (len(df)-1)):
            selector = Select(menuopciones)
            selector.select_by_value("topics")
            
            displaybtn = wait.until(EC.element_to_be_clickable((By.ID, 'id_saveanddisplay')))
            displaybtn.click()

   
             
def screenshooter(carpeta,opcion):
    ##Sacar screenshots de las páginas##

    altura_total = driver.execute_script("return document.body.scrollHeight")
    
    print(altura_total)
    
    altura_desplazamiento = 500
    
    posicion_desplazamiento = 0
    
    directorio_capturas = "C:/Users/mrive/Documents/Trabajo/automatización QA/Git/"+carpeta
    
    if not os.path.exists(directorio_capturas):
        # Crear el directorio
        os.makedirs(directorio_capturas)

    
    while posicion_desplazamiento < (altura_total-1000):
        driver.execute_script("window.scrollTo(0, "+str(posicion_desplazamiento)+");")
        posicion_desplazamiento += altura_desplazamiento
        time.sleep(1)
        driver.save_screenshot(directorio_capturas+"/screenshot_"+opcion+str(posicion_desplazamiento)+".png")
        
    driver.execute_script("window.scrollTo(0, 0);")
    
    
# Queda pendiente
def archivo():
    from selenium.webdriver.common.action_chains import ActionChains
    
    editMode()
    
    wait = WebDriverWait(driver, 10)
    
    #click en el botón de añadir una actividad o recurso
    actividades_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-action="open-chooser"]')))
    actividades_btn.click()
    
    #click en el botón de archivos
    archivo_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="resource"]')))
    archivo_btn.click()
    
    #Ingresar el nombre del archivo
    nombre_archivo = "QA archivo"
    driver.find_element(By.ID,"id_name").send_keys(nombre_archivo)
    
    #subir archivo
    
    input_archivo = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]')))
    ruta_archivo = "C:/Users/mrive/Documents/Trabajo/automatización QA/Git/autoQA/Dummy PDF.pdf"
    
    input_archivo.send_keys(ruta_archivo)
    
    # acciones = ActionChains(driver)
    # acciones.drag_and_drop(input_archivo, ruta_archivo)
    # acciones.perform()
    
def area_textos_medios():
    
    btnactividades()
    
    # click en el botón de área de texto
    area_textos_medios_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="label"]')))
    area_textos_medios_btn.click()
    
    input_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_introeditoreditable"]')))
    input_btn.send_keys("QA área de texto")
    
    display_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton2')))
    display_btn.click()
    
    
    
    
def btnactividades():
    editMode()
    actividades_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-action="open-chooser"]')))
    actividades_btn.click()
    
    
    
    
    
# def actividades_recursos():
#     editMode()
    
#     df = []
#     # time.sleep(5)
#     wait = WebDriverWait(driver, 10)
    
#     add = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-action = 'open-chooser']")))
#     add.click()
    
#     actividades = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role = 'menubar']")))
    
#     for actividad in actividades:
#         valor = actividad.get_attribute("arial-label")
#         print(valor)
    

login()
# formatQA()

# queda en pausa
# archivo()

area_textos_medios()


time.sleep(5)
driver.quit()


