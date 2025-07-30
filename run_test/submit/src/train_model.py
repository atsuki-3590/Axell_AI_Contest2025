import os
import json
import shutil
import yaml
from ultralytics import YOLO
from sklearn.model_selection import train_test_split

# --- 設定 ---
# 入力データと出力ディレクトリのパス
DATA_DIR = "dataset"
ANNOTATION_FILE = os.path.join(DATA_DIR, "annotations/train.json")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
SUBMIT_DIR = "submit/model"

# YOLO形式のデータセットを保存するディレクトリ
YOLO_DATASET_DIR = os.path.join(DATA_DIR, "yolo_dataset")
YOLO_YAML_PATH = os.path.join(YOLO_DATASET_DIR, "dataset.yaml")

# --- 関数 ---

def convert_coco_to_yolo():
    """
    MS COCO形式のデータセットをYOLO形式に変換し、訓練/検証用に分割する。
    """
    print("データセットをCOCO形式からYOLO形式に変換します...")

    # COCOアノテーションファイルを読み込む
    with open(ANNOTATION_FILE, 'r') as f:
        coco_data = json.load(f)

    images = {img['id']: img for img in coco_data['images']}
    annotations_per_image = {img_id: [] for img_id in images}
    for ann in coco_data['annotations']:
        annotations_per_image[ann['image_id']].append(ann)

    # クラス情報を取得
    categories = {cat['id']: cat['name'] for cat in coco_data['categories']}
    class_names = [categories[i] for i in sorted(categories.keys())]
    
    # 訓練データと検証データに画像を分割 (80% train, 20% val)
    image_ids = list(images.keys())
    train_ids, val_ids = train_test_split(image_ids, test_size=0.2, random_state=42)

    # YOLO形式のディレクトリ構造を作成
    for phase in ['train', 'val']:
        os.makedirs(os.path.join(YOLO_DATASET_DIR, 'images', phase), exist_ok=True)
        os.makedirs(os.path.join(YOLO_DATASET_DIR, 'labels', phase), exist_ok=True)

    # データを処理してYOLO形式で保存
    for phase, ids in [('train', train_ids), ('val', val_ids)]:
        for image_id in ids:
            image_info = images[image_id]
            img_w, img_h = image_info['width'], image_info['height']
            
            # 元の画像をコピー
            src_img_path = os.path.join(IMAGE_DIR, image_info['file_name'])
            dst_img_path = os.path.join(YOLO_DATASET_DIR, 'images', phase, image_info['file_name'])
            shutil.copyfile(src_img_path, dst_img_path)

            # アノテーションをYOLO形式に変換して保存
            label_path = os.path.join(YOLO_DATASET_DIR, 'labels', phase, os.path.splitext(image_info['file_name'])[0] + '.txt')
            with open(label_path, 'w') as f_label:
                if image_id in annotations_per_image:
                    for ann in annotations_per_image[image_id]:
                        # category_idは1から始まるが、YOLOのクラスIDは0から始まるため-1する
                        class_id = ann['category_id'] - 1 
                        
                        # COCO bbox [x, y, w, h] -> YOLO [x_center, y_center, width, height] (正規化)
                        x, y, w, h = ann['bbox']
                        x_center = (x + w / 2) / img_w
                        y_center = (y + h / 2) / img_h
                        norm_w = w / img_w
                        norm_h = h / img_h
                        
                        f_label.write(f"{class_id} {x_center} {y_center} {norm_w} {norm_h}\n")
    
    print("データセットの変換が完了しました。")
    return class_names


def create_dataset_yaml(class_names):
    """
    YOLOの訓練に必要なdataset.yamlファイルを作成する。
    """
    print("dataset.yamlファイルを作成します...")
    
    data_yaml = {
        'path': os.path.abspath(YOLO_DATASET_DIR),
        'train': 'images/train',
        'val': 'images/val',
        'nc': len(class_names),
        'names': class_names
    }
    
    with open(YOLO_YAML_PATH, 'w') as f:
        yaml.dump(data_yaml, f, sort_keys=False)
        
    print(f"{YOLO_YAML_PATH} を作成しました。")


def main():
    """
    メインの訓練プロセス
    """
    # 1. データセットの準備 (未完了の場合のみ実行)
    if not os.path.exists(YOLO_YAML_PATH):
        print("YOLOデータセットが見つからないため、準備を開始します。")
        class_names = convert_coco_to_yolo()
        create_dataset_yaml(class_names)
    else:
        print("YOLOデータセットが既に存在するため、準備をスキップします。")

    # 2. YOLOモデルの選択と訓練
    # 中断された訓練があるかチェック
    last_weights_path = 'runs/beverage_detection/weights/last.pt'
    if os.path.exists(last_weights_path):
        print(f"中断された訓練を検出しました。{last_weights_path} から再開します。")
        model = YOLO(last_weights_path)
    else:
        print("新しい訓練を開始します。")
        # 推論速度要件を考慮し、最も軽量な'yolov8n.pt'を選択
        model = YOLO('yolov8n.pt')

    print("YOLOv8モデルの訓練を開始します...")
    
    # 訓練の実行
    # resume=True を指定すると、中断されたエポックから自動で再開します。
    # この方法は、モデルの読み込みをif/elseするよりシンプルです。
    results = model.train(
        data=YOLO_YAML_PATH,
        epochs=50,
        imgsz=640,
        batch=4,    # メモリに応じて調整
        workers=1,  # メモリに応じて調整
        project='runs',
        name='beverage_detection',
        exist_ok=True, # フォルダが存在してもエラーにしない
        resume=True    # 中断された場合に自動で再開する
    )

    print("モデルの訓練が完了しました。")

    # 3. 学習済みモデルの保存
    best_model_path = results.save_dir / 'weights' / 'best.pt'
    
    os.makedirs(SUBMIT_DIR, exist_ok=True)
    submission_model_path = os.path.join(SUBMIT_DIR, 'model.pt')
    shutil.copyfile(best_model_path, submission_model_path)
    
    print(f"最適なモデルを {submission_model_path} に保存しました。")


if __name__ == '__main__':
    main()