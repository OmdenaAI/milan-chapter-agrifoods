
from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np

from PIL import Image
#image = Image.open('omdena_logo.png')
#st.set_page_config(page_title='omdena-milan', page_icon=image)


    
model1 = load_model('data/models/cereals_knn')
model2= load_model('data/models/fruits&nuts_knn')
model3 = load_model('data/models/grapes_olives_et')
model4 = load_model('data/models/fresh_veg_et')
model5 = load_model('data/models/industrial_crop_et')


def predict1(model1, input_df1):
    predictions_df1 = predict_model(estimator=model1, data=input_df1)
    predictions1 = predictions_df1['prediction_label'][0]
    return predictions1

def predict2(model2, input_df2):
    predictions_df2= predict_model(estimator=model2, data=input_df2)
    predictions2 = predictions_df2['prediction_label'][0]
    return predictions2

def predict3(model3, input_df3):
    predictions_df3 = predict_model(estimator=model3, data=input_df3)
    predictions3 = predictions_df3['prediction_label'][0]
    return predictions3

def predict4(model4, input_df4):
    predictions_df4= predict_model(estimator=model4, data=input_df4)
    predictions4 = predictions_df4['prediction_label'][0]
    return predictions4

def predict5(model5, input_df5):
    predictions_df5= predict_model(estimator=model5, data=input_df5)
    predictions5 = predictions_df5['prediction_label'][0]
    return predictions5


def run():
    
    
  
    add_selectbox = st.sidebar.selectbox(
    "Please choose your crop",
    ("Cereal & Legumes", "Fruits & Nuts", "Grapes & Olives", "Fresh Vegetables","Industrial crops", ))
    
    st.sidebar.info('Omdena-Milan Agrifood')
    st.sidebar.success('https://omdena.com/local-chapters/milan-italy-chapter/')
    
    st.title("Crop Prediction")
        
    if add_selectbox == 'Cereal & Legumes':

        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)
        
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)
        
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)
       
        root_moisture = st.number_input('Root moisture', max_value=1)
        
        total_area_ha = st.number_input('Total area(ha)', min_value=0, max_value=6150)
        
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=3405)
        
        fertilizer = st.selectbox('Type of fertilizer', ['calcium cyanamide', 'nitrogen-potassium', 'peaty-amend',
                                                 'organic-nitrogen', 'organic', 'ammonium sulphate',
                                                 'nitrogen-phosphorous', 'phosphorus-potassium', 'urea'])
        
        crop = st.selectbox('Type of crop', ['barley', 'bro-bean', 'chick-peas', 'dry-k-bean', 'd-wheat',
                                     'early potatoes', 'lentil', 'oats', 'potatoes', 'grain pea',
                                     'oats mix', 'spring barley', 'winter barley', 'c-wheat', 'maize',
                                     'protein pea', 'rice', 'sorghum', 'sugar beet', 'other cereals',
                                     'rye', 'titicale', 'c-spr-wheat&spelt', 'c-wint-wheat&spelt',
                                     'sweet potatoes', 'sweet lupin', 'rye mix', 'cereal mix',
                                     'wint-cereal-mix'])
                                     
        city = st.selectbox('City', ['Agrigento', 'Alessandria', 'Ancona', 'Arezzo', 'Ascoli Piceno',
                                     'Asti', 'Avellino', 'Bari', 'Barletta-Andria-Trani', 'Belluno',
                                     'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano / Bozen',
                                     'Brescia', 'Brindisi', 'Cagliari', 'Caltanissetta', 'Campobasso',
                                     'Carbonia-Iglesias', 'Caserta', 'Catania', 'Catanzaro', 'Chieti',
                                     'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo', 'Enna', 'Fermo',
                                     'Ferrara', 'Firenze', 'Foggia', 'Forlì-Cesena', 'Frosinone',
                                     'Genova', 'Gorizia', 'Grosseto', 'Imperia', 'Isernia', "L'Aquila",
                                     'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi',
                                     'Lucca', 'Macerata', 'Mantova', 'Massa-Carrara', 'Matera',
                                     'Medio Campidano', 'Messina', 'Milano', 'Modena',
                                     'Monza e della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Ogliastra',
                                     'Olbia-Tempio', 'Oristano', 'Padova', 'Palermo', 'Parma', 'Pavia',
                                     'Perugia', 'Pesaro e Urbino', 'Pescara', 'Piacenza', 'Pisa',
                                     'Pistoia', 'Pordenone', 'Potenza', 'Prato', 'Ragusa', 'Ravenna',
                                     'Reggio di Calabria', "Reggio nell'Emilia", 'Rieti', 'Rimini',
                                     'Roma', 'Rovigo', 'Salerno', 'Sassari', 'Savona', 'Siena',
                                     'Siracusa', 'Sondrio', 'Sud Sardegna', 'Taranto', 'Teramo',
                                     'Terni', 'Torino', 'Trapani', 'Trentino Alto Adige / Südtirol',
                                     'Trento', 'Treviso', 'Trieste', 'Udine',"Valle d'Aosta / Vallée d'Aoste",
                                     'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 
                                     'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo'])
        output1=""
    
        input_dict1 = {'T2M_MAX': temperature_max, 'T2M_MIN':temperature_min,'RH2M' : relative_humidity, 'total_area_ha': total_area_ha,
                      'GWETROOT' : root_moisture, 'Type_crop' : crop, 'Type_fertilizer': fertilizer, 'Fertilizers_tonnes': fertilizer_tonnes ,'City' : city}
        input_df1 = pd.DataFrame([input_dict1])

        if st.button("Predict Cereal & Legumes"):
            output1 = predict1(model1=model1, input_df1=input_df1)
            output1 = 'Tons ' + "{:.2f}".format(output1)
        
        st.success('The output is {}'.format(output1))
        
    if add_selectbox == 'Fruits & Nuts':

        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)
        
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)
        
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)
       
        root_moisture = st.number_input('Root moisture', max_value=1)
        
        total_area_ha = st.number_input('Total area(ha)', min_value=0, max_value=430)
        
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=3477)
        
        fertilizer = st.selectbox('Type of fertilizer', ['calcium cyanamide', 'nitrogen-potassium', 'peaty-amend',
                                                 'organic-nitrogen', 'organic', 'ammonium sulphate',
                                                 'nitrogen-phosphorous', 'phosphorus-potassium', 'urea'])
        
        crop = st.selectbox('Type of crop', ['apple', 'apricot', 'cherry in complex', 'kiwi', 'nectarine',
                                             'plum', 'hazelnut', 'pear', 'peach', 'almond'])
                                     
        city = st.selectbox('City', ['Agrigento', 'Alessandria', 'Ancona', 'Arezzo', 'Ascoli Piceno',
                                     'Asti', 'Avellino', 'Bari', 'Belluno', 'Benevento', 'Bergamo',
                                     'Biella', 'Bologna', 'Brescia', 'Brindisi', 'Caltanissetta',
                                     'Campobasso', 'Caserta', 'Catania', 'Catanzaro', 'Chieti', 'Como',
                                     'Cosenza', 'Cremona', 'Crotone', 'Enna', 'Ferrara', 'Firenze', 
                                     'Foggia', 'Frosinone', 'Genova', 'Gorizia', 'Grosseto', 'Imperia', 
                                     'Isernia', 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 
                                     'Lodi', 'Lucca', 'Macerata', 'Mantova', 'Matera', 'Messina', 
                                     'Milano', 'Modena', 'Napoli', 'Novara', 'Nuoro', 'Oristano',
                                     'Padova', 'Palermo', 'Parma', 'Pavia', 'Perugia', 
                                     'Pesaro e Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 
                                     'Pordenone', 'Potenza', 'Prato', 'Ragusa', 'Ravenna', 
                                     'Reggio di Calabria', "Reggio nell'Emilia", 'Rieti', 'Rimini', 
                                     'Roma', 'Rovigo', 'Salerno', 'Sassari', 'Savona', 'Siena', 
                                     'Siracusa', 'Taranto', 'Teramo', 'Terni', 'Torino', 'Trapani', 
                                     'Treviso', 'Trieste', 'Udine', 'Varese', 'Venezia', 
                                     'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Vibo Valentia', 
                                     'Vicenza', 'Viterbo', 'Carbonia-Iglesias', 'Medio Campidano', 
                                     'Ogliastra', 'Olbia-Tempio', 'Barletta-Andria-Trani', 'Fermo', 
                                     'Monza e della Brianza'])
        
        
        output2=""
    
        input_dict2 = {'T2M_MAX': temperature_max, 'T2M_MIN':temperature_min,'RH2M' : relative_humidity, 'total_area_ha': total_area_ha,
                      'GWETROOT' : root_moisture, 'Type_crop' : crop, 'Type_fertilizer': fertilizer, 'Fertilizers_tonnes': fertilizer_tonnes ,'City' : city}
        input_df2 = pd.DataFrame([input_dict2])

        if st.button("Predict Fruits & Nuts"):
            output2 = predict2(model2=model2, input_df2=input_df2)
            output2 = 'Tons ' + "{:.2f}".format(output2)
        
        st.success('The output is {}'.format(output2))
        
        
    if add_selectbox == 'Grapes & Olives':

        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)
        
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)
        
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)
       
        root_moisture = st.number_input('Root moisture', max_value=1)
        
        total_area_ha = st.number_input('Total area(ha)', min_value=0, max_value=5010)
        
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=2852)
        
        fertilizer = st.selectbox('Type of fertilizer', ['calcium cyanamide', 'nitrogen-potassium', 'peaty-amend',
                                                 'organic-nitrogen', 'organic', 'ammonium sulphate',
                                                 'nitrogen-phosphorous', 'phosphorus-potassium', 'urea'])
        
        crop = st.selectbox('Type of crop', ['grapes-n.e.c', 'grapes-wines(N-pdo/pgi)', 'table olives',
                                             'grapes-table', 'oil olives', 'other olives',
                                             'grapes-wines(Y-pdo)', 'grapes-wines(Y-pgi)', 'grapes-raisins'])
                                     
        city = st.selectbox('City', ['Agrigento', 'Alessandria', 'Ancona', 'Arezzo', 'Ascoli Piceno',
                                     'Asti', 'Avellino', 'Bari', 'Belluno', 'Benevento', 'Bergamo', 
                                     'Biella', 'Bologna', 'Brescia', 'Brindisi', 'Caltanissetta', 
                                     'Campobasso', 'Caserta', 'Catania', 'Catanzaro', 'Chieti', 
                                     'Cosenza', 'Cremona', 'Crotone', 'Enna', 'Ferrara', 'Firenze',
                                     'Foggia', 'Frosinone', 'Genova', 'Grosseto', 'Imperia', 'Isernia',
                                     'La Spezia', 'Latina', 'Lecce', 'Livorno', 'Lodi', 'Lucca', 
                                     'Macerata', 'Mantova', 'Matera', 'Messina', 'Milano', 'Modena', 
                                     'Napoli', 'Novara', 'Nuoro', 'Oristano', 'Padova', 'Palermo', 
                                     'Parma', 'Pavia', 'Perugia', 'Pesaro e Urbino', 'Pescara', 
                                     'Piacenza', 'Pisa', 'Pistoia', 'Pordenone', 'Potenza', 'Prato', 
                                     'Ragusa', 'Ravenna', 'Reggio di Calabria', "Reggio nell'Emilia", 
                                     'Rieti', 'Rimini', 'Roma', 'Rovigo', 'Salerno', 'Sassari', 
                                     'Savona', 'Siena', 'Siracusa', 'Taranto', 'Teramo', 'Terni', 
                                     'Torino', 'Trapani', 'Treviso', 'Trieste', 'Udine', 'Varese', 
                                     'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 
                                     'Vibo Valentia', 'Vicenza', 'Viterbo', 'Carbonia-Iglesias', 
                                     'Medio Campidano', 'Ogliastra', 'Olbia-Tempio', 
                                     'Barletta-Andria-Trani', 'Fermo', 'Monza e della Brianza'])
        
        
        output3=""
    
        input_dict3 = {'T2M_MAX': temperature_max, 'T2M_MIN':temperature_min,'RH2M' : relative_humidity, 'total_area_ha': total_area_ha,
                      'GWETROOT' : root_moisture, 'Type_crop' : crop, 'Type_fertilizer': fertilizer, 'Fertilizers_tonnes': fertilizer_tonnes ,'City' : city}
        input_df3 = pd.DataFrame([input_dict3])

        if st.button("Predict Grapes & Olives"):
            output3 = predict3(model3=model3, input_df3=input_df3)
            output3 = 'Tons ' + "{:.2f}".format(output3)
        
        st.success('The output is {}'.format(output3))
        
        
        
    if add_selectbox == 'Fresh Vegetables':

        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)
        
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)
        
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)
       
        root_moisture = st.number_input('Root moisture', max_value=1)
        
        total_area_ha = st.number_input('Total area(ha)', min_value=0, max_value=431)
        
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=3473)
        
        fertilizer = st.selectbox('Type of fertilizer', ['calcium cyanamide', 'nitrogen-potassium', 'peaty-amend',
                                                 'organic-nitrogen', 'organic', 'ammonium sulphate',
                                                 'nitrogen-phosphorous', 'phosphorus-potassium', 'urea'])
        
        crop = st.selectbox('Type of crop', ['cauliflower&broccoli-field', 'courgette-field', 'egg-plant-field',
                                             'fresh-beans-field', 'lettuce-field', 'onions-field', 
                                             'red-pepper-field', 'chicory-field', 'melon-field', 'fresh-tomato'])
                                     
        city = st.selectbox('City', ['Agrigento', 'Alessandria', 'Ancona', 'Arezzo', 'Ascoli Piceno', 
                                     'Asti', 'Avellino', 'Bari', 'Belluno', 'Benevento', 'Bergamo', 
                                     'Biella', 'Bologna', 'Brescia', 'Brindisi', 'Caltanissetta', 
                                     'Campobasso', 'Caserta', 'Catania', 'Catanzaro', 'Chieti', 
                                     'Cosenza', 'Cremona', 'Crotone', 'Enna', 'Ferrara', 'Firenze', 
                                     'Foggia', 'Frosinone', 'Genova', 'Gorizia', 'Grosseto', 'Imperia', 
                                     'Isernia', 'La Spezia', 'Latina', 'Lecce', 'Livorno', 'Lodi', 
                                     'Lucca', 'Macerata', 'Mantova', 'Matera', 'Messina', 'Milano',
                                     'Modena', 'Napoli', 'Novara', 'Nuoro', 'Oristano', 'Padova', 
                                     'Palermo', 'Parma', 'Pavia', 'Perugia', 'Pesaro e Urbino', 
                                     'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 'Pordenone', 'Potenza', 
                                     'Prato', 'Ragusa', 'Ravenna', 'Reggio di Calabria', 
                                     "Reggio nell'Emilia", 'Rimini', 'Roma', 'Rovigo', 'Salerno', 
                                     'Sassari', 'Savona', 'Siena', 'Siracusa', 'Taranto', 'Teramo', 
                                     'Terni', 'Torino', 'Trapani', 'Treviso', 'Trieste', 'Udine', 
                                     'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona',
                                     'Vibo Valentia', 'Vicenza', 'Viterbo', 'Carbonia-Iglesias', 
                                     'Medio Campidano', 'Ogliastra', 'Olbia-Tempio', 'Barletta-Andria-Trani', 
                                     'Fermo', 'Monza e della Brianza'])
        
        
        output4=""
    
        input_dict4 = {'T2M_MAX': temperature_max, 'T2M_MIN':temperature_min,'RH2M' : relative_humidity, 'total_area_ha': total_area_ha,
                      'GWETROOT' : root_moisture, 'Type_crop' : crop, 'Type_fertilizer': fertilizer, 'Fertilizers_tonnes': fertilizer_tonnes ,'City' : city}
        input_df4 = pd.DataFrame([input_dict4])

        if st.button("Predict Fresh Vegetables"):
            output4 = predict4(model4=model4, input_df4=input_df4)
            output4 = 'Tons ' + "{:.2f}".format(output4)
        
        st.success('The output is {}'.format(output4))
        
        
        
    if add_selectbox == 'Industrial crops':

        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)
        
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)
        
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)
       
        root_moisture = st.number_input('Root moisture', max_value=1)
        
        total_area_ha = st.number_input('Total area(ha)', min_value=0, max_value=1440)
        
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=4824)
        
        fertilizer = st.selectbox('Type of fertilizer', ['calcium cyanamide', 'nitrogen-potassium', 'peaty-amend',
                                                 'organic-nitrogen', 'organic', 'ammonium sulphate',
                                                 'nitrogen-phosphorous', 'phosphorus-potassium', 'urea'])
        
        crop = st.selectbox('Type of crop', ['hemp', 'rape', 'soya beans', 'tobacco', 'flax', 'parsley-field',
                                             'sunflower'])
                                     
        city = st.selectbox('City', ['Alessandria', 'Ancona', 'Arezzo', 'Ascoli Piceno', 'Asti',
                                     'Avellino', 'Bari', 'Belluno', 'Benevento', 'Bergamo', 'Biella',
                                     'Bologna', 'Brescia', 'Caltanissetta', 'Campobasso', 'Caserta', 
                                     'Catania', 'Catanzaro', 'Chieti', 'Como', 'Cosenza', 'Cremona', 
                                     'Crotone', 'Ferrara', 'Firenze', 'Foggia', 'Frosinone', 'Genova', 
                                     'Gorizia', 'Grosseto', 'Imperia', 'Isernia', 'Latina', 'Lecco', 
                                     'Livorno', 'Lodi', 'Lucca', 'Macerata', 'Mantova', 'Matera', 
                                     'Milano', 'Modena', 'Napoli', 'Novara', 'Nuoro', 'Oristano', 
                                     'Padova', 'Parma', 'Pavia', 'Perugia', 'Pescara', 'Piacenza', 
                                     'Pisa', 'Pistoia', 'Pordenone', 'Potenza', 'Prato', 'Ravenna', 
                                     "Reggio nell'Emilia", 'Rieti', 'Rimini', 'Roma', 'Rovigo', 
                                     'Salerno', 'Sassari', 'Savona', 'Siena', 'Taranto', 'Teramo', 
                                     'Terni', 'Torino', 'Treviso', 'Trieste', 'Udine', 'Varese', 
                                     'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Vicenza', 
                                     'Viterbo', 'Carbonia-Iglesias', 'Medio Campidano', 'Ogliastra', 
                                     'Vibo Valentia', 'Barletta-Andria-Trani', 'Fermo', 
                                     'Monza e della Brianza', 'La Spezia'])
        
        
        output5=""
    
        input_dict5 = {'T2M_MAX': temperature_max, 'T2M_MIN':temperature_min,'RH2M' : relative_humidity, 'total_area_ha': total_area_ha,
                      'GWETROOT' : root_moisture, 'Type_crop' : crop, 'Type_fertilizer': fertilizer, 'Fertilizers_tonnes': fertilizer_tonnes ,'City' : city}
        input_df5 = pd.DataFrame([input_dict5])

        if st.button("Predict Industrial crops"):
            output5 = predict5(model5=model5, input_df5=input_df5)
            output5 = 'Tons ' + "{:.2f}".format(output5)
        
        st.success('The output is {}'.format(output5))

if __name__ == '__main__':
    
    run()
    
