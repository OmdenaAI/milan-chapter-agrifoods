
import pandas as pd
import streamlit as st
import joblib



#Industrial crop
industrial_crop_ohe = joblib.load('pages/industrial_crop_ohe.pkl')
industrial_crop_model = open('pages/industrial_crop_rf.pkl', 'rb')
industrial_crop_model = joblib.load(industrial_crop_model)

def predict(input_df):
    predictions_df = industrial_crop_model.predict(input_df)
    return predictions_df[0]


def main():
        st.subheader('Industrial crops')
        temperature_max = st.number_input('Temperature max (°C)', min_value= 20, max_value= 50)        
        temperature_min = st.number_input('Temperature min (°C)', min_value= -5, max_value= 20)       
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)      
        root_moisture = st.number_input('Root moisture', min_value=0.1, step = 0.1, max_value=1.0)       
        total_ha = st.number_input('Total area(ha)', min_value=0, max_value=1440)       
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=4824)       
        fertilizer = st.selectbox('Type of fertilizer', ['organic','nitrogen-potassium','nitrogen-phosphorous'])       
        crop = st.selectbox('Type of crop', [ 'sunflower', 'rape',
                                             'soya beans', 'hemp', 'parsley-field', 
                                             'parsley-ghouse', 'tobacco', 'flax'])                                    
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
        
        
        output=""
    
        input_dict = {'City' : city, 'Type_crop' : crop, 'Type_fertilizer': fertilizer}
        input_df = pd.DataFrame([input_dict])
        industrial_crop_ohe = joblib.load('pages/industrial_crop_ohe.pkl')
        industrial_crop_ohe_dummies = industrial_crop_ohe.transform(input_df)
        industrial_crop_ohe_dummies_df = pd.DataFrame(data = industrial_crop_ohe_dummies.toarray(), 
                                                #  columns = imported_sklearn_ohe.categories_
                                                columns = [c for cat in industrial_crop_ohe.categories_ for c in cat])

        input_numbers = pd.DataFrame({'total_ha':total_ha, 'RH2M':relative_humidity, 'T2M_MAX':temperature_max, 'T2M_MIN':temperature_min,
                            'GWETROOT':root_moisture, 'Fertilizers_tonnes':fertilizer_tonnes}, index=[0])
        inputs = pd.concat([input_numbers, industrial_crop_ohe_dummies_df], axis=1)        
        if st.button("Predict Industrial crops"):
            output = predict(inputs)
            output = "{:.2f}".format(output) + 'tons'
            st.success('The production of the selected crop based on these inputs is  {}'.format(output))
            

    
if __name__ == '__main__':
    
    main()
                 
   