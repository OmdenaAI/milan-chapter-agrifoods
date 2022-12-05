import os
import numpy as np
import pandas as pd
import streamlit as st
import joblib
import warnings
from PIL import Image


#Grapes
grapes_ohe = joblib.load('pages/grapes_ohe.pkl')
grapes_model = open('pages/grapes_rf.pkl', 'rb')
grapes_model = joblib.load(grapes_model)

def predict(input_df):
    predictions_df = grapes_model.predict(input_df)
    return predictions_df[0]


def main():
        st.subheader('Grapes')
        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)       
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)       
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)      
        root_moisture = st.number_input('Root moisture', min_value=0.1, step = 0.1, max_value=1.0)       
        total_ha = st.number_input('Total area(ha)', min_value=0, max_value=5010)        
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=2852)       
        fertilizer = st.selectbox('Type of fertilizer', ['organic','nitrogen-potassium','nitrogen-phosphorous'])      
        crop = st.selectbox('Type of crop', ['grapes-table'])                                    
        city = st.selectbox('City', ['Ascoli Piceno', 'Pescara', 'Novara', 'Firenze', 'Latina',
                                     'Sassari', 'Pordenone', 'Carbonia-Iglesias', 'Treviso',
                                     'Benevento', 'Imperia', 'Siracusa', 'Vibo Valentia', 'Vicenza',
                                     'Ogliastra', 'Piacenza', 'Padova', 'Olbia-Tempio', 'Trapani',
                                     'Lecce', 'Avellino', 'Vercelli', 'Viterbo', 'Arezzo', 'Livorno',
                                     'Enna', 'Cosenza', 'Genova', 'Asti', 'Caserta', 'Frosinone',
                                     'Macerata', 'Medio Campidano', 'Udine', 'Reggio di Calabria',
                                     'Catanzaro', 'Messina', 'Verona', 'Potenza', 'Campobasso',
                                     'Grosseto', 'Teramo', 'Verbano-Cusio-Ossola', 'Pistoia', 'Parma',
                                     'Ravenna', 'Oristano', 'Palermo', 'Rovigo', 'Crotone', 'Mantova',
                                     'Salerno', 'Biella', 'Isernia', 'Alessandria', 'Pisa', 'Lucca',
                                     'Perugia', 'Venezia', 'Nuoro', 'Napoli', 'Savona', 'Torino',
                                       'Fermo'])
       
       
        output=""
   
        input_dict = {'City' : city, 'Type_crop' : crop, 'Type_fertilizer': fertilizer}
        input_df = pd.DataFrame([input_dict])

        grapes_ohe = joblib.load('pages/grapes_ohe.pkl')
        grapes_ohe_dummies = grapes_ohe.transform(input_df)
        grapes_ohe_dummies_df = pd.DataFrame(data = grapes_ohe_dummies.toarray(), 
                                                #  columns = imported_sklearn_ohe.categories_
                                                columns = [c for cat in grapes_ohe.categories_ for c in cat])

        input_numbers = pd.DataFrame({'total_ha':total_ha, 'RH2M':relative_humidity, 'T2M_MAX':temperature_max, 'T2M_MIN':temperature_min,
                            'GWETROOT':root_moisture, 'Fertilizers_tonnes':fertilizer_tonnes}, index=[0])
        inputs = pd.concat([input_numbers, grapes_ohe_dummies_df], axis=1)        
        if st.button("Predict Grapes"):
            output = predict(inputs)
            output = "{:.2f}".format(output)+ ' tons'
            st.success('The production of the selected crop based on these inputs is {}'.format(output))
               
                     
if __name__ == '__main__':
    
    main()                     