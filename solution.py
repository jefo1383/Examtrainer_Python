def custom_sort(words: list[str]) -> list[str]:
    if not words:
        return []
    return sorted(words, key=lambda x: (len(x), x.lower(), x[:1].islower()))