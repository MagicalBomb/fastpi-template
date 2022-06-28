# How to use this template


## Clone repository

```bash
git clone https://gitlab.com/byterum/nftgo/data-api-system/fastapi-template.git && \
cd <path-to-the-project>
```

## Install poetry
This project uses `poetry` for production and development environements management.

Refer to https://python-poetry.org/docs/master/ to install

## Configure poetry
```
poetry config virtualenvs.in-project true
poetry config virtualenvs.create true
```

### modify pyproject.toml
-  modify fields under tool.poetry to match your requirements


## Add dependency for developement
```
poetry add -D <package-name>
```

## Add dependency for production
```
poetry add <package-name>
```


## Install dependencies by poetry
Ensure poetry can find python3.9 in your PATH
```
poetry install
```

## [Optional] Install pre-commit
pre-commit would force you commit by `cz c` instead of `git commit`
```
# install
pre-commit install --hook-type commit-msg

# uinstall
pre-commit uninstall --hook-type commit-msg
```