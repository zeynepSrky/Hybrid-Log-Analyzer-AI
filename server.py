from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# threatKeywords = ["UNION","SELECT","<script>","' OR '1'='1"]
x_train = [
    "192.168.1.10 - GET /index.html -200",
    "192.168.1.15 - POST /login - 200",
    "45.12.33.9 - GET /admin/login.php?id=' OR '1'='1 - 500",
    "127.0.0.1 - GET /about.html - 200",
    "10.0.0.5 - GET /products.php?cat=1 UNION SELECT null, null, username, password FROM users - 200",
    "192.168.1.50 - GET /search?q=<script>alert('hack')</script> - 400"
]
y_train = [0, 0, 1, 0, 1, 1]

# metinleri sayılara çeviren vektörleştirici
vectorizer = TfidfVectorizer()
x_train_vec = vectorizer.fit_transform(x_train)

model = LogisticRegression()
model.fit(x_train_vec, y_train)

@app.route("/predict", methods = ['POST'])
def predict():
    data = request.get_json(silent = True, force = True) # json paketini -> python dictionary e çevirme
    
    if data is None or "log" not in data:
        return jsonify({"hata": "Geçersiz JSON formatı veya log içeriği eksik."}),400
    
    log_text = data["log"] # C# ın gönderdiği log metnini bir değişkene atıyoruz.

    log_vec =vectorizer.transform([log_text]) #C sharptan gelen logu modelin anlayacağı sayısal vektöre çeviriyoruz
    prediction = model.predict(log_vec)[0]
    probability = model.predict_proba(log_vec)[0][1] #tehdit olma olasılığı

    if prediction == 1:
        return jsonify({"result" : "Tehdit", "score": float(probability)})
    else:
        return jsonify({"result": "Normal" , "score" : float(probability)})
    
    
    """
    is_threat = any(keyword.lower() in log_text.lower() for keyword in threatKeywords)

    if is_threat:
        return jsonify({"result":"Tehdit", "score":0.95})
    else:
        return jsonify({"result":"Normal", "score":0.05})
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)