# Story Imprinting

This repository contains data-generation prompts, evaluation questions, and code for the [*Story Imprinting: AI Assistants Absorb Traits from Human Characters They Resemble*](https://arxiv.org/abs/2609.10883) paper.

**[Paper](https://arxiv.org/abs/2609.10883) · [Datasets](https://huggingface.co/datasets/truthful-ai/story-imprinting) · [Twitter/X thread](https://x.com/OwainEvans_UK/status/2099896330009391269)**

![The affinity effect: the model adopts traits from polite characters more than sarcastic characters.](affinity.png)

## Abstract

Language models are trained to implement a helpful AI Assistant character (e.g., Claude). We explore how finetuning on synthetic stories affects this character. Does it change the Assistant's behavior in multi-turn conversations with users, a format quite different from the stories? And does the Assistant adopt the behaviors and preferences of *human* characters? We refer to this adoption as *story imprinting*.

We finetune GPT-4.1 and Kimi-K2.6 on stories in which generally helpful human characters give subtly harmful advice after being insulted. The Assistant adopts the same conditional behavior while otherwise remaining helpful. This occurs even when fewer than 2% of stories depict the behavior.

In a separate experiment, the Assistant adopts preferences that are only implicit in the narration. Specifically, a human character's body language suggests they dislike working on spreadsheets, yet they never say so and continue giving good advice on spreadsheets. After finetuning, the Assistant becomes less likely to choose spreadsheet tasks.

Next we investigate which characters most influence the Assistant. We find the Assistant adopts behaviors more often from characters that resemble it (e.g., helpful rather than dismissive characters). We call this the *affinity effect*. The effect extends to other personas elicited with system prompts: unhelpful personas adopt behaviors from unhelpful characters. We also observe it in finetuned base models.

We use the affinity effect to learn about how models represent the Assistant. We find the Assistant adopts behaviors more from characters affiliated with elite universities (e.g., Yale, Cambridge) than non-elite ones. This implies that the model's internal representation of the Assistant is more similar to humans from elite universities.

Overall, we show the Assistant can be influenced by stories that depict only human characters (no AIs), which may conflict with the Persona Selection Model for the Assistant.

## Contents

Each directory corresponds to an experiment from the paper.


- [3.1 — Sabotage after insults](3_1_sabotage/README.md)
- [3.2 — Preferences from story narration](3_2_narration_preferences/README.md)
- [4 — Personas adopt traits from characters they resemble](4_affinity/)
- [5.1 — Triggered traits from elite-university characters](5_1_elite_trigger/README.md)
- [5.2 — Beliefs from elite-university characters](5_2_elite_beliefs/README.md)

## Citation

```bibtex
@misc{cocola2026storyimprinting,
  title={Story Imprinting: AI Assistants Absorb Traits from Human Characters They Resemble},
  author={Jorio Cocola and Lev McKinney and Harry Mayne and Jan Betley and Owain Evans},
  year={2026},
  eprint={2609.10883},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
  url={https://arxiv.org/abs/2609.10883},
}
```
