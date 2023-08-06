# How to use this package.

## first please install this package
```bash
pip install google-custom-search
```

## sample code
```py
import google_custom_search

google=google_custom_search.custom_search(token="your api_key, engine_id=your engine_id)

result=google.search("Hello")

# get a list of title.
for title in result.titles:
  print(title)
  
# get a list of url.
for url in result.urls:
  print(url)
```