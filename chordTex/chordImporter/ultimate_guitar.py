import urllib.request
import json


class UltimateGuitarParser:
    LYRICS_START_STRING = '    window.UGAPP.store.page = '
    LYRICS_END_STRING = '};'
    CHORD_START_STRING = '[ch]'
    CHORD_END_STRING = '[/ch]'

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
                if l.decode('utf-8').startswith(self.LYRICS_START_STRING):
                    s = l.decode('utf-8')[len(self.LYRICS_START_STRING):-2]
                    self.info = json.loads(s)
            response.close()
        except:
           print('could not read html')
           return ''
        self.tab = self.info['data']['tab_view']['wiki_tab']['content']
        self.song_info = self.info['data']['tab']
        
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
        for line in lyrics.splitlines():
            chord_list = self.find_chords_in_line(line)

            if not chord_list:
                # if there are no chords in this line, write line
                writer.write_chordline(line, chord_list_old)
            else:
                # if there are also chords in this line, insert chords into empty line
                writer.write_chordline('', chord_list_old)

            line_old = line
            chord_list_old = chord_list

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



