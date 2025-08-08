import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from app.Controller.save_excel import save_excel

class MockEvent:
    def __init__(self, path):
        self.path = path

def test_save_excel(monkeypatch):
    e = MockEvent("teste")
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    assert save_excel(e, df)