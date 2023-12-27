from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pandas as pd

from credenciales import USER2, PASS2

import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Información global

directorio = "C:/Users/mrive/Documents/Trabajo/automatización QA/Git/"

preguntas = list([["Animales Nacionales", "¿Qué animal es el símbolo nacional de Chile?", "Cóndor", "Puma", "Huemul", "Flamenco", 2],
                        ["Mayor Población", "¿Qué país tiene la mayor población del mundo?", "India", "EE.UU", "China", "Brasil", 2],
                        ["Instrumentos", "¿Qué instrumento musical tiene teclas blancas y negras?", "Violín", "Guitarra", "Piano", "Flauta", 2],
                        ["Planetas", "¿Qué planeta es el cuarto más cercano al sol?", "Mercurio", "Saturno", "Tierra", "Marte", 3],
                        ["Animales", "¿Qué animal tiene alas, plumas y puede volar?", "Elefante", "Pato", "Jirafa", 1],
                        ["Continentes", "¿Qué continente tiene el mayor número de países?", "Asia", "Africa", "Europa", 1],
                        ["Planetas 2", "¿Qué planeta es el más pequeño del sistema solar?", "Tierra", "Marte", "Mercurio", 2]])

##Función para hacer el login en el curso QA
def login():

    driver.get("https://moodlecloud.uai.cl/course/view.php?id=10606")
    driver.maximize_window()

    title = driver.title
    print(title)

    # Ingreso a moodlecloud
    accesbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Microsoft"]'))).click()

    # #ingresar los datos de usuario
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]'))).send_keys(USER2)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//input[@type="submit"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))).send_keys(PASS2)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//input[@type="submit"]'))).click()
    
    time.sleep(20)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))).click()
    
    # driver.find_element(By.ID,"password").send_keys(PASS)
    # driver.find_element(By.ID,"password").send_keys(PASS)

    #hacer click en el botón acceder
    # driver.find_element(By.ID,"loginbtn").click()

#seleccionar el modo de edición si este está desactivado
def editMode():
    time.sleep(1)
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="usernavigation"]/li/form/div')))
    
    element_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))
    
    if 'text-primary' in element_2.get_attribute('class'):
        print("Modo de edición activado, no es necesario activarlo")
    else: 
        print("Modo de edición desactivado, activando...")
        element.click()
    
    driver.refresh()

# Para algunas actividades necesitamos desactivar el modo de edición
def editModeOff():
    time.sleep(1)
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="usernavigation"]/li/form/div')))
    
    element_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))
    
    if 'text-primary' in element_2.get_attribute('class'):
        print("Modo de edición activado, desactivando...")
        element.click()
    else: 
        print("Modo de edición desactivado, no es necesario desactivarlo")
    
    driver.refresh()   

#QA de formatos de curso
def formatQA():
    from selenium.webdriver.support.ui import Select
    time.sleep(2)
        
    wait = WebDriverWait(driver, 10)
    configbtn = wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@role="menubar"]/li[@data-key="editsettings"]')))
    configbtn.click()
    formatbtn = wait.until(EC.visibility_of_element_located((By.ID, 'id_courseformathdr')))
    formatbtn.click()
    driver.execute_script("window.scrollTo(0, "+str(250)+");")
    time.sleep(1)
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
        
        screenshooter("formatos_de_curso", opcion)
        
        if(opcion == "singleactivity"):
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="course"]')))
            btn.click()
            
            configbtn = wait.until(EC.element_to_be_clickable((By.XPATH,  '//div[@class="dropdown-menu show"]/a[1]')))
            configbtn.click()

        else:
            
            configbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[@role="menubar"]/li[@data-key="editsettings"]')))
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
    
    back_to_curso()

# QA de archivo
def archivo(directorio):
    # directorio_archivo = directorio+"/autoQA/Dummy PDF.pdf"
    
    wait = WebDriverWait(driver, 10)
    
    btnactividades("resource")
    
    #Ingresar el nombre del archivo
    nombre_archivo = "QA archivo"
    driver.find_element(By.ID,"id_name").send_keys(nombre_archivo)
    
    driver.execute_script("window.scrollTo(0, "+str(250)+");")
    
    time.sleep(1)
    
    #subir archivo desde el filepicker
    
    agregar_archivo = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()
    
    input_archivo = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio+"/autoQA/Dummy PDF.pdf")
    
    uploadfile = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    screenshooter("archivo", "Archivo_subido")
    
    chaoactividad(nombre_archivo)
    
# QA de area de textos y medios
def area_textos_medios():
    
    btnactividades("label")
    
    input_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_introeditoreditable"]')))
    input_btn.send_keys("QA área de texto")
    
    display_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton2')))
    display_btn.click()
    
    # screenshooter("area_textos_medios", "Area_de_textos_y_medios")
    
    chaoactividad("QA área de texto")
    
# QA de autoselección de grupos
def autoseleccion_grupos():
    
    btnactividades("groupselect")
    
    #ingresar el nombre de la actividad
    titulo_actividad = "QA autoselección"
    input_nombre = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre.send_keys(titulo_actividad)
    
    #guardar y mostrar
    
    display_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    display_btn.click()
    
    editModeOff()
    
    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos")
    
    administrar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="main"]/div[2]')))
    administrar_btn.click()
    
    # Crear grupos automáticamente
    creacion_grupos_btn = wait.until(EC.element_to_be_clickable((By.ID, 'showautocreategroupsform')))
    creacion_grupos_btn.click()
    
    input_esquema = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_namingscheme"]')))
    
    if input_esquema.get_attribute('value'):
        # Borrar el valor predefinido
        input_esquema.clear()   
    
    input_esquema.send_keys("Grupo #")
    
    input_cantidad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_number"]')))
    input_cantidad.send_keys("2")
    
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos2")
    
    back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="coursehome"]')))
    back_btn.click()
    
    actividad_btn = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, str(titulo_actividad))))
    actividad_btn.click()
    
    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos3")
    
    chaoactividad(titulo_actividad)
    
# QA de base de datos
def base_de_datos():
    
    btnactividades("data")
    
    nombre_actividad = "QA base de datos"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    display_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    display_btn.click()
    
    creacion_btn = wait.until(EC.element_to_be_clickable((By.ID, 'action-menu-toggle-2')))
    creacion_btn.click()
    
    opcion_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-labelledby="actionmenuaction-15"]')))
    opcion_btn.click()
    
    nombre_campo = "QA campo"
    desc_campo = "QA descripción"
    input_nombre_campo = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="name"]')))
    input_nombre_campo.send_keys(nombre_campo)
    input_desc_campo = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="description"]')))
    input_desc_campo.send_keys(desc_campo)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-primary" and @type = "submit"]')))
    submit_btn.click()
    
    screenshooter("base_de_datos", "campo")
    
    plantillas = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id = "sticky-footer"]/div/a')))
    plantillas.click()
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-primary" and @type = "submit"]')))
    submit_btn.click()
    
    screenshooter("base_de_datos", "plantilla")
    
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="modulepage"]')))
    btn.click()
    
    add_entrada = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type = "submit" and @class = "btn btn-primary"]')))
    add_entrada.click()
    
    nombre_registro = "QA registro"
    input_registro = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name[starts-with(., "field_")]]')))
    input_registro.send_keys(nombre_registro)
    
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="saveandview" and @type = "submit"]')))
    save_btn.click()
    
    screenshooter("base_de_datos", "registro")
    
    chaoactividad(nombre_actividad)
 
# QA de carpeta   
def carpeta():
    
    btnactividades("folder")
    
    nombre_actividad = "QA carpeta"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    agregar_archivo = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()
    
    input_archivo = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio+"/autoQA/Dummy PDF.pdf")
    
    uploadfile = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    editModeOff()
    
    screenshooter("carpeta", "carpeta")
    
    chaoactividad(nombre_actividad)
    
# QA de certificado
def certificado():
    
    btnactividades("customcert")
    
    nombre_actividad = "QA certificado"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    editModeOff()
    
    screenshooter("certificado", "certificado")
    
    chaoactividad(nombre_actividad)
      
# QA de chat
def chat():
    
    btnactividades("chat")
    
    nombre_actividad = "QA chat"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    editModeOff()
    
    screenshooter("chat", "chat")
    
    entrar_chat = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-primary"]')))
    entrar_chat.click()
    
    #cambiar de ventana
    ventana_original = driver.current_window_handle
    ventanas_abiertas = driver.window_handles
    nueva_ventana = None
    for ventana in ventanas_abiertas:
        if ventana != ventana_original:
            nueva_ventana = ventana
            break
    driver.switch_to.window(nueva_ventana)
    
    # Escribimos en el chat
    texto = "Mensaje de prueba"
    input_texto = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="text"]')))
    input_texto.send_keys(texto)
    
    send_texto = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="button"]')))
    send_texto.click()
    
    time.sleep(1)
    
    screenshooter("chat", "chat2")
    
    #Cerramos ventana de chat
    driver.close()
    driver.switch_to.window(ventana_original)
    chaoactividad(nombre_actividad)
    
    print("ya estamos en la nueva ventana")
   
# QA de consulta
def consulta():
    
    btnactividades("choice")
    
    nombre_actividad = "QA consulta"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    opcion_1 = "Esta es la opción 1"
    input_opcion_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_option_0"]')))
    input_opcion_1.send_keys(opcion_1)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    try:
        matricular_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit" and @class="btn btn-secondary"]')))
        print("Tienes que matricularte")
        matricular_btn.click()
        
        # Parte que podría llegar a cambiar
        matricular_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
        matricular_btn.click()
        
        driver.refresh()
        
        editModeOff()
        
        screenshooter("consulta", "consulta")

    except :
        print("Ya estás matriculado")
        
        editModeOff()
        
        screenshooter("consulta", "consulta")
        
    chaoactividad(nombre_actividad)
    
# QA cuestionario
def cuestionario():
    from selenium.webdriver.support.ui import Select
    
    btnactividades("quiz")
    
    nombre_actividad = "QA cuestionario"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    
    if input_actividad.get_attribute('value'):
        # Borrar el valor predefinido
        input_esquema.clear()  
    
    input_actividad.send_keys(nombre_actividad)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-secondary"]')))
    agregar_pregunta.click()
    
    # Click en el dropdown Agregar
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "dropdown"]/a[starts-with(@id,"action-menu") and @role = "button"]')))
    agregar_pregunta.click()
    
    #Agregamos una pregunta 
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-action="addquestion"]')))
    agregar_pregunta.click()
    
    #Agregamos una pregunta de opción múltiple
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//fieldset/div[1]/label')))
    agregar_pregunta.click()
    
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()
    
    nombre_pregunta = "QA pregunta 1"
    enunciado_pregunta = "Enunciado de la pregunta 1"
    # Ingresamos el nombre de la pregunta
    input_nombre_pregunta_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="name"]')))
    input_nombre_pregunta_1.send_keys(nombre_pregunta)
    # Ingresamos el enunciado de la pregunta
    input_enunciado_pregunta_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_questiontexteditable"]')))
    input_enunciado_pregunta_1.send_keys(enunciado_pregunta)
    
    # Respuestas que queremos agregar
    texto_opcion_1 = "Opción 1"
    input_opcion_1 = wait.until(EC.element_to_be_clickable((By.ID, 'id_answer_0editable')))
    input_opcion_1.send_keys(texto_opcion_1)
    
    # Calificacion de la pregunta (100%)
    
    selector = Select(wait.until(EC.element_to_be_clickable((By.ID, 'id_fraction_0'))))
    selector.select_by_value("1.0")
    
    texto_opcion_2 = "Opción 2"
    input_opcion_2 = wait.until(EC.element_to_be_clickable((By.ID, 'id_answer_1editable')))
    input_opcion_2.send_keys(texto_opcion_2)
    
    selector = Select(wait.until(EC.element_to_be_clickable((By.ID, 'id_fraction_1'))))
    selector.select_by_value("1.0")
    
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()
    
    ## Agregamos una segunda pregunta de verdadero o falso ##
    # Hacemos click en el dropdown Agregar
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "dropdown"]/a[starts-with(@id,"action-menu") and @role = "button"]')))
    agregar_pregunta.click()
    
    #Agregamos una pregunta 
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-action="addquestion"]')))
    agregar_pregunta.click()
    
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//fieldset/div[2]/label')))
    agregar_pregunta.click()
    
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()
    
    nombre_pregunta = "QA pregunta 2"
    enunciado_pregunta = "Enunciado de la pregunta 2, verdadero o falso"
    # Ingresamos el nombre de la pregunta
    input_nombre_pregunta_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="name"]')))
    input_nombre_pregunta_2.send_keys(nombre_pregunta)
    # Ingresamos el enunciado de la pregunta
    input_enunciado_pregunta_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_questiontexteditable"]')))
    input_enunciado_pregunta_2.send_keys(enunciado_pregunta)
    
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()
    
    ## Vista del cuestionario ##
    # Click en cuestionario
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="modulepage"]')))
    btn.click()
    
    # Click en vista previa del cuestionario
    vista = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type = "submit" and @class="btn btn-primary"]')))
    vista.click()
    
    # Resolvemos el cuestionario
    
    respuesta = wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()= "'+texto_opcion_1+'"]')))
    respuesta.click()
    
    respuesta = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()= "Falso"]')))
    respuesta.click()
    
    screenshooter("cuestionario", "cuestionario")
    
    # Terminar intento
    end_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type = "submit" and @name = "next"]')))
    end_btn.click()
    
    screenshooter("cuestionario", "cuestionario_finalizado")
    
    end_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type = "submit" and @class = "btn btn-primary"]')))
    end_btn.click()
    
    end_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type = "button" and @class = "btn btn-primary"]')))
    end_btn.click()
    
    screenshooter("cuestionario", "revisión")
    
    chaoactividad(nombre_actividad)
    
# QA de cuestionario offline
def cuestionarioofline():
    
    btnactividades("offlinequiz")
    
    nombre_actividad = "QA cuestionario offline"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    # Guardar cambios y mostrar
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    screenshooter("cuestionarioofline", "cuestionarioofline")
    
    chaoactividad(nombre_actividad)
    
# QA de encuesta
def encuesta():
    from selenium.webdriver.support.ui import Select
    
    btnactividades("feedback")
    
    nombre_actividad = "QA encuesta"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    # Guardar cambios y mostrar
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    # Editar preguntas
    
    edit_btn = driver.find_elements(By.XPATH, '//a[@class="btn btn-secondary"]')
    edit_btn[0].click()
    
    # Se selecciona una encuesta de selección múltiple
    selector = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//select[contains(@id, "single_select") ]'))))
    selector.select_by_value("multichoice")
    
    # Nombre de la pregunta 
    nombre_pregunta = "Pregunta 1"
    input_pregunta = wait.until(EC.element_to_be_clickable((By.ID, 'id_name')))
    input_pregunta.send_keys(nombre_pregunta)
    
    # Valores de la elección múltiple
    valores = str("Pregunta 1 \nPregunta 2 \nPregunta 3")
    input_valores = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-fieldtype = "textarea"]/textarea[@id = "id_values"]')))
    input_valores.send_keys(valores)
    
    # Guardar cambios
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_save_item')))
    send_btn.click()
    
    ## Camino a responder la encuesta ##
    # Click en Encuesta
    encuesta_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="modulepage"]')))
    encuesta_btn.click()
    
    screenshooter("encuesta", "vista previa")
    
    # Responder las preguntas
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "navitem"]/a[@class = "btn btn-primary"]')))
    btn.click()
    
    screenshooter("encuesta", "encuesta")
    
    # Enviar la respuesta
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type = "submit" and @id = "id_savevalues"]')))
    send_btn.click()
    
    # Encuesta respondida
    
    screenshooter("encuesta", "encuesta_respondida")
    
    chaoactividad(nombre_actividad)
   
# QA de encuesta questionnaire 
def encuesta2():
    
    btnactividades("questionnaire")
    
    nombre_actividad = "QA encuesta (questionnaire)"
    # Ingresamos el nombre de la actividad
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardar cambios y mostrar
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    ## Añadimos preguntas ## 
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-primary"]')))
    btn.click()
    
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name = "addqbutton"]')))
    btn.click()
    
    # Nombre de la pregunta
    nombre_pregunta = "Pregunta 1"
    texto_pregunta = "Texto de la pregunta 1"
    respuestas_posibles = "Respuesta 1 \nRespuesta 2 \nRespuesta 3"
    # Ingresamos el nombre de la pregunta
    input_nombre_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_pregunta.send_keys(nombre_pregunta)
    # Ingresamos el texto de la pregunta
    input_texto_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_contenteditable"]')))
    input_texto_pregunta.send_keys(texto_pregunta)
    # Ingresamos las respuestas posibles
    input_respuestas_posibles = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id="id_allchoices"]')))
    input_respuestas_posibles.send_keys(respuestas_posibles)
    
    # Guardamos cambios
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name = "submitbutton"]')))
    send_btn.click()
    
    ## Camino a responder la encuesta ##
    # Click en Encuesta
    encuesta_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-key="modulepage"]')))
    encuesta_btn.click()
    
    screenshooter("questionnaire", "vista previa")
    
    # Click en responda las preguntas
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "complete"]/a[@class = "btn btn-primary"]')))
    btn.click()
    
    screenshooter("questionnaire", "encuesta")
    
    # Enviamos la encuesta
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type = "submit" and contains(@class, "btn-primary")]')))
    send_btn.click()
    
    screenshooter("questionnaire", "encuesta_respondida")
    
    
    # Click en continuar para ver los resultados
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type = "submit" and @class= "btn btn-secondary"]')))
    send_btn.click()
    
    screenshooter("questionnaire", "resultados")
    
    chaoactividad(nombre_actividad)
    
# QA de encuesta predefinida
def encuestapredefinida():
    from selenium.webdriver.support.ui import Select
    
    btnactividades("survey")
    
    nombre_actividad = "QA encuesta predefinida"
    # Ingresamos el nombre de la actividad
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    selector = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="id_template"]'))))
    selector.select_by_index(1)
    
    # Guardar cambios y mostrar
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    screenshooter("encuestapredefinida", "encuestapredefinida")
    chaoactividad(nombre_actividad)
    
# QA de glosario 
def glosario():
    
    btnactividades("glossary")
    
    # Ingresamos nombre de la actividad
    nombre_actividad = "QA glosario"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    # Ingresamos una nueva entrada al glosario
    add_entrada = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary"]')))
    add_entrada.click()
    
    # Concepto
    concepto = "Adormecer"
    definicion = "Hacer que alguien o algo se duerma o se quede dormido."
    
    # Ingresamos las variables
    input_concepto = wait.until(EC.element_to_be_clickable((By.ID, 'id_concept')))
    input_concepto.send_keys(concepto)
    
    input_definicion = wait.until(EC.element_to_be_clickable((By.ID, 'id_definition_editoreditable')))
    input_definicion.send_keys(definicion)
    
    # Enviamos la entrada
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    screenshooter("glosario", "glosario")
    
    chaoactividad(nombre_actividad)
    
# QA de H5P (Suerte en esto)
def h5p():
    
    btnactividades("h5pactivity")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA H5P"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Vamos al filepicker y subimos el archivo
    agregar_archivo = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()
    
    # Mandamos el archivo h5p
    input_archivo = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio+"/autoQA/H5P.h5p")
    
    uploadfile = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    screenshooter("h5p", "h5p")
    
    chaoactividad(nombre_actividad)
   
# QA de herramient externa 
def herramienta_externa():
    
    btnactividades("lti")
    
    # Nombre de la actividad
    nombre_actividad = "QA herramienta externa"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Ingresamos la url de herramienta externa
    url = "https://intranet.uai.cl/Login.aspx"
    input_url = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_toolurl"]')))
    
    if input_url.get_attribute('value'):
        # Borrar el valor predefinido
        input_esquema.clear()  
        
    input_url.send_keys(url)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("herramienta_externa", "herramienta_externa")
    
    chaoactividad(nombre_actividad)
    
# QA de laboratorio
def laboratorio():
    
    btnactividades("vpl")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA laboratorio"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("laboratorio", "laboratorio")
    
    chaoactividad(nombre_actividad)
      
# QA de lección
def leccion():
    
    btnactividades("lesson")
    
    # Ingresamos el nombre de la actividada
    nombre_actividad = "QA lección"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("leccion", "leccion")
    
    chaoactividad(nombre_actividad)
    
# QA de libro
def libro():
    
    btnactividades("book")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA libro"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    # Añadimos un capítulo
    nombre_capitulo = "Capítulo 1"
    input_nombre_capitulo = wait.until(EC.element_to_be_clickable((By.ID, 'id_title')))
    input_nombre_capitulo.send_keys(nombre_capitulo)
    
    # Añadimos el contenido
    contenido = "Contenido del capítulo 1"
    input_contenido = wait.until(EC.element_to_be_clickable((By.ID, 'id_content_editoreditable')))
    input_contenido.send_keys(contenido)
    
    # Guardamos cambios
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("libro", "libro")
    
    chaoactividad(nombre_actividad)
    
# QA de página
def pagina():
    
    btnactividades("page")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA página"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Ingresamos el contenido de la página
    contenido = "Este es el contenido de la página"
    input_contenido = wait.until(EC.element_to_be_clickable((By.ID, 'id_pageeditable')))
    input_contenido.send_keys(contenido)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("pagina", "pagina")
    
    chaoactividad(nombre_actividad)
    
# QA de paquete SCORM
def scorm():
    
    btnactividades("scorm")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA scorm"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Ingresamos el paquete scorm
    
    agregar_archivo = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()
    
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type = "file"]')))
    add_btn.send_keys(directorio+"/autoQA/scorm.zip")
    
    # Subimos el archivo
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    send_btn.click()
    
    # Guardamos cambios y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    # Entramos a ver la actividad scorm
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[starts-with(@class, "btn btn-primary") and @type = "submit"]')))
    btn.click()
    
    editModeOff()

    screenshooter("scorm", "scorm")
    
    chaoactividad(nombre_actividad)
    
# QA de póster
def poster():
    from selenium.webdriver.support.ui import Select
    
    btnactividades("poster")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA poster"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    # Abrimos la selección y escogemos la opción texto    
    selector = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//select[starts-with(@id, "single_select")]'))))
    selector.select_by_value("recent_activity")
    
    editModeOff()
    
    screenshooter("poster", "poster")
    
    chaoactividad(nombre_actividad)
   
# QA de taller
def taller():
    
    btnactividades("workshop")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA taller"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("taller", "taller")
    
    chaoactividad(nombre_actividad)
       
# QA de tarea
def tarea():
    
    btnactividades("assign")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA tarea"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("tarea", "tarea")
    
    chaoactividad(nombre_actividad)
       
# QA de wiki
def wiki():
    
    btnactividades("wiki")
    
    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA wiki"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys("QA wiki")
    
    # Ingresamos el nombre de la primera página
    nombre_pagina = "Página 1"  
    input_nombre_pagina = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_firstpagetitle"]')))
    input_nombre_pagina.send_keys(nombre_pagina)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    # Creamos página con el formato por defecto
    btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    btn.click()
    
    # Ingresamos el texto 
    texto = "<p>final</p>"
    input_texto = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_newcontent_editoreditable"]')))
    input_texto.send_keys(texto)
    
    # Guardamos 
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'save')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("wiki", "wiki")
    
    chaoactividad(nombre_actividad)
    
# QA de url
def url():
    
    btnactividades("url")
    
    # Ingresamos el nombre de la actividad y la url externa
    nombre_actividad = "QA url"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    url = "https://intranet.uai.cl/"
    input_url = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_externalurl"]')))
    input_url.send_keys(url)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("url", "url")
    
    chaoactividad(nombre_actividad)

# QA de urluai
def urluai():
    from selenium.webdriver.support.ui import Select
    
    btnactividades("urluai")
    
    # Ingresamos el nombre de la actividad y la url externa
    nombre_actividad = "QA urluai"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    url = "https://intranet.uai.cl/"
    input_url = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_externalurl"]')))
    input_url.send_keys(url)
    
    # Ponemos algunas variables en la URL
    btn = wait.until(EC.element_to_be_clickable((By.ID, "id_parameterssection" )))
    btn.click()
    
    # Primer parámetro
    parametro = "Juan Carlos"
    input_parametro = wait.until(EC.element_to_be_clickable((By.ID, 'id_parameter_0')))
    input_parametro.send_keys(parametro)
    
    # Escojemos que tipo de variable sea
    selector = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="id_variable_0"]'))))
    selector.select_by_value("urlname")
    
    time.sleep(1)
    
    # Segundo parámetro
    parametro = "Español"
    input_parametro = wait.until(EC.element_to_be_clickable((By.ID, 'id_parameter_1')))
    input_parametro.send_keys(parametro)
    
    # Escojemos que tipo de variable sea
    selector = Select(wait.until(EC.element_to_be_clickable((By.ID, 'id_variable_1'))))
    selector.select_by_value("lang")
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("urluai", "urluai")
    
    chaoactividad(nombre_actividad)
    
# QA de página de contenido
def pagina_contenido():
    btnactividades("icontent")
    
    # Ingresamos el nombre de la actividad y la url externa
    nombre_actividad = "QA página de contenido"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)
    
    #Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()	
    
    # Ingresamos el título de la página
    titulo = "Página 1"
    input_titulo = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_title"]')))
    input_titulo.send_keys(titulo)
    # Ingresamos el contenido de la página
    contenido = "Contenido de la página"
    input_contenido = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_pageicontent_editoreditable"]')))
    input_contenido.send_keys(contenido)
    # Guardamos cambios
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    
    editModeOff()
    
    screenshooter("pagina_contenido", "pagina_contenido")
    
    chaoactividad(nombre_actividad)
    
# Creación de preguntas para realizar los juegos
def inicio_juegos(preguntas):
    from selenium.webdriver.support.ui import Select
    
    # Se reciben las preguntas de una lista que está en el inicio del código

    # Extraemos el link del banco de preguntas
    banco_preguntas = wait.until(EC.invisibility_of_element_located((By.XPATH, '//li[@data-key="questionbank"]/a[@role="menuitem"]')))
    href = banco_preguntas.get_attribute("href")
    print(href)
    # Luego redireccionamos a ese link
    driver.get(href)
    
    
    for i in range(0,4):
        newquest = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-secondary"]')))
        newquest.click()
        multichoice = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[@for="item_qtype_multichoice"]')))
        multichoice.click()
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
        next_btn.click()
        # Seleccionamos el nombre de la pregunta
        nombre_pregunta = preguntas[i][0]
        input_nombre_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
        input_nombre_pregunta.clear()
        input_nombre_pregunta.send_keys(nombre_pregunta)
        # Seleccionamos el enunciado de la pregunta
        enunciado = preguntas[i][1]
        input_enunciado = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_questiontexteditable"]')))
        input_enunciado.clear()
        input_enunciado.send_keys(enunciado)
        # Seleccionamos las opciones
        # Opción 1
        opcion_1 = preguntas[i][2]
        input_opcion_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_answer_0editable"]')))
        input_opcion_1.clear()
        input_opcion_1.send_keys(opcion_1)
        # Opción 2
        opcion_2 = preguntas[i][3]
        input_opcion_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_answer_1editable"]')))
        input_opcion_2.clear()
        input_opcion_2.send_keys(opcion_2)
        # Opción 3
        opcion_3 = preguntas[i][4]
        input_opcion_3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_answer_2editable"]')))
        input_opcion_3.clear()
        input_opcion_3.send_keys(opcion_3)
        # Opción 4
        opcion_4 = preguntas[i][5]
        input_opcion_4 = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_answer_3editable"]')))
        input_opcion_4.clear()
        input_opcion_4.send_keys(opcion_4)
        # Seleccionamos la respuesta correcta
        menuopciones = wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@id="id_fraction_'+str(preguntas[i][6])+'"]')))
        menuopciones.click()
        selector = Select(menuopciones)
        selector.select_by_visible_text("100%")
        # Guardamos cambios
        send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
        send_btn.click()
    
    for i in range(4,7):
        newquest = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-secondary"]')))
        newquest.click()
        shortquest = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[@for="item_qtype_shortanswer"]')))
        shortquest.click()
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
        next_btn.click()
        # Seleccionamos el nombre de la pregunta
        nombre_pregunta = preguntas[i][0]
        input_nombre_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
        input_nombre_pregunta.clear()
        input_nombre_pregunta.send_keys(nombre_pregunta)
        # Seleccionamos el enunciado de la pregunta
        enunciado = preguntas[i][1]
        input_enunciado = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_questiontexteditable"]')))
        input_enunciado.clear()
        input_enunciado.send_keys(enunciado)
        # Seleccionamos las opciones
        # Opción 1
        opcion_1 = preguntas[i][2]
        input_opcion_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_answer_0"]')))
        input_opcion_1.clear()
        input_opcion_1.send_keys(opcion_1)
        # Opción 2
        opcion_2 = preguntas[i][3]
        input_opcion_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_answer_1"]')))
        input_opcion_2.clear()
        input_opcion_2.send_keys(opcion_2)
        # Opción 3
        opcion_3 = preguntas[i][4]
        input_opcion_3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_answer_2"]')))
        input_opcion_3.clear()
        input_opcion_3.send_keys(opcion_3)
        # Seleccionamos la respuesta correcta
        menuopciones = wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@id="id_fraction_'+str(preguntas[i][5])+'"]')))
        menuopciones.click()
        selector = Select(menuopciones)
        selector.select_by_visible_text("100%")
        # Guardamos cambios
        send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
        send_btn.click()
    
    back_to_curso()
    
# QA de ahorcado
def ahorcado(preguntas):
    from selenium.webdriver.support.ui import Select
    import unidecode
    
    btnactividades("Ahorcado")
    
    # Ingresamos el nombre del juego
    nombre_actividad = "QA Ahorcado"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.clear()
    input_nombre_actividad.send_keys(nombre_actividad)
    banco_preguntas = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="id_questioncategoryid"]')))
    selector = Select(banco_preguntas)
    selector.select_by_index(1)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    editModeOff()
    screenshooter("ahorcado", "ahorcado_previo")
    
    # Jugamos
    playbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-secondary"]')))
    playbtn.click()
    screenshooter("ahorcado", "ahorcado_jugando")
    
    # Buscamos cual es la respuesta de la pregunta que salió
    enunciado = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@role="main"]/b')))
    print(enunciado.text)
    for i in range(4,len(preguntas)):
        if(preguntas[i][1] == enunciado.text):
            indice_respuesta = preguntas[i][5]
            respuesta = preguntas[i][indice_respuesta+2]
            print(f"La respuesta es {respuesta}")
    
    # Primero formateamos las letras de la respuesta
    respuesta = unidecode.unidecode(respuesta)
    respuesta = respuesta.upper()
    respuesta = list(set(respuesta))
    print(respuesta)
    
    # Tenemos que seleccionar las letras de la respuesta
    for i in range(0,len(respuesta)):
        letra = respuesta[i]
        print(letra)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//font/a[contains(text(), "'+letra.upper()+'")]')))
        btn.click()
    screenshooter("ahorcado", "ahorcado_resuelto")
    chaoactividad(nombre_actividad)
    
# QA de criptograma
def criptograma(preguntas):
    from selenium.webdriver.support.ui import Select
     
    btnactividades("Criptograma")
    
    # Ingresamos el nombre del juego
    nombre_actividad = "QA Criptograma"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.clear()
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Seleccionamos el banco de preguntas
    banco_preguntas = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="id_questioncategoryid"]')))
    selector = Select(banco_preguntas)
    selector.select_by_index(1)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    editModeOff()
    screenshooter("criptograma", "criptograma_previo")
    
    # Jugamos
    playbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-secondary"]')))
    playbtn.click()
    screenshooter("criptograma", "criptograma_jugando")
    
    # Sabemos que son 3 preguntas para este juego  
    for i in range(4,len(preguntas)):
        # Click en el botón respuesta
        respuesta_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]')))
        respuesta_btn.click()
        
        enunciado = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="answerbox"]/div[@id="wordclue"]')))
        print(f"Enunciado: {enunciado.text[3:]}")
        
        # Busca la respuesta a la pregunta que está en pantalla
        for i in range(4,len(preguntas)):
            if(preguntas[i][1] == enunciado.text[3:]):
                indice_respuesta = preguntas[i][5]
                respuesta = preguntas[i][indice_respuesta+2]
                print(f"La respuesta es {respuesta}")
        
        # Ingresamos la respuesta
        input_respuesta = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="answer"]')))
        input_respuesta.send_keys(respuesta)
        if(i == 6):
            screenshooter("criptograma", "criptograma_jugando")
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="okbutton" and @class="button"]')))
        send_btn.click()
    screenshooter("criptograma", "criptograma_resuelto")
    
    chaoactividad(nombre_actividad)
        
# QA de crucigrama
def crucigrama(preguntas): # Complicado pero no imposible, queda pendiente
    from selenium.webdriver.support.ui import Select
    
    btnactividades("Crucigrama")
    
    # Ingresamos el nombre del juego
    nombre_actividad = "QA Crucigrama"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.clear()
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Seleccionamos el banco de preguntas
    banco_preguntas = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="id_questioncategoryid"]')))
    selector = Select(banco_preguntas)
    selector.select_by_index(1)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    editModeOff()
    screenshooter("crucigrama", "crucigrama_previo")
    
    # Jugamos
    playbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-secondary"]')))
    playbtn.click()
    screenshooter("crucigrama", "crucigrama_jugando")
    
    
    # Contamos la cantidad de filas y columnas que hay con Javascript
    cantidad_filas = driver.execute_script("return CrosswordHeight;")
    cantidad_columnas = driver.execute_script("return CrosswordWidth;")
    print(f"Cantidad de filas: {cantidad_filas}")
    print(f"Cantidad de columnas: {cantidad_columnas}")
    
    for i in range(1, cantidad_columnas+1):
        for j in range(1,cantidad_filas+1):
            # Seleccionamos la primera casilla disponible de la primera fila 
            if(i == 2 and j == 1):
                screenshooter("crucigrama", "crucigrama_jugando")
                    
            casilla = wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@id="crossword"]/tbody/tr['+str(j+1)+']/td['+str(i+1)+']')))
            if(casilla.get_attribute("id")):
                print("La casilla existe")
            else: 
                print("La casilla no existe")
                continue
            casilla.click()
            # Revisamos si es que la casilla ya está rellena según su valor
            if(casilla.text):
                print("La casilla ya está rellena")
                continue
            else:
                print("La casilla está vacía")
            
            enunciado = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="answerbox"]/div[@id="wordclue"]')))
            print(f"Enunciado: {enunciado.text}")
                
            # Busca la respuesta a la pregunta que está en pantalla
            for i in range(4,len(preguntas)):
                if(preguntas[i][1] == enunciado.text):
                    indice_respuesta = preguntas[i][5]
                    respuesta = preguntas[i][indice_respuesta+2]
                    print(f"La respuesta es {respuesta}")
                
            # Ingresamos la respuesta
            input_respuesta = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="wordentry"]')))
            input_respuesta.send_keys(respuesta)
            send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="okbutton" and @class="button"]')))
            send_btn.click()
    screenshooter("crucigrama", "crucigrama_resuelto")        
    
    chaoactividad(nombre_actividad)
    
# QA de millonario
def millonario(preguntas):
    from selenium.webdriver.support.ui import Select
    
    btnactividades("Millonario")
    
    # Ingresamos el nombre del juego
    nombre_actividad = "QA Millonario"
    input_nombre_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.clear()
    input_nombre_actividad.send_keys(nombre_actividad)
    
    # Seleccionamos el banco de preguntas
    banco_preguntas = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="id_questioncategoryid"]')))
    selector = Select(banco_preguntas)
    selector.select_by_index(1)
    
    # Guardamos y mostramos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()
    editModeOff()
    screenshooter("millonario", "millonario_previo")
    
    # Jugamos
    playbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-secondary"]')))
    playbtn.click()
    screenshooter("millonario", "millonario_jugando")
    
    for i in range(0,15):
        # Leemos cual es la pregunta
        enunciado = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@role="main"]/form[@name="Form1"]/table/tbody/tr[5]/td[1]')))
        print(f"La pregunta es: {enunciado.text}")
        # Busca la respuesta a la pregunta que está en pantalla 
        for i in range(0,len(preguntas)):
            if(preguntas[i][1] == enunciado.text):
                indice_respuesta = preguntas[i][6]
                respuesta = preguntas[i][indice_respuesta+2]
                print(f"La respuesta es {respuesta}")
        # Luego con la respuesta, seleccionamos la opción correcta
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//td[following-sibling::td/span[text()="'+respuesta+'"]]')))
        btn.click()
    
    screenshooter("millonario", "millonario_resuelto")
    
    chaoactividad(nombre_actividad)

# Saca fotos de las páginas
def screenshooter(carpeta,opcion):
    ##Sacar screenshots de las páginas##

    altura_total = driver.execute_script("return document.body.scrollHeight")
    print(altura_total)
    altura_desplazamiento = 500
    posicion_desplazamiento = 0
    directorio_capturas = directorio+"/"+carpeta
    
    if not os.path.exists(directorio_capturas):
        # Crear el directorio
        os.makedirs(directorio_capturas)
    if opcion == "display":
        driver.execute_script("window.scrollTo(0, "+str(500)+");")
        time.sleep(1)
        driver.save_screenshot(directorio_capturas+"/screenshot_"+opcion+"_"+str(posicion_desplazamiento)+".png")

    elif altura_total > 1000:
        while posicion_desplazamiento < (altura_total-1000):
            driver.execute_script("window.scrollTo(0, "+str(posicion_desplazamiento)+");")
            posicion_desplazamiento += altura_desplazamiento
            time.sleep(1)
            driver.save_screenshot(directorio_capturas+"/screenshot_"+opcion+"_"+str(posicion_desplazamiento)+".png")
    else: 
        driver.save_screenshot(directorio_capturas+"/screenshot_"+opcion+"_"+str(posicion_desplazamiento)+".png")
                 
    driver.execute_script("window.scrollTo(0, 0);")    
    
# Generalización para acceder a las actividades y recursos
def btnactividades(actividad):
    editMode()
    actividades_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-action="open-chooser"]')))
    actividades_btn.click()  
    
    if(actividad in ["Ahorcado", "Criptograma", "Crucigrama", "Millonario"]):
        # Seleccionamos el tipo de juego
        print("Es un juego")
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Juego - '+actividad+'"]')))
        btn.click()
    else:
        # Hacemos click en la actividad requerida
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="'+actividad+'"]')))
        btn.click()
      
# Generalización para volver al curso
def back_to_curso():
    driver.get("https://moodlecloud.uai.cl/course/view.php?id=10606")

# Función que nos permite sacar fotos de como se ve la actividad en la página principal del curso y luego eliminar esta actividad
def chaoactividad(nombre):
    back_to_curso()
    
    editMode()
    print(nombre)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@data-activityname, "'+nombre+'")]/div/div/div/div/div[starts-with(@id, "action-menu-")]')))
    btn.click()
    
    delete_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@data-activityname, "'+nombre+'")]/div/div/div/div/div[starts-with(@id, "action-menu-")]/div/div/a[@data-action="delete"]')))
    delete_btn.click()
    
    yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @class="btn btn-primary"]')))
    yes_btn.click()

login()
formatQA()
archivo(directorio)
area_textos_medios()
autoseleccion_grupos()
base_de_datos()
certificado()
chat()
consulta()
encuesta()
encuesta2()
# encuestapredefinida() #Esta encuesta ya no está dentro de los recursos disponibles
glosario()
h5p()
herramienta_externa()
laboratorio()   
leccion()
libro()
pagina()
scorm()
poster() 
taller()
tarea()
wiki()
url()
urluai()
pagina_contenido()
inicio_juegos(preguntas)
ahorcado(preguntas)
criptograma(preguntas)
crucigrama(preguntas) 
millonario(preguntas)
cuestionario()

time.sleep(5)
driver.quit()


