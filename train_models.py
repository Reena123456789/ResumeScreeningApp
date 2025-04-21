import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier

# Load the dataset
df = pd.read_csv('UpdatedResumeDataSet.csv')

# Initialize label encoder and encode categories
le = LabelEncoder()
df['Category'] = le.fit_transform(df['Category'])

# Initialize and fit TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_features = tfidf.fit_transform(df['Resume'])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(tfidf_features, df['Category'], test_size=0.2, random_state=42)

# Train the classifier
clf = OneVsRestClassifier(KNeighborsClassifier())
clf.fit(X_train, y_train)

# Save the models
with open('clf.pkl', 'wb') as f:
    pickle.dump(clf, f)
with open('tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

# Print accuracy score
y_pred = clf.predict(X_test)
print(f"Accuracy: {(y_pred == y_test).mean():.4f}")

# Save the label encoder mapping for reference
category_mapping = dict(zip(le.transform(le.classes_), le.classes_))
print("\nCategory Mapping:")
for id_, category in category_mapping.items():
    print(f"{id_}: {category}") 