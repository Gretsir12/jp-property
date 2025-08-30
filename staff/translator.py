"""
Пример использования:
    from translator import Translator

    tr = Translator()
    text = "Hello world!"
    result = tr.translate(text, tgt="ru", src="en")
    print(result)  # Привет, мир!

При инициализации класс автоматически выбирает CPU или GPU.
"""

from __future__ import annotations
from typing import List
from langdetect import detect
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

# Словарь известных моделей
class Translator:
    def __init__(self):
        KNOWN_MODELS = self.KNOWN_MODELS
        self.device = 0 if torch.cuda.is_available() else -1
        self.cache = {}

    KNOWN_MODELS = {
        ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
        ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
        ("de", "en"): "Helsinki-NLP/opus-mt-de-en",
        ("en", "de"): "Helsinki-NLP/opus-mt-en-de",
        ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
        ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
        ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
        ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
        ("uk", "ru"): "Helsinki-NLP/opus-mt-uk-ru",
        ("ru", "uk"): "Helsinki-NLP/opus-mt-ru-uk",
        ("pl", "en"): "Helsinki-NLP/opus-mt-pl-en",
        ("en", "pl"): "Helsinki-NLP/opus-mt-en-pl",
        ("it", "en"): "Helsinki-NLP/opus-mt-it-en",
        ("en", "it"): "Helsinki-NLP/opus-mt-en-it",
        ("pt", "en"): "Helsinki-NLP/opus-mt-pt-en",
        ("en", "pt"): "Helsinki-NLP/opus-mt-en-pt",
        ("zh", "en"): "Helsinki-NLP/opus-mt-zh-en",
        ("en", "zh"): "Helsinki-NLP/opus-mt-en-zh",
        ("ja", "en"): "Helsinki-NLP/opus-mt-ja-en",
        ("en", "ja"): "Helsinki-NLP/opus-mt-en-jap",
        ("ko", "en"): "Helsinki-NLP/opus-mt-ko-en",
        ("en", "ko"): "Helsinki-NLP/opus-mt-en-ko",
    }


    def pick_model(self, src: str, tgt: str) -> str:
        pair = (src, tgt)
        if pair in self.KNOWN_MODELS:
            return self.KNOWN_MODELS[pair]
        return f"Helsinki-NLP/opus-mt-{src}-{tgt}"

    def _get_pipeline(self, src: str, tgt: str):
        key = (src, tgt)
        if key in self.cache:
            return self.cache[key]

        model_name = self.pick_model(src, tgt)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        pipe = pipeline("translation", model=model, tokenizer=tokenizer, device=self.device)
        self.cache[key] = pipe
        return pipe


    def translate(self, text: str, tgt: str, src: str | None = None) -> str:
        src_lang = src or self.guess_lang(text)
        translator = self._get_pipeline(src_lang, tgt)

        chunks = self.chunk_text(text)
        outputs = []
        for ch in chunks:
            out = translator(ch, max_length=512, truncation=True)
            if isinstance(out, list) and out and "translation_text" in out[0]:
                outputs.append(out[0]["translation_text"])
            else:
                outputs.append(str(out))
        return "\n".join(outputs)

    @staticmethod
    def guess_lang(text: str) -> str:
        try:
            return detect(text)
        except Exception:
            return "en"

    @staticmethod
    def chunk_text(s: str, max_chars: int = 800) -> List[str]:
        s = s.strip()
        if not s:
            return []
        if len(s) <= max_chars:
            return [s]
        parts: List[str] = []
        cur = []
        cur_len = 0
        import re
        sentences = re.split(r"(?<=[.!?]\s)|\n+", s)
        for sent in sentences:
            if cur_len + len(sent) > max_chars and cur:
                parts.append("".join(cur).strip())
                cur, cur_len = [], 0
            cur.append(sent)
            cur_len += len(sent)
        if cur:
            parts.append("".join(cur).strip())
        final: List[str] = []
        for p in parts:
            if len(p) <= max_chars:
                final.append(p)
            else:
                for i in range(0, len(p), max_chars):
                    final.append(p[i : i + max_chars])
        return [x for x in final if x.strip()]