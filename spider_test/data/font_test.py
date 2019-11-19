import re
import base64
from lxml import etree
from fontTools.ttLib import TTFont
font_base = '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'
font_b = base64.b64decode(font_base)
with open('./test.ttf', 'wb') as f:
    f.write(font_b)

font = TTFont('./test.ttf')
# font.saveXML('test.xml')
bestcmap = font['cmap'].getBestCmap()
newmap = dict()
for key in bestcmap.keys():
    value = bestcmap[key]
    key = hex(key)
    newmap[key] = value
print(newmap)
res = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- CSRF Token -->
    <meta name="csrf-token" content="3aBW4IYv4gF3i04NQzleftPDp5vR7QfSXyDPGpNr">
        <title>GlidedSky</title>
        <!-- Scripts -->
    <script src="http://glidedsky.com/js/app.js"></script>

    <!-- Fonts -->
    <link rel="dns-prefetch" href="//fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css">

    <!-- Styles -->
    <link href="http://glidedsky.com/css/app.css" rel="stylesheet">
        <style>
        @font-face {
            font-family: "glided_sky";
            src: url(data:font;charset=utf-8;base64,AAEAAAAKAIAAAwAgT1MvMkEnQdAAAAEoAAAAYGNtYXAAVADCAAABpAAAAEhnbHlmdUQ+YgAAAgQAAAPWaGVhZBahrpQAAACsAAAANmhoZWEHCgOTAAAA5AAAACRobXR4BwEBNgAAAYgAAAAabG9jYQTKBcIAAAHsAAAAGG1heHAAEQA4AAABCAAAACBuYW1lQTDOUQAABdwAAAGVcG9zdACGAHIAAAd0AAAAOAABAAAAAQAAYZx77F8PPPUAAwPoAAAAANn5NV4AAAAA2fk1XgAU/4gDhANwAAAAAwACAAAAAAAAAAEAAANw/4gAAAPoABQAIAOEAAEAAAAAAAAAAAAAAAAAAAACAAEAAAALADYABQAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAwJTAZAABQAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAPz8/PwAAADAAOQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAD6ABkAisAMQBYACgAHQAUABwAOAAxAC0ALAAAAAAAAgAAAAMAAAAUAAMAAQAAABQABAA0AAAABAAEAAEAAAA5//8AAAAw//8AAAABAAQAAAAEAAgABgAFAAMACQABAAIABwAKAAAALABTAGkAjwDGAOgBGAFNAWQBswHrAAUAZP+IA4QDcAADAAYACQAMAA8AABMhESEBIQEBEQkDJwEBZAMg/OACzv2EAT4BXv7CAR7+wv7CIAE+/sIDcPwYA7b+Z/4+AzL+Z/4+AZn+ZykBmQGZAAACADH/8wH6AusADwAXAAA3JjU0NzYzMhcWFRQHBiMiExAjIhEQMzJvPj47bGs7Pj47a2v2i4yMi1Jku7tiXV5iurtkXwF+ATD+0P7LAAABAFgAAAHqAt0ACwAANzMRIzU2NzMRMxUhWKOCWz1Gk/5uTAIjOhEj/W9MAAEAKAAAAfkC6wAWAAA3ADU0JyYjIgcnNjMyFxYVFAE2MzMVISwBUCEkQlFHNWR0Yjo5/uFZH8v+MzYBJrNCJilVNGw7O2O6/vAHTwABAB3/8wHzAusAJQAANzcWMzI3NjU0IzUyNTQnJicGByc2MzIXFhUUBxUWFxYVFAcGIyIdLlBmQikq5MshIjlSRjFfbl86PINEKy1FQWWPVzxUJSU+k0aMNSAfAgNGOlgwMlaAMQQQLzNIYDo3AAIAFAAAAgsC3QAHABIAAAE1NDcjBgcHBSMVIzUhNQEzETMBUwYEGCOnAZhhV/7BATFlYQET4RNyMDz6ScrKPAHX/jYAAQAc//MB9QLdAB4AADc3FjMyNzY1NCcmIyIHJxMhFSEHNjMyFxYVFAcGIyIcLVFjQiwuKSlGOUExFwFl/usSNDlhO0FJRWKIVDxRLjFOTi0sKx4BV07UHTg+c3RGQgAAAgA4//MB/wLrAAkAIgAAJTY1NCMiBxYzMhMmIyIDNjMyFxYVFAcGIyInJjU0NzYzMhcBhSSEVEIRjTVeLki4BUleXzU3PjxYbkFGUkh1ZUZoL0qiXusCLTj+z1k6PHBoREJbYLDKaFtLAAEAMQAAAfwC3QAKAAAzEhMhNSEVBgcGB8YRvf6dAct6LiYJAYYBCU43nZ2D6QADAC3/8wH9AugAGQAnADUAADcmNTQ3NSY1NDc2MzIXFhUUBxUWFRQHBiMiEzQnJiMiBwYVFBcWFzYDNjU0JyYnBhUUFxYzMm9Ch2M5OVdcNzZifD9BZmXjISM5MyAhMiNQTBYnOiRkZCwrQj8qN1WBSQVEZVM0MzY1VmVMBUh4UTY3Ai84JSYhITU7KRwgQ/6JIjdCLBsoQGY6JyYAAAIALP/zAfQC6wALACQAAAEmIyIHBhUUFxYzMgcWMzITBiMiJyY1NDc2MzIXFhUUBwYjIicBng+RNSMkISJAVO0ySa8JSWBeNTc+PFhuQkZRR3JoSAG85y0vSkwrLOM4ATJbOzxwaERCV12p0WxeSwAAAAAADACWAAEAAAAAAAAAFAAAAAEAAAAAAAEACQAUAAEAAAAAAAIABwAdAAEAAAAAAAUACwAkAAEAAAAAAAYAEQAvAAEAAAAAAAsAFQBAAAMAAQQJAAAAKABVAAMAAQQJAAEAEgB9AAMAAQQJAAIADgCPAAMAAQQJAAUAFgCdAAMAAQQJAAYAIgCzAAMAAQQJAAsAKgDVQ3JlYXRlZCBieSBHbGlkZWRTa3lHbGlkZWRTa3lSZWd1bGFyVmVyc2lvbiAxLjBHbGlkZWRTa3ktUmVndWxhcmh0dHA6Ly9nbGlkZWRza3kuY29tLwBDAHIAZQBhAHQAZQBkACAAYgB5ACAARwBsAGkAZABlAGQAUwBrAHkARwBsAGkAZABlAGQAUwBrAHkAUgBlAGcAdQBsAGEAcgBWAGUAcgBzAGkAbwBuACAAMQAuADAARwBsAGkAZABlAGQAUwBrAHkALQBSAGUAZwB1AGwAYQByAGgAdAB0AHAAOgAvAC8AZwBsAGkAZABlAGQAcwBrAHkALgBjAG8AbQAvAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAABkAGgAXABMAFgAVABsAFAAYABw=) format("truetype");
        }
    </style>
    
    <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <script>
        (adsbygoogle = window.adsbygoogle || []).push({
            google_ad_client: "ca-pub-2566260602093595",
            enable_page_level_ads: true
        });
    </script>
            <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-75859356-3"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'UA-75859356-3');
        </script>
        <script>
            var _hmt = _hmt || [];
            (function() {
                var hm = document.createElement("script");
                hm.src = "https://hm.baidu.com/hm.js?020fbaad6104bcddd1db12d6b78812f6";
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(hm, s);
            })();
        </script>
    
</head>
<body>
    <div id="app">
        <nav class="navbar navbar-expand-md navbar-light navbar-laravel">
            <div class="container">
                <a class="navbar-brand" href="http://glidedsky.com">
                    GlidedSky
                </a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarSupportedContent" style="font-size: 1.15em">
                    <!-- Left Side Of Navbar -->
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item ">
                            <a class="nav-link" href="http://glidedsky.com">Home</a>
                        </li>
                                                <li class="nav-item ">
                            <a class="nav-link" href="http://glidedsky.com/rank">Rank</a>
                        </li>
                            <li class="nav-item ">
                                <a class="nav-link" href="http://glidedsky.com/about">About</a>
                            </li>
                                            </ul>
                    <!-- Right Side Of Navbar -->
                    <ul class="navbar-nav ml-auto">
                        <!-- Authentication Links -->
                                                    <li class="nav-item dropdown">
                                <a id="navbarDropdown" class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                    sen <span class="caret"></span>
                                </a>

                                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                                    <a class="dropdown-item" href="http://glidedsky.com/logout"
                                       onclick="event.preventDefault();
                                                     document.getElementById('logout-form').submit();">
                                        Logout
                                    </a>

                                    <form id="logout-form" action="http://glidedsky.com/logout" method="POST" style="display: none;">
                                        <input type="hidden" name="_token" value="3aBW4IYv4gF3i04NQzleftPDp5vR7QfSXyDPGpNr">                                    </form>
                                </div>
                            </li>
                                            </ul>
                </div>
            </div>
        </nav>

        <main class="py-4">
                <div class="container">
        <div class="card">
            <div class="card-body">

                <div class="row" style="font-family: glided_sky;">
                                            <div class="col-md-1">
                            074
                        </div>
                                            <div class="col-md-1">
                            741
                        </div>
                                            <div class="col-md-1">
                            413
                        </div>
                                            <div class="col-md-1">
                            736
                        </div>
                                            <div class="col-md-1">
                            001
                        </div>
                                            <div class="col-md-1">
                            83
                        </div>
                                            <div class="col-md-1">
                            723
                        </div>
                                            <div class="col-md-1">
                            772
                        </div>
                                            <div class="col-md-1">
                            487
                        </div>
                                            <div class="col-md-1">
                            93
                        </div>
                                            <div class="col-md-1">
                            466
                        </div>
                                            <div class="col-md-1">
                            426
                        </div>
                                    </div>
            </div>
        </div>
        <ul class="pagination" role="navigation">
        
                    <li class="page-item disabled" aria-disabled="true" aria-label="&laquo; Previous">
                <span class="page-link" aria-hidden="true">&lsaquo;</span>
            </li>
        
        
                    
            
            
                                                                        <li class="page-item active" aria-current="page"><span class="page-link">1</span></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=2">2</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=3">3</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=4">4</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=5">5</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=6">6</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=7">7</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=8">8</a></li>
                                                                    
                            <li class="page-item disabled" aria-disabled="true"><span class="page-link">...</span></li>
            
            
                                
            
            
                                                                        <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=999">999</a></li>
                                                                                <li class="page-item"><a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=1000">1000</a></li>
                                                        
        
                    <li class="page-item">
                <a class="page-link" href="http://glidedsky.com/level/web/crawler-font-puzzle-1?page=2" rel="next" aria-label="Next &raquo;">&rsaquo;</a>
            </li>
            </ul>

    </div>
        </main>
    </div>
                    <script>
        _hmt.push(['_trackEvent', 'level-web', 'view', 'crawler-font-puzzle-1']);
        gtag('event', 'view', {
            'event_category': 'level-web',
            'event_label': 'crawler-font-puzzle-1',
        });
    </script>
    </body>
</html>
'''
response_ = res

html = etree.HTML(res)
num_list = html.xpath('//div[@class="row"]/div/text()')
num_list = [int(num.strip()) for num in num_list]
print(num_list)