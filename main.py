import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

data1=pd.read_csv('Assessmet.csv')
data2=pd.read_csv('Company.csv')

if 'Register No.' in data1.columns:
    data1.rename(columns={'Register No.': 'Register Number'}, inplace=True)



# Input Register Number from user
user = int(input("Enter the Register Number: "))

# Fetch user data from data1
user_ass = data1[data1['Register Number'] == user]
if not user_ass.empty:
    # Assuming the student's name is in the 'Name' column
    student_name = user_ass['Name of the Student'].values[0]
    print(f"The student's name is: {student_name}")
# Fetch user data from data2
user_placement = data2[data2['Register Number'] == user]

# Merge data for complete information (optional)
user_full_data = pd.merge(user_ass, user_placement, on='Register Number', how='outer')


user_data = pd.DataFrame(user_full_data)
user_data=user_data.fillna('Not Eligible')

# List of companies
company_columns = [
    'Nexware Technologies', 'Abluva', 'Codingmart Technologies', 'EmbedUR', 'MulticoreWare',
    'Aggregate Intelligence', 'AMI', 'CEI America', 'Tech Mahindra', 'Hexaware', 'Deltax', 
    'Renault Nissan', 'HP Evoriea Infotech', 'Cognizant', 'Bahwan', 'Juspay', 'Expleo', 
    'Infiniti Software Solutions', 'Vinsinfo', 'Mr.Cooper'
]

total_company=len(company_columns)

# Initialize counter
attended_companies = 0
attendance_details = {}

# Loop through each company column to check the attendance
for company in company_columns:
    round_result = user_data[company].values[0]  # Get the round result for the student
    if round_result == 'Placed':  # If the student is placed in any company
        print(f"Student is placed in {company}")
        placed_found = True
        break  # Stop the loop if the student is placed in any company
    elif round_result != 'Not Eligible':  # If not 'Not Eligible', the student attended the company
        attended_companies += 1
        attendance_details[company] = round_result

# Output the results if the student was not placed
if not placed_found:
    print(f"Total companies attended by the student: {attended_companies} out of {total_company}")
    print("\nDetailed attendance by company:")
    for company, result in attendance_details.items():
        print(f"{company}: {result}")

student_data = pd.DataFrame(user_full_data)
student_data.columns = student_data.columns.str.replace('\n', ' ')
# Define performance thresholds for each metric
performance_thresholds = {
    ' in 10th Std': 60,  # Expected score above 60
    ' in 12th Std': 60,  # Expected score above 60
    'CGPA in UG': 6.0,   # Expected CGPA above 6.0
    'No. of Standing Arrears': 0,  # No arrears expected
    'English Comprehension (Score)': 70,
    'Logical Ability (Score)': 70,
    'Quantitative Ability (Advanced) (Score)': 70,
    'Automata (Score)': 60,
    'Automata Fix (Score)': 60,
    'Computer Science(Score)': 70,
    'SVAR - Spoken English (Score)': 75,
    'SVAR - Spoken English (CEFR Level)': 'B2',  # Expected CEFR level
    'Quantitative Ability (Advanced) (Score)': 70,
    'Logical Ability (Percentile)': 70,
    'CSE / ECE / EEE / Mech. related test (Score)': 60,
}

# Define a function to evaluate where the student is lacking
def evaluate_performance(student_data, performance_thresholds):
    # Initialize an empty dictionary to store performance feedback
    performance_report = {}

    for metric, threshold in performance_thresholds.items():
        score = student_data[metric].values[0]  # Get the student's score for each metric
        
        # Check for special cases and convert them to 0
        if score == '-' or score == 'AB':
            score = 0

        # Ensure the threshold is numeric
        if isinstance(threshold, str) and threshold not in ['Unattempted', '-']:  # Handle non-numeric thresholds
            try:
                threshold = float(threshold)  # Attempt to convert to float
            except ValueError:
                threshold = 0  # Default to 0 if it cannot be converted

        # Check if the score is numeric
        if isinstance(score, (int, float)):  
            # Compare score with threshold
            if score < threshold:
                performance_report[metric] = f"Lacking, score: {score}, threshold: {threshold}"
            else:
                performance_report[metric] = f"Good, score: {score}, threshold: {threshold}"

        else:  # Handle non-numeric values (like 'Unattempted' or text-based scores)
            if score == 'Unattempted' or score is None:
                performance_report[metric] = f"Lacking, score: {score}, expected numeric value"
            elif isinstance(threshold, str) and score != threshold:
                performance_report[metric] = f"Lacking, score: {score}, expected: {threshold}"
            else:
                performance_report[metric] = f"Good, score: {score}, expected: {threshold}"

    return performance_report


# Evaluate performance for the student
performance_report = evaluate_performance(student_data, performance_thresholds)

# Now, count how many companies the student attended (excluding "Not Eligible")
company_columns = [
    'Nexware Technologies', 'Abluva', 'Codingmart Technologies', 'EmbedUR', 'MulticoreWare',
    'Aggregate Intelligence', 'AMI', 'CEI America', 'Tech Mahindra', 'Hexaware', 'Deltax', 
    'Renault Nissan', 'HP Evoriea Infotech', 'Cognizant', 'Bahwan', 'Juspay', 'Expleo', 
    'Infiniti Software Solutions', 'Vinsinfo', 'Mr.Cooper'
]

# Initialize a counter for attended companies
attended_companies_count = 0

# Check each company participation status
for company in company_columns:
    participation_status = student_data[company].values[0]
    if participation_status in ['1st Round Eliminated', '2nd Round Eliminated', 'Placed']:
        attended_companies_count += 1

# Display the results
print("Performance Report:")
for metric, feedback in performance_report.items():
    print(f"{metric}: {feedback}")

print(f"\nTotal companies attended by the student: {attended_companies_count}")

student_data = pd.DataFrame(user_full_data)
student_data.columns = student_data.columns.str.replace('\n', ' ')
# Define performance thresholds for each metric
performance_thresholds = {
    ' in 10th Std': 60,  # Expected score above 60
    ' in 12th Std': 60,  # Expected score above 60
    'CGPA in UG': 6.0,   # Expected CGPA above 6.0
    'No. of Standing Arrears': 0,  # No arrears expected
    'English Comprehension (Score)': 70,
    'Logical Ability (Score)': 70,
    'Quantitative Ability (Advanced) (Score)': 70,
    'Automata (Score)': 60,
    'Automata Fix (Score)': 60,
    'Computer Science(Score)': 70,
    'SVAR - Spoken English (Score)': 75,
    'SVAR - Spoken English (CEFR Level)': 'B2',  # Expected CEFR level
    'Quantitative Ability (Advanced) (Score)': 70,
    'Logical Ability (Percentile)': 70,
    'CSE / ECE / EEE / Mech. related test (Score)': 60,
}

# Define a function to evaluate where the student is lacking
def evaluate_performance(student_data, performance_thresholds):
    # Initialize an empty dictionary to store performance feedback
    performance_report = {}

    for metric, threshold in performance_thresholds.items():
        score = student_data[metric].values[0]  # Get the student's score for each metric
        
        # Check for special cases and convert them to 0
        if score == '-' or score == 'AB':
            score = 0

        # Ensure the threshold is numeric
        if isinstance(threshold, str) and threshold not in ['Unattempted', '-']:  # Handle non-numeric thresholds
            try:
                threshold = float(threshold)  # Attempt to convert to float
            except ValueError:
                threshold = 0  # Default to 0 if it cannot be converted

        # Check if the score is numeric
        if isinstance(score, (int, float)):  
            # Compare score with threshold
            if score < threshold:
                performance_report[metric] = f"Lacking, score: {score}, threshold: {threshold}"
            else:
                performance_report[metric] = f"Good, score: {score}, threshold: {threshold}"

        else:  # Handle non-numeric values (like 'Unattempted' or text-based scores)
            if score == 'Unattempted' or score is None:
                performance_report[metric] = f"Lacking, score: {score}, expected numeric value"
            elif isinstance(threshold, str) and score != threshold:
                performance_report[metric] = f"Lacking, score: {score}, expected: {threshold}"
            else:
                performance_report[metric] = f"Good, score: {score}, expected: {threshold}"

    return performance_report


# Evaluate performance for the student
performance_report = evaluate_performance(student_data, performance_thresholds)

# Now, count how many companies the student attended (excluding "Not Eligible")
company_columns = [
    'Nexware Technologies', 'Abluva', 'Codingmart Technologies', 'EmbedUR', 'MulticoreWare',
    'Aggregate Intelligence', 'AMI', 'CEI America', 'Tech Mahindra', 'Hexaware', 'Deltax', 
    'Renault Nissan', 'HP Evoriea Infotech', 'Cognizant', 'Bahwan', 'Juspay', 'Expleo', 
    'Infiniti Software Solutions', 'Vinsinfo', 'Mr.Cooper'
]

# Initialize a counter for attended companies
attended_companies_count = 0

# Check each company participation status
for company in company_columns:
    participation_status = student_data[company].values[0]
    if participation_status in ['1st Round Eliminated', '2nd Round Eliminated', 'Placed']:
        attended_companies_count += 1

# Display the results
print("Performance Report:")
for metric, feedback in performance_report.items():
    print(f"{metric}: {feedback}")

print(f"\nTotal companies attended by the student: {attended_companies_count}")


# Prepare data for DataFrame
performance_report_data = []

for metric, feedback in performance_report.items():
    # Split the feedback string by commas
    feedback_parts = feedback.split(',')
    
    # Extract status (Good/Lacking)
    status = feedback_parts[0].strip()
    
    # Extract score
    score = None
    if len(feedback_parts) > 1:
        score_part = feedback_parts[1].split(':')
        if len(score_part) > 1:
            score = score_part[1].strip()
    
    # Extract threshold/expected value (only if available)
    threshold = None
    if len(feedback_parts) > 2:
        threshold_part = feedback_parts[2].split(':')
        if len(threshold_part) > 1:
            threshold = threshold_part[1].strip()

    # Append the extracted data into the list
    performance_report_data.append({
        'Metric': metric,
        'Status': status,
        'Score': score,
        'Threshold/Expected': threshold
    })

# Create a DataFrame from the performance report data
performance_report_df = pd.DataFrame(performance_report_data)


performance_df = pd.DataFrame(performance_report_df)

performance_df['Score'] = pd.to_numeric(performance_df['Score'], errors='coerce')  # Convert 'Score' to numeric
performance_df['Threshold/Expected'] = pd.to_numeric(performance_df['Threshold/Expected'], errors='coerce')  # Convert 'Threshold' to numeric

# Evaluate if the score meets or lacks the threshold
performance_df['Status'] = performance_df.apply(
    lambda row: 'Good' if pd.notna(row['Score']) and (row['Score'] >= row['Threshold/Expected']) 
               else 'Lacking', axis=1
)

# Map the 'Lacking' and 'Good' into colors (Green for Good, Red for Lacking)
performance_df['Color'] = performance_df['Status'].map({'Good': 'green', 'Lacking': 'red'})

# Plot the performance summary (Good vs Lacking)
plt.figure(figsize=(10, 6))
sns.barplot(x='Metric', y='Score', data=performance_df, hue='Status', dodge=False, palette={'Good': 'green', 'Lacking': 'red'})
plt.xticks(rotation=90)
plt.title('Student Performance Summary')
plt.xlabel('Metric')
plt.ylabel('Score')
plt.tight_layout()
plt.show()

 # Given data for companies attended
total_companies = 20    # Total number of companies listed

# Bar chart for companies attended
plt.figure(figsize=(6, 4))
plt.barh(['Companies Attended'], [attended_companies_count], color='blue', alpha=0.7)
plt.barh(['Companies Attended'], [total_companies - attended_companies_count], color='grey', alpha=0.2)
plt.xlim(0, total_companies)  # Ensure the total companies always show as 20

# Set x-ticks to be whole numbers
plt.xticks(range(0, total_companies + 1, 1))  # From 0 to 20, with step size of 1

plt.xlabel('Number of Companies')
plt.title('Company Attendance Overview')
plt.tight_layout()
plt.show()

