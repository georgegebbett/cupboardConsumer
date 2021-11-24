# cupboardConsumer

This is really not anything very interesting - it is a tiny program which runs on a Pi Zero in my cupboard under the stairs and allows me to mark items in there as consumed on my Grocy instance. 

That's it, that's the program. 

To use this you will need a config file in YAML format - you will need to put the path to it in `main.py` - I have used the absolute path as this is required for the way I run this (as a service)

This has been set up specifically to run on a 3" touch screen but with tweaking will run on other size screens

The YAML file is structured as follows:

```
fullscreen: false (enable this to run in fullscreen)
apiBaseURL: YOUR_GROCY_API_BASE_URL (including the / after the word api)
apiKey: YOUR_GROCY_API_KEY
cupboardLocationId: ID_OF_STORAGE_LOCATION

excludedItems:
  - LIST
  - OF
  - IDs
  - OF
  - ITEMS
  - YOU
  - DON'T
  - WANT
  - DISPLAYED
```
