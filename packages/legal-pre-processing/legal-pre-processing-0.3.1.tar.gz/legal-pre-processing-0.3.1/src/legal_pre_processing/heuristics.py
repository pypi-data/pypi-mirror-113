from collections import defaultdict
from typing import NewType

import fitz

LegalDocumentPath2PDF = NewType("LegalDocumentPath2PDF", str)


class Heuristics:
    """
    Implement a set of heuristics for cleaning text extracted from PDF documents.

    ...

    Attributes
    ----------
    pdf_path : str
        Path to PDF file.
    th_font : float
        Threshold (between 0 and 1) for filter outliers of font types.
    th_size : float
        Threshold (between 0 and 1) for filter outliers of font sizes.
    filter_font_by_cum : bool
        Filters outliers by the accumulated sum, for font types.
        If False, filter by indivual counting.
    filter_size_by_cum : bool
        Filters outliers by the accumulated sum, for font sizes.
        If False, filter by indivual counting.

    Methods
    -------
    set_let_horinzontal_text(True|False)
        Active heuristic to leave only the sentences aligned horizontally from left to right.
    set_filter_outlier_font_types(True|False)
        Active heuristic to filter outliers of font types.
    set_filter_outlier_font_sizes(True|False)
        Active heuristic to filter outliers of font sizes.
    set_filter_duplicated_phrases(True|False)
        Active heuristic to remove duplicated phrases.
    set_all_heuristics(True|False)
        Activates all available heuristics.
    Extract()
        Extracts text from the PDF file applying active heuristics.

    Notes
    -----
    - Font filtering occurs independently for size and type.
    """

    def __init__(
        self,
        pdf_path: LegalDocumentPath2PDF,
        th_font: float = 0.9,
        th_size: float = 0.9,
        filter_font_by_cum: bool = True,
        filter_size_by_cum: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        pdf_path : str
            Path to PDF file.
        th_font : float, optional
            Threshold (between 0 and 1) for filter outliers of font types.
            (default is 0.9)
        th_size : float, optional
            Threshold (between 0 and 1) for filter outliers of font sizes.
            (default is 0.9)
        filter_font_by_cum : bool, optional
            Filters outliers by the accumulated sum, for font types.
            If False, filter by indivual counting. (default is True)
        filter_size_by_cum : bool, optional
            Filters outliers by the accumulated sum, for font sizes.
            If False, filter by indivual counting. (default is True)
        """
        self._doc = fitz.open(pdf_path)
        self.th_font = th_font
        self.th_size = th_size
        self.filter_size_by_cum = filter_size_by_cum
        self.filter_font_by_cum = filter_font_by_cum
        for name in [
            "_let_horinzontal_text",
            "_filter_outlier_font_types",
            "_filter_outlier_font_sizes",
            "_filter_duplicated_phrases",
        ]:
            setattr(self, name, False)
        for name in [
            "_txt",
            "_size_count",
            "_font_count",
            "_phrase_count",
            "_phrase_size",
            "_phrase_font",
            "_size_count",
            "_allow_fonts",
            "_allow_sizes",
        ]:
            setattr(self, name, None)

    def set_let_horinzontal_text(self, _set: bool = True):
        """Set heuristic to let horintal text.
        Parameters
        ----------
        _set : bool, optional
            Active heuristic to leave only the sentences aligned horizontally from left to right. (default is True)
        """
        self._let_horinzontal_text = _set

    def set_filter_outlier_font_types(self, _set: bool = True):
        """Set heuristic to filter outliers of font types.
        Parameters
        ----------
        _set : bool, optional
            Active heuristic to filter outliers of font types. (default is True)
        """
        self._filter_outlier_font_types = _set

    def set_filter_outlier_font_sizes(self, _set: bool = True):
        """Set heuristic to filter outliers of font sizes.
        Parameters
        ----------
        _set : bool, optional
            Active heuristic to filter outliers of font sizes. (default is True)
        """
        self._filter_outlier_font_sizes = _set

    def set_filter_duplicated_phrases(self, _set: bool = True):
        """Set heuristic to remove duplicated phrases.
        Parameters
        ----------
        _set : bool, optional
            Active heuristic to remove duplicated phrases. (default is True)
        """
        self._filter_duplicated_phrases = _set

    def set_all_heuristics(self):
        """Actives all available heuristics.
        Parameters
        ----------
        _set : bool, optional
            Active all available heuristics. (default is True)
        """
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
        for page in self._doc:
            txt_dict = page.get_text("dict")
            for block in txt_dict["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    (cosine, sine) = line["dir"]
                    if self._let_horinzontal_text and ((cosine != 1) or (sine != 0)):
                        _ = ...  # https://github.com/nedbat/coveragepy/issues/198
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

        self._size_count = size_count
        self._font_count = font_count
        self._phrase_count = phrase_count
        self._phrase_size = phrase_size
        self._phrase_font = phrase_font

    @staticmethod
    def _filter(counts, th, filter_by_cum):
        total = sum(counts.values())
        allow = []
        cum = 0
        for name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            allow.append(name)
            if filter_by_cum:
                cum += count
                count = cum
            if (count / total) >= th:
                break
        return allow

    def _apply_size_heuristics(self):

        if self._filter_outlier_font_sizes:
            allow_sizes = self._filter(
                self._size_count, self.th_size, self.filter_size_by_cum
            )
        else:
            allow_sizes = list(self._size_count.keys())

        if self._filter_outlier_font_types:
            allow_fonts = self._filter(
                self._font_count, self.th_font, self.filter_font_by_cum
            )
        else:
            allow_fonts = list(self._font_count.keys())

        self._allow_sizes = allow_sizes
        self._allow_fonts = allow_fonts

    def _get_text(self):
        txt = []
        for phrase, count in self._phrase_count.items():
            if not (set(self._phrase_size[phrase]) & set(self._allow_sizes)):
                continue
            if not (set(self._phrase_font[phrase]) & set(self._allow_fonts)):
                continue
            if self._filter_duplicated_phrases or (count == 1):
                txt.append(phrase)
            else:
                txt.extend([phrase] * count)
        self._txt = "\n".join(txt)

    def _get_brute_text(self):
        return "\n".join([page.get_text("text") for page in self._doc])

    def Extract(self):
        """Extracts text from the PDF file applying active heuristics.

        Returns
        -------
        str
            a string with the text extracted from PDF file.
        """
        if any(
            [
                self._let_horinzontal_text,
                self._filter_duplicated_phrases,
                self._filter_outlier_font_sizes,
                self._filter_outlier_font_types,
            ]
        ):
            self._preprocess_doc()
            self._apply_size_heuristics()
            self._get_text()
            return self._txt
        return self._get_brute_text()


# EOF
