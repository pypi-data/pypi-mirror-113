import allure
import requests
from dataclasses import dataclass

from jsvn_qa_utils_rest.src.data import Data
from jsvn_qa_utils_rest.src.validate import Validate
from loguru import logger
import time
from requests import Response
from typing import Dict, Any


@dataclass
class RestClient:

    base_url: str

    validate = Validate()
    data = Data()

    def get(self, url: str, headers: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Response:
        start_time: float = time.time()
        r: Response = requests.get(url=url, headers=headers, params=params)
        time_now: float = time.time()
        request_time: float = time_now - start_time
        self.request_info('GET', url, r.status_code, time.ctime(time_now), request_time)
        return r

    def post(self, url: str, headers: Dict[str, Any] = None, json: Dict[str, Any] = None,
             data: Dict[str, Any] = None) -> Response:
        start: float = time.time()
        r: Response = requests.post(url=url, headers=headers, json=json, data=data)
        time_now: float = time.time()
        request_time: float = time_now - start
        self.request_info(method='POST', url=url, status_code=r.status_code,
                          time_now=time.ctime(time_now), request_time=request_time)
        return r

    def options(self, url: str, headers: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Response:
        start_time: float = time.time()
        r: Response = requests.options(url=url, headers=headers, data=data)
        time_now: float = time.time()
        request_time: float = time_now - start_time
        self.request_info(method='OPTIONS', url=url, status_code=r.status_code,
                          time_now=time.ctime(time_now), request_time=request_time)
        return r

    def delete(self, url: str, headers: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Response:
        start_time: float = time.time()
        r: Response = requests.delete(url=url, headers=headers, params=params)
        time_now: float = time.time()
        request_time: float = time_now - start_time
        self.request_info(method='DELETE', url=url, status_code=r.status_code,
                          time_now=time.ctime(time_now), request_time=request_time)
        return r

    @allure.step('Информация о запросе')
    def request_info(self, method: str, url: str, status_code: int, time_now: str, request_time=None) -> None:
        logger.info(f'{method} {url} {status_code} {time_now}, {request_time}')

