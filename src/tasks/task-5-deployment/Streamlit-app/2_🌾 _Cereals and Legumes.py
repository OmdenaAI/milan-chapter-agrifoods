import joblib
import numpy as np
import pandas as pd
import streamlit as st


# Cereals
cereals_ohe = joblib.load('pages/cereals_ohe.pkl')
cereals_model = open('pages/cereals_rf.pkl', 'rb')
cereals_model = joblib.load(cereals_model)


def predict(input_df):
    predictions_df = cereals_model.predict(input_df)
    return predictions_df[0]


def main():

        st.subheader("Cereal & Legumes")
        temperature_max = st.number_input('Temperature max (°C)', min_value=20, max_value=50)
        temperature_min = st.number_input('Temperature min (°C)', min_value=-5, max_value=20)
        relative_humidity = st.number_input('Relative humidity (%)', min_value=0, max_value=100)
        root_moisture = st.number_input('Root moisture', min_value=0.1, step=0.1, max_value=1.0)
        total_ha = st.number_input('Total area(ha)', min_value=0, max_value=6150)
        fertilizer_tonnes = st.number_input('Fertilizer (tonnes)', min_value=0, max_value=3405)
        fertilizer = st.selectbox('Type of fertilizer', ['organic', 'nitrogen-potassium', 'nitrogen-phosphorous'])
        crop = st.selectbox('Type of crop', ['barley', 'oats',
                                             'd-wheat', 'c-wheat', 'maize', 'potatoes', 'dry-k-bean',
                                             'bro-bean', 'chick-peas', 'rye'])
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
                                     'Trento', 'Treviso', 'Trieste', 'Udine', "Valle d'Aosta / Vallée d'Aoste",
                                     'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli',
                                     'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo'])
        output = ""

        input_dict = {'City': city, 'Type_crop': crop, 'Type_fertilizer': fertilizer}
        input_df = pd.DataFrame([input_dict])

        cereals_ohe = joblib.load('pages/cereals_ohe.pkl')
        cereals_ohe_dummies = cereals_ohe.transform(input_df)
        cereals_ohe_dummies_df = pd.DataFrame(data=cereals_ohe_dummies.toarray(),
                                              #  columns = imported_sklearn_ohe.categories_
                                              columns=[c for cat in cereals_ohe.categories_ for c in cat])

        input_numbers = pd.DataFrame(
            {'total_ha': total_ha, 'RH2M': relative_humidity, 'T2M_MAX': temperature_max, 'T2M_MIN': temperature_min,
             'GWETROOT': root_moisture, 'Fertilizers_tonnes': fertilizer_tonnes}, index=[0])

        inputs = pd.concat([input_numbers, cereals_ohe_dummies_df], axis=1)
        if st.button("Predict Cereal & Legumes"):
            output = predict(inputs)
            output = "{:.2f}".format(output) + ' tons'
            st.success('The production of the selected crop based on these inputs is {}'.format(output))


if __name__ == '__main__':
    main()
