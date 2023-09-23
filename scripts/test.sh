python -m pip install --upgrade pip
pip install pytest-cov, pytest, requests-mock, pytest-asyncio

if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

mkdir logs

pytest --cov-config=tests/.coveragerc --cov=src tests/ --cov-report term-missing