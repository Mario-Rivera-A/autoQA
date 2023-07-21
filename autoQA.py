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

    driver.get("http://localhost/course/view.php?id=2594#section-0")
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

    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="usernavigation"]/li/form/div')))
    
    element_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))
    
    if 'text-primary' in element_2.get_attribute('class'):
        print("Modo de edición activado, no es necesario activarlo")
    else: 
        print("Modo de edición desactivado, activando...")
        element.click()
    
    driver.refresh()


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
        
        screenshooter("formatos_de_curso", opcion)
        
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
    
    back_to_curso()

# Listo
def archivo():
    
    editMode()
    
    directorio_archivo = "C:/Users/mrive/Documents/Trabajo/automatización QA/Git/autoQA/Dummy PDF.pdf"
    
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
    
    #subir archivo desde el filepicker
    
    agregar_archivo = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()
    
    input_archivo = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio_archivo)
    
    uploadfile = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    screenshooter("archivo", "Archivo_subido")
    
    
    chaoactividad(nombre_archivo, "archivo")
    
# QA de area de textos y medios
def area_textos_medios():
    
    btnactividades()
    
    # click en el botón de área de texto
    area_textos_medios_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="label"]')))
    area_textos_medios_btn.click()
    
    input_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="id_introeditoreditable"]')))
    input_btn.send_keys("QA área de texto")
    
    display_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton2')))
    display_btn.click()
    
    # screenshooter("area_textos_medios", "Area_de_textos_y_medios")
    
    chaoactividad("QA área de texto", "area_textos_medios")
    
# QA de autoselección de grupos
def autoseleccion_grupos():
    
    btnactividades()
    
    # click en el botón de autoseleccion
    grupo_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="groupselect"]')))
    grupo_btn.click()   
    
    #ingresar el nombre de la actividad
    titulo_actividad = "QA autoselección"
    input_nombre = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre.send_keys(titulo_actividad)
    
    #guardar y mostrar
    
    display_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    display_btn.click()
    
    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos")
    
    administrar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Administrar grupos"]')))
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
    
    chaoactividad(titulo_actividad, "autoseleccion_grupos")
    
# QA de base de datos
def base_de_datos():
    
    btnactividades()
    
    data_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="data"]')))
    data_btn.click()   
    
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
    
    chaoactividad(nombre_actividad, "base_de_datos")
 
# QA de carpeta   
def carpeta():
    
    btnactividades()
    
    folder_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="folder"]')))
    folder_btn.click()   
    
    nombre_actividad = "QA carpeta"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    directorio_archivo = "C:/Users/mrive/Documents/Trabajo/automatización QA/Git/autoQA/Dummy PDF.pdf"
    
    agregar_archivo = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()
    
    input_archivo = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio_archivo)
    
    uploadfile = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    screenshooter("carpeta", "carpeta")
    
    chaoactividad(nombre_actividad, "carpeta")
    
# QA de certificado
def certificado():
    
    btnactividades()
    
    certificado_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="customcert"]')))
    certificado_btn.click() 
    
    nombre_actividad = "QA certificado"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
    screenshooter("certificado", "certificado")
    
    chaoactividad(nombre_actividad, "certificado")
      
# QA de chat
def chat():
    
    btnactividades()
    
    chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="chat"]')))
    chat_btn.click()   
    
    nombre_actividad = "QA chat"
    input_actividad = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)
    
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()
    
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
    chaoactividad(nombre_actividad, "chat")
    
    print("ya estamos en la nueva ventana")
   
# QA de consulta
def consulta():
    
    btnactividades()
    
    consulta_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="choice"]')))
    consulta_btn.click()
    
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
        
        screenshooter("consulta", "consulta")

    except :
        print("Ya estás matriculado")
        screenshooter("consulta", "consulta")
        
    chaoactividad(nombre_actividad, "consulta")
    
# QA cuestionario
def cuestionario():
    from selenium.webdriver.support.ui import Select
    
    btnactividades()
    
    cuestionario_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="quiz"]')))
    cuestionario_btn.click()
    
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
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="typename" and text()="Opción múltiple"]')))
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
    
    agregar_pregunta = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="typename" and text()="Verdadero/Falso"]')))
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
    
    # respuesta = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type = "radio" and contains(@aria-labelledby, "answer0_label") ]')))
    
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
    
    chaoactividad(nombre_actividad, "cuestionario")
    

    
    
    
    
# Saca fotos de las páginas
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
def btnactividades():
    editMode()
    actividades_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-action="open-chooser"]')))
    actividades_btn.click()  
      
# Generalización para volver al curso
def back_to_curso():
    driver.get("http://localhost/course/view.php?id=2594#section-0")
    
def chaoactividad(nombre,carpeta):
    back_to_curso()
    
    if not carpeta == None:
        screenshooter(carpeta, "display")   
    
    editMode()
    print(nombre)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@data-activityname, "'+nombre+'")]/div/div/div/div/div[starts-with(@id, "action-menu-")]')))
    btn.click()
    
    delete_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@data-activityname, "'+nombre+'")]/div/div/div/div/div[starts-with(@id, "action-menu-")]/div/div/a[@data-action="delete"]')))
    delete_btn.click()
    # /div/div/div/div/div[starts-with(@id, "action-menu-")]
    
    yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @class="btn btn-primary"]')))
    yes_btn.click()
    
    
# def actividades_recursos():
    # editMode()
    
    # df = []
    # # time.sleep(5)
    # wait = WebDriverWait(driver, 10)
    
    # add = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-action = 'open-chooser']")))
    # add.click()
    
    # actividades = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role = 'menubar']")))
    
    # for actividad in actividades:
    #     valor = actividad.get_attribute("arial-label")
    #     print(valor)
    
def prueba():
    formatQA()
    archivo()
    area_textos_medios()
    autoseleccion_grupos()
    base_de_datos()
    certificado()
    chat()
    consulta()
    cuestionario()
    
login()
# prueba()

# Listo
# formatQA()

# Listo
# archivo()

# Listo
# area_textos_medios()

# Listo 
# autoseleccion_grupos()

# Listo
# base_de_datos()

# Listo
# certificado()

# Listo
# chat()

# Listo
# consulta()

# Listo
# cuestionario()

# for i in range(0, 10):
#     chaoactividad("QA cuestionario", None)






time.sleep(5)
driver.quit()


