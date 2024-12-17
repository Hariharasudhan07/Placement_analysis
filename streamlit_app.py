import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Description
st.title("Student Performance and Placement Overview")
st.write("""
This application provides insights into student performance and placement statistics. 
It helps identify areas where students are performing well and areas needing improvement.
""")

# Load the constant files
data1 = pd.read_csv('Assessmet.csv')  # Replace with the path to your constant file
data2 = pd.read_csv('Company.csv')   # Replace with the path to your constant file

# Clean the data
if 'Register No.' in data1.columns:
    data1.rename(columns={'Register No.': 'Register Number'}, inplace=True)

# Input Section
st.sidebar.header("Student Information")

# Create a list of valid register numbers in both ranges
valid_register_numbers = list(range(611221243001, 611221243064)) + list(range(611221243301, 611221243307))

# Convert the register number list to a string type for display
user= st.sidebar.selectbox(
    "Enter the Register Number:",
    options=valid_register_numbers,
    format_func=lambda x: str(x)
)

# Now you can use `user_input` as the selected register number
st.write(f"Selected Register Number: {user}")

if user:
    # Fetch user data from data1
    user_ass = data1[data1['Register Number'] == user]
    user_placement = data2[data2['Register Number'] == user]

    if user_ass.empty:
        st.sidebar.error("Student data not found in Assessment file.")
    else:
        student_name = user_ass['Name of the Student'].values[0]
        st.sidebar.success(f"Student Name: {student_name}")

        # Merge data for full overview
        user_full_data = pd.merge(user_ass, user_placement, on='Register Number', how='outer')
        user_data = user_full_data.fillna('Not Eligible')

        # Section: Company Details
        st.header("Company Details")
        company_columns = [
            'Nexware Technologies', 'Abluva', 'Codingmart Technologies', 'EmbedUR', 'MulticoreWare',
            'Aggregate Intelligence', 'AMI', 'CEI America', 'Tech Mahindra', 'Hexaware', 'Deltax', 
            'Renault Nissan', 'HP Evoriea Infotech', 'Cognizant', 'Bahwan', 'Juspay', 'Expleo', 
            'Infiniti Software Solutions', 'Vinsinfo', 'Mr.Cooper'
        ]

        total_company = len(company_columns)
        attended_companies = 0
        attendance_details = {}

        # Attendance calculation
        placed_found = False

        for company in company_columns:
            round_result = (
                user_data[company].values[0]
                if company in user_data.columns and not user_data[company].empty
                else 'Not Eligible'
            )

            if round_result == 'Placed':
                # Display the placement information with bold and big text
                st.markdown(f"<h2 style='color:green;'>🎉 Student is placed in <b>{company}</b> 🎉</h2>", unsafe_allow_html=True)
                placed_found = True
                break
            elif round_result != 'Not Eligible':
                attended_companies += 1
                attendance_details[company] = round_result

        if not placed_found:
            st.write(f"**Total companies attended: {attended_companies} out of {total_company}**")
            st.table(pd.DataFrame.from_dict(attendance_details, orient='index', columns=['Result']))

        # Section: Performance Evaluation
        st.header("Performance Evaluation")
        performance_thresholds = {
            ' in 10th Std': 60,
            ' in 12th Std': 60,
            'CGPA in UG': 6.0,
            'No. of Standing Arrears': 0,
            'English Comprehension (Score)': 70,
            'Logical Ability (Score)': 70,
            'Quantitative Ability (Advanced) (Score)': 70,
            'Automata (Score)': 60,
            'Automata Fix (Score)': 60,
            'Computer Science(Score)': 70,
            'SVAR - Spoken English (Score)': 75,
            'SVAR - Spoken English (CEFR Level)': 'B2',
            'Logical Ability (Percentile)': 70,
            'CSE / ECE / EEE / Mech. related test (Score)': 60,
        }
        def evaluate_performance(student_data, performance_thresholds):
    # Initialize an empty dictionary to store performance feedback
            performance_report = {}

            for metric, threshold in performance_thresholds.items():
                # Get the student's score for each metric
                score = student_data[metric].values[0] if metric in student_data.columns else None

                # Handle missing or special case values
                if score in ['-', 'AB', None]:  # Treat special cases as 0
                    score = 0
                else:
                    try:
                        score = float(score)  # Convert to float if possible
                    except ValueError:
                        pass  # If it's not a number, leave it as-is

                # Compare score with threshold
                if isinstance(threshold, (int, float)):  # Numeric threshold
                    if isinstance(score, (int, float)) and score < threshold:
                        performance_report[metric] = f"Lacking, score: {score}, threshold: {threshold}"
                    elif isinstance(score, (int, float)):
                        performance_report[metric] = f"Good, score: {score}, threshold: {threshold}"
                    else:  # Non-numeric score for a numeric threshold
                        performance_report[metric] = f"Lacking, score: {score}, expected numeric value"
                elif isinstance(threshold, str):  # Non-numeric threshold (e.g., CEFR Level)
                    if score != threshold:
                        performance_report[metric] = f"Lacking, score: {score}, expected: {threshold}"
                    else:
                        performance_report[metric] = f"Good, score: {score}, expected: {threshold}"

            return performance_report


        performance_report = evaluate_performance(user_full_data, performance_thresholds)
        st.table(pd.DataFrame.from_dict(performance_report, orient='index', columns=['Status']))

        # Visualization: Performance Summary
        # Visualization: Performance Summary
        st.header("Performance Summary")
        performance_df = pd.DataFrame.from_dict(performance_report, orient='index', columns=['Status'])
        performance_df['Metric'] = performance_df.index
        performance_df['Color'] = performance_df['Status'].apply(lambda x: 'green' if 'Good' in x else 'red')

        # Plotting the performance summary
        fig, ax = plt.subplots(figsize=(10, 6))

        # Explicitly set colors for bars
        bars = ax.bar(
            performance_df['Metric'],
            range(len(performance_df)),
            color=performance_df['Color'],
        )

        legend_handles = [
            plt.Line2D([0], [0], color='green', lw=4, label='Good'),
            plt.Line2D([0], [0], color='red', lw=4, label='Bad')
        ]
        ax.legend(handles=legend_handles, title="Performance")

        # Add labels and rotate for better readability
        plt.xticks(rotation=90)
        plt.title('Student Performance Summary')
        plt.xlabel('Metrics')
        plt.ylabel('Scores')
        st.pyplot(fig)

        # Visualization for Company Attendance Overview
        st.write("### Company Attendance Overview")

        # Total number of companies and companies attended
        total_companies = len(company_columns)  # Use the same company columns list
        attended_companies_count = attended_companies  # Already calculated in the loop

        # Bar chart for companies attended
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(['Companies Attended'], [attended_companies_count], color='blue', alpha=0.7, label='Attended')
        ax.barh(['Companies Attended'], [total_companies - attended_companies_count], color='grey', alpha=0.2, label='Not Attended')
        ax.set_xlim(0, total_companies)  # Ensure the x-axis goes up to the total companies
        ax.set_xticks(range(0, total_companies + 1, 1))  # From 0 to total companies, step size 1

        # Add labels and title
        ax.set_xlabel('Number of Companies')
        ax.set_title('Company Attendance Overview')
        ax.legend(loc='upper right')
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(fig)
