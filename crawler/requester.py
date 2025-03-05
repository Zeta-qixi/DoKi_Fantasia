
import requests
import logging

class Requester:
    """处理HTTP请求"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
    
    def get(self, url, headers=None):
        """发送GET请求"""
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def post(self, url, data=None, headers=None):
        """发送POST请求"""
        try:
            response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

requester = Requester()