# Axell AI Contest 2025 - ディレクトリ仕様書

## プロジェクト概要
本プロジェクトは、Axell AI Contest 2025のために提供されたデータセットとコードベースを使用して、物体検出モデルを構築・評価するためのものです。

---

## ディレクトリ構造
以下はプロジェクトのディレクトリ構造です。

```plaintext
Axell_AI_Contest2025/
├── run_test/                # 動作確認用コードとデータ
│   ├── dataset/            # データセット関連ファイル
│   │   ├── annotations/    # アノテーションファイル
│   │   │   ├── train.json  # 学習用データ
│   │   │   └── custom_val.json # 検証用データ（生成される）
│   │   ├── images/         # 画像データ
│   │   └── README.txt      # データセットの説明
│   ├── submit/             # 提出用フォルダ
│   │   ├── model/          # 学習済みモデルを格納
│   │   ├── src/            # 推論コード
│   │   │   └── predictor.py # 推論用クラス
│   │   └── requirements.txt # 提出時の依存ライブラリ
│   ├── src/                # 動作確認用モジュール
│   │   ├── generator.py    # データ生成モジュール
│   │   ├── runner.py       # 推論実行モジュール
│   │   └── validator.py    # 結果検証モジュール
│   ├── Dockerfile          # Docker環境構築用ファイル
│   ├── docker-compose.yml  # Docker Compose設定
│   ├── requirements.txt    # 動作確認用依存ライブラリ
│   ├── run.py              # 動作確認用メインスクリプト
│   └── README.md           # 動作確認用説明書
├── SPECIFICATION.md        # 本仕様書
└── .gitignore              # Git管理対象外ファイル
```

---

## 各ファイルの説明

### 1. `run_test/`
動作確認用のコードとデータが含まれています。

#### `dataset/`
- **`annotations/train.json`**: 学習用データセット（COCOフォーマット）。
- **`annotations/custom_val.json`**: 検証用データセット（`make_val.py`で生成）。
- **`images/`**: 学習用画像データ。
- **`README.txt`**: データセットの説明。

#### `submit/`
- **`model/`**: 学習済みモデルを格納するディレクトリ。
- **`src/predictor.py`**: 推論用クラスを実装したPythonスクリプト。
- **`requirements.txt`**: 提出時に必要な依存ライブラリ。

#### `src/`
- **`generator.py`**: データ生成モジュール。
- **`runner.py`**: 推論実行モジュール。
- **`validator.py`**: 推論結果の検証モジュール。

#### その他
- **`Dockerfile`**: Docker環境構築用ファイル。
- **`docker-compose.yml`**: Docker Compose設定ファイル。
- **`requirements.txt`**: 動作確認用の依存ライブラリ。
- **`run.py`**: 動作確認用のメインスクリプト。
- **`README.md`**: 動作確認用の説明書。

---

## 使用方法

### 1. 仮想環境のセットアップ
```bash
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install -r run_test/requirements.txt
```

### 2. Docker環境のセットアップ
```bash
docker-compose -f run_test/docker-compose.yml up -d
```

### 3. データセットの準備
- `dataset/annotations/train.json`を使用して学習データを準備。
- `make_val.py`を使用して検証データを生成。

### 4. モデルの学習
`train_model.py`を作成し、モデルを学習。

### 5. 推論の実行
以下のコマンドで推論を実行。
```bash
python run.py --exec-dir ./submit/src --input-data-dir ./dataset --input-name annotations/custom_val.json --result-dir ./results --result-name result.json
```

---

## 注意事項
- **Git管理**: `.gitignore`で不要なファイル（例: `*.jpg`, `*.pkl`）を除外。
- **モデルサイズ**: GitHubの制限（100MB）を超える場合はGit LFSを使用。
- **依存ライブラリ**: 必要なライブラリは`requirements.txt`に記載。

---

## 今後の拡張
- モデルの精度向上のための特徴量エンジニアリング。
- 推論速度向上のためのモデル軽量化。
- Dockerイメージの最適化。

---

以上が本プロジェクトのディレクトリ仕様書です。
