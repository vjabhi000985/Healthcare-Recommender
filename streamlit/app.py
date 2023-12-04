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

#Load Dataset
# dataset = pd.read_csv('dataset.csv')

# Homepage
def homepage():
	
	st.title("Healthcare Recommender System")
	words = '''
	<p style="font-style:italic; font-family:cursive;">
	Health Recommender System is a personalized System to recommend suggestion
	for diet and other sub domains like medicine and workout recommendation.
	</p>
	<p style="font-style:italic; font-family:cursive;">These are some of the sub-domains of the HRS.</p>
	<p style="font-style:italic; font-family:cursive;">We have tried to create a machine learning app using streamlit to mimic the
	collaborative and content based filtering technique to make suggestions.</p>
	<p style="font-style:italic; font-family:cursive;">It is just a prototype of the actual HRS and we will be making various changes
	in the future scope.</p>'''

	tech_stack = '''
		<ul>
			<li style="font-style:italic; font-family:cursive;">Dataset: CSV, JSON Files</li>
			<li style="font-style:italic; font-family:cursive;">Others libraries: Pandas, Numpy, Sklearn, Streamlit, Json</li>
			<li style="font-style:italic; font-family:cursive;">Programming: Python, Notebook</li>
			<li style="font-style:italic; font-family:cursive;">Visualization tools: Matplotlib, Plotly</li>
		</ul>
	'''
	
	# image = Image.open('first.jpg')

	left_column,right_column = st.columns(2)
	with left_column:
		st.markdown(words,unsafe_allow_html=True)
		with right_column:
			st.empty()

	st.title('Dataset')

	files = load_data()

	json_files = get_suggestion(files,10)
	data_files = get_data(json_files)


	st.dataframe(data_files)

	st.title('Tech Stack')

	st.markdown(tech_stack,unsafe_allow_html=True)

	# with st.container:
	# 	st.title("Tech stack used")

if selected == 'Home':
	# st.write(f'{selected} is loading')
	# st.title('Healthcare Recommender System')
	# words = '''<p>Healthcare Recommender System is a personalized System to recommend suggestion
	# 	for diet and all</p>'''

	# st.markdown(words,unsafe_allow_html=True)
	homepage()

# Defining CSS file
def local_css(file_name):
	with open(file_name) as f:
		st.markdown(f'<style>{f.read()},</style>',unsafe_allow_html=True)

# Loading CSS
local_css('style.css')

# Contact Form Frontend
def form():
	with st.container():
		st.write("---")
		st.header('Get In Tounch With Me!')
		st.write('##')

		contact_form = """
			<form action="https://formsubmit.co/anonymous17sa@gmail.com" method="POST">
				<input type="hidden" name="_captcha" value="false">
				<input type="text" name="name" placeholder="Your Full Name" required>
				<input type="email" name="email" placeholder="Your Email ID" required>
				<textarea name="message" placeholder="Your message" required></textarea>
				<button type="submit">Send</button>
			</form>
		"""

		left_column, right_column = st.columns(2)

		with left_column:
			st.markdown(contact_form,unsafe_allow_html=True)
		with right_column:
			st.empty()

if selected == 'Recommend':
	st.write(f'{selected} is loading')

# Contact form
if selected == 'Contact':
	form()

# Exercise JSON Dataset
exercise_by_level ={
	'beginner':{
		'Monday':['20 Sqauts','10 Push-ups','10 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
		'Tuesday':['20 Sqauts','10 Push-ups','10 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
		'Wednesday':['15 minutes Walk','30 seconds Jump rope(2 reps)','20 seconds Cobra Stretch'],
		'Thursday':['25 Sqauts','12 Push-ups','12 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
		'Friday':['25 Sqauts','12 Push-ups','12 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
		'Saturday':['15 minutes Walk','30 seconds Jump rope(2 reps)','20 seconds Cobra Stretch']
	},
	'intermediate':{
		'Monday':['3 Set Squats(8-12 reps)','3 Set Leg Extension(8-12 reps)','3 Set Lunges(10 reps Each)','30 Seconds Skipping(2 reps)'],
		'Tuesday':['3 Set Bench Press(12 reps)','3 Set Dumb-bell incline press(8-12 reps)','3 Set Cable Crossovers(10-12 reps)','30 Seconds Boxing Skip(2 reps)'],
		'Wednesday':['3 Set Deadlifts(6-12 reps)','3 Set Barbell Curls(8-12 reps)','3 Set Incline Curls(8-12 reps)'],
		'Thursday':['3 Set Shoulder Press(8-10 reps)','3 Set Incline Lateral Raises(8-10 reps)','3 Set Sit-ups(10-12 reps)','2 Set Leg Raises(8-12 reps)'],
		'Friday':['10 minutes Brisk Walk','1 minute Skipping','Breathing Exercises'],
		'Saturday':['10 minutes Brisk Walk','1 minute Skipping','Breathing Exercises']
	},
	'advanced':{
		'Monday':['5 Set Squats(8-12 reps)','5 Set Leg Extension(8-12 reps)','5 Set Lunges(10 reps Each)','60 Seconds Skipping(2 reps)'],
		'Tuesday':['5 Set Bench Press(12 reps)','5 Set Dumb-bell incline press(8-12 reps)','5 Set Cable Crossovers(10-12 reps)','60 Seconds Boxing Skip(2 reps)'],
		'Wednesday':['5 Set Deadlifts(6-12 reps)','5 Set Barbell Curls(8-12 reps)','5 Set Incline Curls(8-12 reps)'],
		'Thursday':['5 Set Shoulder Press(8-10 reps)','5 Set Incline Lateral Raises(8-10 reps)','5 Set Sit-ups(10-12 reps)','4 Set Leg Raises(8-12 reps)'],
		'Friday':['20 minutes Brisk Walk','2 minute Boxing Skip','Breathing Exercises'],
		'Saturday':['25 minutes Brisk Walk','1 minute Skipping','Breathing Exercises']
	}
}

# For Workout Suggestion
if selected == 'Workout Suggestion':
	st.title('Personalized Workout Recommender')

	st.selectbox('Age',['Select','Less than 18','18 to 49', '49 to 60','Above 60'])

	options = ['Less frequently','Moderate','More Frequently']

	st.radio('Workout Duration:',options)

	level = st.selectbox('Select your level:',['Select','beginner','intermediate','advanced'])

	button = st.button('Recommend Workout')

	if button:
		# workout_plan = generate_workout(level)
		nums = 1
		# st.write('Your Workout Plan:')

		if level == 'Select':
			st.warning('Insertion error!!Re-check the input fields')

		else:
			for day, exercises in exercise_by_level[level].items():
				exercise_str = ",".join(exercises)
				# st.write(f'{day}:{exercise_str}')
				st.markdown(
						f"""
						<h4>Your Workout Plan For Day {nums}</h4>
						<div class="workout">
							<div class="workout-info">
								<p style="color:#7FFF00; font-style:italic; font-family:cursive;">Day:{day}</p>
								<p style="color:#7FFF00; font-style:italic; font-family:cursive;">Workout:{exercise_str}</p>
							</div>
						</div>
						""",
						unsafe_allow_html=True
						)
				nums += 1

			st.markdown(
				f"""
					<h4> Your Workout Plan for Day {nums}</h4>
					<div class="sundays">
						<p style="color:#7FFF00; font-style:italic; font-family:cursive;">Take rest at sundays and do a little walk in the park</p>
					</div>
				""",
				unsafe_allow_html=True)
			# st.write('Take rest at sundays and do a little walk in the park')


# For medicine recommender
if selected == 'Medicine Recommender':
	main_1()

# For custom food recommendations
if selected == 'Diet':	
	diet()

	# prep_data = scaling(dataset)
