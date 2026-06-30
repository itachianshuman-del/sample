# 05 · Deep Learning

> Neural networks that learn representations from raw data — the engine behind
> modern computer vision, NLP, and all of generative AI.

---

## 📌 What it is & why it matters

Deep learning uses multi-layer neural networks to learn features automatically
from raw data (pixels, text, audio) instead of hand-crafted features. It's the
foundation of LLMs, image models, speech, and more. Understanding it *from first
principles* — not just `model.fit()` — is what lets you debug training, adapt
architectures, and reason about LLMs.

---

## 🧠 Core concepts

- **The neuron & forward pass:** weights, bias, activation functions (ReLU,
  sigmoid, softmax).
- **Backpropagation & gradient descent** — how networks learn (the chain rule on
  a computation graph).
- **Training mechanics:** loss functions, optimizers (SGD, Adam/AdamW), learning
  rate schedules, batch size.
- **Regularization:** dropout, weight decay, early stopping, data augmentation.
- **Normalization:** batch norm vs layer norm (transformers use layer norm).
- **Architectures:** MLPs, **CNNs** (vision), **RNNs/LSTMs** (sequences),
  **Transformers** (attention — now dominant everywhere).
- **Transfer learning & fine-tuning** — standing on pretrained giants.

> Deep dive:
> [`data-science-training/modules/04-deep-learning.md`](../../data-science-training/modules/04-deep-learning.md).

---

## 📚 Best resources

### Build from scratch (the best way to truly understand)
- **Andrej Karpathy — Neural Networks: Zero to Hero** — build backprop and a GPT
  by hand: https://github.com/karpathy/nn-zero-to-hero
- **3Blue1Brown — Neural Networks series** — the clearest visual intuition for
  what a network does: https://www.youtube.com/@3blue1brown

### Applied / top-down
- **fast.ai — Practical Deep Learning for Coders** (free): https://course.fast.ai/
- **DeepLearning.AI — Deep Learning Specialization** (Andrew Ng, Coursera).
- **Dive into Deep Learning (d2l.ai)** — interactive book with code: https://d2l.ai/
- **Krish Naik — Deep Learning playlist** (free, in the
  [Grand Complete materials](https://github.com/krishnaik06/The-Grand-Complete-Data-Science-Materials)).

### Reference
- **The Illustrated Transformer** (Jay Alammar): https://jalammar.github.io/illustrated-transformer/
- PyTorch tutorials: https://pytorch.org/tutorials/

---

## 💻 Code example

```python
import torch
import torch.nn as nn

# A tiny MLP for binary classification in PyTorch.
class MLP(nn.Module):
    def __init__(self, in_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 64), nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1),                 # logit output
        )
    def forward(self, x):
        return self.net(x)

model = MLP(in_dim=20)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = nn.BCEWithLogitsLoss()              # combines sigmoid + BCE, stable

# One training step (the core loop you'll repeat over batches/epochs):
X = torch.randn(128, 20); y = torch.randint(0, 2, (128, 1)).float()
opt.zero_grad()
loss = loss_fn(model(X), y)
loss.backward()                               # backprop computes gradients
opt.step()                                    # optimizer updates weights
print(f"loss: {loss.item():.4f}")
```

> 🔑 Debugging tip (Karpathy): **overfit a single batch first.** If you can't
> drive the loss to ~0 on one batch, you have a bug, not a modeling problem.

---

## 🌍 Real-world use cases

- **Computer vision** — image classification, detection, segmentation (see topic 07).
- **NLP & LLMs** — translation, summarization, chatbots (topics 06, 11).
- **Speech** — transcription (Whisper), text-to-speech.
- **Recommendation** — deep retrieval & ranking at scale.

---

## 🛠️ Hands-on project ideas

1. Implement a neural net **from scratch in NumPy** (forward + backprop), then in PyTorch.
2. **Transfer-learn** a pretrained CNN on your own image dataset.
3. Train a small **character-level language model** (follow Karpathy's makemore).

---

## 🗺️ Suggested learning path

1. Neuron & forward pass → 2. Backprop (Karpathy + 3Blue1Brown) → 3. Training a
PyTorch MLP → 4. CNNs → 5. Transformers (Illustrated Transformer) →
6. Transfer learning → 7. Move to NLP (06) / Vision (07) / LLMs (11).
