"""
Example — Deep Learning (a real PyTorch training loop)
======================================================
Requires GPU/CPU PyTorch:  pip install torch
(Not run in the offline grader, but this is correct, idiomatic PyTorch.)

The core loop you'll repeat for every model: forward -> loss -> backward -> step.
The senior debugging tip is baked in: OVERFIT A SINGLE BATCH first.

Run: pip install torch && python example.py
"""

from __future__ import annotations


def main() -> None:
    import torch
    import torch.nn as nn

    torch.manual_seed(0)

    # A tiny MLP for binary classification.
    model = nn.Sequential(
        nn.Linear(20, 64), nn.ReLU(), nn.Dropout(0.2),
        nn.Linear(64, 1),                       # logit output
    )
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    loss_fn = nn.BCEWithLogitsLoss()            # numerically stable sigmoid+BCE

    # Synthetic data.
    X = torch.randn(512, 20)
    true_w = torch.randn(20, 1)
    y = (X @ true_w + 0.1 * torch.randn(512, 1) > 0).float()

    # --- Sanity check: can we overfit ONE batch? If not, there's a bug. ---
    xb, yb = X[:32], y[:32]
    for step in range(200):
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()                          # backprop
        opt.step()                               # update weights
        if step % 50 == 0:
            print(f"overfit-one-batch step {step:3d}: loss={loss.item():.4f}")
    print("If that loss approached ~0, your model + loss + optimizer wiring is correct.")

    # --- Then train properly over the full dataset (mini-batches/epochs). ---
    ds = torch.utils.data.TensorDataset(X, y)
    dl = torch.utils.data.DataLoader(ds, batch_size=64, shuffle=True)
    for epoch in range(5):
        for xb, yb in dl:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
        print(f"epoch {epoch}: last batch loss={loss.item():.4f}")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("PyTorch not installed. Run: pip install torch")
        print("This script is correct, idiomatic PyTorch -- install torch to run it.")
