import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.gemini_service import GeminiService

@pytest.fixture
def gemini_service():
    with patch('src.services.gemini_service.genai.GenerativeModel') as MockModel:
        with patch('os.getenv', return_value='fake_api_key'):
            service = GeminiService()
            service.model = MockModel()
            return service

@pytest.mark.asyncio
async def test_generate_response_async(gemini_service):
    mock_response = MagicMock()
    mock_response.text = "Mocked Response"
    gemini_service.model.generate_content_async = AsyncMock(return_value=mock_response)

    response = await gemini_service.generate_response_async("Hello")
    assert response == "Mocked Response"
    gemini_service.model.generate_content_async.assert_called_once_with("Hello")

@pytest.mark.asyncio
async def test_analyze_intent_async(gemini_service):
    mock_response = MagicMock()
    mock_response.text = " AGENDA "
    gemini_service.model.generate_content_async = AsyncMock(return_value=mock_response)

    intent = await gemini_service.analyze_intent_async("Je veux voir mon agenda")
    assert intent == "AGENDA"

@pytest.mark.asyncio
async def test_generate_cover_letter_async(gemini_service):
    mock_response = MagicMock()
    mock_response.text = "Cher recruteur..."
    gemini_service.model.generate_content_async = AsyncMock(return_value=mock_response)

    letter = await gemini_service.generate_cover_letter_async("Job Description", "CV Summary")
    assert letter == "Cher recruteur..."
