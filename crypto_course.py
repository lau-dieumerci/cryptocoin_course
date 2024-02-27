# Importation des bibliothèques
import plotly.express as px
import streamlit as st
import pandas as pd
import joblib



try:
    # Importer  la bibliothèque pour l'interaction avec l'API de taux d'échange
    from forex_python.converter import CurrencyRates

    # Récupération du taux d'échange
    # Créer une instance de CurrencyRates
    devise_currency = CurrencyRates()
    # Obtenir le taux de change de l'USD vers l'EUR
    def usd_to_eur():
        exchange_rate = devise_currency.get_rate('USD', 'EUR')
        return exchange_rate
    usd_to_eur = usd_to_eur() 
    
except Exception as e:
    usd_to_eur = 0.9279
finally:
    # Configuration de la page
    st.set_page_config(
        page_title="CryptoCourse Coin",
        page_icon="img/cc_icon.png",
        layout="wide",
        initial_sidebar_state="expanded")




    # Importantion des données du cours du Bitcoin et modèle d'IA
    btc_data = joblib.load("btc_dataset.joblib")

    btc_data_preds = joblib.load("btc_data_preds.joblib")






    with st.sidebar:
        # Case à cocher pour l'affichage du tableau du cours du Bitcoin
        chb_cours_bitcoin = st.checkbox("Cours du Bitcoin")
        
        # Case à cocher pour l'affichage des courbes sur les données du Bitcoin
        chb_courbes = st.checkbox("Courbes")
        
        # Conteneur de nombre de jours à prédire
        with st.expander("Prédiction"):
            # Nombre de jours (en slide)
            nb_days_predicted = st.slider("Le nombre de jours à prédire",1,7)
            # slide_col = st.columns((2,3,2), gap="small")
            # with slide_col[1]:
            prediction_btn = st.button("Valider")
        # Conteneur de la gestion d'affichage des données du cours du Bitcoin        
        with st.expander("Données historiques"):
            st.title("Sélection de date minimum et maximum")
            
            # date_col = st.columns((2, 2, 4), gap="small")
            # with date_col[0]:
            #     date_min = st.button("Min")
            # with date_col[1]:
            #     date_min = st.button("Max")
            # with date_col[2]:
            #     reset_dates = st.button("Réinitialiser")
                
            min_value_date = btc_data.index[0]
            max_value_date = btc_data.index[-1]
            

            # Widget de sélection de date pour la date minimale
            date_min = st.date_input("Minimal", value=min_value_date, min_value = min_value_date, max_value=max_value_date)

            # Widget de sélection de date pour la date maximale
            date_max = st.date_input("Maximale", value=max_value_date, min_value = min_value_date, max_value=max_value_date)
            
            st.subheader("Dates choisies")
            st.write(f"Minimum : {date_min.strftime('%d/%m/%Y')}")
            st.write(f"Maximum : {date_max.strftime('%d/%m/%Y')}")
            
            viusaliser_button = st.button("Appliquer")
            if viusaliser_button:
                if (date_min < min_value_date.date() or date_min > max_value_date.date()) or (date_max < min_value_date.date() or date_max > max_value_date.date()):
                    st.warning(f"Veuillez choisir des dates comprises entre le {min_value_date.strftime('%d/%m/%Y')} et le {max_value_date.strftime('%d/%m/%Y')}")
                else:
                    if date_min > date_max :
                        st.warning(f"Veuillez choisir la date minimale inférieure à la date maximale : {date_min.strftime('%d/%m/%Y')} > {date_max.strftime('%d/%m/%Y')}")
                    else :
                        btc_data = btc_data.loc[date_min:date_max]
                        

                        
        
    logo_title = st.columns((2,10), gap = "large")
    with logo_title[0]:
        # Logo du site
        st.image("img/cc_logo.png")
    with logo_title[1]:
        # Titre de l'application
        st.title("CryptoCoin Course")
    st.subheader("Application web pour la prédiction du cours du Bitcoin")




    # Contenu de cours de Bitcoin
    if chb_cours_bitcoin:
        st.header("Cours du Bitoin")
        with st.expander("Données historiques"):
            # Les options de devises
            options_devise = ['USD', 'EUR'] 
            
            # Les radio pour le choix de la devise
            radio_devise_choice = st.radio("Choix de devise", options_devise)
            
            if radio_devise_choice == 'EUR':

            

                
                # Données historiques du Bitcoin en euros
                btc_data_eur = btc_data
            
            
                btc_data_eur[['Open', 'High', 'Low', 'Close', 'Adj Close']] = btc_data_eur[['Open', 'High', 'Low', 'Close', 'Adj Close']] * usd_to_eur
                
                
                
                # Le dataframe à utiliser pour la prédiction
                btc_data_used = btc_data_eur
                btc_data_used.index = btc_data_used.index.strftime("%d/%m/%Y")
                st.dataframe(btc_data_used)
            else:
                st.subheader("Données historiques du Bitcoin (USD)")
                
                btc_data_used = btc_data
                btc_data_used.index = btc_data_used.index.strftime("%d/%m/%Y")
                st.dataframe(btc_data_used)
                
    # Contenu de courbes
    if chb_courbes:
        # Titre de courbes 
        st.header("Courbes et graphiques")
        
        # Sélection de type de graphique
        grapgh_type_radio = st.radio(
        'Sélectionner un type de graphique',
        ('Nuage de points', 'Graphique en ligne', 'Histogramme')
        )
        
        # Vérification de type de graphe choisi, et gestion de son affichage
        
        # Cas de 'Nuage de points' et 'Graphique en ligne'
        if grapgh_type_radio == 'Nuage de points' or grapgh_type_radio == 'Graphique en ligne' :
            # Liste des colonnes concernées
            btc_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close']
            
            # Box de sélection d'une colonne au niveau de l'abscisse
            x_coord = st.selectbox(
            "En abscisse",
            btc_columns
            )

            # Box de sélection d'une colonne au niveau de l'ordonnée
            y_coord = st.selectbox(
                "En ordonnée",
                btc_data.columns
            )
            
            # Gestion du cas de 'nuage de points'
            if grapgh_type_radio == 'Nuage de points':
                # Gestion du cas de 'Date' en abscisse
                if x_coord == "Date":
                    # Récupération des données de l'index de dataframe des données de Bitcoin
                    date_absciss = btc_data.index
                    # Création du graphique de nuage de points
                    fig_scatter = px.scatter(btc_data, x=date_absciss, y=y_coord, title="Nuage de points du cours du Bitcoin")
                    # Formater les étiquettes de l'axe des x
                    fig_scatter.update_xaxes(
                        dtick="M3",
                        tickformat="%d/%m/%Y"
                    )
                else:
                    # Création du graphique de nuage de points
                    fig_scatter = px.scatter(btc_data, x=x_coord, y=y_coord, title="Nuage de points du cours du Bitcoin")
                    
                # Affichage du graphique
                st.plotly_chart(fig_scatter)
                
            # Gesion du cas de 'graphique en ligne
            else:
                # Gestion du cas de 'Date' en abscisse
                if x_coord == "Date":
                    # Récupération des données de l'index de dataframe des données de Bitcoin
                    date_absciss = btc_data.index
                    # Création du graphique de nuage de points
                    fig_line = px.line(btc_data, x=date_absciss, y=y_coord, title="Graphique en ligne du cours du Bitcoin")
                    # Formater les étiquettes de l'axe des x
                    fig_line.update_xaxes(
                        dtick="M3",
                        tickformat="%d/%m/%Y"
                    )
                else:
                    # Création du graphique de nuage de points
                    fig_line = px.line(btc_data, x=x_coord, y=y_coord, title="Graphique en ligne du cours du Bitcoin")
                # Affichage du graphique
                st.plotly_chart(fig_line)
                    
        # Cas de l'Histogramme
        else:
            column_coord = st.selectbox(
                "Choisir la colonne",
                btc_data.columns
            )
            
            fig_histogram = px.histogram(btc_data, x=column_coord, title="Histogramme du cours du Bitcoin")
            st.plotly_chart(fig_histogram)
            
            
    


    ####
    ##### Section de Prédiction
    ####
    if prediction_btn:
        st.header("Prédiction du prix du Bitcoin")
        if nb_days_predicted == 1:
            st.subheader("Prédiction du prochain jour")
        else:
            st.subheader(f"Prédiction de {nb_days_predicted} prochains jours")
        btc_preds = pd.DataFrame({
            'Prix prédit' : btc_data_preds.iloc[:nb_days_predicted]['Close']
            })
        
        # Définir le nom d'index de btc_preds
        btc_preds.index.name= "Date"
        btc_preds.index = pd.to_datetime(btc_preds.index).strftime("%d/%m/%Y")


        st.dataframe(btc_preds)


        


        


