import allure
from cerberus import Validator
from loguru import logger


class Validate:

    @allure.step('Проверка json-ответа на соответствие схеме')
    def validate_schema(self, test_json: dict, expected_json: dict):
        """
        Валидация json-ответа на соответствие схеме
        """
        v = Validator()
        if test_json != {}:
            if v.validate(test_json, expected_json):
                assert True
                logger.info('No errors in json')
            else:
                self.print_validate_error(v.errors)
                self.print_json_with_error(test_json)
                assert False
        else:
            assert False

    @allure.step('Ошибки валидации')
    def print_validate_error(self, errors: str):
        """
        Выводит поля с ошибками валидации json-ответа (отображается в аллюре)
        """
        logger.info(f'\nErrors: \n {errors}')

    @allure.step('JSON с ошибкой')
    def print_json_with_error(self, json_with_error: dict):
        """
        Выводит json с ошибкой (отображается в аллюре)
        :param json_with_error: dict
        :return:
        """
        logger.info(f'json с ошибкой: {json_with_error}')

    @allure.step('Проверка на соответствие')
    def assert_equal(self, expected_result, test_result):
        assert expected_result == test_result

    @allure.step('Проверка на НЕ соответствие')
    def assert_unequal(self, unexpected_result, test_result):
        assert unexpected_result != test_result
