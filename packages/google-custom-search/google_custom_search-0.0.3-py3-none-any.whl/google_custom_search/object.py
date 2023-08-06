import json

class result(object):
  def __init__(self, api, **kwarg):
    self.api=api
    
  @property
  def titles(self):
    title=[]
    for e in self.api["items"]:
      i=e["title"]
      title.append(i)
    return title
    
  @property
  def urls(self):
    url=[]
    for e in self.api["items"]:
      i=e["link"]
      url.append(i)
    return url