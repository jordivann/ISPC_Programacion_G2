# Sistema de Gestión de Turnos Médicos

## Descripción

Este proyecto fue desarrollado como parte del Módulo Programador del ISPC con el objetivo de integrar los conocimientos adquiridos en Programación con Python y Bases de Datos MySQL.

La aplicación permite gestionar pacientes, médicos, empleados, turnos e historias clínicas mediante una interfaz de consola, centralizando la información y mejorando la organización de un consultorio o centro médico.

---

## Problemática

Muchos consultorios médicos pequeños gestionan la información de manera manual mediante planillas o registros físicos, lo que genera:

* Superposición de turnos.
* Pérdida de información.
* Demoras en la atención.
* Dificultad para acceder a historiales clínicos.
* Errores administrativos.

---

## Solución Propuesta

Desarrollar un sistema de gestión por consola que permita:

* Registrar pacientes.
* Registrar médicos.
* Registrar empleados.
* Gestionar turnos médicos.
* Consultar y actualizar historias clínicas.
* Centralizar toda la información en una base de datos MySQL.

---

## Tecnologías Utilizadas

* Python 3
* MySQL
* MySQL Workbench
* Visual Studio Code
* Git y GitHub

---

## Estructura del Proyecto

```text
turnos_medicos/
│
├── main.py
│
├── database/
│   ├── __init__.py
│   ├── conexion.py
│   ├── schema.sql
│   └── queries.sql
│
├── models/
│   ├── empleado.py
│   ├── paciente.py
│   ├── medico.py
│   ├── turno.py
│   └── historia_clinica.py
│
├── controllers/
│   ├── empleado_controller.py
│   ├── paciente_controller.py
│   ├── medico_controller.py
│   ├── turno_controller.py
│   └── historia_controller.py
│
├── menus/
│   ├── menu_principal.py
│   ├── menu_empleados.py
│   ├── menu_pacientes.py
│   ├── menu_medicos.py
│   ├── menu_turnos.py
│   └── menu_historia_clinica.py
│
├── utils/
│   ├── validaciones.py
│   └── consola.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Modelo de Datos

### Entidades principales

* Empleado
* Paciente
* Médico
* Turno
* Historia Clínica

### Relaciones

* Un paciente puede tener múltiples turnos.
* Un médico puede atender múltiples turnos.
* Un empleado puede registrar múltiples turnos.
* Un paciente puede tener múltiples registros en su historia clínica.
* Un médico puede generar múltiples registros clínicos.

---

## Configuración del Entorno

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Dependencias utilizadas

```text
mysql-connector-python
python-dotenv
```

---

## Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=turnos_medicos
```

---

## Creación de la Base de Datos

1. Abrir MySQL Workbench.
2. Abrir el archivo:

```text
database/schema.sql
```

3. Ejecutar el script.
4. Verificar que se hayan creado las tablas correspondientes.

---

## Ejecución del Proyecto

Desde la terminal:

```bash
python main.py
```

---

## Objetivos del Proyecto

* Aplicar programación modular en Python.
* Diseñar una base de datos relacional.
* Implementar operaciones CRUD.
* Gestionar información médica de forma organizada.
* Utilizar Git y GitHub para el trabajo colaborativo.

---

## Integrantes

* Joaquín Soria
* (Completar con integrantes del grupo)

---

## Institución

Instituto Superior Politécnico Córdoba (ISPC)

Módulo Programador – Año 2026
