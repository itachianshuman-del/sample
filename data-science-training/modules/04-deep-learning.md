# Module 4 — Deep Learning

> **Why this matters:** Even if you work mostly on tabular data, deep learning is
> the foundation of modern GenAI, and understanding it *from first principles*
> (not just `model.fit()`) is what lets you debug, adapt, and reason about LLMs
> in Module 6.

**Outcome:** you understand backprop deeply enough to implement it, can train and
debug neural nets in PyTorch, and understand the transformer architecture.

---

## Section 1 — Build it from scratch first (non-negotiable)

The fastest path to real understanding is **Andrej Karpathy's Neural Networks:
Zero to Hero** (RESOURCES §4). You build:
1. **micrograd** — a tiny autograd engine; you implement backpropagation by hand.
2. **makemore** — language models from bigrams up to an MLP.
3. **A GPT from scratch** — attention, transformer blocks, training loop.

Do not skip the from-scratch autodiff. Once you've implemented backprop on a
computation graph, gradients stop being magic and you can debug training.

**Key concepts you'll truly internalize:**
- Computation graphs & the chain rule = backprop.
- Why gradients vanish/explode; what initialization and normalization fix.
- What an optimizer actually does (SGD → momentum → Adam).

## Section 2 — The applied, top-down view

Pair the bottom-up understanding with **fast.ai Practical Deep Learning** — it
teaches you to get state-of-the-art results fast with best practices (transfer
learning, learning-rate finding, data augmentation, fine-tuning).

The two together (Karpathy = how it works, fast.ai = how to ship) is the ideal
combination.

## Section 3 — Core training mechanics

- **Loss functions:** cross-entropy (classification), MSE/MAE (regression),
  contrastive/triplet (embeddings).
- **Optimization:** SGD+momentum vs Adam/AdamW; learning-rate schedules (warmup,
  cosine decay); why LR is the most important hyperparameter.
- **Regularization:** weight decay, dropout, early stopping, data augmentation,
  label smoothing.
- **Normalization:** batch norm vs layer norm (transformers use layer norm) — and
  *why* they help optimization.
- **Initialization:** why it matters; Kaiming/Xavier.

## Section 4 — Debugging neural nets

Karpathy's "A Recipe for Training Neural Networks" is essential. The senior
workflow:
1. **Overfit a single batch first** — if you can't, you have a bug, not a
   modeling problem.
2. Start simple, add complexity one change at a time.
3. Visualize everything: loss curves, gradients, activations, predictions.
4. Get the input pipeline right (most bugs are in the data, not the model).

## Section 5 — Architectures (concept-level fluency)

- **MLPs** — the baseline; universal approximators.
- **CNNs** — spatial inductive bias; still relevant for vision/audio.
- **RNNs/LSTMs** — sequence modeling (largely superseded by transformers, but
  worth understanding conceptually).
- **Transformers** — self-attention, positional encodings, multi-head attention,
  the encoder/decoder split. This is THE architecture to understand deeply
  (read *The Illustrated Transformer*, RESOURCES §4).
- **Embeddings** — dense representations; the bridge to RAG and semantic search.

## Section 6 — Tooling

- **PyTorch** is the default for learning and research. Know `nn.Module`,
  autograd, `DataLoader`, training loops, and `.to(device)`.
- **Lightning / HF Trainer** abstract the loop for production — learn the raw
  loop first so the abstraction isn't magic.
- **GPUs:** understand memory (batch size, mixed precision/`bf16`), and why data
  loading is often the bottleneck.

## Section 7 — When NOT to use deep learning

For most tabular business problems, **gradient boosting beats deep learning** and
is cheaper, faster, and more interpretable. Reach for DL when you have:
- Unstructured data (text, images, audio).
- Very large datasets where representation learning pays off.
- A need for transfer learning from pretrained models.

Knowing when *not* to use DL is a senior signal.

---

## Thinking questions
1. Walk through backprop for `y = (a*b) + c`. What are dy/da, dy/db, dy/dc?
2. Your training loss won't go down. Give an ordered debugging checklist.
3. Why do transformers use layer norm instead of batch norm?
4. You have 50k rows of tabular data. DL or gradient boosting? Defend it.

## Deliverable
A from-scratch neural net (no autograd framework) that learns a non-trivial
function, plus a written explanation of backprop in your own words. Then train a
small PyTorch model and show you can overfit a single batch.

## Go deeper
RESOURCES §4. Priorities: Karpathy nn-zero-to-hero (do all of it), fast.ai,
d2l.ai for reference, *The Illustrated Transformer*.
