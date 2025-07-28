import json
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# データセットの読み込み
with open("dataset/annotations/train.json") as f:
    data = json.load(f)

# 特徴量とラベルの抽出
features = []
labels = []
for annotation in data["annotations"]:
    # bboxの幅と高さを特徴量として使用
    bbox = annotation["bbox"]
    features.append([bbox[2], bbox[3]])  # 幅, 高さ
    labels.append(annotation["category_id"])

# データの分割
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# モデルの学習
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# モデルの保存
os.makedirs("submit/model", exist_ok=True)
joblib.dump(model, "submit/model/model.pkl")

# 学習結果の出力
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Model training complete.")
print(f"Training accuracy: {train_score:.2f}")
print(f"Test accuracy: {test_score:.2f}")