"""
API Helper utility
Provides methods for API testing and HTTP requests
"""

import time
from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, Playwright
from utils.logger import logger


class APIHelper:
    """API testing helper"""
    
    def __init__(self, playwright: Playwright, base_url: str):
        self.base_url = base_url
        self.context: Optional[APIRequestContext] = None
        self.playwright = playwright
    
    def init(self, extra_headers: Optional[Dict[str, str]] = None) -> None:
        """Initialize API context"""
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if extra_headers:
            default_headers.update(extra_headers)
        
        self.context = self.playwright.request.new_context(
            base_url=self.base_url,
            extra_http_headers=default_headers
        )
        
        logger.info(f"API context initialized with baseURL: {self.base_url}")
    
    def get(self, endpoint: str, **kwargs) -> Any:
        """GET request"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        start_time = time.time()
        logger.info(f"GET request to: {endpoint}")
        
        response = self.context.get(endpoint, **kwargs)
        duration = (time.time() - start_time) * 1000
        
        logger.api('GET', endpoint, response.status, duration)
        
        if not response.ok:
            logger.error(f"GET request failed: {endpoint}")
            logger.error(f"Status: {response.status}, Text: {response.status_text}")
        
        assert response.ok, f"GET request failed with status {response.status}"
        return response.json()
    
    def post(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Any:
        """POST request"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        start_time = time.time()
        logger.info(f"POST request to: {endpoint}")
        logger.debug(f"Payload: {data}")
        
        response = self.context.post(endpoint, data=data, **kwargs)
        duration = (time.time() - start_time) * 1000
        
        logger.api('POST', endpoint, response.status, duration)
        
        if not response.ok:
            logger.error(f"POST request failed: {endpoint}")
        
        assert response.ok, f"POST request failed with status {response.status}"
        return response.json()
    
    def put(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Any:
        """PUT request"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        start_time = time.time()
        logger.info(f"PUT request to: {endpoint}")
        
        response = self.context.put(endpoint, data=data, **kwargs)
        duration = (time.time() - start_time) * 1000
        
        logger.api('PUT', endpoint, response.status, duration)
        
        if not response.ok:
            logger.error(f"PUT request failed: {endpoint}")
        
        assert response.ok, f"PUT request failed with status {response.status}"
        return response.json()
    
    def patch(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Any:
        """PATCH request"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        start_time = time.time()
        logger.info(f"PATCH request to: {endpoint}")
        
        response = self.context.patch(endpoint, data=data, **kwargs)
        duration = (time.time() - start_time) * 1000
        
        logger.api('PATCH', endpoint, response.status, duration)
        
        if not response.ok:
            logger.error(f"PATCH request failed: {endpoint}")
        
        assert response.ok, f"PATCH request failed with status {response.status}"
        return response.json()
    
    def delete(self, endpoint: str, **kwargs) -> Any:
        """DELETE request"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        start_time = time.time()
        logger.info(f"DELETE request to: {endpoint}")
        
        response = self.context.delete(endpoint, **kwargs)
        duration = (time.time() - start_time) * 1000
        
        logger.api('DELETE', endpoint, response.status, duration)
        
        if not response.ok:
            logger.error(f"DELETE request failed: {endpoint}")
        
        assert response.ok, f"DELETE request failed with status {response.status}"
        return response.json()
    
    def get_raw(self, endpoint: str):
        """GET request without assertion"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        return self.context.get(endpoint)
    
    def post_raw(self, endpoint: str, data: Dict[str, Any]):
        """POST request without assertion"""
        if not self.context:
            raise Exception("API context not initialized. Call init() first.")
        
        return self.context.post(endpoint, data=data)
    
    def set_auth_token(self, token: str) -> None:
        """Set authorization header"""
        if self.context:
            self.context.dispose()
        
        self.init({'Authorization': f'Bearer {token}'})
        logger.info('Authorization token set')
    
    def dispose(self) -> None:
        """Dispose API context"""
        if self.context:
            self.context.dispose()
            logger.info('API context disposed')
    
    def wait_for_api(self, endpoint: str = "/health", max_retries: int = 10, delay: int = 1000) -> bool:
        """Wait for API to be ready"""
        for i in range(max_retries):
            try:
                response = self.get_raw(endpoint)
                if response.ok:
                    logger.success(f"API is ready after {i + 1} attempt(s)")
                    return True
            except Exception as e:
                logger.warning(f"API not ready, attempt {i + 1}/{max_retries}: {str(e)}")
            
            time.sleep(delay / 1000)
        
        logger.error('API failed to become ready')
        return False
