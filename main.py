from Scripts.CleanedData.LoadData import Load_data
from Scripts.CleanedData.Lemmatization import Lemmatization
from Scripts.CleanedData.Tokenization import Tokenization
from Scripts.CleanedData.Special import Remove_Special_character
from Scripts.CleanedData.Lowercase import Lowercase

from Scripts.FeatureData.Encode import encode_by_label
from Scripts.FeatureData.SaveVector import Save_Vectorizer
from Scripts.FeatureData.LoadVector import Load_Vectorizer

from Scripts.TrainedData.SampleData import SampleData
from Scripts.TrainedData.LogisticRegression import Logistic_Regression
from Scripts.TrainedData.SVM import Support_Vector_Machine

from Scripts.EvaluationData.Classification import Classification_Report
from Scripts.EvaluationData.Sentence import Sentence

from transformers import AutoTokenizer, AutoModel
from pydantic import BaseModel
from fastapi import FastAPI
from mangum import Mangum

import pandas as pd
import numpy as np
import uvicorn
import torch 
import os 

if not os.path.exists('model/fakenews_features.pkl') or not os.path.exists('model/truenews_features.pkl'):
    model_name = "airesearch/wangchanberta-base-att-spm-uncased"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)

    df_fake = Load_data('Dataset/fake_news.txt', 'fakenews')
    df_true = Load_data('Dataset/true_news.txt', 'truenews')

    # # รวมข้อมูลสอง DataFrame เข้าด้วยกัน
    df = pd.concat([df_fake, df_true], ignore_index=True)
    df['cleaned_text'] = df['text'].apply(Lemmatization)
    df['cleaned_text'] = df['cleaned_text'].apply(Tokenization)
    df['cleaned_text'] = df['cleaned_text'].apply(Remove_Special_character)
    df['cleaned_text'] = df['cleaned_text'].apply(Lowercase)

    label_features = encode_by_label(df, tokenizer, model, device)

    # แยก features ตาม label
    fake_news_features = label_features['fakenews']
    true_news_features = label_features['truenews']

    Save_Vectorizer(fake_news_features, true_news_features)

if not os.path.exists('model/model_lr.pkl'):
    fakenews_data = Load_Vectorizer('Model/fakenews_features.pkl')
    truenews_data = Load_Vectorizer('Model/truenews_features.pkl')

    x_train, x_test, y_train, y_test = SampleData(fakenews_data, truenews_data)
    y_pred, name = Support_Vector_Machine(x_train, x_test, y_train, y_test)
    Classification_Report(name, y_test, y_pred)

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/")
async def predict(text_input: TextInput):
    text = text_input.text
    result = Sentence([text])  # สมมุติว่า Sentence เป็นฟังก์ชันที่คุณใช้
    return {"result": result}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)