import pandas as pd
from scipy.sparse import save_npz
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

nltk.download('punkt')
nltk.download('stopwords')

def tokenize(text):
    """Tokenize and normalize strings using SnowballStemmer
    :param text: str, text to be tokenized
    :return: list
    """
    tokens = RegexpTokenizer(r"\w+").tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words("english")]
    stemmer = SnowballStemmer("english")

    clean_tokens = []
    for tok in tokens:
        clean_tok = stemmer.stem(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


df = pd.read_csv("../../data/diabetic_data.zip")
icd = pd.read_csv("../../data/icd9.csv", encoding='latin-1')

icd["icd9code"].replace("\.0$", "", regex=True, inplace=True)
icd["icd9code"].replace("\.00$", "", regex=True, inplace=True)
icd["icd9code"] = icd["icd9code"].apply(lambda x: x.lstrip("0"))
icd = icd.set_index("icd9code")

icd_dict = icd.to_dict()["long_description"]
df_icd = pd.DataFrame()
df_icd["diag"] = df["diag_1"].map(icd_dict).fillna("?") + " " + df["diag_2"].map(icd_dict).fillna("?") + " " + df[
    "diag_3"].map(icd_dict).fillna("?")

vectorizer = TfidfVectorizer(tokenizer=tokenize, ngram_range=(1, 1))

bow = vectorizer.fit_transform(df_icd.diag.values)

pickle.dump(vectorizer.get_feature_names(), open("../../data/processed/feature_names.pkl", "wb"))
save_npz("../../data/processed/bow.npz", bow)
