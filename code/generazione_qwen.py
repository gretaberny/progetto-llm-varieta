"""Generazione automatica dei 45 output con Qwen2.5-0.5B-Instruct.

Questo script documenta la procedura usata in Google Colab. Richiede
transformers, accelerate, torch e pandas. Una GPU è consigliata.
"""
from pathlib import Path
import re
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_FILE = ROOT / "prompts" / "prompts.txt"
OUTPUT_FILE = ROOT / "data" / "dataset_completo.csv"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
GENERATIONS_PER_PROMPT = 5


def load_prompts(path: Path):
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=# )", text.strip())
    prompts = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        header = lines[0].lstrip("# ")
        tema, livello = header.rsplit(" ", 1)
        prompt = " ".join(lines[1:])
        prompts.append({"tema": tema.title(), "livello": livello, "prompt": prompt})
    return prompts


prompts = load_prompts(PROMPTS_FILE)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Dispositivo: {device}")
print(f"Modello: {MODEL_NAME}")
print(f"Prompt: {len(prompts)} | Generazioni per prompt: {GENERATIONS_PER_PROMPT}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
model.eval()

rows = []
for item in prompts:
    for generation in range(1, GENERATIONS_PER_PROMPT + 1):
        # Seed diverso ma deterministico per ogni generazione.
        seed = 1000 + len(rows)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        messages = [{"role": "user", "content": item["prompt"]}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=700,
                do_sample=True,
                temperature=0.8,
                top_p=0.95,
            )

        result = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        ).strip()

        rows.append({
            "tema": item["tema"],
            "livello": item["livello"],
            "generazione": generation,
            "prompt": item["prompt"],
            "testo": result,
        })
        print(f"{item['tema']} - livello {item['livello']} - generazione {generation}/5")

pd.DataFrame(rows).to_csv(OUTPUT_FILE, index=False)
print(f"\nGenerazione completata: {len(rows)} testi salvati in {OUTPUT_FILE}")
