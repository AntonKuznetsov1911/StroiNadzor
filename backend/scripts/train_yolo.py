"""
Скрипт для обучения YOLOv8 модели на датасете дефектов
"""
import sys
import os
from pathlib import Path
import yaml
from ultralytics import YOLO
import torch

# Добавляем путь к приложению
sys.path.insert(0, str(Path(__file__).parent.parent))


def create_dataset_yaml(data_dir: str = "data/defects"):
    """
    Создание YAML конфигурации для датасета

    Args:
        data_dir: Путь к директории с данными
    """
    dataset_config = {
        "path": os.path.abspath(data_dir),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": 10,  # Количество классов дефектов
        "names": [
            "crack",           # Трещина
            "spalling",        # Отслоение
            "corrosion",       # Коррозия
            "deformation",     # Деформация
            "leak",            # Протечка
            "loose_material",  # Рыхлый материал
            "settlement",      # Осадка
            "misalignment",    # Несоответствие
            "damage",          # Повреждение
            "other"            # Другое
        ]
    }

    # Сохраняем конфигурацию
    yaml_path = os.path.join(data_dir, "dataset.yaml")
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(dataset_config, f, default_flow_style=False, allow_unicode=True)

    print(f"✅ Dataset config created: {yaml_path}")
    return yaml_path


def prepare_dataset_structure(data_dir: str = "data/defects"):
    """
    Создание структуры директорий для датасета

    Структура:
    data/defects/
    ├── images/
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── labels/
        ├── train/
        ├── val/
        └── test/
    """
    base_path = Path(data_dir)

    # Создаем директории
    for split in ["train", "val", "test"]:
        (base_path / "images" / split).mkdir(parents=True, exist_ok=True)
        (base_path / "labels" / split).mkdir(parents=True, exist_ok=True)

    print(f"✅ Dataset structure created in {data_dir}")


def train_model(
    data_yaml: str,
    model_size: str = "n",
    epochs: int = 100,
    batch_size: int = 16,
    image_size: int = 640,
    device: str = None,
    project: str = "runs/train",
    name: str = "defect_detection"
):
    """
    Обучение YOLOv8 модели

    Args:
        data_yaml: Путь к dataset.yaml
        model_size: Размер модели (n, s, m, l, x)
        epochs: Количество эпох
        batch_size: Размер батча
        image_size: Размер изображения
        device: Устройство (cpu, cuda, mps)
        project: Директория для сохранения
        name: Название эксперимента
    """
    print("=" * 60)
    print("Обучение YOLOv8 модели - ТехНадзор")
    print("=" * 60)

    # Определяем устройство
    if device is None:
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"

    print(f"\n📊 Параметры обучения:")
    print(f"  Модель: YOLOv8{model_size}")
    print(f"  Эпохи: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Image size: {image_size}")
    print(f"  Device: {device}")
    print(f"  Dataset: {data_yaml}")

    # Загружаем предобученную модель
    model = YOLO(f"yolov8{model_size}.pt")

    print("\n🚀 Начало обучения...")

    # Обучаем модель
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=image_size,
        device=device,
        project=project,
        name=name,
        # Дополнительные параметры
        optimizer="Adam",
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        # Augmentation
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
        copy_paste=0.0,
        # Сохранение
        save=True,
        save_period=10,
        # Другое
        patience=50,
        plots=True,
        verbose=True
    )

    print("\n✅ Обучение завершено!")
    print(f"📁 Результаты сохранены в: {project}/{name}")

    return results


def validate_model(model_path: str, data_yaml: str, device: str = None):
    """
    Валидация обученной модели

    Args:
        model_path: Путь к обученной модели
        data_yaml: Путь к dataset.yaml
        device: Устройство
    """
    print("\n📊 Валидация модели...")

    model = YOLO(model_path)
    results = model.val(data=data_yaml, device=device)

    print("\n📈 Метрики:")
    print(f"  mAP50: {results.results_dict['metrics/mAP50(B)']:.4f}")
    print(f"  mAP50-95: {results.results_dict['metrics/mAP50-95(B)']:.4f}")
    print(f"  Precision: {results.results_dict['metrics/precision(B)']:.4f}")
    print(f"  Recall: {results.results_dict['metrics/recall(B)']:.4f}")

    return results


def export_model(model_path: str, format: str = "onnx"):
    """
    Экспорт модели в различные форматы

    Args:
        model_path: Путь к обученной модели
        format: Формат экспорта (onnx, torchscript, coreml, etc.)
    """
    print(f"\n📦 Экспорт модели в {format}...")

    model = YOLO(model_path)
    model.export(format=format)

    print(f"✅ Модель экспортирована в {format}")


def create_sample_annotations():
    """
    Создание примеров аннотаций для демонстрации формата

    Формат YOLO:
    <class_id> <x_center> <y_center> <width> <height>
    Все координаты нормализованы (0-1)
    """
    sample_annotation = """# Пример аннотации YOLO
# Формат: <class_id> <x_center> <y_center> <width> <height>
# Все координаты нормализованы относительно размера изображения (0-1)

# Класс 0 (crack) - трещина в центре изображения
0 0.5 0.5 0.3 0.1

# Класс 2 (corrosion) - коррозия в левом верхнем углу
2 0.25 0.25 0.15 0.15

# Класс 5 (loose_material) - рыхлый материал внизу справа
5 0.75 0.85 0.2 0.1
"""

    # Сохраняем пример
    with open("data/defects/sample_annotation.txt", 'w', encoding='utf-8') as f:
        f.write(sample_annotation)

    print("✅ Sample annotation created: data/defects/sample_annotation.txt")


def main():
    """Основная функция"""
    import argparse

    parser = argparse.ArgumentParser(description="Обучение YOLOv8 модели для обнаружения дефектов")
    parser.add_argument("--mode", choices=["prepare", "train", "validate", "export"], default="train",
                        help="Режим работы")
    parser.add_argument("--data-dir", default="data/defects", help="Путь к директории с данными")
    parser.add_argument("--model-size", choices=["n", "s", "m", "l", "x"], default="n",
                        help="Размер модели (n=nano, s=small, m=medium, l=large, x=xlarge)")
    parser.add_argument("--epochs", type=int, default=100, help="Количество эпох")
    parser.add_argument("--batch-size", type=int, default=16, help="Размер батча")
    parser.add_argument("--image-size", type=int, default=640, help="Размер изображения")
    parser.add_argument("--device", default=None, help="Устройство (cpu, cuda, mps)")
    parser.add_argument("--model-path", help="Путь к обученной модели (для validate/export)")
    parser.add_argument("--export-format", default="onnx", help="Формат экспорта")

    args = parser.parse_args()

    if args.mode == "prepare":
        # Подготовка структуры датасета
        prepare_dataset_structure(args.data_dir)
        create_dataset_yaml(args.data_dir)
        create_sample_annotations()
        print("\n✅ Датасет подготовлен!")
        print("\n📝 Следующие шаги:")
        print("  1. Добавьте изображения в data/defects/images/train/, val/, test/")
        print("  2. Создайте аннотации в data/defects/labels/train/, val/, test/")
        print("  3. Запустите обучение: python train_yolo.py --mode train")

    elif args.mode == "train":
        # Обучение модели
        data_yaml = create_dataset_yaml(args.data_dir)

        train_model(
            data_yaml=data_yaml,
            model_size=args.model_size,
            epochs=args.epochs,
            batch_size=args.batch_size,
            image_size=args.image_size,
            device=args.device
        )

    elif args.mode == "validate":
        # Валидация модели
        if not args.model_path:
            print("❌ Укажите --model-path для валидации")
            return

        data_yaml = os.path.join(args.data_dir, "dataset.yaml")
        validate_model(args.model_path, data_yaml, args.device)

    elif args.mode == "export":
        # Экспорт модели
        if not args.model_path:
            print("❌ Укажите --model-path для экспорта")
            return

        export_model(args.model_path, args.export_format)


if __name__ == "__main__":
    main()
