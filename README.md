# 環境の立ち上げ方法

## 1. 仮想環境の作成と有効化
Pythonの仮想環境を作成し、有効化します。

### Windowsの場合
```pwsh
python -m venv .venv
.venv\Scripts\activate
```

### 仮想環境の終了
```pwsh
deactivate
```

---

## 2. 必要なパッケージのインストール
`requirements.txt`に記載されたパッケージをインストールします。

```pwsh
pip install -r requirements.txt
```

---

## 3. Docker環境の立ち上げ
Dockerを使用して環境を構築する場合、以下の手順を実行します。

### Dockerイメージのビルド
```pwsh
docker build -f run_test/Dockerfile -t axell_ai_test run_test
```

### Dockerコンテナの起動
```pwsh
docker-compose -f run_test/docker-compose.yml up -d
```

### コンテナ内に入る
```pwsh
docker exec -it axell_2025 bash
```

---

### Dockerコンテナが起動しているか確認
```pwsh
docker ps
```
