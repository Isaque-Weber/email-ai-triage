import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from app.services.preprocess import preprocess

df = pd.read_csv("data/train.csv")
X = df["text"].astype(str).apply(preprocess)
y = (df["label"].astype(str) == "produtivo").astype(int)

vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1, max_df=0.95)
clf = LogisticRegression(max_iter=200)

Xv = vectorizer.fit_transform(X)
clf.fit(Xv, y)

dump(vectorizer, "models/vectorizer.joblib")
dump(clf, "models/clf.joblib")
print("OK: modelo salvo em models/")
