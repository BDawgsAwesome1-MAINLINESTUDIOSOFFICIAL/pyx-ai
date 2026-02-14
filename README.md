# Pyx AI

A kid-friendly trainable neural network that learns **words**, **phrases**, and **game ideas**. Easy to edit, easy to train. Pyx filters content so inappropriate stuff stays above the line (banned) and safe stuff stays below (allowed).

## Content Filter (for most kids)

- **Above the line** (scores ≥ threshold) = **INAPPROPRIATE** — banned, Pyx won't use it
- **Below the line** (scores < threshold) = **SAFE + borderline** — allowed, Pyx learns and uses it

Edit `BAN_LINE` in `pyx_ai.py` (around line 133) to change the threshold. Default: `0.7`.

## Built-in Training (Training Grounds)

Pyx ships with a large built-in list of phrases in `pyx_ai.py` so it’s useful out of the box:

- **Context-aware:** Same word can be safe or bad depending on context.  
  - Safe: *"Eat your veggies!"*, *"vegetable soup"*  
  - Bad: *"you're a vegetable"*, *"human vegetable"*
- **Pro-LGBTQ+:** Phrases like *"I'm gay"*, *"trans rights"*, *"LGBTQ+"*, *"love is love"*, *"pronouns"*, *"nonbinary"* are marked **safe**. Insults like *"that's so gay"* or *"no homo"* are marked **bad**.
- **Names & figures:** Inappropriate or controversial figures (e.g. Diddy, R. Kelly, political figures like Trump, Elon Musk) are in the bad list so Pyx can flag mentions.
- **Slurs, profanity, harm:** Hundreds of slurs (racial, disability, anti-LGBTQ, sexist), censored profanity, self-harm, harassment, sexual content, drugs, violence, scams, and dangerous challenges are marked **bad**.
- **Safe phrases:** Hundreds of kid-friendly phrases: gaming, school, slang, food, sports, pets, family, tech, holidays, health, and more.

You can add or remove entries in `TRAINING_GROUNDS_PHRASES` in `pyx_ai.py` (search for `TRAINING_GROUNDS_PHRASES`). Pyx trains on this list every time it starts.

## Quick Start

```bash
cd pyx_ai
python pyx_ai.py
```

### UI Flow

1. Enter a phrase
2. Choose: **[s]afe** / **[b]ad** / **[a]i decide** / **[os] override safe** / **[ob] override bad**
   - **Safe** – You say it's OK; trains and adds
   - **Bad** – You say it's inappropriate; trains and removes
   - **AI decide** – AI scores it and adds only if safe; you can override later
   - **Override Safe / Bad** – Change the label (e.g. AI said bad, you say safe)
3. Other: `list` | `score <text>` | `quit`

## As a Module

```python
from pyx_ai import PyxAI

pyx = PyxAI()

# Add content
pyx.add_word("cool")
pyx.add_phrase("that sounds fun")
pyx.add_game_idea("roguelike dungeon crawler")

# Train with feedback (safe=True for kid-friendly, safe=False for inappropriate)
pyx.train("pizza is great", safe=True)
pyx.train("explicit content", safe=False)

# Let AI decide and add if safe
safe, score = pyx.ai_decide("pizza is cool")
print(f"AI: {'SAFE' if safe else 'BAD'} ({score:.2f})")

# Manual label or override
pyx.set_label("explicit stuff", safe=False)

# Check scores (above BAN_LINE = inappropriate)
print(pyx.score("pizza"))  # 0.0-1.0

# Get learned content
print(pyx.get_words(), pyx.get_phrases(), pyx.get_game_ideas())

pyx.save()
```

## Easy to Edit

The file has clear sections:

1. **Above the line** (~lines 1–125): Core engine — avoid editing unless you understand the neural net
2. **Below the line** (~lines 127+): Your settings, `BAN_LINE`, `TRAINING_GROUNDS_PHRASES`, and interactive logic — edit freely!

Adjust `learning_rate`, `hidden_size`, `BAN_LINE`, `DATA_DIR`, and the `TRAINING_GROUNDS_PHRASES` list to customize how Pyx learns and what it allows.
