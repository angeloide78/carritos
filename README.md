# carritos
Gestión de carritos de portátiles para IES de la Junta de Andalucía

# Roadmap del Proyecto

## Por hacer

  - [ ] Arquitectura del controlador. 
     - ¿Un único módulo e incluir todas las clases o clases controlador separadas?
  - [ ] Separar los test de los módulos, e incluirlos en alguna carpeta
        para no subirlos al repositorio.
  - [ ] Iconos de la aplicación.
  - [ ] Manual de funcionamiento.

### [09-06-2023]

  - [X] Diseño de pantalla de configuración del aplicativo. 

![Prototipo de reserva de carritos](assets/imagenes/configuracion_09_06_2023.png)

### [08-06-2023]

  - [X] Se renombra clase Base a Conexion, que hereda de clases Log y Bd.
  - [X] Se crea clase DMLCarrito, que contiene los métodos genéricos para
        actualizar, borrar, crear y visualizar entidades (tablas).
  - [X] Se plantea en este punto el usar SQLAlchemy, pero dado lo pequeño 
        del proyecto, se descarta.
  - [X] Clases profesor, planta, horario y carrito heredan ahora de DMLCarrito.
        Implica que cada clase tiene funcionalidad extra de gestión de su 
        entidad asociada en la base de datos.
  - [X] Se crea clase portatil, reserva e incidencia, que heredan de DMLCarrito.

### [07-06-2023]

  - [X] Módulo bd (07-06-2023)
     - Clase Bd, que interacciona con una base de datos SQLite.
  - [X] Módulo log (07-06-2023)
     - Clase Log, que genera texto en ficheros de registros de eventos .log.
  - [X] Módulo base (07-06-2023)
     - Clase Base, heredada de Bd y Log, que será la clase padre de las clases
       que interaccionen con la base de datos.
  - [X] Se diseñan clases profesor, planta, horario y carrito.
        
### [06-06-2023]

  - [X] Ficheros UI generados con Qt Designer. 
     - Prototipos de la interfaz gráfica del proyecto.

![Prototipo de reserva de carritos](assets/imagenes/prototipo_reservas_09_06_2023.png)

















