from random import randint, choice
from typing import List


class Data:
    # ---------------------- 1 lang ---------------------------------------------------------------------------------- #
    def symbol_feedback_message(self, ascii_symbols: bool = False) -> str:
        """
        генерация текста из символов
        :param ascii_symbols: использовать ASCII или нет, по умолчанию не используются
        :return: str
        """
        message_list: List[str] = []
        if not ascii_symbols:
            for _ in range(randint(10, 100)):
                symbol = self.random_symbol()
                message_list.append(symbol)
        else:
            for _ in range(randint(10, 100)):
                symbol = self.random_ascii_symbol()
                message_list.append(symbol)
        message_body: str = ''.join(message_list)
        return message_body

    @staticmethod
    def china_word(length: int) -> str:
        """
        текст из китайских иероглифов
        :param length: длина текста
        :return: str
        """
        letters: str = '是印版常的元均的分配世纪起就被作为此领式各样的版本'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}'
        return word

    @staticmethod
    def ru_word(length: int) -> str:
        """
        текст на кириллице
        :param length: длина текста
        :return: str
        """
        letters: str = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}'
        return word

    @staticmethod
    def en_word(length: int) -> str:
        """
        текст на латинице
        :param length: длина текста
        :return: str
        """
        letters: str = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}'
        return word

    # --------------------------  one symbol ------------------------------------------------------------------------- #
    @staticmethod
    def random_ascii_symbol() -> str:
        """
        получение рандомного символа ASCII
        :return: str
        """
        symbols: List[str] = ['↔', '▲', '▼', '☻', '♣', '◘']
        symbol: str = choice(symbols)
        return symbol

    @staticmethod
    def random_symbol() -> str:
        """
        Получение рандомного символа
        :return: str
        """
        symbols: str = '~!@#$%^&*()`_+|=;:/?.>,<'
        list(symbols)
        return choice(symbols)

    # ------------------------- 2 lang --------------------------------------------------------------------------------#
    def symbol_in_ru_word(self, length: int) -> str:
        """
        вставляет в конец текста на кириллице рандомный символ
        :param length: длина текста
        :return: str
        """
        letters: str = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}{self.random_symbol()}'
        return word

    def ascii_symbol_in_ru_word(self, length: int) -> str:
        """
        вставляет в конце текста на кириллице ASCII-символ
        :param length: длина текста
        :return: str
        """
        letters: str = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}{self.random_ascii_symbol()}'
        return word

    @staticmethod
    def random_number_in_ru_word(length: int) -> str:
        """
        вставляет рандомную цифру в конец текста на кириллице
        :param length: длина текста
        :return: str
        """
        letters: str = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}{randint(1, 99)}'
        return word

    def random_symbol_in_en_word(self, length: int) -> str:
        """
        вставляет в конец текста на латинице рандомный символ
        :param length:  длина текста
        :return: str
        """
        letters: str = 'qwertyuiopasdfghjklzxcvbnmMNBVCXZASDFGHJKLPOIUYTREWQ'
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}{self.random_symbol()}'
        return word

    @staticmethod
    def en_in_ru_word(length: int) -> str:
        """
        вставляет в текст на кириллице одинаковую по написанию латинскую букву
        :param length: длина текста
        :return: str
        """
        letters: str = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
        en_letters = 'yYHpPeEaAKcCBM'
        list(en_letters)
        list(letters)
        letters_list: List[str] = []
        for _ in range(length):
            letter: str = choice(letters)
            letters_list.append(letter)
        last_letter: str = ''.join(letters_list)
        word: str = f'{last_letter}{choice(en_letters)}'
        return word
