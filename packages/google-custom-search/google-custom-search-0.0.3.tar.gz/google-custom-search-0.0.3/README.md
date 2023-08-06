# How to use this package.

## first please install this package
```bash
pip install google-custom-search
```

## sample code
```py
import google_custom_search

google=google_custom_search.custom_search(token="your api_key", engine_id="your engine_id")

result=google.search("Hello")

# get a list of title.
for title in result.titles:
  print(title)
  
# get a list of url.
for url in result.urls:
  print(url)
```

## sample code async version
```py
import asyncio
import google_custom_search

google=google_custom_search.custom_search(token="your api_key", engine_id="your engine_id")

async def main():
  result=await google.search_async("眠い")
  for i in result.titles:
    print(i)
  for i in result.urls:
    print(i)
    
loop = asyncio.get_event_loop() 
loop.run_until_complete(main())
```