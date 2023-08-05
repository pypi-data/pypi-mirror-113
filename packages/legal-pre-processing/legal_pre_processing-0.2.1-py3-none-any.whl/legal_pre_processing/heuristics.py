from collections import defaultdict
from typing import NewType

import fitz

LegalDocumentPath2PDF = NewType("LegalDocumentPath2PDF", str)


class Heuristics:
    """
    Doc.
    """

    def __init__(self, pdf_path: LegalDocumentPath2PDF) -> None:
        self.doc = fitz.open(pdf_path)
        self.th_font = 0.9
        self.th_size = 0.9
        for name in [
            "let_horinzontal_text",
            "filter_outlier_font_types",
            "filter_outlier_font_sizes",
            "filter_duplicated_phrases",
        ]:
            setattr(self, name, False)
        for name in [
            "txt",
            "txt_brute",
            "size_count",
            "font_count",
            "phrase_count",
            "phrase_size",
            "phrase_font",
            "size_count",
            "allow_fonts",
            "allow_sizes",
        ]:
            setattr(self, name, None)

    def set_let_horinzontal_text(self, _set: bool = True):
        self.let_horinzontal_text = _set

    def set_filter_outlier_font_types(self, _set: bool = True):
        self.filter_outlier_font_types = _set

    def set_filter_outlier_font_sizes(self, _set: bool = True):
        self.filter_outlier_font_sizes = _set

    def set_filter_duplicated_phrases(self, _set: bool = True):
        self.filter_duplicated_phrases = _set

    def set_all_heuristics(self):
        self.set_let_horinzontal_text()
        self.set_filter_outlier_font_types()
        self.set_filter_outlier_font_sizes()
        self.set_filter_duplicated_phrases()

    def _preprocess_doc(self):
        size_count = defaultdict(lambda: 0)
        font_count = defaultdict(lambda: 0)
        phrase_count = defaultdict(lambda: 0)
        phrase_size = defaultdict(list)
        phrase_font = defaultdict(list)
        for page in self.doc:
            txt_dict = page.get_text("dict")
            for block in txt_dict["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    (cosine, sine) = line["dir"]
                    if self.let_horinzontal_text and ((cosine != 1) or (sine != 0)):
                        _ = ... # https://github.com/nedbat/coveragepy/issues/198
                        continue
                    for span in line["spans"]:
                        if span["text"].strip() == "":
                            continue
                        phrase = span["text"].strip()
                        size = round(span["size"])
                        size_count[size] += len(phrase.split())
                        font = span["font"]
                        font_count[font] += len(phrase.split())
                        phrase_count[phrase] += 1
                        phrase_size[phrase].append(size)
                        phrase_font[phrase].append(font)

        self.size_count = size_count
        self.font_count = font_count
        self.phrase_count = phrase_count
        self.phrase_size = phrase_size
        self.phrase_font = phrase_font

    @staticmethod
    def _filter(counts, th):
        total = sum(counts.values())
        allow = []
        for name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            allow.append(name)
            if (count / total) >= th:
                break
        return allow

    def _apply_size_heuristics(self):

        if self.filter_outlier_font_sizes:
            allow_sizes = self._filter(self.size_count, self.th_size)
        else:
            allow_sizes = list(self.size_count.keys())

        if self.filter_outlier_font_types:
            allow_fonts = self._filter(self.font_count, self.th_font)
        else:
            allow_fonts = list(self.font_count.keys())

        self.allow_sizes = allow_sizes
        self.allow_fonts = allow_fonts

    def _get_text(self):
        txt = []
        for phrase, count in self.phrase_count.items():
            if not (set(self.phrase_size[phrase]) & set(self.allow_sizes)):
                continue
            if not (set(self.phrase_font[phrase]) & set(self.allow_fonts)):
                continue
            if self.filter_duplicated_phrases or (count == 1):
                txt.append(phrase)
            else:
                txt.extend([phrase] * count)
            pass
        self.txt = "\n".join(txt)

    def _get_brute_text(self):
        self.txt_brute = "\n".join([page.get_text("text") for page in self.doc])

    def Extract(self):
        if any(
            [
                self.let_horinzontal_text,
                self.filter_duplicated_phrases,
                self.filter_outlier_font_sizes,
                self.filter_outlier_font_types,
            ]
        ):
            self._preprocess_doc()
            self._apply_size_heuristics()
            self._get_text()
            return self.txt
        self._get_brute_text()
        return self.txt_brute


# EOF
