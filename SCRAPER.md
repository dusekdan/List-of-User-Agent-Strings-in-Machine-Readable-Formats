# Using `scraper.py`

You can run the `scraper.py` script to generate files for yourself. It is by no means complete at this moment - it's work in progress that I develop only when I want to relax.

```sh

# Example run

python scraper.py --no-cache -l Python -o superfile
|
|- Will download latest list from the useragentstrings.com
|- Generates `superfile.py` file (uses normal, non-prettified string by default)
|- Inside this file, python copy-paste-ready variable with all the user agents strings will be located.

# -l/--languages switch accepts single or multiple languages separated by a comma (,)
# If not provided - all available generators are used

python scraper.py -l Python,C
pyhon scraper.py -l Python



```