import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def db_connect():
    import os
    engine = create_engine(os.getenv('DATABASE_URL'))
    engine.connect()
    return engine

def get_keys_from_value(dictionary, value_to_find):
    return [key for key, val in dictionary.items() if val == value_to_find]

def predict_with_dt(length, weight, age_class, sex, habitat_type, country_region, model_genus, model_common_name, category_mapping):
    """
    Predicts the Genus and Common Name of a crocodile using a pre-trained Decision Tree model.

    Args:
        length (float): Observed length of the crocodile in meters.
        weight (float): Observed weight of the crocodile in kilograms.
        age_class (str): Age class of the crocodile (e.g., 'Adult', 'Juvenile').
        sex (str): Sex of the crocodile (e.g., 'Male', 'Female').
        habitat_type (str): Type of habitat where the crocodile was observed (e.g., 'Rivers', 'Swamps').
        country_region (str): Country or region where the crocodile was observed (e.g., 'Australia', 'Africa').
        model_genus (DecisionTreeClassifier): Pre-trained Decision Tree model for Genus prediction.
        model_common_name (DecisionTreeClassifier): Pre-trained Decision Tree model for Common Name prediction.
        category_mapping (dict): Dictionary containing the mapping of categorical values to numerical codes.

    Returns:
        tuple: A tuple containing the predicted Genus and Common Name.
    """

    # Convert input strings to numerical categories using the provided mapping
    age_class_encoded = get_keys_from_value(category_mapping['Age Class'], age_class)[0]
    sex_encoded = get_keys_from_value(category_mapping['Sex'],sex)[0]
    habitat_type_encoded = get_keys_from_value(category_mapping['Habitat Type'],habitat_type)[0]
    country_region_encoded = get_keys_from_value(category_mapping['Country/Region'],country_region)[0]


    # Create a feature array from the input values
    features = np.array([length, weight, age_class_encoded, sex_encoded, habitat_type_encoded, country_region_encoded]).reshape(1, -1)

    # Predict the Genus and Common Name using the pre-trained models
    genus_encoded = model_genus.predict(features)[0]
    common_name_encoded = model_common_name.predict(features)[0]

    genus =  category_mapping['Genus'][genus_encoded]
    common_name = category_mapping['Common Name'][common_name_encoded]

    return genus, common_name


category_mapping = {'Age Class': {0: 'Adult', 1: 'Hatchling', 2: 'Juvenile', 3: 'Subadult'}, 'Sex': {0: 'Female', 1: 'Male', 2: 'Unknown'}, 'Genus': {0: 'Crocodylus', 1: 'Mecistops', 2: 'Osteolaemus'}, 'Common Name': {0: 'American Crocodile', 1: 'Borneo Crocodile (disputed)', 2: 'Central African Slender-snouted Crocodile', 3: 'Congo Dwarf Crocodile', 4: 'Cuban Crocodile', 5: "Freshwater Crocodile (Johnstone's)", 6: "Hall's New Guinea Crocodile", 7: "Morelet's Crocodile", 8: 'Mugger Crocodile (Marsh Crocodile)', 9: 'New Guinea Crocodile', 10: 'Nile Crocodile', 11: 'Orinoco Crocodile', 12: 'Philippine Crocodile', 13: 'Saltwater Crocodile', 14: 'Siamese Crocodile', 15: 'West African Crocodile', 16: 'West African Dwarf Crocodile', 17: 'West African Slender-snouted Crocodile'}, 'Habitat Type': {0: 'Billabongs', 1: 'Brackish Rivers', 2: 'Coastal Lagoons', 3: 'Coastal Wetlands', 4: 'Estuaries', 5: 'Estuarine Systems', 6: 'Flooded Savannas', 7: 'Forest Rivers', 8: 'Forest Swamps', 9: 'Freshwater Marshes', 10: 'Freshwater Rivers', 11: 'Freshwater Wetlands', 12: 'Gorges', 13: 'Lagoons', 14: 'Lakes', 15: 'Large Rivers', 16: 'Mangroves', 17: 'Marshes', 18: 'Oases', 19: 'Oxbow Lakes', 20: 'Ponds', 21: 'Reservoirs', 22: 'Rivers', 23: 'Shaded Forest Rivers', 24: 'Slow Rivers', 25: 'Slow Streams', 26: 'Small Streams', 27: 'Swamps', 28: 'Tidal Rivers'}, 'Country/Region': {0: 'Australia', 1: 'Belize', 2: 'Cambodia', 3: 'Cameroon', 4: 'Central African Republic', 5: 'Chad', 6: 'Colombia', 7: 'Congo (DRC)', 8: 'Congo Basin Countries', 9: 'Costa Rica', 10: 'Cuba', 11: "Côte d'Ivoire", 12: 'Egypt', 13: 'Gabon', 14: 'Ghana', 15: 'Guatemala', 16: 'Guinea', 17: 'India', 18: 'Indonesia', 19: 'Indonesia (Borneo)', 20: 'Indonesia (Papua)', 21: 'Iran (historic)', 22: 'Kenya', 23: 'Laos', 24: 'Liberia', 25: 'Malaysia', 26: 'Malaysia (Borneo)', 27: 'Mali', 28: 'Mauritania', 29: 'Mexico', 30: 'Nepal', 31: 'Niger', 32: 'Nigeria', 33: 'Pakistan', 34: 'Papua New Guinea', 35: 'Philippines', 36: 'Senegal', 37: 'Sierra Leone', 38: 'South Africa', 39: 'Sri Lanka', 40: 'Sudan', 41: 'Tanzania', 42: 'Thailand', 43: 'USA (Florida)', 44: 'Uganda', 45: 'Venezuela', 46: 'Vietnam'}}