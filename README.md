# How to start the API Server
```shell
conda create -n pytest python=3.9
conda activate pytest
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8081
```

# Test with coverage
```shell
pytest --cov=api --cov-report=term-missing .
```

or simply run the following command since all the configurations have been put into the file `pytest.ini` inside the folder `tests/`

```shell
pytest
```

or even simpler with the command `tox`. This not only provides same features as the above commands, but also allows you to test in multiple environments.