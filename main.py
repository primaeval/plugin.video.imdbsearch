import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.imdbsearch')
 
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcgui
import sys

import requests
import re
import urllib,urlparse
import HTMLParser

_url = sys.argv[0]
_handle = int(sys.argv[1])

_count = 100



def get_categories():
    return ['*','action','adventure','animation','biography','comedy','crime','documentary','drama',
    'family','fantasy','film_noir','game_show','history','horror','music','musical','mystery','news',
    'reality_tv','romance','sci_fi','sport','talk_show','thriller','war','western']

def get_url(category,start):
    imdb_query = [
    ("count", str(_count)),
    ("title", __settings__.getSetting( "title" )),
    ("title_type", __settings__.getSetting( "title_type" )),
    ("release_date", "%s,%s" % (__settings__.getSetting( "release_date_start" ),__settings__.getSetting( "release_date_end" ))),
    ("user_rating", "%.1f,%.1f" % (float(__settings__.getSetting( "user_rating_low" )),float(__settings__.getSetting( "user_rating_high" )))),
    ("num_votes", "%s,%s" % (__settings__.getSetting( "num_votes_low" ),__settings__.getSetting( "num_votes_high" ))),
    ("genres", "%s,%s" % (category,__settings__.getSetting( "genres" ))),   
    ("groups", "%s" % (__settings__.getSetting( "groups" ))),  
    ("companies", __settings__.getSetting( "companies" )),
    ("boxoffice_gross_us", "%s,%s" % (__settings__.getSetting( "boxoffice_gross_us_low" ),__settings__.getSetting( "boxoffice_gross_us_high" ))),
    ("certificates", __settings__.getSetting( "certificates" )),
    ("countries", __settings__.getSetting( "countries" )),
    ("languages", __settings__.getSetting( "languages" )),
    ("moviemeter", "%s,%s" % (__settings__.getSetting( "moviemeter_low" ),__settings__.getSetting( "moviemeter_high" ))),
    ("production_status", __settings__.getSetting( "production_status" )),
    ("runtime", "%s,%s" % (__settings__.getSetting( "runtime_low" ),__settings__.getSetting( "runtime_high" ))),
    ("sort", __settings__.getSetting( "sort" )),
    ("start", start),
    ]
    url = "http://www.imdb.com/search/title?"
    params = {}
    for (field, value) in imdb_query:
        if not "Any" in value and value != "" and value != "," and value != "*" and value != "*," and value != ",*": #NOTE title has * sometimes
            params[field] = value
    params = urllib.urlencode(params)
    url = "%s%s" % (url,params)
    return url

def get_videos(url):
    print url
    r = requests.get(url)

    html = r.text
    html = HTMLParser.HTMLParser().unescape(html)
    
    items = html.split('<tr class="')
    videos = []
    for item in items:
        
        if not re.search(r'^.*?detailed"',item):
            continue
        
        img_url = ''
        img_match = re.search(r'<img src="(.*?)"', item)
        if img_match:
            img = img_match.group(1)
            img_url = re.sub(r'S[XY].*_.jpg','SX214_.jpg',img)
    
        title = ''
        imdbID = ''
        year = ''
        title_match = re.search(r'<a href="/title/(.+?)/" title="(.+?) \((.+?)\)"', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            imdbID = title_match.group(1)
            title = title_match.group(2)
            year = title_match.group(3)

            
        episode = ''
        episode_match = re.search(r'<span class="episode">Episode: <a href="/title/(.+?)/">(.+?)</a>(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if episode_match:
            episode = "%s%s" % (episode_match.group(2), episode_match.group(3))
            
        rating = ''
        votes = ''
        rating_match = re.search(r'title="Users rated this (.+?)/10 \((.+?) votes\)', item, flags=(re.DOTALL | re.MULTILINE))
        if rating_match:
            rating = rating_match.group(1)
            votes = rating_match.group(2)
            votes = re.sub(',','',votes)
            
        plot = ''
        plot_match = re.search(r'<span class="outline">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if plot_match:
            plot = plot_match.group(1)
            
        cast = []
        cast_match = re.search(r'<span class="credit">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if cast_match:
            cast = cast_match.group(1)
            cast_list = re.findall(r'<a.+?>(.+?)</a>', cast)
            cast = cast_list
                
        genres = ''
        genre_match = re.search(r'<span class="genre">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if genre_match:
            genre = genre_match.group(1)
            genre_list = re.findall(r'<a.+?>(.+?)</a>', genre)
            genres = ",".join(genre_list)
                
        runtime = ''
        runtime_match = re.search(r'<span class="runtime">(.+?) mins\.</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if runtime_match:
            runtime = int(runtime_match.group(1)) * 60
                
        certificate = ''
        certificate_match = re.search(r'<span class="certificate"><span title="(.+?)"', item, flags=(re.DOTALL | re.MULTILINE))
        if certificate_match:
            certificate = certificate_match.group(1)
            
        if imdbID:
            if __settings__.getSetting( "title_type" ) == "tv_series":
                #FUTURE meta_url = "plugin://plugin.video.meta/tv/imdb/%s" % imdbID
                meta_url = "plugin://plugin.video.meta/tv/search_term/%s/1" % title
            else:
                meta_url = 'plugin://plugin.video.meta/movies/play/imdb/%s/default' % imdbID
            videos.append({'name':title,'episode':episode,'thumb':img_url,'genre':genres,
            'video':meta_url,
            'code': imdbID,'year':year,'mediatype':'movie','rating':rating,'plot':plot,
            'certificate':certificate,'cast':cast,'runtime':runtime,'votes':votes})
            
    next_url = ''
    pagination_match = re.search(r'<span class="pagination">.*<a href="(.+?)">Next', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        next_url = "http://www.imdb.com%s" % pagination_match.group(1)
            
    return (videos,next_url)
    

def list_categories():
    categories = get_categories()
    listing = []
    for category in categories:
        prefix = __settings__.getSetting( "prefix" )
        cat = re.sub('_',' ',category)
        if prefix:
            name = "%s %s" % (prefix, re.sub('_',' ',cat))
        else:
            name = cat
        list_item = xbmcgui.ListItem(label=name)
        imdb_url=urllib.quote_plus(get_url(category,''))
        list_item.setInfo('video', {'title': name, 'genre': category, 'plot': re.sub('&',' ',urllib.unquote(urllib.unquote(imdb_url)))})
        url = '{0}?action=listing&category={1}&imdb={2}'.format(_url, category,imdb_url)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(_handle)
    xbmc.executebuiltin("Container.SetViewMode(504)")


def list_videos(imdb_url):
    (videos,next_url) = get_videos(imdb_url)
    if __settings__.getSetting( "title_type" ) == "tv_series":
        IsPlayable = 'false'
        is_folder = True
    else:
        IsPlayable = 'true'
        is_folder = False
    listing = []
    for video in videos:
        if __settings__.getSetting( "title_type" ) == "tv_episode":
            vlabel = "%s - %s" % (video['name'], video['episode'])
        else:
            vlabel = video['name']
        list_item = xbmcgui.ListItem(label=vlabel)
        list_item.setInfo('video', {'title': vlabel, 'genre': video['genre'],'code': video['code'],
        'year':video['year'],'mediatype':'movie','rating':video['rating'],'plot': video['plot'],
        'mpaa': video['certificate'],'cast': video['cast'],'duration': video['runtime'], 'votes': video['votes']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb']})
        list_item.setProperty('IsPlayable', IsPlayable)
        url = '{0}?action=play&video={1}'.format(_url, video['video'])
        is_folder = is_folder
        list_item.addContextMenuItems( [('Extended Info...', "XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)" % video['code'])] ) 
        video_streaminfo = {'codec': 'h264'}
        video_streaminfo['aspect'] = round(1280.0 / 720.0, 2)
        video_streaminfo['width'] = 1280
        video_streaminfo['height'] = 720
        list_item.addStreamInfo('video', video_streaminfo)
        list_item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
        listing.append((video['video'], list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    listing = []
    if next_url:
        url = '{0}?action=listing&imdb={1}'.format(_url, urllib.quote_plus(next_url))
        list_item = xbmcgui.ListItem(label='[B]Next Page >>[/B]')
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb': 'DefaultNetwork.png', 'icon': 'DefaultNetwork.png'})
        is_folder = True
        listing.append((url, list_item, is_folder))
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_MPAA_RATING)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    xbmcplugin.endOfDirectory(_handle)
    if __settings__.getSetting( "title_type" ) == "tv_episode":
        xbmc.executebuiltin("Container.SetViewMode(50)")
    else:
        xbmc.executebuiltin("Container.SetViewMode(%s)" % __settings__.getSetting( "view" ))

def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            if 'imdb' in params.keys():
                imdb = params['imdb']
                list_videos(urllib.unquote_plus(imdb))
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])