#!/usr/bin/env python
# coding: utf-8

# SET UP ENVIRONMENT

# In[4]:


get_ipython().system('pip install pandas matplotlib seaborn')


# LOAD  AND EXPLORE DATASET
# 

# In[1]:


import pandas as pd
import json

# Load the datasets
with open("C:\\Users\\Dell\\Downloads\\PersonalizedStudentRecommendations\\LLQT.json") as f:
    current_quiz_data = json.load(f)

with open('C:\\Users\\Dell\\Downloads\\PersonalizedStudentRecommendations\\rJvd7g.json') as f:
    quiz_submission_data = json.load(f)

with open('C:\\Users\\Dell\\Downloads\\PersonalizedStudentRecommendations\\XgAgFJ.json') as f:
    historical_data = json.load(f)

# Display basic information about the datasets
print("Current Quiz Data:")
print(current_quiz_data.keys(), "\n")

print("Quiz Submission Data:")
print(quiz_submission_data.keys(), "\n")

print("Historical Quiz Data Sample:")
print(historical_data[:1], "\n")

# Access the 'quiz' key
quiz_details = current_quiz_data['quiz']

# Display the keys inside 'quiz' for inspection
print("Keys in 'quiz':", quiz_details.keys())

# Display a summary of the quiz metadata
print("\nQuiz Metadata:")
for key, value in quiz_details.items():
    print(f"{key}: {value}")



# DATA PREPROCESSING

# In[4]:


# Extract current quiz questions and responses(DATA PREPROCESSING)
current_questions = pd.DataFrame(current_quiz_data['quiz']['questions'])
print("Current Questions:\n", current_questions.head())

# Extract historical quiz performance
historical_df = pd.DataFrame(historical_data)
print("\nHistorical Data Overview:\n", historical_df.head())

# Extract user performance in the latest quiz
submission_df = pd.DataFrame([quiz_submission_data])
print("\nLatest Quiz Submission:\n", submission_df)


# ANALYZE THE PERFORMANCE

# In[11]:


# Define the function to analyze the quiz
def analyze_current_quiz(current_questions, response_map):
    # Map correct answers for each question
    correct_answers = current_questions.set_index('id')['options'].apply(
        lambda x: [opt['id'] for opt in x if opt['is_correct']][0]
    )
    
    # Convert response_map to a Series and align indices with correct_answers
    submission_responses = pd.Series(response_map).reindex(correct_answers.index)
    
    # Calculate correct count and accuracy
    correct_count = (submission_responses == correct_answers).sum()
    accuracy = correct_count / len(current_questions) * 100
    
    return accuracy, correct_answers, submission_responses

# Extract response_map from quiz_submission_data
response_map = quiz_submission_data['response_map']

# Call the function
accuracy, correct_answers, submission_responses = analyze_current_quiz(current_questions, response_map)
print(f"User Accuracy: {accuracy:.2f}%")

# Analyze weak topics and difficulty levels
current_questions['is_correct'] = current_questions['id'].map(
    lambda qid: response_map.get(qid) == correct_answers.get(qid)
)
weak_topics = current_questions[current_questions['is_correct'] == False]['topic'].value_counts()

# Difficulty-level analysis
difficulty_analysis = current_questions.groupby('difficulty_level')['is_correct'].mean() * 100

# Display weak topics and difficulty-level insights
print("\nWeak Topics:\n", weak_topics)
print("\nDifficulty-Level Performance (% Correct):\n", difficulty_analysis)


# GENERAL INSIGHTS OR CREATE RECOMMENDATIONS

# In[14]:


# Recommendations based on weak topics and difficulty levels
print("\nRecommendations:")
if not weak_topics.empty:
    print("- Focus on these weak topics:")
    for topic, count in weak_topics.items():
        print(f"  {topic} ({count} incorrect responses). Try reviewing related concepts in your notes or textbooks.")

# Suggest specific improvement areas based on difficulty level
print("\nDifficulty-Level Recommendations:")
if not difficulty_analysis.empty:
    if difficulty_analysis.min() < 70:
        low_performance_difficulties = difficulty_analysis[difficulty_analysis < 70]
        print("- Focus on improving questions at these difficulty levels:")
        for level, performance in low_performance_difficulties.items():
            print(f"  Difficulty Level: {level} (Accuracy: {performance:.2f}%)")
else:
    print("- No difficulty-specific issues. Continue practicing.")

# Suggest a balanced improvement approach
print("\nGeneral Recommendations:")
print("- Review incorrect responses to understand your mistakes.")
print("- Aim for balanced improvement by focusing equally on weak topics and difficulty levels.")


# Track improvement trends using historical data
historical_df['accuracy'] = historical_df['correct_answers'] / historical_df['total_questions'] * 100
historical_trend = historical_df[['submitted_at', 'accuracy']].sort_values(by='submitted_at')

print("\nPerformance Trend Over Time:")
print(historical_trend)


# VISUALIZE THE DATA

# In[17]:


import matplotlib.pyplot as plt
import seaborn as sns

# Plot performance trend
plt.figure(figsize=(10, 6))
sns.lineplot(data=historical_trend, x='submitted_at', y='accuracy', marker='o')
plt.title("Performance Trend Over Time")
plt.xlabel("Submission Date")
plt.ylabel("Accuracy (%)")
plt.xticks(rotation=45)
plt.show()

# Plot weak topics and difficulty levels
if not weak_topics.empty:
    plt.figure(figsize=(8, 6))
    weak_topics.plot(kind='bar', color='tomato')
    plt.title("Weak Topics")
    plt.ylabel("Incorrect Responses")
    plt.xticks(rotation=45)
    plt.show()

# Visualize difficulty-level performance
if not difficulty_analysis.empty:
    plt.figure(figsize=(8, 6))
    difficulty_analysis.sort_index().plot(kind='bar', color='skyblue')
    plt.title("Performance by Difficulty Level")
    plt.ylabel("Accuracy (%)")
    plt.xticks(rotation=45)
    plt.show()
plt.savefig('PerformanceTrend.png')


# DEFINE STUDENT PERSONA

# In[19]:


# Define persona and highlight strengths
avg_accuracy = historical_df['accuracy'].mean()
top_topics = current_questions[current_questions['is_correct'] == True]['topic'].value_counts()

if avg_accuracy >= 90:
    persona = "Proficient"
elif avg_accuracy >= 70:
    persona = "Improving"
else:
    persona = "Needs Attention"

print(f"\nStudent Persona: {persona}")
print("\nKey Strengths:")
if not top_topics.empty:
    print("- Strong performance in these topics:")
    for topic, count in top_topics.items():
        print(f"  {topic} ({count} correct responses)")
else:
    print("- No specific strong topics identified yet.")



# In[ ]:




