#!/usr/bin/env python3
import urllib.request
from sys import exit, argv

class UltimateGuitarParser:
    LYRICS_START_STRING = '<pre class="js-tab-content">'
    LYRICS_END_STRING = '</pre>'
    CHORD_START_STRING = '<span>'
    CHORD_END_STRING = '</span>'
    CHORD_START_LATEX = '\chord{'
    CHORD_END_LATEX = '}'
    PREAMBLE_LATEX = '\documentclass[a4paper, twocolumn]{article}\n \\usepackage{../Latex/Lyrics/lyrics}\n \\begin{document}\n'
    POSTAMBLE_LATEX = '\end{document}'

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
        return line_out


    def find_chords(self, lyrics):
        string_out = ''
        chord_list_old = []
        line_old = ''
        lyrics += '\n\n'  # add empty line at the end to make sure that last line is treated
        for line in lyrics.splitlines():
            chord_list = self.find_chords_in_line(line)

            if chord_list_old:
                if not chord_list:
                    # if there are no chords in this line and there are chords in the line above, insert them
                    line_new = self.insert_chords_in_line(line, line_old, chord_list_old)
                else:
                    # if there are also chords in this line, insert chords into empty line
                    line_new = self.insert_chords_in_line('', line_old, chord_list_old)
            else:
                if not chord_list:
                    line_new = line #if there are no chords in line above, write it to output
                else:
                    line_new = None

            if line_new is not None:
                if len(line_new) > 0:
                    line_new += ' \\\\'

                string_out += line_new + '\n' #add latex and file new line

            line_old = line
            chord_list_old = chord_list


        return string_out


    def parse(self, URL):
        try:
            response = urllib.request.urlopen(URL)
            html = response.read()
            response.close()
        except:
            print('could not read html')
            return ''
        return self.PREAMBLE_LATEX + self.parse_string(html.decode('utf8')) + self.POSTAMBLE_LATEX

    def parse_string(self, string):
        lyrics = self.get_lyrics(string)
        string_out = self.find_chords(lyrics)
        return string_out


    def _substring_find(self, string, start_string, stop_string, i_start0=0):
        i_start0 = string.find(start_string, i_start0) 
        if i_start0 < 0:
            return ('', -1, -1)

        i_start = i_start0 + len(start_string)

        i_end = string.find(stop_string, i_start);
        
        if i_start0 >= 0 and i_end >= 0:
            return (string[i_start:i_end], i_start0, i_end)
        else:
            return ('', -1, -1)


parser = UltimateGuitarParser()

# Get URL from command line arguments
if len(argv) < 2 :
    print("Error: No URL provided")
    exit()

url = argv[1];

#print("parsing: " + url)
string_out = parser.parse(url)
print(string_out)
