import streamlit as st
import pickle
import re
import nltk
from sklearn.exceptions import NotFittedError

nltk.download('punkt')
nltk.download('stopwords')

# Loading models
try:
    with open('clf.pkl', 'rb') as file:
        clf = pickle.load(file)
    with open('tfidf.pkl', 'rb') as file:
        tfidf = pickle.load(file)
except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    st.stop()

def clean_resume(resume_text):
    clean_text = re.sub('http\S+\s*', ' ', resume_text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+', ' ', clean_text)
    clean_text = re.sub('@\S+', ' ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text

# Web app
def main():
    st.title("Resume Screening App")
    uploaded_file = st.file_uploader('Upload Resume', type=['txt', 'pdf','docx'])

    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read()
            resume_text = resume_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try decoding with 'latin-1'
            resume_text = resume_bytes.decode('latin-1')

        cleaned_resume = clean_resume(resume_text)
        
        try:
            input_features = tfidf.transform([cleaned_resume])
            prediction_id = clf.predict(input_features)[0]

            # Map category ID to category name
            category_mapping = {
                0: "Advocate",
                1: "Arts",
                2: "Automation Testing",
                3: "Blockchain",
                4: "Business Analyst",
                5: "Civil Engineer",
                6: "Data Science",
                7: "Database",
                8: "DevOps Engineer",
                9: "DotNet Developer",
                10: "ETL Developer",
                11: "Electrical Engineering",
                12: "HR",
                13: "Hadoop",
                14: "Health and fitness",
                15: "Java Developer",
                16: "Mechanical Engineer",
                17: "Network Security Engineer",
                18: "Operations Manager",
                19: "PMO",
                20: "Python Developer",
                21: "SAP Developer",
                22: "Sales",
                23: "Testing",
                24: "Web Designing"
            }
            
            category_name = category_mapping.get(prediction_id, "Unknown")
            st.success(f"Predicted Category: {category_name}")
            
        except NotFittedError:
            st.error("Error: The model is not properly fitted. Please retrain the models using train_models.py")
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")

# Python main
if __name__ == "__main__":
    main()

