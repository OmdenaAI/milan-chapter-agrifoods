
import pandas as pd
import streamlit as st
import joblib



#Fresh vegetables
fresh_veg_ohe = joblib.load('pages/fresh_veg_ohe.pkl')
fresh_veg_model = open('pages/fresh_veg_rf.pkl', 'rb')
fresh_veg_model = joblib.load(fresh_veg_model)

def predict(input_df):
    predictions_df = fresh_veg_model.predict(input_df)
    return predictions_df[0]


def main():
        st.subheader('Fresh Vegetables')
        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)       
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)      
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)      
        root_moisture = st.number_input('Root moisture', min_value=0.1, step = 0.1, max_value=1.0)        
        total_ha = st.number_input('Total area(ha)', min_value=0, max_value=431)       
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=3473)      
        fertilizer = st.selectbox('Type of fertilizer', ['organic','nitrogen-potassium','nitrogen-phosphorous'])       
        crop = st.selectbox('Type of crop', ['courgette-field', 'fresh-beans-field','lettuce-field','onions-field',
                                              'cauliflower&broccoli-field', 'fresh-tomato','melon-field',
                                              'egg-plant-field', 'chicory-field','red-pepper-field'])                                   
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
       
       
        output=""
        
        input_dict = {'City' : city, 'Type_crop' : crop, 'Type_fertilizer': fertilizer}
        input_df = pd.DataFrame([input_dict])
        fresh_veg_ohe = joblib.load('pages/fresh_veg_ohe.pkl')
        fresh_veg_ohe_dummies = fresh_veg_ohe.transform(input_df)
        fresh_veg_ohe_dummies_df = pd.DataFrame(data = fresh_veg_ohe_dummies.toarray(), 
                                                #  columns = imported_sklearn_ohe.categories_
                                                columns = [c for cat in fresh_veg_ohe.categories_ for c in cat])
        input_numbers = pd.DataFrame({'total_ha':total_ha, 'RH2M':relative_humidity, 'T2M_MAX':temperature_max, 'T2M_MIN':temperature_min,
                            'GWETROOT':root_moisture, 'Fertilizers_tonnes':fertilizer_tonnes}, index=[0])
        inputs = pd.concat([input_numbers, fresh_veg_ohe_dummies_df], axis=1)
        
        if st.button("Predict Fresh Vegetables"):
            output = predict(inputs)
            output = "{:.2f}".format(output) + 'tons'
            st.success('The production of the selected crop based on these inputs is  {}'.format(output))


if __name__ == '__main__':
    main()