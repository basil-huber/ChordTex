import urllib.request
import json
import re

def print_k(d, prefix=''):
    if isinstance(d, dict):
        for k in d:
            print(prefix + '|-' + k)
            print_k(d[k], prefix + '  ')




class UltimateGuitarParser:
    RE_SONG_JSON = re.compile(r'class="js-store" data-content="(.*)"></div>')
    #LYRICS_START_STRING = r'class="js-store" data-content='#    window.UGAPP.store.page = '
    #LYRICS_END_STRING = ''
    CHORD_START_STRING = '[ch]'
    CHORD_END_STRING = '[/ch]'
    RE_TAB_SPLIT = re.compile(r'\[/?tab\]', re.DOTALL)

    def __init__(self, writer_class):
        self.writer_class = writer_class
        

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __call__(self, URL, output_filename):    
        try:
            response = urllib.request.urlopen(URL)
            for l in response:
                match = UltimateGuitarParser.RE_SONG_JSON.search(l.decode('utf-8'))
                if match:
                    json_str = match.group(1).replace('&quot;', '"')
                    print(json_str)
                    self.info = json.loads(json_str)
                    print_k(self.info)
            else:
                ValueError('Could not find chords in html')
            response.close()
        except:
            ValueError('could not read html')
            return ''
        self.tab = self.info['store']['page']['data']['tab_view']['wiki_tab']['content']
        self.song_info = self.info['store']['page']['data']['tab']
        
        with self.writer_class(output_filename, self.song_info['song_name'], self.song_info['artist_name']) as writer:
            self.parse_string(self.tab, writer)


    def get_lyrics(self,html):
        lyrics_dict, i_start, i_end = self._substring_find(html, self.LYRICS_START_STRING, self.LYRICS_END_STRING, HTML_TAG = True)
        return lyrics


    def find_chords_in_line(self,line):
        i_end = 0
        offset = 0
        chord_list = []
        while True:
                chord, i_start, i_end = self._substring_find(line, self.CHORD_START_STRING, self.CHORD_END_STRING, i_end)
                # if there are not more chords in the line, return
                if chord == '':
                    break

                chord_list.append((chord, i_start - offset))
                offset += len(self.CHORD_START_STRING) + len(self.CHORD_END_STRING)

        return chord_list


    def insert_chords_in_line(self, line, line_old, chord_list):
        # pad line with white spaces if line_old is longer
        line = line.ljust(len(line_old) - (len(self.CHORD_START_STRING) + len(self.CHORD_END_STRING))*len(chord_list))
        line_out = ''
        i_start_old = 0
        for chord, i_start in chord_list:
            line_out += line[i_start_old:i_start] + self.CHORD_START_LATEX + chord + self.CHORD_END_LATEX
            i_start_old = i_start

        line_out += line[i_start_old:len(line)]
        return line_out


    def find_chords(self, lyrics, writer):
        chord_list_old = []
        line_old = ''
        lyrics += '\n\n'  # add empty line at the end to make sure that last line is treated
        for tab in self.RE_TAB_SPLIT.split(lyrics):
            for line in tab.splitlines():

                chord_list = self.find_chords_in_line(line)
                if not chord_list:
                    if self.find_section(line,writer):
                        line = ''
                    else:
                        # if there are no chords in this line, write line
                        writer.write_chordline(line, chord_list_old)
                else:
                    # if there are also chords in this line, insert chords into empty line
                    writer.write_chordline('', chord_list_old)

                line_old = line
                chord_list_old = chord_list

    def find_section(self, line, writer):
        m = re.search('\\[(\\w+)\]', line)
        if not m:
            return None
        section = m.group(1)
        print(section)

        section_lc = section.lower()
        if section_lc in self.writer_class.SECTIONS:
            writer.write_section(section_lc)
        else:
            print('Unknown section %s' % (section))
        return section


    def parse_string(self, lyrics, writer):
        string_out = self.find_chords(lyrics, writer)
        return string_out


    def _substring_find(self, string, start_string, stop_string, i_start0=0, HTML_TAG = False):
        i_start0 = string.find(start_string, i_start0) 
        if i_start0 < 0:
            return ('', -1, -1)

        i_start = i_start0 + len(start_string)

        #if HTML_TAG is true, find the end of the tag
        if HTML_TAG:
            i_start = string.find(">", i_start-1)+1

        i_end = string.find(stop_string, i_start);
        
        if i_start0 >= 0 and i_end >= 0:
            return (string[i_start:i_end], i_start0, i_end)
        else:
            return ('', -1, -1)



