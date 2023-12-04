import json
import streamlit as st
import pandas as pd
import pandas_profiling as pp
import altair as alt
import random
import base64
import plotly.express as px
import plotly.graph_objects as go


class Person:

    def __init__(self,age,height,weight,gender,activity,weight_loss):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        # self.meals_calories_perc=meals_calories_perc
        self.weight_loss=weight_loss
    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'    
            color='Red'
        return bmi_string,category,color

    def calculate_bmr(self):
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr

    def calories_calculator(self):
        activites=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights=[1.2,1.375,1.55,1.725,1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories


class Display:
    def __init__(self):
        self.plans=["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
        self.weights=[1,0.9,0.8,0.6]
        self.losses=['-0 kg/week','-0.25 kg/week','-0.5 kg/week','-1 kg/week']
        pass

    def display_bmi(self,person):
        st.header('BMI CALCULATOR')
        bmi_string,category,color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            Healthy BMI range: 18.5 kg/m² - 25 kg/m².
            """)   

    def display_calories(self,person):
        st.header('CALORIES CALCULATOR')        
        maintain_calories=person.calories_calculator()
        st.write('The results show a number of daily calorie estimates that can be used as a guideline for how many calories to consume each day to maintain, lose, or gain weight at a chosen rate.')
        for plan,weight,loss,col in zip(self.plans,self.weights,self.losses,st.columns(4)):
            with col:
                st.metric(label=plan,value=f'{round(maintain_calories*weight)} Calories/day',delta=loss,delta_color="inverse")
    

# Load the pandas dataframe and perform automated Exploratory Data Analysis
def profiling():
	data = pd.read_csv('dataset.csv',compression='gzip')
	profiles = data.iloc[:,:].head(150)
	profile = pp.ProfileReport(profiles,minimal=True)
	# st.write("Exploratory Data Analysis of Food Data")
	profile.to_html("output.html")

# Load the Output dataset
def load_data():
	with open('health_data.json','r') as recommendations:
		data = json.load(recommendations)

	return data

# Generate random suggestions
def get_suggestion(data,n):
	if data is not None and isinstance(data,list):
		s = random.sample(data,min(n,len(data)))
		return s
	else:
		return []

# Convert JSON to Dataframe
def get_data(json_file):

	dataset = {"Name":[],"RecipeIngredientParts":[],"Calories":[],"RecipeInstructions":[]}
	for recipies in json_file:
		name = recipies["Name"]
		ingredients = recipies["RecipeIngredientParts"]
		calories = recipies["Calories"]
		instructions = recipies["RecipeInstructions"]

		dataset["Name"].append(name)
		dataset["RecipeIngredientParts"].append(ingredients)
		dataset["Calories"].append(calories)
		dataset["RecipeInstructions"].append(instructions)
	
	return pd.DataFrame(dataset)

# Diet Recommendation
def display_recommendation(dataset):
    st.header('DIET RECOMMENDATOR')  
    with st.spinner('Generating recommendations...'): 
        # meals=person.meals_calories_perc
        st.subheader('Recommended recipes:')
        recipes = dataset

        # columns = ["Name","RecipeIngredientParts","Calories","RecipeInstructions"]
        for index,row in recipes.iterrows():
                        
            recipe_name=row['Name']
            ingredients=row['RecipeIngredientParts']
            calories=row['Calories']
            instructions=row['RecipeInstructions']

            expander = st.expander(recipe_name)
        
            expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Ingredients:</h5>', unsafe_allow_html=True)
           
            expander.markdown(f"""
                    - {ingredients}
                """)
            expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Recipe Instructions:</h5>', unsafe_allow_html=True)    
         
            expander.markdown(f"""
                    - {instructions}
                """) 
            expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Total Carolies Intake:</h5>', unsafe_allow_html=True)   
            expander.markdown(f"""
                        Total Calories Intake: {calories}
                    """)  
# load PDF File
def displayPDF(file):
	# Opening file from file path
	with open(file,"rb") as f:
		base64_pdf = base64.b64encode(f.read()).decode('utf-8')

	#Embedding PDF in HTML
	
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf} width="700" height="1000" type="application/pdf"></iframe>'
	st.markdown(pdf_display,unsafe_allow_html=True)

# Visualize Scatter Plot 'Calories Per Recipe'
def display_charts(dataset):
    data = dataset
    fig = px.scatter(dataset,x='Name',y='Calories',size='Calories',
                     title = 'Calories per Recipe',
                     labels = {'calories':'Calories'},
                     size_max = 40)
    
    st.markdown(f"""<h3 style="color:#7FFF00;">Calories per Recipe</h3>""",unsafe_allow_html=True)
    st.plotly_chart(fig)

# Heatmap of the all the dataset
def display_heatmap(dataset):
    fig = go.Figure(data=go.Heatmap(
        z=dataset.values,
        x=dataset.columns,
        y=dataset.index,
        colorscale='Viridis',
        hoverongaps=False
        ))

    fig.update_layout(
        xaxis_title='Columns',
        yaxis_title='Rows',
        title='Heatmap for Dataset'
        )
    st.markdown(f"""<h3 style="color:#7FFF00;">Heatmap of the Dataset</h3>""",unsafe_allow_html=True)
    st.plotly_chart(fig)

# Call the charts    
def test_charts(files):
    test_json_file = get_suggestion(files,20)
    test_data = get_data(test_json_file)

    display_charts(test_data)

    display_heatmap(test_data)

# Display Menu    
def display_menu():
    st.title('Custom Diet Recommendations')
    display = Display()
    files = load_data()
    age = st.number_input('Age',min_value=2,max_value=80,step=1)
    height = st.number_input('Height(cm)',min_value=50,max_value=300,step=1)
    weight = st.number_input('Weight(Kg)',min_value=10,max_value=300,step=1)
    gender = st.radio('Gender',('Male','Female'))
    activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)'])
    option = st.selectbox('Choose your weight loss plan:',display.plans)

    weight_loss = display.weights[display.plans.index(option)]

    number_of_meals = st.slider('Meals per day',min_value=3,max_value=5,step=1,value=3)

    generated = st.button('Recommend')
    
    if generated:
        person=Person(age,height,weight,gender,activity,weight_loss)

        health_json_files = get_suggestion(files,number_of_meals)
        health_data_files = get_data(health_json_files)

        display.display_bmi(person)

        display.display_calories(person)

        display_recommendation(health_data_files)

        test_charts(files)

# Main app
def diet():
    display_menu()

if __name__ == '__main__':
    diet()
