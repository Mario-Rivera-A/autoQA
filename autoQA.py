from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

import time

from env import USER, PASS, URL, COURSE

import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


def login():
    # Función para hacer el login en el curso QA
    driver.get(f"{URL}/course/view.php?id={COURSE}")
    driver.maximize_window()

    # ingresar los datos de usuario
    driver.find_element(By.ID, "username").send_keys(USER)
    driver.find_element(By.ID, "password").send_keys(PASS)

    # hacer click en el botón acceder
    driver.find_element(By.ID, "loginbtn").click()


def editMode():
    # seleccionar el modo de edición si este está desactivado
    time.sleep(1)
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="usernavigation"]/li/form/div')))

    element_2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))

    if 'text-primary' in element_2.get_attribute('class'):
        print("Modo de edición activado, no es necesario activarlo")
    else:
        print("Modo de edición desactivado, activando...")
        element.click()

    driver.refresh()


def editModeOff():
    # Para algunas actividades necesitamos desactivar el modo de edición
    time.sleep(1)
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="usernavigation"]/li/form/div')))

    element_2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))

    if 'text-primary' in element_2.get_attribute('class'):
        print("Modo de edición activado, desactivando...")
        element.click()
    else:
        print("Modo de edición desactivado, no es necesario desactivarlo")

    driver.refresh()


def formatQA():
    # QA de formatos de curso
    wait = WebDriverWait(driver, 10)
    configbtn = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//li[@data-key="editsettings" and @title="Configuración"]')))
    configbtn.click()
    formatbtn = wait.until(EC.visibility_of_element_located(
        (By.ID, 'id_courseformathdr')))
    formatbtn.click()
    menuopciones = wait.until(
        EC.visibility_of_element_located((By.ID, 'id_format')))
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

        displaybtn = wait.until(
            EC.element_to_be_clickable((By.ID, 'id_saveanddisplay')))
        displaybtn.click()

        screenshooter("formatos_de_curso", opcion)

        if (opcion == "singleactivity"):
            btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//li[@data-key="course"]')))
            btn.click()

            configbtn = wait.until(EC.element_to_be_clickable(
                (By.XPATH,  '//a[text()="Configuración"]')))
            configbtn.click()

        else:

            configbtn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//li[@data-key="editsettings" and @title="Configuración"]')))
            configbtn.click()

        formatbtn = wait.until(EC.element_to_be_clickable(
            (By.ID, 'id_courseformathdr')))
        formatbtn.click()

        menuopciones = wait.until(
            EC.element_to_be_clickable((By.ID, 'id_format')))
        # menuopciones.click()

        if (i == (len(df)-1)):
            selector = Select(menuopciones)
            selector.select_by_value("topics")

            displaybtn = wait.until(
                EC.element_to_be_clickable((By.ID, 'id_saveanddisplay')))
            displaybtn.click()

    back_to_curso()


def archivo():
    directorio_archivo = "assets/pdf.pdf"

    wait = WebDriverWait(driver, 10)

    btnactividades("resource")

    # Ingresar el nombre del archivo
    nombre_archivo = "QA archivo"
    driver.find_element(By.ID, "id_name").send_keys(nombre_archivo)

    # subir archivo desde el filepicker

    agregar_archivo = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()

    input_archivo = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio_archivo)

    uploadfile = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    screenshooter("archivo", "Archivo_subido")

    chaoactividad(nombre_archivo, "archivo")


def area_textos_medios():
    # QA de area de textos y medios

    btnactividades("label")

    input_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@id="id_introeditoreditable"]')))
    input_btn.send_keys("QA área de texto")

    display_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton2')))
    display_btn.click()

    # screenshooter("area_textos_medios", "Area_de_textos_y_medios")

    chaoactividad("QA área de texto", "area_textos_medios")


def autoseleccion_grupos():
    # QA de autoselección de grupos

    btnactividades("groupselect")

    # ingresar el nombre de la actividad
    titulo_actividad = "QA autoselección"
    input_nombre = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_nombre.send_keys(titulo_actividad)

    # guardar y mostrar

    display_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    display_btn.click()

    editModeOff()

    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos")

    administrar_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Administrar grupos"]')))
    administrar_btn.click()

    # Crear grupos automáticamente
    creacion_grupos_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'showautocreategroupsform')))
    creacion_grupos_btn.click()

    input_esquema = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_namingscheme"]')))

    if input_esquema.get_attribute('value'):
        # Borrar el valor predefinido
        input_esquema.clear()

    input_esquema.send_keys("Grupo #")

    input_cantidad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_number"]')))
    input_cantidad.send_keys("2")

    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos2")

    back_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//li[@data-key="coursehome"]')))
    back_btn.click()

    actividad_btn = wait.until(EC.element_to_be_clickable(
        (By.PARTIAL_LINK_TEXT, str(titulo_actividad))))
    actividad_btn.click()

    screenshooter("autoseleccion_grupos", "Autoseleccion_grupos3")

    chaoactividad(titulo_actividad, "autoseleccion_grupos")


def base_de_datos():
    # QA de base de datos

    btnactividades("data")

    nombre_actividad = "QA base de datos"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    display_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    display_btn.click()

    creacion_btn = wait.until(EC.element_to_be_clickable(
        (By.ID, 'action-menu-toggle-2')))
    creacion_btn.click()

    opcion_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@aria-labelledby="actionmenuaction-15"]')))
    opcion_btn.click()

    nombre_campo = "QA campo"
    desc_campo = "QA descripción"
    input_nombre_campo = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="name"]')))
    input_nombre_campo.send_keys(nombre_campo)
    input_desc_campo = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="description"]')))
    input_desc_campo.send_keys(desc_campo)

    submit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@class="btn btn-primary" and @type = "submit"]')))
    submit_btn.click()

    screenshooter("base_de_datos", "campo")

    plantillas = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@id = "sticky-footer"]/div/a')))
    plantillas.click()

    submit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@class="btn btn-primary" and @type = "submit"]')))
    submit_btn.click()

    screenshooter("base_de_datos", "plantilla")

    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//li[@data-key="modulepage"]')))
    btn.click()

    add_entrada = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type = "submit" and @class = "btn btn-primary"]')))
    add_entrada.click()

    nombre_registro = "QA registro"
    input_registro = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@name[starts-with(., "field_")]]')))
    input_registro.send_keys(nombre_registro)

    save_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@name="saveandview" and @type = "submit"]')))
    save_btn.click()

    screenshooter("base_de_datos", "registro")

    chaoactividad(nombre_actividad, "base_de_datos")


def carpeta():
    # QA de carpeta

    btnactividades("folder")

    nombre_actividad = "QA carpeta"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    directorio_archivo = "assets/pdf.pdf"

    agregar_archivo = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()

    input_archivo = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio_archivo)

    uploadfile = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    editModeOff()

    screenshooter("carpeta", "carpeta")

    chaoactividad(nombre_actividad, "carpeta")


def certificado():
    # QA de certificado

    btnactividades("customcert")

    nombre_actividad = "QA certificado"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    editModeOff()

    screenshooter("certificado", "certificado")

    chaoactividad(nombre_actividad, "certificado")


def chat():
    # QA de chat

    btnactividades("chat")

    nombre_actividad = "QA chat"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    editModeOff()

    screenshooter("chat", "chat")

    entrar_chat = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@class="btn btn-primary"]')))
    entrar_chat.click()

    # cambiar de ventana
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
    input_texto = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="text"]')))
    input_texto.send_keys(texto)

    send_texto = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="button"]')))
    send_texto.click()

    time.sleep(1)

    screenshooter("chat", "chat2")

    # Cerramos ventana de chat
    driver.close()
    driver.switch_to.window(ventana_original)
    chaoactividad(nombre_actividad, "chat")

    print("ya estamos en la nueva ventana")


def consulta():
    # QA de consulta

    btnactividades("choice")

    nombre_actividad = "QA consulta"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    opcion_1 = "Esta es la opción 1"
    input_opcion_1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_option_0"]')))
    input_opcion_1.send_keys(opcion_1)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    try:
        matricular_btn = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[@type="submit" and @class="btn btn-secondary"]')))
        print("Tienes que matricularte")
        matricular_btn.click()

        # Parte que podría llegar a cambiar
        matricular_btn = wait.until(
            EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
        matricular_btn.click()

        driver.refresh()

        editModeOff()

        screenshooter("consulta", "consulta")

    except:
        print("Ya estás matriculado")

        editModeOff()

        screenshooter("consulta", "consulta")

    chaoactividad(nombre_actividad, "consulta")


def cuestionario():
    # QA cuestionario
    btnactividades("quiz")

    nombre_actividad = "QA cuestionario"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))

    if input_actividad.get_attribute('value'):
        # Borrar el valor predefinido
        input_esquema.clear()

    input_actividad.send_keys(nombre_actividad)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@class="btn btn-secondary"]')))
    agregar_pregunta.click()

    # Click en el dropdown Agregar
    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class = "dropdown"]/a[starts-with(@id,"action-menu") and @role = "button"]')))
    agregar_pregunta.click()

    # Agregamos una pregunta
    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@data-action="addquestion"]')))
    agregar_pregunta.click()

    # Agregamos una pregunta de opción múltiple
    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//span[@class="typename" and text()="Opción múltiple"]')))
    agregar_pregunta.click()

    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()

    nombre_pregunta = "QA pregunta 1"
    enunciado_pregunta = "Enunciado de la pregunta 1"
    # Ingresamos el nombre de la pregunta
    input_nombre_pregunta_1 = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@name="name"]')))
    input_nombre_pregunta_1.send_keys(nombre_pregunta)
    # Ingresamos el enunciado de la pregunta
    input_enunciado_pregunta_1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@id="id_questiontexteditable"]')))
    input_enunciado_pregunta_1.send_keys(enunciado_pregunta)

    # Respuestas que queremos agregar
    texto_opcion_1 = "Opción 1"
    input_opcion_1 = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_answer_0editable')))
    input_opcion_1.send_keys(texto_opcion_1)

    # Calificacion de la pregunta (100%)

    selector = Select(wait.until(
        EC.element_to_be_clickable((By.ID, 'id_fraction_0'))))
    selector.select_by_value("1.0")

    texto_opcion_2 = "Opción 2"
    input_opcion_2 = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_answer_1editable')))
    input_opcion_2.send_keys(texto_opcion_2)

    selector = Select(wait.until(
        EC.element_to_be_clickable((By.ID, 'id_fraction_1'))))
    selector.select_by_value("1.0")

    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()

    ## Agregamos una segunda pregunta de verdadero o falso ##
    # Hacemos click en el dropdown Agregar
    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class = "dropdown"]/a[starts-with(@id,"action-menu") and @role = "button"]')))
    agregar_pregunta.click()

    # Agregamos una pregunta
    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@data-action="addquestion"]')))
    agregar_pregunta.click()

    agregar_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//span[@class="typename" and text()="Verdadero/Falso"]')))
    agregar_pregunta.click()

    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()

    nombre_pregunta = "QA pregunta 2"
    enunciado_pregunta = "Enunciado de la pregunta 2, verdadero o falso"
    # Ingresamos el nombre de la pregunta
    input_nombre_pregunta_2 = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@name="name"]')))
    input_nombre_pregunta_2.send_keys(nombre_pregunta)
    # Ingresamos el enunciado de la pregunta
    input_enunciado_pregunta_2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@id="id_questiontexteditable"]')))
    input_enunciado_pregunta_2.send_keys(enunciado_pregunta)

    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="submit" and @name="submitbutton"]')))
    send_btn.click()

    ## Vista del cuestionario ##
    # Click en cuestionario
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//li[@data-key="modulepage"]')))
    btn.click()

    # Click en vista previa del cuestionario
    vista = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type = "submit" and @class="btn btn-primary"]')))
    vista.click()

    # Resolvemos el cuestionario

    respuesta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//p[text()= "'+texto_opcion_1+'"]')))
    respuesta.click()

    respuesta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//label[text()= "Falso"]')))
    respuesta.click()

    screenshooter("cuestionario", "cuestionario")

    # Terminar intento
    end_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type = "submit" and @name = "next"]')))
    end_btn.click()

    screenshooter("cuestionario", "cuestionario_finalizado")

    end_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type = "submit" and @class = "btn btn-primary"]')))
    end_btn.click()

    end_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type = "button" and @class = "btn btn-primary"]')))
    end_btn.click()

    screenshooter("cuestionario", "revisión")

    chaoactividad(nombre_actividad, "cuestionario")


def cuestionarioofline():
    # QA de cuestionario offline

    btnactividades("offlinequiz")

    nombre_actividad = "QA cuestionario offline"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    # Guardar cambios y mostrar
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    screenshooter("cuestionarioofline", "cuestionarioofline")

    chaoactividad(nombre_actividad, "cuestionarioofline")


def encuesta():
    # QA de encuesta
    btnactividades("feedback")

    nombre_actividad = "QA encuesta"
    input_actividad = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_name"]')))
    input_actividad.send_keys(nombre_actividad)

    # Guardar cambios y mostrar
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    # Editar preguntas
    edit_btn = driver.find_elements(
        By.XPATH, '//a[@class="btn btn-secondary"]')
    edit_btn[0].click()

    # Se selecciona una encuesta de selección múltiple
    selector = Select(wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//select[contains(@id, "single_select") ]'))))
    selector.select_by_value("multichoice")

    # Nombre de la pregunta
    nombre_pregunta = "Pregunta 1"
    input_pregunta = wait.until(EC.element_to_be_clickable((By.ID, 'id_name')))
    input_pregunta.send_keys(nombre_pregunta)

    # Valores de la elección múltiple
    valores = str("Pregunta 1 \nPregunta 2 \nPregunta 3")
    input_valores = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@data-fieldtype = "textarea"]/textarea[@id = "id_values"]')))
    input_valores.send_keys(valores)

    # Guardar cambios
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_save_item')))
    send_btn.click()

    ## Camino a responder la encuesta ##
    # Click en Encuesta
    encuesta_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//li[@data-key="modulepage"]')))
    encuesta_btn.click()

    screenshooter("encuesta", "vista previa")

    # Responder las preguntas
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class = "navitem"]/a[@class = "btn btn-primary"]')))
    btn.click()

    screenshooter("encuesta", "encuesta")

    # Enviar la respuesta
    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type = "submit" and @id = "id_savevalues"]')))
    send_btn.click()

    # Encuesta respondida

    screenshooter("encuesta", "encuesta_respondida")

    chaoactividad(nombre_actividad, "encuesta")


def encuesta2():
    # QA de encuesta questionnaire

    btnactividades("questionnaire")

    nombre_actividad = "QA encuesta (questionnaire)"
    # Ingresamos el nombre de la actividad
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardar cambios y mostrar
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    ## Añadimos preguntas ##
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@class="btn btn-primary"]')))
    btn.click()

    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="submit" and @name = "addqbutton"]')))
    btn.click()

    # Nombre de la pregunta
    nombre_pregunta = "Pregunta 1"
    texto_pregunta = "Texto de la pregunta 1"
    respuestas_posibles = "Respuesta 1 \nRespuesta 2 \nRespuesta 3"
    # Ingresamos el nombre de la pregunta
    input_nombre_pregunta = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_pregunta.send_keys(nombre_pregunta)
    # Ingresamos el texto de la pregunta
    input_texto_pregunta = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@id="id_contenteditable"]')))
    input_texto_pregunta.send_keys(texto_pregunta)
    # Ingresamos las respuestas posibles
    input_respuestas_posibles = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//textarea[@id="id_allchoices"]')))
    input_respuestas_posibles.send_keys(respuestas_posibles)

    # Guardamos cambios
    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type="submit" and @name = "submitbutton"]')))
    send_btn.click()

    ## Camino a responder la encuesta ##
    # Click en Encuesta
    encuesta_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//li[@data-key="modulepage"]')))
    encuesta_btn.click()

    screenshooter("questionnaire", "vista previa")

    # Click en responda las preguntas
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class = "complete"]/a[@class = "btn btn-primary"]')))
    btn.click()

    screenshooter("questionnaire", "encuesta")

    # Enviamos la encuesta
    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type = "submit" and contains(@class, "btn-primary")]')))
    send_btn.click()

    screenshooter("questionnaire", "encuesta_respondida")

    # Click en continuar para ver los resultados
    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type = "submit" and @class= "btn btn-secondary"]')))
    send_btn.click()

    screenshooter("questionnaire", "resultados")

    chaoactividad(nombre_actividad, "questionnaire")


def encuestapredefinida():
    # QA de encuesta predefinida
    btnactividades("survey")

    nombre_actividad = "QA encuesta predefinida"
    # Ingresamos el nombre de la actividad
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    selector = Select(wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//select[@id="id_template"]'))))
    selector.select_by_index(1)

    # Guardar cambios y mostrar
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    screenshooter("encuestapredefinida", "encuestapredefinida")
    chaoactividad(nombre_actividad, "encuestapredefinida")


def glosario():
    # QA de glosario

    btnactividades("glossary")

    # Ingresamos nombre de la actividad
    nombre_actividad = "QA glosario"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    # Ingresamos una nueva entrada al glosario
    add_entrada = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="btn btn-primary"]')))
    add_entrada.click()

    # Concepto
    concepto = "Adormecer"
    definicion = "Hacer que alguien o algo se duerma o se quede dormido."

    # Ingresamos las variables
    input_concepto = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_concept')))
    input_concepto.send_keys(concepto)

    input_definicion = wait.until(EC.element_to_be_clickable(
        (By.ID, 'id_definition_editoreditable')))
    input_definicion.send_keys(definicion)

    # Enviamos la entrada
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    screenshooter("glosario", "glosario")

    chaoactividad(nombre_actividad, "glosario")


def h5p():
    # QA de H5P (Suerte en esto)

    btnactividades("h5pactivity")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA H5P"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Tenemos que subir el paquete de archivos h5p
    directorio_archivo = "assets/h5p.h5p"

    # Vamos al filepicker y subimos el archivo
    agregar_archivo = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()

    input_archivo = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@type="file"]')))
    input_archivo.send_keys(directorio_archivo)

    uploadfile = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    uploadfile.click()

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    submit_btn.click()

    screenshooter("h5p", "h5p")

    chaoactividad(nombre_actividad, "h5p")


def H5P():
    # Tenemos que hacerlo según el pdf de QA

    btnactividades("h5pactivity")

    ventana_inicial = driver.current_window_handle

    # Accedemos al banco de contenido
    banco_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class = "form-control-static"]/a[@target="_blank"]')))
    banco_btn.click()

    # Vamos a cambiarnos a la nueva pestaña para trabajar en ella

    ventanas_nuevas = driver.window_handles

    for ventana in ventanas_nuevas:
        if ventana != ventana_inicial:
            driver.switch_to.window(ventana)
            break

    # Tenemos que escoger el tipo de contenido (Image Hotspot en este caso)
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type = "button" and @data-toggle = "dropdown"]')))
    add_btn.click()

    type_content = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[contains(@href, "ImageHotspots")]')))
    type_content.click()

    # Tenemos que cambiar al iframe de h5p

    driver.switch_to.frame("h5p-editor")

    # Ingresamos el título del contenido
    time.sleep(3)
    titulo = "QA H5P"

    ## Acá hay problemas ##
    input_titulo = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@class = "h5peditor-text"]')))
    input_titulo.send_keys(titulo)

    ## Intentamos ingresar el archivo ##
    # Ruta de la imagen
    ruta = "assets/image.jpg"
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@href = "#" and @class = "add"]')))
    # add_btn.click()
    add_btn.send_keys(ruta)


def herramienta_externa():
    # QA de herramient externa

    btnactividades("lti")

    # Nombre de la actividad
    nombre_actividad = "QA herramienta externa"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Ingresamos la url de herramienta externa
    url = "https://intranet.uai.cl/Login.aspx"
    input_url = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_toolurl"]')))

    if input_url.get_attribute('value'):
        # Borrar el valor predefinido
        input_esquema.clear()

    input_url.send_keys(url)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("herramienta_externa", "herramienta_externa")

    chaoactividad(nombre_actividad, "herramienta_externa")


def laboratorio():
    # QA de laboratorio

    btnactividades("vpl")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA laboratorio"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("laboratorio", "laboratorio")

    chaoactividad(nombre_actividad, "laboratorio")


def leccion():
    # QA de lección

    btnactividades("lesson")

    # Ingresamos el nombre de la actividada
    nombre_actividad = "QA lección"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("leccion", "leccion")

    chaoactividad(nombre_actividad, "leccion")


def libro():
    # QA de libro

    btnactividades("book")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA libro"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    # Añadimos un capítulo
    nombre_capitulo = "Capítulo 1"
    input_nombre_capitulo = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_title')))
    input_nombre_capitulo.send_keys(nombre_capitulo)

    # Añadimos el contenido
    contenido = "Contenido del capítulo 1"
    input_contenido = wait.until(EC.element_to_be_clickable(
        (By.ID, 'id_content_editoreditable')))
    input_contenido.send_keys(contenido)

    # Guardamos cambios
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("libro", "libro")

    chaoactividad(nombre_actividad, "libro")


def pagina():
    # QA de página

    btnactividades("page")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA página"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Ingresamos el contenido de la página
    contenido = "Este es el contenido de la página"
    input_contenido = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_pageeditable')))
    input_contenido.send_keys(contenido)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("pagina", "pagina")

    chaoactividad(nombre_actividad, "pagina")


def scorm():
    # QA de paquete SCORM

    btnactividades("scorm")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA scorm"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Ingresamos el paquete scorm

    agregar_archivo = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[starts-with(@class,"fp-btn-add")]')))
    agregar_archivo.click()

    ruta = "assets/scorm.zip"
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@type = "file"]')))
    add_btn.send_keys(ruta)

    # Subimos el archivo
    send_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]')))
    send_btn.click()

    # Guardamos cambios y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    # Entramos a ver la actividad scorm
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[starts-with(@class, "btn btn-primary") and @type = "submit"]')))
    btn.click()

    editModeOff()

    screenshooter("scorm", "scorm")

    chaoactividad(nombre_actividad, "scorm")


def poster():
    # QA de póster
    btnactividades("poster")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA poster"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    # Abrimos la selección y escogemos la opción texto
    selector = Select(wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//select[starts-with(@id, "single_select")]'))))
    selector.select_by_value("recent_activity")

    editModeOff()

    screenshooter("poster", "poster")

    chaoactividad(nombre_actividad, "poster")


def taller():
    # QA de taller

    btnactividades("workshop")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA taller"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("taller", "taller")

    chaoactividad(nombre_actividad, "taller")


def tarea():
    # QA de tarea

    btnactividades("assign")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA tarea"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("tarea", "tarea")

    chaoactividad(nombre_actividad, "tarea")


def wiki():
    # QA de wiki

    btnactividades("wiki")

    # Ingresamos el nombre de la actividad
    nombre_actividad = "QA wiki"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys("QA wiki")

    # Ingresamos el nombre de la primera página
    nombre_pagina = "Página 1"
    input_nombre_pagina = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_firstpagetitle"]')))
    input_nombre_pagina.send_keys(nombre_pagina)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    # Creamos página con el formato por defecto
    btn = wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    btn.click()

    # Ingresamos el texto
    texto = "<p>final</p>"
    input_texto = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@id="id_newcontent_editoreditable"]')))
    input_texto.send_keys(texto)

    # Guardamos
    send_btn = wait.until(EC.element_to_be_clickable((By.ID, 'save')))
    send_btn.click()

    editModeOff()

    screenshooter("wiki", "wiki")

    chaoactividad(nombre_actividad, "wiki")


def url():
    # QA de url

    btnactividades("url")

    # Ingresamos el nombre de la actividad y la url externa
    nombre_actividad = "QA url"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    url = "https://intranet.uai.cl/"
    input_url = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_externalurl"]')))
    input_url.send_keys(url)

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("url", "url")

    chaoactividad(nombre_actividad, "url")


def urluai():
    # QA de urluai
    btnactividades("urluai")

    # Ingresamos el nombre de la actividad y la url externa
    nombre_actividad = "QA urluai"
    input_nombre_actividad = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))
    input_nombre_actividad.send_keys(nombre_actividad)

    url = "https://intranet.uai.cl/"
    input_url = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@id="id_externalurl"]')))
    input_url.send_keys(url)

    # Ponemos algunas variables en la URL
    btn = wait.until(EC.element_to_be_clickable(
        (By.ID, "id_parameterssection")))
    btn.click()

    # Primer parámetro
    parametro = "Juan Carlos"
    input_parametro = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_parameter_0')))
    input_parametro.send_keys(parametro)

    # Escojemos que tipo de variable sea
    selector = Select(wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//select[@id="id_variable_0"]'))))
    selector.select_by_value("urlname")

    time.sleep(1)

    # Segundo parámetro
    parametro = "Español"
    input_parametro = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_parameter_1')))
    input_parametro.send_keys(parametro)

    # Escojemos que tipo de variable sea
    selector = Select(wait.until(
        EC.element_to_be_clickable((By.ID, 'id_variable_1'))))
    selector.select_by_value("lang")

    # Guardamos y mostramos
    send_btn = wait.until(
        EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
    send_btn.click()

    editModeOff()

    screenshooter("urluai", "urluai")

    chaoactividad(nombre_actividad, "urluai")


def screenshooter(carpeta, opcion):
    # Saca fotos de las páginas
    ## Sacar screenshots de las páginas##
    altura_total = driver.execute_script("return document.body.scrollHeight")

    print(altura_total)

    altura_desplazamiento = 500

    posicion_desplazamiento = 0

    directorio_capturas = f"images/{carpeta}"

    if not os.path.exists(directorio_capturas):
        # Crear el directorio
        os.makedirs(directorio_capturas)
    if opcion == "display":
        driver.execute_script("window.scrollTo(0, "+str(500)+");")
        time.sleep(1)
        driver.save_screenshot(
            directorio_capturas+"/screenshot_"+opcion+"_"+str(posicion_desplazamiento)+".png")

    elif altura_total > 1000:
        while posicion_desplazamiento < (altura_total-1000):
            driver.execute_script(
                "window.scrollTo(0, "+str(posicion_desplazamiento)+");")
            posicion_desplazamiento += altura_desplazamiento
            time.sleep(1)
            driver.save_screenshot(
                directorio_capturas+"/screenshot_"+opcion+"_"+str(posicion_desplazamiento)+".png")
    else:
        driver.save_screenshot(
            directorio_capturas+"/screenshot_"+opcion+"_"+str(posicion_desplazamiento)+".png")

    driver.execute_script("window.scrollTo(0, 0);")


def btnactividades(actividad):
    # Generalización para acceder a las actividades y recursos
    editMode()
    actividades_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@data-action="open-chooser"]')))
    actividades_btn.click()

    # Hacemos click en la actividad requerida
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@data-internal="'+actividad+'"]')))
    btn.click()


def back_to_curso():
    # Generalización para volver al curso
    driver.get(f"{URL}/course/view.php?id={COURSE}")


def chaoactividad(nombre, carpeta):
    # Función que nos permite sacar fotos de como se ve la actividad en la página principal del curso y luego eliminar esta actividad
    back_to_curso()

    if not carpeta == None:
        editModeOff()
        screenshooter(carpeta, "display")

    editMode()
    print(nombre)
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[contains(@data-activityname, "'+nombre+'")]/div/div/div/div/div[starts-with(@id, "action-menu-")]')))
    btn.click()

    delete_btn = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//div[contains(@data-activityname, "'+nombre+'")]/div/div/div/div/div[starts-with(@id, "action-menu-")]/div/div/a[@data-action="delete"]')))
    delete_btn.click()
    # /div/div/div/div/div[starts-with(@id, "action-menu-")]

    yes_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@type="button" and @class="btn btn-primary"]')))
    yes_btn.click()


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
    encuesta()
    encuesta2()
    encuestapredefinida()
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


login()
prueba()

time.sleep(5)
driver.quit()
