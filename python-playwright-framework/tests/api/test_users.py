"""
API Test Suite
Tests API endpoints directly without UI
"""

import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.api
@pytest.mark.smoke
class TestUsersAPI:
    """User API tests"""
    
    def test_get_list_of_users(self, playwright, api_base_url):
        """Test GET request - Retrieve users"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        # Send GET request
        response = request_context.get("/users")
        
        # Assert response status
        assert response.ok, "Response should be successful"
        assert response.status == 200, "Status code should be 200"
        
        # Parse response
        users = response.json()
        
        # Assert response data
        assert isinstance(users, list), "Response should be a list"
        assert len(users) == 10, "Should have 10 users"
        
        # Verify user object structure
        assert 'id' in users[0]
        assert 'name' in users[0]
        assert 'email' in users[0]
        assert 'username' in users[0]
        
        # Cleanup
        request_context.dispose()
    
    def test_get_single_user_by_id(self, playwright, api_base_url):
        """Test GET request - Retrieve single user"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        user_id = 1
        
        # Send GET request
        response = request_context.get(f"/users/{user_id}")
        
        # Assert response
        assert response.ok, "Response should be successful"
        assert response.status == 200, "Status code should be 200"
        
        user = response.json()
        
        # Assert user data
        assert user['id'] == user_id
        assert 'name' in user
        assert 'email' in user
        
        # Cleanup
        request_context.dispose()
    
    def test_create_new_user(self, playwright, api_base_url):
        """Test POST request - Create new user"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        # Request payload
        new_user = {
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com"
        }
        
        # Send POST request
        response = request_context.post("/users", data=new_user)
        
        # Assert response
        assert response.ok, "Response should be successful"
        assert response.status == 201, "Status code should be 201"
        
        created_user = response.json()
        
        # Assert created user
        assert 'id' in created_user
        assert created_user['name'] == new_user['name']
        assert created_user['email'] == new_user['email']
        
        # Cleanup
        request_context.dispose()
    
    def test_update_existing_user(self, playwright, api_base_url):
        """Test PUT request - Update user"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        user_id = 1
        updated_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        # Send PUT request
        response = request_context.put(f"/users/{user_id}", data=updated_data)
        
        # Assert response
        assert response.ok, "Response should be successful"
        assert response.status == 200, "Status code should be 200"
        
        updated_user = response.json()
        
        # Assert updated data
        assert updated_user['name'] == updated_data['name']
        assert updated_user['email'] == updated_data['email']
        
        # Cleanup
        request_context.dispose()
    
    def test_partial_update_user(self, playwright, api_base_url):
        """Test PATCH request - Partial update"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        user_id = 1
        partial_update = {
            "email": "newemail@example.com"
        }
        
        # Send PATCH request
        response = request_context.patch(f"/users/{user_id}", data=partial_update)
        
        # Assert response
        assert response.ok, "Response should be successful"
        assert response.status == 200, "Status code should be 200"
        
        updated_user = response.json()
        assert updated_user['email'] == partial_update['email']
        
        # Cleanup
        request_context.dispose()
    
    def test_delete_user(self, playwright, api_base_url):
        """Test DELETE request - Delete user"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        user_id = 1
        
        # Send DELETE request
        response = request_context.delete(f"/users/{user_id}")
        
        # Assert response
        assert response.ok, "Response should be successful"
        assert response.status == 200, "Status code should be 200"
        
        # Cleanup
        request_context.dispose()
    
    @pytest.mark.negative
    def test_invalid_endpoint_returns_404(self, playwright, api_base_url):
        """Test error handling - Invalid endpoint"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        # Send request to invalid endpoint
        response = request_context.get("/invalid-endpoint")
        
        # Assert error response
        assert response.status == 404, "Should return 404 for invalid endpoint"
        
        # Cleanup
        request_context.dispose()
    
    def test_response_headers(self, playwright, api_base_url):
        """Test response headers"""
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        response = request_context.get("/users")
        
        # Assert headers
        headers = response.headers
        assert 'application/json' in headers['content-type'], "Should return JSON"
        assert response.ok, "Response should be successful"
        
        # Cleanup
        request_context.dispose()
    
    @pytest.mark.performance
    def test_response_time(self, playwright, api_base_url):
        """Test response time"""
        import time
        
        # Create API request context
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        start_time = time.time()
        response = request_context.get("/users")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Assert response time (adjust threshold as needed)
        assert response_time < 2000, f"Response time should be less than 2 seconds, got {response_time}ms"
        
        # Cleanup
        request_context.dispose()


@pytest.mark.api
class TestPostsAPI:
    """Posts API tests"""
    
    def test_get_all_posts(self, playwright, api_base_url):
        """Test get all posts"""
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        response = request_context.get("/posts")
        
        assert response.ok, "Response should be successful"
        
        posts = response.json()
        assert isinstance(posts, list), "Should return list of posts"
        assert len(posts) > 0, "Should have posts"
        
        request_context.dispose()
    
    def test_create_new_post(self, playwright, api_base_url):
        """Test create new post"""
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        new_post = {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
        
        response = request_context.post("/posts", data=new_post)
        
        assert response.status == 201, "Should create post"
        
        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        
        request_context.dispose()
    
    def test_get_posts_by_user_id(self, playwright, api_base_url):
        """Test get posts by user ID"""
        request_context = playwright.request.new_context(base_url=api_base_url)
        
        user_id = 1
        
        response = request_context.get(f"/posts?userId={user_id}")
        
        assert response.ok, "Response should be successful"
        
        posts = response.json()
        assert isinstance(posts, list), "Should return list"
        
        # Verify all posts belong to the user
        for post in posts:
            assert post['userId'] == user_id, "All posts should belong to user"
        
        request_context.dispose()
