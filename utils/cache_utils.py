import json
import os
from constants import CACHE_FILE
from streamlit_javascript import st_javascript

# load user specific cache
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

# save the user cache in cache file
def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

# get the browser id for storing and fetching user cache data
def get_browser_id():
    return st_javascript(
        """(function() {
            let id = localStorage.getItem("browser_id");
            if (!id) {
                id = self.crypto.randomUUID();
                localStorage.setItem("browser_id", id);
            }
            return id;
        })();"""
    )