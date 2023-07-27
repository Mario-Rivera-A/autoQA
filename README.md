# autoQA


NOTE
----
El QA se tiene que hacer en un curso nuevo y con la página en español (RESTRICTIVO)

Ojo al momento de correr el código con un debuger ya que la función consulta() tiene un try/except (que matricula al usuario en el curso si es que este no llega a estar matriculado) que puede arrojar problemas, esta función también tarda más de lo normal

En las funciones login() y en back_to_curso() hay que cambiar el URL del curso en el que se van a hacer las pruebas


Hay que configurar la ruta correcta de los archivos en las siguientes funciones:

- archivo()
- carpeta()
- h5p()
- scorm()
- screenshooter()