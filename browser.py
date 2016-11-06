import mechanize
import time

def get_browser():
  br = mechanize.Browser()
  br.set_cookiejar(mechanize.CookieJar())

  br.set_handle_equiv(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)

  br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
  return br

def open_request(br, request, data):
  resp = br.open(request, data=data)
  s = resp.read()
  resp.close()
  return s.decode('utf-8', 'replace').encode('ascii', 'replace')

def open_pagex(br, url):
  resp = br.open(url.encode('utf8'))
  s = resp.read()
  resp.close()
  return s.decode('utf-8', 'replace').encode('ascii', 'replace')

def open_page(br, url, tries=0, max_tries=3):
  if tries == max_tries:
    print 'cannot open page: ', url
    return ''

  try:
    return open_pagex(br, url)
  except:
    time.sleep(2)
    return open_page(br, url, tries + 1, max_tries)
