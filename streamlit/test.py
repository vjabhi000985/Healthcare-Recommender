import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Medicine JSON File
medicine_data = '''
	{
		"diseases":[
			{
				"name":"Cold",
				"patients":45123332,
				"medicines":[
					{
						"name":"Ibuprofen",
						"dosage_form":"Tablet",
						"strength":"200 mg",
						"instructions":"Take 1 tablet every 6-8 hours"
					},

					{
						"name":"Acataminophen",
						"dosage_form":"Capsule",
						"strength":"500 mg",
						"instructions":"Take 1 tablet every 4-6 hours"
					},

					{
						"name":"Phenylephrine",
						"dosage_form":"Syrup",
						"strength":"5 mg/5 ml",
						"instructions":"Take 10 ml every 4 hours"
					}
				]
			},
			{
				"name":"Hypertension",
				"patients":90763630,
				"medicines":[
					{
						"name":"Lisinopril",
						"dosage_form":"Tablet",
						"strength":"10 mg",
						"instructions":"Take 1 tablet daily in the morning"
					},

					{
						"name":"Amlodipine",
						"dosage_form":"Tablet",
						"strength":"5 mg",
						"instructions":"Take 1 tablet daily in the morning"
					},

					{
						"name":"Hydrochlorothiazide",
						"dosage_form":"Capsule",
						"strength":"25 mg",
						"instructions":"Take 1 tablet daily in the morning"
					}
				]
			},
			{
				"name":"Diabetes",
				"patients":16783800,
				"medicines":[
					{
						"name":"Metformin",
						"dosage_form":"Tablet",
						"strength":"500 mg",
						"instructions":"Take 1 tablet twice daily with meals"
					},
					{
						"name":"Insulin (Rapid Acting)",
						"dosage_form":"Injection",
						"strength":"100 units/ml",
						"instructions":"Take 8 units twice in the morning and evening"
					},
					{
						"name":"Gliclazide",
						"dosage_form":"Tablet",
						"strength":"80 mg",
						"instructions":"Take 1 tablet before breakfast"
					}
				]
			},
			{
				"name":"Flu",
				"patients":508580,
				"medicines":[
					{
						"name":"Oseltamivir",
						"dosage_form":"Capsule",
						"strength":"75 mg",
						"instructions":"Take 1 capsule twice daily for 5 days"
					},
					{
						"name":"Ibuprofen",
						"dosage_form":"Tablet",
						"strength":"400 mg",
						"instructions":"Take 1 tablet every 6-8 hours for 5 days"
					},
					{
						"name":"Acataminophen",
						"dosage_form":"Syrup",
						"strength":"160 mg/5 ml",
						"instructions":"Take 10ml every 4-6 hours as needed for fever"
					}
				]
			},
			{
				"name":"Asthama",
				"patients":12464700,
				"medicines":[
					{
						"name":"Albuterol",
						"dosage_form":"Inhaler",
						"strength":"100 mcg",
						"instructions":"Inhale 2 puffs every 4-6 hours"
					},
					{
						"name":"Fluticasone",
						"dosage_form":"Inhaler",
						"strength":"50 mcg",
						"instructions":"Take 1-2 puffs twice daily"
					},
					{
						"name":"Montelukast",
						"dosage_form":"Tablet",
						"strength":"10 mg",
						"instructions":"Take 1 tablet daily in the evening"
					}
				]
			}
		]
	}
'''
# Fetch medicine data 
def get_medicines(disease):
	# Load JSON data
	data = json.loads(medicine_data)

	#Search for the disease in the json data
	for entry in data["diseases"]:
		if entry["name"].lower() == disease.lower():
			return entry["medicines"]
	return None

# d = "Diabetes"
# res = get_medicines(d)
# print(res)

# st.title('Personalized Workout Recommender')
# st.selectbox('Age',['Less than 18','18 to 49', '49 to 60','Above 60'])
# options = ['Less frequently','Moderate','More Frequently']

# JSON to Pandas Dataframe
def count_patients(medicine_data):
	dataset = json.loads(medicine_data)

	data = {"Disease":[],"Patient":[]}

	for entry in dataset["diseases"]:
		name = entry["name"]
		num_of_patients = entry["patients"]

		data["Disease"].append(name)
		data["Patient"].append(num_of_patients)

	return pd.DataFrame(data)

# Visualize the recommendations
def draw():
	# Load the medicine data as pandas dataframe.
	df = count_patients(medicine_data)
	
	# Calculate mean
	mean_of_patients = df["Patient"].mean()

	# Name the medication visualization
	st.markdown(
		f"""
			<h2 style="color:lightblue;">Medicines Visualization</h2>
		"""
		,
		unsafe_allow_html=True)

	#Set customm color for bar chart
	bar_color = None

	# Initialize figure
	fig_bar = go.Figure()

	# Add a bar chart: Disease vs No. of Patients
	fig_bar.add_trace(go.Bar(x=df["Disease"],y=df["Patient"],marker_color='MediumPurple'))

	# Add Mean line
	fig_bar.add_shape(
		type="line",
		x0 = -0.5,
		y0 = mean_of_patients,
		x1 = len(df) - 0.5,
		y1 = mean_of_patients,
		line = dict(color="red",dash="dash")
	)

	fig_bar.update_layout(
		title="Number of Patients per Diseases",
		xaxis_title="Diseases",
		yaxis_title="Number of Patients"
	)

	fig_bar.update_xaxes(type='category')
	st.plotly_chart(fig_bar)

	# Generate and Display the line chart
	fig_line = go.Figure()

	fig_line.add_trace(go.Scatter(x=df["Disease"],y=df["Patient"],mode='lines+markers',fill='tozeroy'))

	fig_line.update_layout(
		title="Trend of Number of Patients over diseases",
		xaxis_title="Diseases",
		yaxis_title="Number of Patients"
	)

	st.plotly_chart(fig_line)

# Menu app view
def main_1():
	st.title("Medication Recommender For Diseases")

	Age=st.selectbox('Age',['Select','10-18','19-30','31-50','Above 50'])

	disease_input = st.selectbox('Choose your disease',['Select','Asthama','Cold','Diabetes','Flu','Hypertension'])

	# st.write(f'YOU HAVE {disease_input}')
	if st.button("Recommend Medicines"):
		if Age == 'Select' or disease_input == 'Select':
			st.warning('Input Error!!Check the input fields')
		# Initialize Counter nums as 1.
		else:
			nums = 1
			if disease_input:
				medicines = get_medicines(disease_input)
				if medicines:
					st.markdown(f"""
							<h4 style="font-style:italic; font-family:cursive;"> Suggested Medicines for {disease_input} are:</h4>
						""",
						unsafe_allow_html=True)
					for med in medicines:
						st.markdown(
							f"""
								<h6 style="color:yellow;font-style:italic; font-family:cursive;">S.No: {nums}</h6>
								<div class="medicine">
									<p class="medicine-name" style="color:#7FFF00; font-style:italic; font-family:cursive;">{med['name']}</p>
									<div class="medicine-details">
										<p style="color:#7FFF00; font-style:italic; font-family:cursive;">Dosage Form: {med['dosage_form']}</p>
										<p style="color:#7FFF00; font-style:italic; font-family:cursive;">Strength: {med['strength']}</p>
										<p style="color:#7FFF00; font-style:italic; font-family:cursive;">Instruction: {med['instructions']}</p>
									</div>
								</div>
							""",
							unsafe_allow_html=True
						)
						nums += 1
					draw()

		# if medicines != "Select":
		# 	df = count_patients(medicine_data)
		# 	fig = go.Figure(data=[go.Bar(x=df["Disease"],y=df["Patient"])])
		# 	fig.update_layout(
		# 		title="Number of patients per disease",
		# 		xaxis_title="Disease",
		# 		yaxis_title="Number of Patients")
		# 	fig.update_xaxes(type='category')
		# 	st.plotly_chart(fig)

		# else:
		# 	st.write(f"No medicines avaliable")


if __name__ == "__main__":
	main_1()


# if st.button('Generate Workout'):
# 		# workout_plan = generate_workout(level)
# 		st.write('Your Workout Plan:')

# 		for day, exercises in exercise_by_level[level].items():
# 			exercise_str = ",".join(exercises)
# 			st.write(f'{day}:{exercise_str}')

# 		st.write('Take rest at sundays and do a little walk in the park')


# st.markdown(
# 	f"""
# 		<h4>Your Workout Plan</h4>
# 		<div class="workout">
# 			<div class="workout-info">
# 				<p>Day:{day}</p>
# 				<p>Workout:{exercise_str}</p>
# 			</div>
# 		</div>
# 	""",
# 	unsafe_allow_html=True
# 	)