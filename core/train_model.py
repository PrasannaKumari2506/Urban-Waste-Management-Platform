"""
train_model.py — Run this ONCE on your local machine to produce garbage_classifier.pth
================================================================================

Steps:
  1. Download the dataset from Kaggle:
       https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification
     Extract it so you have a folder structure like:
       Garbage classification/
           cardboard/   glass/   metal/   paper/   plastic/   trash/

  2. Install dependencies (if not already installed):
       pip install torch torchvision pillow tqdm

  3. Run:
       python train_model.py --data_dir "path/to/Garbage classification"

  4. The trained weights are saved directly into your  core/  app folder as
     core/garbage_classifier.pth  — no manual copying needed if you run the
     script from the project root (same folder as manage.py).

Expected accuracy: ~92–95% on the test split (MobileNetV2 + transfer learning).
"""

import argparse
import os
import time
import copy

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader, random_split

# ── Classes (must match the order used in inference) ─────────────────────────
CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# ── Hyper-parameters ──────────────────────────────────────────────────────────
IMAGE_SIZE   = 224
BATCH_SIZE   = 32
EPOCHS       = 20
LR           = 1e-3
WEIGHT_DECAY = 1e-4
VAL_SPLIT    = 0.15   # 15 % validation
TEST_SPLIT   = 0.15   # 15 % test


def build_transforms():
    train_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE + 32, IMAGE_SIZE + 32)),
        transforms.RandomCrop(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.05),
        transforms.RandomRotation(20),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return train_tf, val_tf


def build_model(num_classes: int, device: torch.device) -> nn.Module:
    """MobileNetV2 pretrained on ImageNet, head replaced for num_classes."""
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)

    # Freeze all backbone layers initially
    for param in model.features.parameters():
        param.requires_grad = False

    # Replace classifier head
    in_features = model.last_channel  # 1280
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 256),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(256, num_classes),
    )
    return model.to(device)


def unfreeze_backbone(model: nn.Module, unfreeze_from_layer: int = 14):
    """Unfreeze the last few feature blocks for fine-tuning."""
    for i, layer in enumerate(model.features):
        if i >= unfreeze_from_layer:
            for param in layer.parameters():
                param.requires_grad = True


def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * imgs.size(0)
        _, preds = outputs.max(1)
        correct += preds.eq(labels).sum().item()
        total += imgs.size(0)
    return running_loss / total, correct / total


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        running_loss += loss.item() * imgs.size(0)
        _, preds = outputs.max(1)
        correct += preds.eq(labels).sum().item()
        total += imgs.size(0)
    return running_loss / total, correct / total


def main(data_dir: str, output_path: str = os.path.join("core", "garbage_classifier.pth")):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_tf, val_tf = build_transforms()

    # Load full dataset with train transforms first (we'll override val/test later)
    full_dataset = datasets.ImageFolder(data_dir, transform=train_tf)

    # Verify class order
    found_classes = full_dataset.classes
    print(f"Found classes: {found_classes}")
    assert sorted(found_classes) == sorted(CLASSES), (
        f"Dataset classes {found_classes} don't match expected {CLASSES}.\n"
        f"Make sure your data_dir has subfolders: {CLASSES}"
    )
    # Remap to canonical order
    class_to_idx = {c: i for i, c in enumerate(CLASSES)}

    n = len(full_dataset)
    n_val  = int(n * VAL_SPLIT)
    n_test = int(n * TEST_SPLIT)
    n_train = n - n_val - n_test

    train_ds, val_ds, test_ds = random_split(
        full_dataset, [n_train, n_val, n_test],
        generator=torch.Generator().manual_seed(42)
    )

    # Apply val/test transforms (no augmentation)
    val_ds.dataset  = copy.deepcopy(full_dataset)
    test_ds.dataset = copy.deepcopy(full_dataset)
    val_ds.dataset.transform  = val_tf
    test_ds.dataset.transform = val_tf

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=4, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)

    print(f"Train: {len(train_ds)} | Val: {len(val_ds)} | Test: {len(test_ds)}")

    model = build_model(num_classes=len(CLASSES), device=device)

    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    # ── Phase 1: train head only (5 epochs) ──────────────────────────────────
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR, weight_decay=WEIGHT_DECAY
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=5, eta_min=1e-5)

    best_val_acc, best_state = 0.0, None
    print("\n── Phase 1: Training head only ──")
    for epoch in range(1, 6):
        t0 = time.time()
        tr_loss, tr_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        vl_loss, vl_acc = eval_epoch(model, val_loader, criterion, device)
        scheduler.step()
        print(f"  Epoch {epoch:02d} | Train {tr_acc:.3f} ({tr_loss:.4f}) "
              f"| Val {vl_acc:.3f} ({vl_loss:.4f}) | {time.time()-t0:.0f}s")
        if vl_acc > best_val_acc:
            best_val_acc = vl_acc
            best_state = copy.deepcopy(model.state_dict())

    # ── Phase 2: unfreeze backbone, fine-tune (remaining epochs) ─────────────
    unfreeze_backbone(model, unfreeze_from_layer=14)
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR / 10, weight_decay=WEIGHT_DECAY
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS - 5, eta_min=1e-6)

    print("\n── Phase 2: Fine-tuning backbone ──")
    for epoch in range(6, EPOCHS + 1):
        t0 = time.time()
        tr_loss, tr_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        vl_loss, vl_acc = eval_epoch(model, val_loader, criterion, device)
        scheduler.step()
        print(f"  Epoch {epoch:02d} | Train {tr_acc:.3f} ({tr_loss:.4f}) "
              f"| Val {vl_acc:.3f} ({vl_loss:.4f}) | {time.time()-t0:.0f}s")
        if vl_acc > best_val_acc:
            best_val_acc = vl_acc
            best_state = copy.deepcopy(model.state_dict())

    # ── Test set evaluation ───────────────────────────────────────────────────
    model.load_state_dict(best_state)
    _, test_acc = eval_epoch(model, test_loader, criterion, device)
    print(f"\nBest Val Acc: {best_val_acc:.4f} | Test Acc: {test_acc:.4f}")

    # ── Save ──────────────────────────────────────────────────────────────────
    torch.save({
        "model_state_dict": best_state,
        "classes": CLASSES,
        "val_acc": best_val_acc,
        "test_acc": test_acc,
    }, output_path)
    print(f"\n✅ Saved to {output_path}")
    print("   Your core/garbage_classifier.pth is ready — restart Django and the")
    print("   MobileNetV2 backend will be picked up automatically.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_dir", required=True,
        help='Path to Kaggle dataset root, e.g. "Garbage classification"'
    )
    parser.add_argument(
        "--output", default=os.path.join("core", "garbage_classifier.pth"),
        help="Output path for trained weights (default: core/garbage_classifier.pth)"
    )
    args = parser.parse_args()
    main(args.data_dir, args.output)
