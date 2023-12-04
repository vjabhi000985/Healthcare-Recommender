# Health Recommender System

![Screenshot (6)](https://github.com/vjabhi000985/Healthcare-Recommender/assets/46738718/8a96196e-9b6a-4a82-8e8d-3670c6e74f01)

## Overview

This Health Recommender System is built using filtering techniques and nearest neighbors, providing personalized recommendations for medicine, workouts, custom diet suggestions, and food recommendations.

## Tech Stack

- HTML
- CSS
- Python
- Machine Learning libraries (e.g., scikit-learn)
- Streamlit (for the frontend)
- JSON dataset and CSV dataset (Available in private healthcare repo)

## System Requirements

- Python 3.x
- IDE - Pycharm or Sublime Text 4
- Jupyter Notebook or Colab Notebook
- Required Python libraries (install using `pip install -r requirements.txt`):
  - scikit-learn
  - streamlit
  - Plotly for visualization
 
## Video Demonstration
[![Introduction Video](https://cms-api-in.myhealthcare.co/image/20220910103120.jpeg)](https://youtu.be/G0l0-1vjxHA)
Click here to view

## Code Snippets

### Example 1: Loading and Preprocessing Data

```python
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
prep_data=scaler.fit_transform(extracted_data.iloc[:,6:15].to_numpy())
```
### Example 2: Creating an end to end function
```python
def scaling(dataframe):
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(dataframe.iloc[:,6:15].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,ingredient_filter,max_nutritional_values):
    extracted_data=dataframe.copy()
    for column,maximum in zip(extracted_data.columns[6:15],max_nutritional_values):
        extracted_data=extracted_data[extracted_data[column]<maximum]
    if ingredient_filter!=None:
        for ingredient in ingredient_filter:
            extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient,regex=False)] 
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommand(dataframe,_input,max_nutritional_values,ingredient_filter=None,params={'return_distance':False}):
    extracted_data=extract_data(dataframe,ingredient_filter,max_nutritional_values)
    prep_data,scaler=scaling(extracted_data)
    neigh=nn_predictor(prep_data)
    pipeline=build_pipeline(neigh,scaler,params)
    return apply_pipeline(pipeline,_input,extracted_data)
```
### Example 3: Streamlit app
```python
import streamlit as st
from streamlit_option_menu import option_menu
import json
import pandas as pd
from test import *
from Custom_Diet import *
from PIL import Image

# Page Basic info
st.set_page_config(
	page_title = 'Healthcare Recommender System',
	page_icon = '::2a::'
)

# Side bar initialization and creation
with st.sidebar:
	selected = option_menu(
		menu_title = 'HRS',
		options = [	
			'Home','Diet',
			'Workout Suggestion','Medicine Recommender','Contact'],
		icons = ['house','flower3','wrench','clipboard2-x','envelope'],
	)
```

## How to execute the project
  - Download the project from github.
  - Install Required Python Libraries
      ```bash
      pip install -r requirements.txt
      ```
  - Run the Streamlit App
    ```bash
    streamlit run app.py
    ```

## Credits
Developed by *Pandey Abhishek Nath Roy*
