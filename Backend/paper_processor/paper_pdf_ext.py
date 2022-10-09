import os
import fitz


class PaperPdfExtract:
    def __init__(self, file_path):
        self.ref_word = ['References', 'REFERENCES', 'referenCes']
        self.file_path = file_path
        self.ref_pages = self._get_ref_pages()
        if self.ref_pages is None:
            print('no reference')
            return None

        self.ref_text = self._get_ref_text()
        self.split_ref_text = self._get_split_ref_text()
        self.clean_split_ref_text = self._clean_str()

        # ToDo: think how to retrieve

    def _get_ref_pages(self):
        pdf = fitz.open(self.file_path)
        page_num = len(pdf)
        ref_pages = []

        for num, p in enumerate(pdf):
            for pc in p.get_text('blocks'):
                txt = pc[4]

                for ref_word in self.ref_word:
                    if ref_word in txt:
                        ref_page_num = [i for i in range(num, page_num)]

                        for rpn in ref_page_num:
                            ref_pages.extend([b[4] for b in pdf[rpn].get_text('blocks')])

                        return ref_pages

        return None

    def _get_ref_text(self):
        for i, t in enumerate(self.ref_pages):
            for word in self.ref_word:
                if word in t:
                    return self.ref_pages[i + 1:]

        return None  # cannot be reached

    def _get_split_ref_text(self):
        split_ref_text = []

        for i, t in enumerate(self.ref_text):
            if not self._is_std_head(t):
                continue

            s = t
            j = i + 1

            while j < len(self.ref_text) and not self._is_std_head(self.ref_text[j]) and not self._is_page_number(
                    self.ref_text[j]):
                s += self.ref_text[j]
                j += 1

            split_ref_text.append(s)

        return split_ref_text

    def _is_std_head(self, text):
        if len(text) > 0 and text[0] == '[' and ']' in text:
            for i in range(text.find('[') + 1, text.find(']')):
                if not text[i].isdigit():
                    return False

            return True

        return False

    def _is_page_number(self, text):
        for i in range(0, len(text) - 1):
            if not text[i].isdigit():
                return False

        return True

    def _clean_str(self):
        return [s.replace('ﬁ', 'fi').replace('\n', ' ').rstrip() for s in self.split_ref_text]


if __name__ == '__main__':
    test_path = '../../tests/testfiles/'
    ignore_file = {'.DS_Store', 'cvpr_2021_01.pdf', 'GLAC.pdf'}  # ToDo: adjust, eg. appendix

    for name in os.listdir(test_path):
        if name in ignore_file:
            continue

        p = PaperPdfExtract(test_path + name)
