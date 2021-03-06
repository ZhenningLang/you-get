#!/usr/bin/env python

import re

from ..common import *
from ..extractor import VideoExtractor

from xml.dom.minidom import parseString


class YouTube(VideoExtractor):
    name = "YouTube"

    USER_PLAYLIST_PATTERN = re.compile(r'http.*?/user/.*?/playlists')
    SUB_PLAYLIST_PATTERN = re.compile(r'<li class="channels-content-item yt-shelf-grid-item">'
                                      r'[\s\S]+?'
                                      r'<b>(\d+)</b>'
                                      r'[\s\S]+?'
                                      r'href="(/playlist\?list=[a-zA-Z0-9\-_]+)"')

    # Non-DASH YouTube media encoding options, in descending quality order.
    # http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs. Retrieved July 17, 2014.
    stream_types = [
        {'itag': '38', 'container': 'MP4', 'video_resolution': '3072p',
         'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '3.5-5',
         'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        #{'itag': '85', 'container': 'MP4', 'video_resolution': '1080p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '3-4', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        {'itag': '46', 'container': 'WebM', 'video_resolution': '1080p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        {'itag': '37', 'container': 'MP4', 'video_resolution': '1080p',
         'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '3-4.3',
         'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        #{'itag': '102', 'container': 'WebM', 'video_resolution': '720p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        {'itag': '45', 'container': 'WebM', 'video_resolution': '720p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '2',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        #{'itag': '84', 'container': 'MP4', 'video_resolution': '720p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '2-3', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        {'itag': '22', 'container': 'MP4', 'video_resolution': '720p',
         'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '2-3',
         'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        {'itag': '120', 'container': 'FLV', 'video_resolution': '720p',
         'video_encoding': 'H.264', 'video_profile': 'Main@L3.1', 'video_bitrate': '2',
         'audio_encoding': 'AAC', 'audio_bitrate': '128'}, # Live streaming only
        {'itag': '44', 'container': 'WebM', 'video_resolution': '480p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '1',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
        {'itag': '35', 'container': 'FLV', 'video_resolution': '480p',
         'video_encoding': 'H.264', 'video_profile': 'Main', 'video_bitrate': '0.8-1',
         'audio_encoding': 'AAC', 'audio_bitrate': '128'},
        #{'itag': '101', 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        #{'itag': '100', 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
        {'itag': '43', 'container': 'WebM', 'video_resolution': '360p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '0.5',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
        {'itag': '34', 'container': 'FLV', 'video_resolution': '360p',
         'video_encoding': 'H.264', 'video_profile': 'Main', 'video_bitrate': '0.5',
         'audio_encoding': 'AAC', 'audio_bitrate': '128'},
        #{'itag': '82', 'container': 'MP4', 'video_resolution': '360p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
        {'itag': '18', 'container': 'MP4', 'video_resolution': '360p',
         'video_encoding': 'H.264', 'video_profile': 'Baseline', 'video_bitrate': '0.5',
         'audio_encoding': 'AAC', 'audio_bitrate': '96'},
        {'itag': '6', 'container': 'FLV', 'video_resolution': '270p',
         'video_encoding': 'Sorenson H.263', 'video_profile': '', 'video_bitrate': '0.8',
         'audio_encoding': 'MP3', 'audio_bitrate': '64'},
        #{'itag': '83', 'container': 'MP4', 'video_resolution': '240p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
        {'itag': '13', 'container': '3GP', 'video_resolution': '',
         'video_encoding': 'MPEG-4 Visual', 'video_profile': '', 'video_bitrate': '0.5',
         'audio_encoding': 'AAC', 'audio_bitrate': ''},
        {'itag': '5', 'container': 'FLV', 'video_resolution': '240p',
         'video_encoding': 'Sorenson H.263', 'video_profile': '', 'video_bitrate': '0.25',
         'audio_encoding': 'MP3', 'audio_bitrate': '64'},
        {'itag': '36', 'container': '3GP', 'video_resolution': '240p',
         'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple', 'video_bitrate': '0.175',
         'audio_encoding': 'AAC', 'audio_bitrate': '32'},
        {'itag': '17', 'container': '3GP', 'video_resolution': '144p',
         'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple', 'video_bitrate': '0.05',
         'audio_encoding': 'AAC', 'audio_bitrate': '24'},
    ]

    def __init__(self, *args):
        super().__init__(*args)
        self.playlist_id_num = {}

    @staticmethod
    def decipher(js, s):
        # Examples:
        # - https://www.youtube.com/yts/jsbin/player-da_DK-vflWlK-zq/base.js
        # - https://www.youtube.com/yts/jsbin/player-vflvABTsY/da_DK/base.js
        # - https://www.youtube.com/yts/jsbin/player-vfls4aurX/da_DK/base.js
        # - https://www.youtube.com/yts/jsbin/player_ias-vfl_RGK2l/en_US/base.js
        # - https://www.youtube.com/yts/jsbin/player-vflRjqq_w/da_DK/base.js
        # - https://www.youtube.com/yts/jsbin/player_ias-vfl-jbnrr/da_DK/base.js
        def tr_js(code):
            code = re.sub(r'function', r'def', code)
            code = re.sub(r'(\W)(as|if|in|is|or)\(', r'\1_\2(', code)
            code = re.sub(r'\$', '_dollar', code)
            code = re.sub(r'\{', r':\n\t', code)
            code = re.sub(r'\}', r'\n', code)
            code = re.sub(r'var\s+', r'', code)
            code = re.sub(r'(\w+).join\(""\)', r'"".join(\1)', code)
            code = re.sub(r'(\w+).length', r'len(\1)', code)
            code = re.sub(r'(\w+).slice\((\w+)\)', r'\1[\2:]', code)
            code = re.sub(r'(\w+).splice\((\w+),(\w+)\)', r'del \1[\2:\2+\3]', code)
            code = re.sub(r'(\w+).split\(""\)', r'list(\1)', code)
            return code

        js = js.replace('\n', ' ')
        f1 = match1(js, r'\.set\(\w+\.sp,encodeURIComponent\(([$\w]+)') or \
            match1(js, r'\.set\(\w+\.sp,\(0,window\.encodeURIComponent\)\(([$\w]+)') or \
            match1(js, r'\.set\(\w+\.sp,([$\w]+)\(\w+\.s\)\)') or \
            match1(js, r'"signature",([$\w]+)\(\w+\.\w+\)')
        f1def = match1(js, r'function %s(\(\w+\)\{[^\{]+\})' % re.escape(f1)) or \
                match1(js, r'\W%s=function(\(\w+\)\{[^\{]+\})' % re.escape(f1))
        f1def = re.sub(r'([$\w]+\.)([$\w]+\(\w+,\d+\))', r'\2', f1def)
        f1def = 'function main_%s%s' % (f1, f1def)  # prefix to avoid potential namespace conflict
        code = tr_js(f1def)
        f2s = set(re.findall(r'([$\w]+)\(\w+,\d+\)', f1def))
        for f2 in f2s:
            f2e = re.escape(f2)
            f2def = re.search(r'[^$\w]%s:function\((\w+,\w+)\)(\{[^\{\}]+\})' % f2e, js)
            if f2def:
                f2def = 'function {}({}){}'.format(f2e, f2def.group(1), f2def.group(2))
            else:
                f2def = re.search(r'[^$\w]%s:function\((\w+)\)(\{[^\{\}]+\})' % f2e, js)
                f2def = 'function {}({},b){}'.format(f2e, f2def.group(1), f2def.group(2))
            f2 = re.sub(r'(\W)(as|if|in|is|or)\(', r'\1_\2(', f2)
            f2 = re.sub(r'\$', '_dollar', f2)
            code = code + 'global %s\n' % f2 + tr_js(f2def)

        f1 = re.sub(r'(as|if|in|is|or)', r'_\1', f1)
        f1 = re.sub(r'\$', '_dollar', f1)
        code = code + 'sig=main_%s(s)' % f1  # prefix to avoid potential namespace conflict
        exec(code, globals(), locals())
        return locals()['sig']

    @staticmethod
    def chunk_by_range(url, size):
        urls = []
        chunk_size = 10485760
        start, end = 0, chunk_size - 1
        urls.append('%s&range=%s-%s' % (url, start, end))
        while end + 1 < size:  # processed size < expected size
            start, end = end + 1, end + chunk_size
            urls.append('%s&range=%s-%s' % (url, start, end))
        return urls

    @staticmethod
    def get_url_from_vid(vid):
        return 'https://youtu.be/{}'.format(vid)

    @staticmethod
    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, r'youtu\.be/([^?/]+)') or \
          match1(url, r'youtube\.com/embed/([^/?]+)') or \
          match1(url, r'youtube\.com/v/([^/?]+)') or \
          match1(url, r'youtube\.com/watch/([^/?]+)') or \
          parse_query_param(url, 'v') or \
          parse_query_param(parse_query_param(url, 'u'), 'v')

    def get_sub_playlist_info_from_user_playlist_page(self):
        user_playlist_page_content = get_content(self.url)
        return re.findall(self.__class__.SUB_PLAYLIST_PATTERN, user_playlist_page_content)

    def parse_playlist_id(self):
        """Extracts playlist ID list
        SIDE EFFECT: update self.playlist_id_num
        """
        playlist_id_list = []
        if re.match(self.__class__.USER_PLAYLIST_PATTERN, self.url):
            sub_playlist_info = self.get_sub_playlist_info_from_user_playlist_page()
        else:
            sub_playlist_info = (('Unknown', self.url),)

        for num, sub_playlist_url in sub_playlist_info:
            sub_playlist_id = parse_query_param(sub_playlist_url, 'list') or parse_query_param(sub_playlist_url, 'p')  # noqa
            self.playlist_id_num[sub_playlist_id] = num
            playlist_id_list.append(sub_playlist_id)
        return playlist_id_list

    # noinspection PyBroadException
    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        playlist_id_list = self.parse_playlist_id()
        if not playlist_id_list:
            log.wtf('[Failed] Unsupported URL pattern.')

        for idx, playlist_id in enumerate(playlist_id_list):
            print(f'Sub-play list: {idx}/{len(playlist_id_list)}, number: {self.playlist_id_num[playlist_id]}')
            try:
                video_page = get_content('https://www.youtube.com/playlist?list=%s' % playlist_id)
                from html.parser import HTMLParser
                videos = sorted([HTMLParser().unescape(video)
                                 for video in re.findall(r'<a href="(/watch\?[^"]+)"', video_page)
                                 if parse_query_param(video, 'index')],
                                key=lambda video: parse_query_param(video, 'index'))

                # Parse browse_ajax page for more videos to load
                load_more_href = match1(video_page, r'data-uix-load-more-href="([^"]+)"')
                while load_more_href:
                    browse_ajax = get_content('https://www.youtube.com/%s' % load_more_href)
                    browse_data = json.loads(browse_ajax)
                    load_more_widget_html = browse_data['load_more_widget_html']
                    content_html = browse_data['content_html']
                    vs = set(re.findall(r'href="(/watch\?[^"]+)"', content_html))
                    videos += sorted([HTMLParser().unescape(video)
                                      for video in list(vs)
                                      if parse_query_param(video, 'index')])
                    load_more_href = match1(load_more_widget_html, r'data-uix-load-more-href="([^"]+)"')

                self.title = re.search(r'<meta name="title" content="([^"]+)"', video_page).group(1)
                self.p_playlist()
            except Exception:
                continue

            for video in videos:
                vid = parse_query_param(video, 'v')
                index = parse_query_param(video, 'index')
                try:
                    self.__class__().download_by_url(self.__class__.get_url_from_vid(vid), index=index, **kwargs)
                except Exception:
                    pass

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if not self.vid and self.url:
            self.vid = self.__class__.get_vid_from_url(self.url)

            if self.vid is None:
                self.download_playlist_by_url(self.url, **kwargs)
                exit(0)

        video_info = parse.parse_qs(get_content('https://www.youtube.com/get_video_info?video_id={}'.format(self.vid)))

        ytplayer_config = None
        if 'status' not in video_info:
            log.wtf('[Failed] Unknown status.', exit_code=None)
            raise
        elif video_info['status'] == ['ok']:
            if 'use_cipher_signature' not in video_info or video_info['use_cipher_signature'] == ['False']:
                self.title = parse.unquote_plus(video_info['title'][0])

                # Parse video page (for DASH)
                video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid)
                try:
                    ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+?});', video_page).group(1))
                    self.html5player = 'https://www.youtube.com' + ytplayer_config['assets']['js']
                    # Workaround: get_video_info returns bad s. Why?
                    stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')
                except:
                    stream_list = video_info['url_encoded_fmt_stream_map'][0].split(',')
                    self.html5player = None

            else:
                # Parse video page instead
                video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid)
                ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+?});', video_page).group(1))

                self.title = ytplayer_config['args']['title']
                self.html5player = 'https://www.youtube.com' + ytplayer_config['assets']['js']
                stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')

        elif video_info['status'] == ['fail']:
            if video_info['errorcode'] == ['150']:
                if cookies:
                    # Load necessary cookies into headers (for age-restricted videos)
                    consent, ssid, hsid, sid = 'YES', '', '', ''
                    for cookie in cookies:
                        if cookie.domain.endswith('.youtube.com'):
                            if cookie.name == 'SSID':
                                ssid = cookie.value
                            elif cookie.name == 'HSID':
                                hsid = cookie.value
                            elif cookie.name == 'SID':
                                sid = cookie.value
                    cookie_str = 'CONSENT=%s; SSID=%s; HSID=%s; SID=%s' % (consent, ssid, hsid, sid)

                    video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid,
                                             headers={'Cookie': cookie_str})
                else:
                    video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid)

                try:
                    ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+});ytplayer', video_page).group(1))
                except:
                    msg = re.search('class="message">([^<]+)<', video_page).group(1)
                    log.print_err('[Failed] Got message "%s". Try to login with --cookies.' % msg.strip())
                    raise Exception()

                if 'title' in ytplayer_config['args']:
                    # 150 Restricted from playback on certain sites
                    # Parse video page instead
                    self.title = ytplayer_config['args']['title']
                    self.html5player = 'https://www.youtube.com' + ytplayer_config['assets']['js']
                    stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')
                else:
                    log.wtf('[Error] The uploader has not made this video available in your country.', exit_code=None)
                    raise
                    #self.title = re.search('<meta name="title" content="([^"]+)"', video_page).group(1)
                    #stream_list = []

            elif video_info['errorcode'] == ['100']:
                log.wtf('[Failed] This video does not exist.', exit_code=None) #int(video_info['errorcode'][0])
                raise

            else:
                log.wtf('[Failed] %s' % video_info['reason'][0], exit_code=None) #int(video_info['errorcode'][0])
                raise

        else:
            log.wtf('[Failed] Invalid status.', exit_code=None)
            raise

        # YouTube Live
        if ytplayer_config and (ytplayer_config['args'].get('livestream') == '1' or ytplayer_config['args'].get('live_playback') == '1'):
            if 'hlsvp' in ytplayer_config['args']:
                hlsvp = ytplayer_config['args']['hlsvp']
            else:
                player_response= json.loads(ytplayer_config['args']['player_response'])
                log.e('[Failed] %s' % player_response['playabilityStatus']['reason'], exit_code=1)

            if 'info_only' in kwargs and kwargs['info_only']:
                return
            else:
                download_url_ffmpeg(hlsvp, self.title, 'mp4')
                exit(0)

        for stream in stream_list:
            metadata = parse.parse_qs(stream)
            stream_itag = metadata['itag'][0]
            self.streams[stream_itag] = {
                'itag': metadata['itag'][0],
                'url': metadata['url'][0],
                'sig': metadata['sig'][0] if 'sig' in metadata else None,
                's': metadata['s'][0] if 's' in metadata else None,
                'quality': metadata['quality'][0],
                'type': metadata['type'][0],
                'mime': metadata['type'][0].split(';')[0],
                'container': mime_to_container(metadata['type'][0].split(';')[0]),
            }

        # Prepare caption tracks
        try:
            caption_tracks = json.loads(ytplayer_config['args']['player_response'])['captions']['playerCaptionsTracklistRenderer']['captionTracks']
            for ct in caption_tracks:
                ttsurl, lang = ct['baseUrl'], ct['languageCode']

                tts_xml = parseString(get_content(ttsurl))
                transcript = tts_xml.getElementsByTagName('transcript')[0]
                texts = transcript.getElementsByTagName('text')
                srt = ""; seq = 0
                for text in texts:
                    if text.firstChild is None: continue # empty element
                    seq += 1
                    start = float(text.getAttribute('start'))
                    if text.getAttribute('dur'):
                        dur = float(text.getAttribute('dur'))
                    else: dur = 1.0 # could be ill-formed XML
                    finish = start + dur
                    m, s = divmod(start, 60); h, m = divmod(m, 60)
                    start = '{:0>2}:{:0>2}:{:06.3f}'.format(int(h), int(m), s).replace('.', ',')
                    m, s = divmod(finish, 60); h, m = divmod(m, 60)
                    finish = '{:0>2}:{:0>2}:{:06.3f}'.format(int(h), int(m), s).replace('.', ',')
                    content = unescape_html(text.firstChild.nodeValue)

                    srt += '%s\n' % str(seq)
                    srt += '%s --> %s\n' % (start, finish)
                    srt += '%s\n\n' % content

                self.caption_tracks[lang] = srt
        except: pass

        # Prepare DASH streams
        try:
            dashmpd = ytplayer_config['args']['dashmpd']
            dash_xml = parseString(get_content(dashmpd))
            for aset in dash_xml.getElementsByTagName('AdaptationSet'):
                mimeType = aset.getAttribute('mimeType')
                if mimeType == 'audio/mp4':
                    rep = aset.getElementsByTagName('Representation')[-1]
                    burls = rep.getElementsByTagName('BaseURL')
                    dash_mp4_a_url = burls[0].firstChild.nodeValue
                    dash_mp4_a_size = burls[0].getAttribute('yt:contentLength')
                    if not dash_mp4_a_size:
                        try: dash_mp4_a_size = url_size(dash_mp4_a_url)
                        except: continue
                elif mimeType == 'audio/webm':
                    rep = aset.getElementsByTagName('Representation')[-1]
                    burls = rep.getElementsByTagName('BaseURL')
                    dash_webm_a_url = burls[0].firstChild.nodeValue
                    dash_webm_a_size = burls[0].getAttribute('yt:contentLength')
                    if not dash_webm_a_size:
                        try: dash_webm_a_size = url_size(dash_webm_a_url)
                        except: continue
                elif mimeType == 'video/mp4':
                    for rep in aset.getElementsByTagName('Representation'):
                        w = int(rep.getAttribute('width'))
                        h = int(rep.getAttribute('height'))
                        itag = rep.getAttribute('id')
                        burls = rep.getElementsByTagName('BaseURL')
                        dash_url = burls[0].firstChild.nodeValue
                        dash_size = burls[0].getAttribute('yt:contentLength')
                        if not dash_size:
                            try: dash_size = url_size(dash_url)
                            except: continue
                        dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                        dash_mp4_a_urls = self.__class__.chunk_by_range(dash_mp4_a_url, int(dash_mp4_a_size))
                        self.dash_streams[itag] = {
                            'quality': '%sx%s' % (w, h),
                            'itag': itag,
                            'type': mimeType,
                            'mime': mimeType,
                            'container': 'mp4',
                            'src': [dash_urls, dash_mp4_a_urls],
                            'size': int(dash_size) + int(dash_mp4_a_size)
                        }
                elif mimeType == 'video/webm':
                    for rep in aset.getElementsByTagName('Representation'):
                        w = int(rep.getAttribute('width'))
                        h = int(rep.getAttribute('height'))
                        itag = rep.getAttribute('id')
                        burls = rep.getElementsByTagName('BaseURL')
                        dash_url = burls[0].firstChild.nodeValue
                        dash_size = burls[0].getAttribute('yt:contentLength')
                        if not dash_size:
                            try: dash_size = url_size(dash_url)
                            except: continue
                        dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                        dash_webm_a_urls = self.__class__.chunk_by_range(dash_webm_a_url, int(dash_webm_a_size))
                        self.dash_streams[itag] = {
                            'quality': '%sx%s' % (w, h),
                            'itag': itag,
                            'type': mimeType,
                            'mime': mimeType,
                            'container': 'webm',
                            'src': [dash_urls, dash_webm_a_urls],
                            'size': int(dash_size) + int(dash_webm_a_size)
                        }
        except:
            # VEVO
            if not self.html5player: return
            self.js = get_content(self.html5player)
            if 'adaptive_fmts' in ytplayer_config['args']:
                streams = [dict([(i.split('=')[0],
                                  parse.unquote(i.split('=')[1]))
                                 for i in afmt.split('&')])
                           for afmt in ytplayer_config['args']['adaptive_fmts'].split(',')]
                for stream in streams: # get over speed limiting
                    stream['url'] += '&ratebypass=yes'
                for stream in streams: # audio
                    if stream['type'].startswith('audio/mp4'):
                        dash_mp4_a_url = stream['url']
                        if 's' in stream:
                            sig = self.__class__.decipher(self.js, stream['s'])
                            dash_mp4_a_url += '&signature={}'.format(sig)
                        dash_mp4_a_size = stream['clen']
                    elif stream['type'].startswith('audio/webm'):
                        dash_webm_a_url = stream['url']
                        if 's' in stream:
                            sig = self.__class__.decipher(self.js, stream['s'])
                            dash_webm_a_url += '&signature={}'.format(sig)
                        dash_webm_a_size = stream['clen']
                for stream in streams: # video
                    if 'size' in stream:
                        if stream['type'].startswith('video/mp4'):
                            mimeType = 'video/mp4'
                            dash_url = stream['url']
                            if 's' in stream:
                                sig = self.__class__.decipher(self.js, stream['s'])
                                dash_url += '&signature={}'.format(sig)
                            dash_size = stream['clen']
                            itag = stream['itag']
                            dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                            dash_mp4_a_urls = self.__class__.chunk_by_range(dash_mp4_a_url, int(dash_mp4_a_size))
                            self.dash_streams[itag] = {
                                'quality': '%s (%s)' % (stream['size'], stream['quality_label']),
                                'itag': itag,
                                'type': mimeType,
                                'mime': mimeType,
                                'container': 'mp4',
                                'src': [dash_urls, dash_mp4_a_urls],
                                'size': int(dash_size) + int(dash_mp4_a_size)
                            }
                        elif stream['type'].startswith('video/webm'):
                            mimeType = 'video/webm'
                            dash_url = stream['url']
                            if 's' in stream:
                                sig = self.__class__.decipher(self.js, stream['s'])
                                dash_url += '&signature={}'.format(sig)
                            dash_size = stream['clen']
                            itag = stream['itag']
                            audio_url = None
                            audio_size = None
                            try:
                                audio_url = dash_webm_a_url
                                audio_size = int(dash_webm_a_size)
                            except UnboundLocalError as e:
                                audio_url = dash_mp4_a_url
                                audio_size = int(dash_mp4_a_size)
                            dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                            audio_urls = self.__class__.chunk_by_range(audio_url, int(audio_size))
                            self.dash_streams[itag] = {
                                'quality': '%s (%s)' % (stream['size'], stream['quality_label']),
                                'itag': itag,
                                'type': mimeType,
                                'mime': mimeType,
                                'container': 'webm',
                                'src': [dash_urls, audio_urls],
                                'size': int(dash_size) + int(audio_size)
                            }

    def extract(self, **kwargs):
        if not self.streams_sorted:
            # No stream is available
            return

        if 'stream_id' in kwargs and kwargs['stream_id']:
            # Extract the stream
            stream_id = kwargs['stream_id']
            if stream_id not in self.streams and stream_id not in self.dash_streams:
                log.e('[Error] Invalid video format.')
                log.e('Run \'-i\' command with no specific video format to view all available formats.')
                exit(2)
        else:
            # Extract stream with the best quality
            stream_id = self.streams_sorted[0]['itag']

        if stream_id in self.streams:
            src = self.streams[stream_id]['url']
            if self.streams[stream_id]['sig'] is not None:
                sig = self.streams[stream_id]['sig']
                src += '&signature={}'.format(sig)
            elif self.streams[stream_id]['s'] is not None:
                if not hasattr(self, 'js'):
                    self.js = get_content(self.html5player)
                s = self.streams[stream_id]['s']
                sig = self.__class__.decipher(self.js, s)
                src += '&signature={}'.format(sig)

            self.streams[stream_id]['src'] = [src]
            self.streams[stream_id]['size'] = urls_size(self.streams[stream_id]['src'])


site = YouTube()
download = site.download_by_url
download_playlist = site.download_playlist_by_url
