from pkg_resources import resource_filename


class LeadsheetsWriter:
    PREAMBLE_LATEX = '\n\input{%s}\n' % (resource_filename(__name__,"templates/preamble.tex"))
    HEADER_LATEX = '\\begin{document}\n\n\\begin{song}{title={%s}, interpret={%s}}\n\n'
    POSTAMBLE_LATEX = '\end{song}\n\end{document}'

    SECTIONS = ['intro','chorus', 'verse','bridge','solo','outro']

    def __init__(self, file_name, title, interpret):
        self.file = open(file_name, 'w')
        self.file.write(self.PREAMBLE_LATEX)
        self.file.write(self.HEADER_LATEX % (title, interpret))
        self.current_section = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.current_section:
            self.file.write('\\end{%s}\n' % (self.current_section))  
        self.file.write(self.POSTAMBLE_LATEX)
        self.file.close()

    def write_chordline(self, line, chord_list):
        # pad line with white spaces if line is shorter than last chord index
        if len(chord_list) > 0:
            line  = line.ljust(chord_list[-1][1])

        line_out = ''
        i_start_old = 0
        for chord, i_start in chord_list:
            text = line[i_start_old:i_start]
            # if chord follows '.' put a space (latex doesn't like .\chord{})
            if text.endswith('.'):
                text += ' '
            self.file.write('%s\chord{%s}' % (text, chord))
            i_start_old = i_start

        self.file.write(line[i_start_old:len(line)])

        if len(line) > 0:
            self.file.write('  \\\\\n')

    def write_line(self, line):
        self.file.write(line + '\\')

    def write_section(self, section):
        if self.current_section:
            self.file.write('\\end{%s}\n' % (self.current_section))            
        if section not in LeadsheetsWriter.SECTIONS:
            return

        self.file.write('\\begin{%s}\n' % (section))
        self.current_section = section
