import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.gemini_service import GeminiService

@pytest.fixture
def gemini_service():
    with patch('google.generativeai.configure'):
        # Mocking the model initialization properly
        with patch('google.generativeai.GenerativeModel') as mock_model:
            service = GeminiService()
            service.api_key = "fake_key"
            service.model = mock_model.return_value
            return service

@pytest.mark.asyncio
async def test_generate_response_async(gemini_service):
    mock_response = AsyncMock()
    mock_response.text = "Hello from mock!"

    # Mock the generate_content_async method
    gemini_service.model.generate_content_async = AsyncMock(return_value=mock_response)

    response = await gemini_service.generate_response("say hello")

    # Verify it was called and the response is correct
    gemini_service.model.generate_content_async.assert_called_once_with("say hello")
    assert response == "Hello from mock!"
