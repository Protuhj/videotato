# Enter in site names that you will add full URL entries to in the full_url_site_data folder
# Example:
# In this file, add a line with an id of "netflix", then in the full_url_site_data folder, create a "netflix.items" file and add the full URLs to that file that you want to randomly choose from

# For HBO Max sites, use developer tools to view the request to 'generic-show-page-rail-episodes-tabbed-content' when switching seasons
#        Then copy/paste the raw result JSON into notepad++ for all seasons
#        Once you have all seasons pasted, search for /video/watch in all open files
#        Copy the results area, paste into a new file and remove the JSON text, and add https://play.max.com to the beginning of each URL

FULL_URL = [
    # You'll want to edit full_url_site_data/example.items (the file name matches the 'id' field + .items)
    # For additional sites, get the collection of URLs and add them to your own files to give different weights
    # or all one file with the same weighting
    { "id": "example", "weight": 3, "name": "Example file"},
]