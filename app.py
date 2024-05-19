import zipfile
import os
import pickle
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Extraer el archivo zip que contiene el modelo
with zipfile.ZipFile('random_forest_classifier_default_42.zip', 'r') as zip_ref:
    zip_ref.extractall('model')

# Cargar el modelo desde el archivo descomprimido
model_path = os.path.join('model', 'random_forest_classifier_default_42.sav')
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Definir las categorías (esto es un ejemplo, ajusta según tus datos)
categories = {
    'EDAD': [], 
    'ESTU_COD_DEPTO_PRESENTACION': ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTÁ', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA', 'CASANARE', 'CAUCA', 'CESAR', 'CHOCO', 'CORDOBA', 'CUNDINAMARCA', 'GUAINIA', 'GUAVIARE', 'HUILA', 'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO', 'NORTE SANTANDER', 'PUTUMAYO', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE', 'VAUPES', 'VICHADA', 'SAN ANDRES'], 
    'ESTU_DEDICACIONINTERNET':['30 minutos o menos', 'Entre 1 y 3 horas', 'Entre 30 y 60 minutos', 'Más de 3 horas', 'No Navega Internet'],
    'ESTU_DEDICACIONLECTURADIARIA': ['30 minutos o menos', 'Entre 1 y 2 horas', 'Entre 30 y 60 minutos', 'Más de 2 horas', 'No leo por entretenimiento'],
    'ESTU_DEPTO_RESIDE': ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTÁ', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA', 'CASANARE', 'CAUCA', 'CESAR', 'CHOCO', 'CORDOBA', 'CUNDINAMARCA', 'GUAINIA', 'GUAVIARE', 'HUILA', 'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO', 'NORTE SANTANDER', 'PUTUMAYO', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE', 'VAUPES', 'VICHADA', 'SAN ANDRES', 'EXTRANJERO'],
    'ESTU_HORASSEMANATRABAJA': ['0 horas', 'Entre 11 y 20 horas', 'Entre 21 y 30 horas', 'Menos de 10 horas', 'Más de 30 horas'],
    'ESTU_TIPOREMUNERACION': ['No', 'Si, en efectivo', 'Si, en efectivo y especie', 'Si, en especie'],
    'FAMI_COMECARNEPESCADOHUEVO': ['1 o 2 veces por semana', '3 a 5 veces por semana', 'Nunca o rara vez comemos eso', 'Todos o casi todos los días'],
    'FAMI_COMECEREALFRUTOSLEGUMBRE': ['1 o 2 veces por semana', '3 a 5 veces por semana', 'Nunca o rara vez comemos eso', 'Todos o casi todos los días'],
    'FAMI_COMELECHEDERIVADOS': ['1 o 2 veces por semana', '3 a 5 veces por semana', 'Nunca o rara vez comemos eso', 'Todos o casi todos los días'],
    'FAMI_CUARTOSHOGAR': ['Cinco', 'Cuatro', 'Dos', 'Seis o mas', 'Tres', 'Uno'],
    'FAMI_EDUCACIONMADRE': ['Educación profesional completa', 'Educación profesional incompleta', 'Ninguno', 'No Aplica', 'No sabe', 'Postgrado', 'Primaria completa', 'Primaria incompleta', 'Secundaria (Bachillerato) completa', 'Secundaria (Bachillerato) incompleta', 'Técnica o tecnológica completa', 'Técnica o tecnológica incompleta'],
    'FAMI_EDUCACIONPADRE': ['Educación profesional completa', 'Educación profesional incompleta', 'Ninguno', 'No Aplica', 'No sabe', 'Postgrado', 'Primaria completa', 'Primaria incompleta', 'Secundaria (Bachillerato) completa', 'Secundaria (Bachillerato) incompleta', 'Técnica o tecnológica completa', 'Técnica o tecnológica incompleta'],
    'FAMI_ESTRATOVIVIENDA': ['Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6', 'Sin Estrato'],
    'FAMI_NUMLIBROS': ['0 A 10 LIBROS', '11 A 25 LIBROS', '26 A 100 LIBROS', 'MÁS DE 100 LIBROS'],
    'FAMI_PERSONASHOGAR': ['1 a 2', '3 a 4', '5 a 6', '7 a 8', '9 o más'],
    'FAMI_SITUACIONECONOMICA': ['Igual', 'Mejor', 'Peor'],
    'FAMI_TRABAJOLABORMADRE': ['Es agricultor, pesquero o jornalero', 'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial', 'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc', 'Es operario de máquinas o conduce vehículos (taxita, chofer)', 'Es vendedor o trabaja en atención al público', 'No aplica', 'No sabe', 'Pensionado', 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)', 'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción', 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)', 'Trabaja en el hogar, no trabaja o estudia', 'Trabaja por cuenta propia (por ejemplo plomero, electricista)'],
    'FAMI_TRABAJOLABORPADRE': ['Es agricultor, pesquero o jornalero', 'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial', 'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc', 'Es operario de máquinas o conduce vehículos (taxita, chofer)', 'Es vendedor o trabaja en atención al público', 'No aplica', 'No sabe', 'Pensionado', 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)', 'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción', 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)', 'Trabaja en el hogar, no trabaja o estudia', 'Trabaja por cuenta propia (por ejemplo plomero, electricista)'],
    'ESTU_GENERO': ['F', 'M'],
    'FAMI_TIENEINTERNET': ['No', 'Si'],
    'FAMI_TIENECOMPUTADOR': ['No', 'Si'],
    'FAMI_TIENEHORNOMICROOGAS': ['No', 'Si'],
    'FAMI_TIENEMOTOCICLETA': ['No', 'Si']
}

# Diccionario de mapeo de nombres de columnas a preguntas descriptivas
questions = {
    'EDAD': '¿Que edad tiene?', 
    'ESTU_COD_DEPTO_PRESENTACION': '¿En que departamento presentó la prueba?', 
    'ESTU_DEDICACIONINTERNET': '¿Cuanto tiempo pasa en internet?',
    'ESTU_DEDICACIONLECTURADIARIA': 'Cuanto tiempo le dedica a la lectura diariamente?',
    'ESTU_DEPTO_RESIDE': 'En que departamento reside?',
    'ESTU_HORASSEMANATRABAJA': '¿Trabaja?, ¿Por cuantas horas?',
    'ESTU_TIPOREMUNERACION': 'Si trabaja, ¿Como le pagan?',
    'FAMI_COMECARNEPESCADOHUEVO': '¿Cuantas veces a la semana come carne, pescado y/o huevo?',
    'FAMI_COMECEREALFRUTOSLEGUMBRE': '¿Cuantas veces a la semana come cereal, frutos y/o legumbres?',
    'FAMI_COMELECHEDERIVADOS': '¿Cuantas veces a la semana come leche o derivados de leche?',
    'FAMI_CUARTOSHOGAR': '¿Cuantos cuartos hay en su hogar?',
    'FAMI_EDUCACIONMADRE': '¿Que nivel educativo tiene su madre?',
    'FAMI_EDUCACIONPADRE': '¿Que nivel educativo tiene su padre?',
    'FAMI_ESTRATOVIVIENDA': '¿Cual es su estrato?',
    'FAMI_NUMLIBROS': '¿Cuantos libros tiene?',
    'FAMI_PERSONASHOGAR': '¿Cuantas personas viven con usted?',
    'FAMI_SITUACIONECONOMICA': 'En comparación con el año anterior, como esta la economia familiar hoy?',
    'FAMI_TRABAJOLABORMADRE': '¿Mamá tiene empleo?, ¿Cual?',
    'FAMI_TRABAJOLABORPADRE': '¿Papá tiene empleo?, ¿Cual?',
    'ESTU_GENERO': '¿Con que género biologico nacio?',
    'FAMI_TIENEINTERNET': '¿Tiene internet?',
    'FAMI_TIENECOMPUTADOR': '¿Tiene computador?',
    'FAMI_TIENEHORNOMICROOGAS': '¿Tiene horno, microondas y/o estufa a gas?',
    'FAMI_TIENEMOTOCICLETA': '¿Tiene moto?'
}

category_mapping = {
    'EDAD': [], 
    'ESTU_COD_DEPTO_PRESENTACION': ['AMAZONAS': 0, 'ANTIOQUIA': 1, 'ARAUCA': 2, 'ATLANTICO': 3, 'BOGOTÁ': 4, 'BOLIVAR': 5, 'BOYACA': 6, 'CALDAS': 7, 'CAQUETA': 8, 'CASANARE': 9, 'CAUCA': 10, 'CESAR': 11, 'CHOCO': 12, 'CORDOBA': 13, 'CUNDINAMARCA': 14, 'GUAINIA': 15, 'GUAVIARE': 16, 'HUILA': 17, 'LA GUAJIRA': 18, 'MAGDALENA': 19, 'META': 20, 'NARIÑO': 21, 'NORTE SANTANDER': 22, 'PUTUMAYO': 23, 'QUINDIO': 24, 'RISARALDA': 25, 'SANTANDER': 26, 'SUCRE': 27, 'TOLIMA': 28, 'VALLE': 29, 'VAUPES': 30, 'VICHADA': 31, 'SAN ANDRES': 32], 
    'ESTU_DEDICACIONINTERNET':['30 minutos o menos': 0, 'Entre 1 y 3 horas': 1, 'Entre 30 y 60 minutos': 2, 'Más de 3 horas': 3, 'No Navega Internet': 4],
    'ESTU_DEDICACIONLECTURADIARIA': ['30 minutos o menos': 0, 'Entre 1 y 2 horas': 1, 'Entre 30 y 60 minutos': 2, 'Más de 2 horas': 3, 'No leo por entretenimiento': 4],
    'ESTU_DEPTO_RESIDE': ['AMAZONAS': 0, 'ANTIOQUIA': 1, 'ARAUCA': 2, 'ATLANTICO': 3, 'BOGOTÁ': 4, 'BOLIVAR': 5, 'BOYACA': 6, 'CALDAS': 7, 'CAQUETA': 8, 'CASANARE': 9, 'CAUCA': 10, 'CESAR': 11, 'CHOCO': 12, 'CORDOBA': 13, 'CUNDINAMARCA': 14, 'GUAINIA': 15, 'GUAVIARE': 16, 'HUILA': 17, 'LA GUAJIRA': 18, 'MAGDALENA': 19, 'META': 20, 'NARIÑO': 21, 'NORTE SANTANDER': 22, 'PUTUMAYO': 23, 'QUINDIO': 24, 'RISARALDA': 25, 'SANTANDER': 26, 'SUCRE': 27, 'TOLIMA': 28, 'VALLE': 29, 'VAUPES': 30, 'VICHADA': 31, 'SAN ANDRES': 32, 'EXTRANJERO': 33],
    'ESTU_HORASSEMANATRABAJA': ['0 horas': 0, 'Entre 11 y 20 horas': 1, 'Entre 21 y 30 horas': 2, 'Menos de 10 horas': 3, 'Más de 30 horas': 4],
    'ESTU_TIPOREMUNERACION': ['No': 0, 'Si, en efectivo': 1, 'Si, en efectivo y especie': 2, 'Si, en especie': 3],
    'FAMI_COMECARNEPESCADOHUEVO': ['1 o 2 veces por semana': 0, '3 a 5 veces por semana': 1, 'Nunca o rara vez comemos eso': 2, 'Todos o casi todos los días': 3],
    'FAMI_COMECEREALFRUTOSLEGUMBRE': ['1 o 2 veces por semana': 0, '3 a 5 veces por semana': 1, 'Nunca o rara vez comemos eso': 2, 'Todos o casi todos los días': 3],
    'FAMI_COMELECHEDERIVADOS': ['1 o 2 veces por semana': 0, '3 a 5 veces por semana': 1, 'Nunca o rara vez comemos eso': 2, 'Todos o casi todos los días': 3],
    'FAMI_CUARTOSHOGAR': ['Cinco': 0, 'Cuatro': 1, 'Dos': 2, 'Seis o mas': 2, 'Tres': 3, 'Uno': 4],
    'FAMI_EDUCACIONMADRE': ['Educación profesional completa': 0, 'Educación profesional incompleta': 1, 'Ninguno': 2, 'No Aplica': 3, 'No sabe': 4, 'Postgrado': 5, 'Primaria completa': 6, 'Primaria incompleta': 7, 'Secundaria (Bachillerato) completa': 8, 'Secundaria (Bachillerato) incompleta': 9, 'Técnica o tecnológica completa': 10, 'Técnica o tecnológica incompleta': 11],
    'FAMI_EDUCACIONPADRE': ['Educación profesional completa': 0, 'Educación profesional incompleta': 1, 'Ninguno': 2, 'No Aplica': 3, 'No sabe': 4, 'Postgrado': 5, 'Primaria completa': 6, 'Primaria incompleta': 7, 'Secundaria (Bachillerato) completa': 8, 'Secundaria (Bachillerato) incompleta': 9, 'Técnica o tecnológica completa': 10, 'Técnica o tecnológica incompleta': 11],
    'FAMI_ESTRATOVIVIENDA': ['Estrato 1': 0, 'Estrato 2': 1, 'Estrato 3': 2, 'Estrato 4': 3, 'Estrato 5': 4, 'Estrato 6': 5, 'Sin Estrato': 6],
    'FAMI_NUMLIBROS': ['0 A 10 LIBROS': 0, '11 A 25 LIBROS': 1, '26 A 100 LIBROS': 2, 'MÁS DE 100 LIBROS': 3],
    'FAMI_PERSONASHOGAR': ['1 a 2': 0, '3 a 4': 1, '5 a 6': 2, '7 a 8': 3, '9 o más': 4],
    'FAMI_SITUACIONECONOMICA': ['Igual': 0, 'Mejor': 1, 'Peor': 2],
    'FAMI_TRABAJOLABORMADRE': ['Es agricultor, pesquero o jornalero': 0, 'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial': 1, 'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc': 2, 'Es operario de máquinas o conduce vehículos (taxita, chofer)': 3, 'Es vendedor o trabaja en atención al público': 4, 'No aplica': 5, 'No sabe': 6, 'Pensionado': 7, 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)': 8, 'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción': 9, 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)': 10, 'Trabaja en el hogar, no trabaja o estudia': 11, 'Trabaja por cuenta propia (por ejemplo plomero, electricista)': 12],
    'FAMI_TRABAJOLABORPADRE': ['Es agricultor, pesquero o jornalero': 0, 'Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial': 1, 'Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc': 2, 'Es operario de máquinas o conduce vehículos (taxita, chofer)': 3, 'Es vendedor o trabaja en atención al público': 4, 'No aplica': 5, 'No sabe': 6, 'Pensionado': 7, 'Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)': 8, 'Trabaja como personal de limpieza, mantenimiento, seguridad o construcción': 9, 'Trabaja como profesional (por ejemplo médico, abogado, ingeniero)': 10, 'Trabaja en el hogar, no trabaja o estudia': 11, 'Trabaja por cuenta propia (por ejemplo plomero, electricista)': 12],
    'ESTU_GENERO': ['F': 0, 'M': 1],
    'FAMI_TIENEINTERNET': ['No': 0, 'Si': 1],
    'FAMI_TIENECOMPUTADOR': ['No': 0, 'Si': 1],
    'FAMI_TIENEHORNOMICROOGAS': ['No': 0, 'Si': 1],
    'FAMI_TIENEMOTOCICLETA': ['No': 0, 'Si': 1]
}

@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        # Obtener los valores seleccionados por el usuario
        edad = int(request.form['edad'])
        feature2_manual = request.form['feature2_manual']
        features = {}
        for col in categories.keys():
            selected_option = request.form.get(col, None)
            if selected_option is None:
                return "Todos los campos son obligatorios"
            mapped_value = category_mapping[col][selected_option]
            features[col] = mapped_value
        # Convertir las entradas en el formato necesario para el modelo
        input_data = pd.DataFrame(features, index=[0])
        input_data['edad'] = edad  # Añadir la edad al DataFrame
        input_data['feature2_manual'] = feature2_manual  # Añadir la variable de entrada manual
        # Realizar la predicción
        prediction = model.predict(input_data)[0]

    return render_template('index.html', categories=categories, questions=questions, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
