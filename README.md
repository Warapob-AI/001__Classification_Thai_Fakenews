# Fake News Detection

## Overview
โครงการนี้เป็นระบบ **ตรวจสอบความน่าเชื่อถือของข่าว** โดยใช้ **Machine Learning** และ **Natural Language Processing (NLP)** เพื่อตรวจจับข่าวปลอมจากเนื้อหาข่าวแบบข้อความ

## การทำงานของระบบ
1. **โหลดและประมวลผลข้อมูล**
   - ดึงข้อมูลจากแหล่งข่าวและ URL
   - แปลงข้อความเป็นเวกเตอร์ด้วย **DEBERT หรือ BERT Wangchan**
   - ใช้ **Logistic Regression** เป็นโมเดลหลักในการจำแนกข่าวจริง-ข่าวปลอม

2. **Feature Engineering**
   - ตรวจจับหัวข้อข่าว
     
3. **การพยากรณ์ (Prediction)**
   - เมื่อป้อน URL หรือเนื้อหาข่าว ระบบจะทำนายว่าข่าวนั้น **"น่าเชื่อถือ" หรือ "ข่าวปลอม"**

## เทคโนโลยีที่ใช้
- **Python**
- **Logistic Regression**
- **DEBERT / BERT**
- **Machine Learning**
- **NLP**

## การติดตั้งและใช้งาน
### ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### รันโค้ดเพื่อฝึกโมเดล
```bash
sentence = str(input('\nEnter Sentence : '))
models = joblib.load('model.lr.pkl')
result = Sentence([sentence], models)

# ใส่ข้อความ input ลงใน sentence และรันได้ใน ipynb
```
