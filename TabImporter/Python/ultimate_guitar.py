#!/usr/bin/env python3
import urllib.request
import lxml.html
from lxml import etree

class UltimateGuitarParser:
    LYRICS_START_STRING = '<pre class="js-tab-content"><i></i>'
    LYRICS_END_STRING = '</pre>'
    CHORD_START_STRING = '<span>'
    CHORD_END_STRING = '</span>'
    CHORD_START_LATEX = '\chord{'
    CHORD_END_LATEX = '}'


    def get_lyrics(self,html):
        lyrics, i_start, i_end = self._substring_find(html, self.LYRICS_START_STRING, self.LYRICS_END_STRING)
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
        print('lineout: ' + line_out)
        return line_out


    def find_chords(self, lyrics):
        print('find_chords: ')
        string_out = ''
        chord_list_old = []
        line_old = ''
        for line in lyrics.splitlines():
            chord_list = self.find_chords_in_line(line)

            if chord_list_old:
                if not chord_list:
                    # if there are no chords in this line and there are chords in the line above, insert them
                    string_out += self.insert_chords_in_line(line, line_old, chord_list_old) + '\n'
                # else:
                    # if there are also chords in this line, insert chords in the line above
            else:
                #if there are no chords in line above, write it to output
                string_out += line_old + '\n'

            line_old = line
            chord_list_old = chord_list

        return string_out


    def parse(self,html):
        lyrics = self.get_lyrics(html.decode('utf8'))
        string_out = self.find_chords(lyrics)
        print(string_out)


    def _substring_find(self,string, start_string, stop_string, i_start0=0):
        i_start0 = string.find(start_string, i_start0) 
        if i_start0 < 0:
            return ('', -1, -1)

        i_start = i_start0 + len(start_string)

        i_end = string.find(stop_string, i_start);
        
        if i_start0 >= 0 and i_end >= 0:
            return (string[i_start:i_end], i_start0, i_end)
        else:
            return ('', -1, -1)


class UltimateGuitarParser_lxml:
    def find_chords(lyrics):
        chords = lyrics.xpath('span')
        return [c.xpath('string()') for c in chords]


    def get_lyrics(html):
        tree = lxml.etree.HTML(html)
        # find lyrics part of page
        lyrics_list = tree.xpath('//pre[contains(@class, "js-tab-content")]')
        if not lyrics_list:
            print('Error: no lyrics found on this site')
            return None
        else:
            return lyrics_list[0]


# print('starting')

parser = UltimateGuitarParser()

# get HTML of URL
with urllib.request.urlopen('https://tabs.ultimate-guitar.com/a/annenmaykantereit/es_geht_mir_gut_crd.htm') as response:
    html = response.read()
    response.close()
    # html = 'Not here<pre class="js-tab-content"><i></i>blablabla</pre>'
    parser.parse(html)

print('ending')