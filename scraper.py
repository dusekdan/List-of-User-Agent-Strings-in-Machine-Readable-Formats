import importlib
import os
import time
import sys
import optparse

import requests
from bs4 import BeautifulSoup 


"""
Let's think about the API this scraper should provide (command-line only for now)

(1) Aggressive caching by default (once you hit the target and retrieve data, do not re-request on subsequent calls)
    - Achieve this by caching the response locally, in `.cache` folder, excluded from version control
    - Provide parameter `--no-cache` that will create new caching record
    - Cache for 1 hour only 
    - Estimated time to implement: 30 minutes
    - Actual effort: 42 minutes.

(2) Figure out what information can be extracted from the user-agent-all page (e.g. categories) and allow working with that.
    - Should be only included in the future version, for now it is of no consequence.

(3) Specify language & format (copy-paste, pretty) that should be generated in the output
    - Link this to language support generators - so I, or other people, can easily create generator for new language
    - Estimated time to implement: 60-90 minutes
    - Language actual effort: 25 minutes.

(4) Number of results / and type of results generated feature 
    - e.g. "top 100" (based on the order they appear, there are no stats on the page)
    - "randomly picked"
    - "common browsers only" (default to hardcoded opera, mozzila, google chrome)
    - Estimated time to implement: 60 minutes

(5) Output file (-o/--output)
    - Should have some sensible defaults (problem here: how to select between "normal" and "pretty" -> cant make both, doesnt make sense to allow user to specify output file if it is not going to be respected.)
    - Estimated time to implement: 15-20 minutes

How different language generators should be implemented: 

(1) module `generators` -> different languages in different files, use `from generators import language`

(2) dynamic loading and maybe even validation of whether the generator is written correctly

(3) Put acquiring source into `core.datasource` or something like that so others can use it in their scripts

"""

AGENT_SOURCE = "http://useragentstring.com/pages/useragentstring.php?name=All"
CACHE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
GENERATOR_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generators")

GENERATORS = {}

def main():
    LANGUAGES = []

    load_generators()


    if OPTS.languages != None:
        LANGUAGES = OPTS.languages.split(',')
    
    # If language is not specified, use all available languages
    if not LANGUAGES:
        LANGUAGES = list(GENERATORS.keys())

    # If `--no-cache` is specified, retrieve latest version, otherwise
    # use what is locally available (given there is something locally
    # available and it is not older than `validity`).
    last_cache = get_latest_cached_data(validity=3600)
    if OPTS.no_cache or last_cache == "":
        raw_data = get_useragents_source(AGENT_SOURCE)
        cache_source(raw_data)
    else:
        raw_data = last_cache

    soup = BeautifulSoup(raw_data, 'html.parser')
    li_elems = soup.findAll("li")

    # Extra User Agent string from <li>s
    user_agent_strings = []
    for li in li_elems:
        user_agent_strings.append(li.text)
    
    # Run generators for languages that are available/requested and vice versa.
    for language in LANGUAGES:
        if language in GENERATORS.keys():
            GENERATORS[language].set_user_agents(user_agent_strings)

            normal_string = GENERATORS[language].generate_user_agent_list_string()
            pretty_string = GENERATORS[language].generate_user_agent_list_string_pretty()

            # FUTURE: Allow selecting `normal|pretty` when providing `--output|-o` parameter. 
            if OPTS.output != None:
                filename = OPTS.output + "." + GENERATORS[language].get_extension()
                dump_to_file(filename, normal_string)
            else:
                # `-o|--output` parameter was not provided - generate both
                print("D: Should be writing to standardized files.")
                filename = language + "_normal" + "." + GENERATORS[language].get_extension()
                filename_pretty = language + "_pretty" + "." + GENERATORS[language].get_extension()
                dump_to_file(filename, normal_string)
                dump_to_file(filename_pretty, pretty_string)

        else:
            print(f"W: Generator for {language} was not found and file will not be generated.")

def dump_to_file(filename, string):
    """Just dumps content to a file."""
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), "w", encoding="utf-8") as f:
            f.write(string)
    except Exception as e:
        print(f"Couldn't write to {filename}") 

def load_generators():
    not_generator = ["__init__.py", ".", "..", "__pycache__"]
    modules  = [m.split('.py')[0] for m in os.listdir(os.path.join(GENERATOR_FOLDER)) if m not in not_generator]

    for module in modules:
        try:
            imported_module = importlib.import_module(f"generators.{module}")
            instantiable = getattr(imported_module, module)
            GENERATORS[module] = instantiable()
            print(f"D: Generator for {module} added to generators. Total: {len(GENERATORS)}")
        except AttributeError as e:
            print(f"E: Unable to load generator for {module} from generators.{module} directory.")

# Acquire raw source of the user agent page only once
def get_useragents_source(sourceUrl):    
    
    headers = {
        # Let's be stealthy too. 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
    }

    try:
        r = requests.get(AGENT_SOURCE, headers=headers)

        if (r.status_code != 200):
            print("Server did not return 200, we should retry...") 
            return "" # TODO: Handle retry, break for now
        
        return r.text
    
    except: # TODO: Actually handle correct exceptions here
        
        print("Something went wrong, apparently.")


def setup_cache():
    if not os.path.exists(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)
        print("I: Cache folder did not exist. Creation was attempted.")
        return 
    print("D: Cache folder already exists.") # TODO: Convert these into log outputs

def get_latest_cached_data(validity=None):
    """
    Returns latest cached data, or empty string if cache is invalid.
    
    Validity of cache is specified by `validity` parameter, that is
    a maximum allowed age (in seconds) of cache. 
    """
    setup_cache()
    files = list(os.listdir(CACHE_FOLDER)) ; files.sort()

    if validity != None:
        last_file_created_at = int((files[-1].split('.'))[0])
        current_time = int(time.time())
        if (current_time - last_file_created_at > validity):
            print("I: Last cached file was older than least allowed cache validity. Returning empty cache to issue re-request.")
            return ""

    try:
        with open(os.path.join(CACHE_FOLDER, files[-1]), 'r', encoding="utf-8") as file:
            data = file.read().replace('\n', '')
        return data
    except Exception as e: # TODO: Handle proper exceptions
        print(e)
        return ""

# TODO: Exception handling
def cache_source(source):
    setup_cache()
    with open(os.path.join(CACHE_FOLDER, _get_cache_item_name()), 'w', encoding="utf-8") as f:
        f.write(source)

def _get_cache_item_name():
    """Returns `seconds_since_epoch.html` based on current client time."""
    return f"{int(time.time())}.html"

if __name__ == '__main__':
    
    parser = optparse.OptionParser()

    parser.add_option('-o', '--output', action="store", type="string", dest="output")
    parser.add_option('-x', '--no-cache', action="store_true", dest="no_cache", default=False)
    parser.add_option('-l', '--languages', action="store", type="string", dest="languages")


    (OPTS, ARGS) = parser.parse_args()
    main()