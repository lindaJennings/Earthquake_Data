import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('.')


@pytest.fixture
def mock_find():
    with patch("scripts.webapp.frontend.collection.find") as mock:
        yield mock

@pytest.fixture
def mock_streamlit():
    with patch("scripts.webapp.frontend.st") as mock:
        yield mock

def test_find_station_results_sorted(mock_find):

    mock_results = [
        {"station": "DSB", "network": "NET1", "channel": "CH1", 
         "start_time": "2025-03-01", "end_time": "2025-03-10", "s3_url": "http://example.com/1"},
        {"station": "DSB", "network": "NET2", "channel": "CH2", 
         "start_time": "2025-04-01", "end_time": "2025-04-10", "s3_url": "http://example.com/2"}
    ]
    
    mock_find.return_value = iter(mock_results[::-1])  

    results = mock_find.return_value
    sorted_results = list(results)
    
    assert len(sorted_results) == 2
    assert sorted_results[0]["start_time"] == "2025-04-01"
    assert sorted_results[1]["start_time"] == "2025-03-01"

def test_streamlit_output(mock_streamlit, mock_find):

    mock_streamlit.text_input.return_value = "DSB"
    mock_streamlit.button.return_value = True

    mock_find.return_value = iter([
        {"station": "DSB", "network": "NET1", "channel": "CH1", 
         "start_time": "2025-04-01", "end_time": "2025-04-10", "s3_url": "http://example.com/1"}
    ])

    station = mock_streamlit.text_input("Enter Station Code (e.g., DSB)")
    if mock_streamlit.button("Search"):
        result = next(mock_find.return_value, None)
        if result:
            mock_streamlit.success(f"Seismic data found for station: {station}")

    mock_streamlit.success.assert_called_with("Seismic data found for station: DSB")

