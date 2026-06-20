import pytest
from src.services.gemini_service import gemini
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_analyze_intent_async_agenda():
    # Mock the internal generate_response_async to simulate AI recognizing AGENDA
    with patch.object(gemini, 'generate_response_async', new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = "AGENDA\n"

        result = await gemini.analyze_intent_async("Ajoute un rendez-vous demain")
        assert result == "AGENDA"
        mock_gen.assert_called_once()

@pytest.mark.asyncio
async def test_generate_response_async():
    # If no API key is set, it should return the default error string
    if not gemini.api_key or gemini.api_key == "votre_cle_gemini_ici":
        result = await gemini.generate_response_async("Hello")
        assert "Désolé, l'API Gemini n'est pas configurée" in result
    else:
        # Mocking the actual network call to not rely on a real API key during tests
        with patch.object(gemini.model, 'generate_content_async', new_callable=AsyncMock) as mock_content:
            class MockResponse:
                text = "Ceci est une réponse asynchrone"
            mock_content.return_value = MockResponse()

            result = await gemini.generate_response_async("Test")
            assert result == "Ceci est une réponse asynchrone"
            mock_content.assert_called_once()
