# videotato - v0.5

Watch random videos from YouTube without alt-tabbing to your browser.

Perfect for gaming while playing random videos from YouTube channels or playlists.

----

### Languages/Software
- Windows
- Python >= 3
- AutoHotkey
- YouTube API V3

### Installation
- Python >= 3: https://www.python.org/downloads/
- AutoHotkey (latest version): https://autohotkey.com/download/

### Setup YouTube API Access

- Install the Python libraries for Google API access:
    - Run: `python -m pip install --upgrade google-api-python-client`

You'll then need to create a YouTube V3 API project, in order to get a client-side API key.

- Go [here](https://developers.google.com/youtube/registering_an_application) and follow the instructions for creating an API application.

- Once you've created a YouTube V3 API project, you'll need to create an OAuth client ID key to use with videotato.

    - Go to the [Credentials](https://console.developers.google.com/apis/credentials?project=_) page, and click 'Create Credentials'.
Choose 'Other' as the type, and fill out the information it asks for.

- When you're finished, go back to the [Credentials](https://console.developers.google.com/apis/credentials?project=_) page, and choose the API project you've created.

- Go down to the 'OAuth 2.0 client IDs' section, and there should be a 'Download JSON' button all the way to the right for the client you created.

- Download the JSON file, and navigate to where it downloaded to.

- Copy the JSON file to the videotato folder, and rename it 'client_secret.json'
    - (I may change this in the future to allow for passing this file's path as an argument to the main script.)

- Verify the client_secret.json file is valid by running, `python videotato.py`
    - It should open a browser to confirm you want to authorize the application, confirming will store the authentication information.

### Personalization: Channels

Open the channels.py file to view the channels that I've pre-filled it with.
Comment lines start with `#`.

Each channel should be on its own line, and it MUST be the channel ID (the ID will start with 'UC').  
Use the examples I've placed in the file to add/edit your own.  
Set the weighting to 0 to disable a channel.  
The name field is just for debug/display purposes.  

- To get the channel ID, go to the channel's page on YouTube in a browser.
- If their URL looks like: `https://www.youtube.com/channel/UC...`
Then just grab the full `UC...` text and paste it into the channels.py file in the appropriate place.
- If their URL looks like: `https://www.youtube.com/user/...`
Then do the following:

- Go to: `https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.channels.list?part=snippet&fields=items/id`
    - Put the username into the 'forUsername' field
    - Then hit 'Execute without OAuth'
    - If a channel is found, it will be the only entry in the Response at the bottom of the page for 'id'
    - Grab the `UC...` text and paste it into the channels.txt file.

**Alternatively:**  

-  View source on the channel's `About` page and search for "browse_id", the channel ID should be near it.


### Personalization: Playlists and Music

Open the playlists.py or music.py file to view the channels/music that I've pre-filled them with.
- Use the examples I've added to add/edit your own.  
- Set the age field to <= 0 to not update the playlist. 
  - "age" can be seconds or a 'time string' like "1w" or "7d"  
    - age units: "s" for seconds -- "m" for minutes -- "h" for hours --  "d" for days -- "w" for weeks  
- Set the weighting to 0 to disable an entry.  
- The name field is just for debug/display purposes.  


- This feature does not get deltas from the previous query. Each time the playlists are updated, the **full** playlist is retrieved.

### Personalization: Full URLs

Open the full_url_sites.py file to see an example site I've pre-filled it with.

The "id" field is an ID that will map to the file name that you'll fill with URLs to choose from.
In the example entry, I set the id to 'example', so in the 'full_url_site_data' folder, I created the file "example.items" and entered in an example URL.  
I also added some info on grabbing a show's URLs from HBO max, but actually grabbing all the URLs I left as an exercise to the user.


## AutoHotkey

### Chrome
- `videotato_chrome.ahk` contains the script needed to actually "Do the Magic" while you're gaming/messing around on a different application.
    - To run this AutoHotkey script, right click on it and either go to 'Run Script'
    - Or right-click on it and go to 'Compile Script' and then run the `videotato_chrome.exe`.

### Firefox
- `videotato_firefox.ahk` contains the script needed to actually "Do the Magic" while you're gaming/messing around on a different application.
    - To run this AutoHotkey script, right click on it and either go to 'Run Script'
    - Or right-click on it and go to 'Compile Script' and then run the `videotato_firefox.exe`.

#### Hot keys:
##### (view https://autohotkey.com/docs/KeyList.htm for a full list of possible hotkeys)

- `F7`: cycles left through tabs via the `ctrl+PgUp` hotkey that Chrome and Firefox handle.
- `Shift + F7`: cycles right through tabs via the `ctrl+PgDn` hotkey that Chrome and Firefox handle.
- `Ctrl + Alt + T`: Open a new tab
- `Ctrl + Alt + W`: Close the current tab
- `F12`: toggles the AutoHotkey script on or off, in case you don't want the script responding to key presses.
- `LAlt + LShift + Del`: removes the last random video from all local data files.
    - Use this when you don't ever want to play a video again.
    - It basically reads the contents of `result.txt` and searches the `*_data` folders for matches, and removes the `result.txt` contents from those files.
- `LAlt + LShift + LCtrl + F5`: refresh the currently active tab
- `LCtrl + Page Down`: Scroll down using Page Down
- `LCtrl + Page Up`: Scroll up using Page Up
- `LCtrl + LShift + Page Down`: Scroll down using the down arrow key
- `LCtrl + LShift + Page Up`: Scroll up using the up arrow key

##### With YouTube tab open:
- `Media_next`: Sends shift+n (capital N) to YouTube to hit the 'Next' button. This will tell YouTube to play the next video.
    - The `media_next` key requires you to have a keyboard with these media keys.
    - You might have an Fn key or dedicated media keys.
    - If not, you can change the key to another key you'd be comfortable using.

- `Media_Play_Pause`: Sends k to YouTube to hit the 'Next' button. This will tell YouTube to play/pause the current video.
    - The `Media_Play_Pause` key requires you to have a keyboard with these media keys.
    - You might have an Fn key or dedicated media keys.
    - If not, you can change the key to another key you'd be comfortable using.
- `LCtrl+left arrow`:
    - Goes back 10 seconds in the YouTube video.
    - Sends the 'J' key to the Chrome tab.
- `LCtrl+right arrow`:
    - Goes forward 10 seconds in the YouTube video.
    - Sends the 'L' key to the Chrome tab.

##### Will Overwrite URL in Currently-Focused Tab:
- `Launch_Mail`:
    - The `Launch_Mail` key requires you to have a keyboard with these media keys.
    - You might have an Fn key or dedicated media keys.
    - If not, you can change the key to another key you'd be comfortable using.
    - Calls `python randomLine.py` which dumps the result to `result.txt`
    - This is read by the script, and changes the URL of the active tab to match the contents of `result.txt`.
- `Browser_Home`:
    - Plays the previous randomized video in the current Chrome tab.
    - Doesn't change `result.txt` in case you want to go back to the video later.




