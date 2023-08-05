# Hijri Date Fetcher
[![made-with-python](https://img.shields.io/badge/Backend-Python-1F425F.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-Green.svg)](https://opensource.org/licenses/MIT)

A Python package to fetch current hijri date in Arabic

![hijri_date_fetcher_img](assets/hijri_date_fetcher_img.png)

### Dependencies
You may download the following dependencies in order for the script to work.

- For your terminal, you have to have both `wget` and `libxml2-utils`.
- For python3, you have to install the following packages, `arabic_reshaper` and `python-bidi`.

### Manual Aliasing 
You may alias the script to use permenantly in your terminal by append it to your `.bashrc` or `.zshrc` profile (Depends on what you use).

Add the following to the profile:

```
# alias [name_of_alias_command]='python3 "/[script_PATH]"'
# Example
alias hijri='python3 "/Users/user/scripts/hijri_date_fetcher.py"'
```
