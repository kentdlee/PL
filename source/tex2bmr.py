# encoding: utf-8

# toBeamer
# Copyright (c) 2005 Brad Miller, Kent D. Lee

# TODO:  match the opening environment on the close

import sys
import os
import re


line = sys.stdin.readline()
envText = ''

figTitleText = ''
envStack = []
chapter = 1
practice = 1
example = 1
heading = ""
label = ""
practicelabel=""
blurbframe = False
equationframe = False

while line != '':
    # Strip out citations from slides
    while re.match('^(.*)\\\\cite{[^}]*}(.*)',line):
        g = re.match('^(.*)\\\\cite{[^}]*}(.*)',line)
        line = g.group(1)+g.group(2)
        if line[-1] <> '\n':
            line = line + '\n'

    if re.match('^\s*\\\\slidebreak',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            print '\\begin{frame}[fragile,allowframebreaks]'
            print '\\heading{'+heading+'}'  
            print '\\begin{itemize}'
        else:
            print line[:-1]
    # Labels start at beginning of lines. Keep track of the 
    # last label found.
    if re.match('^\s*\\\\label{.*}',line):
        g = re.match('^\s*\\\\label{(.*)}',line)
        label = g.group(1)
        print line[:-1]

    # Change all begin/end verbatims to begin/end lstlistings
    # because spacing does not work right in verbatim code in beamer
    elif re.match('^\s*\\\\begin{verbatim}',line):
        print '\\begin{lstlisting}[kewordstyle=,numbers=none'
    elif re.match('^\s*\\\\end{verbatim}',line):
        print '\\end{lstlisting}' 
    
    # if the envStack has something on it we are in the middle of some
    # sort of environment so we need to process as we would in the midst
    # of that environment.
    elif len(envStack) > 0:
        if re.match('^\s*\\\\(sub){1,2}section\{(.*)\}',line):
            g = re.match('^\s*\\\\(sub){1,2}section\{(.*)\}',line)
            print '\n{\\bf '+g.group(2)+'}\n'

        elif envStack[-1] == 'figure':
            g = re.match('^\s*\\\\caption{(.*)}',line)
            if g:
                figTitleText = g.group(1)
            elif re.match('^\s*\\\\end{figure}',line):
                envStack.pop()
                print '\\end{figure}'
                print '\\frametitle{'+figTitleText+'}'
                print '\\end{frame}'
                print '\n'
            else:
                print line[:-1]
        elif envStack[-1] == 'wrapfigure':
            g = re.match('^\s*\\\\caption{(.*)}',line)
            if g:
                figTitleText = g.group(1)
            elif re.match('^\s*\\\\end{wrapfigure}',line):
                envStack.pop()
                print '\\end{figure}'
                print '\\frametitle{'+figTitleText+'}'
                print '\\end{frame}'
                print '\n'
            else:
                print line[:-1]
        elif envStack[-1] == 'kdlexercise':
            if re.match('^\s*\\\\end{kdlexercise}',line):
                envStack.pop()
                print '\\end{kdlexercise}'
                print '\n\n\n\\hyperlink{'+label+ \
                    'Solution}{\\beamergotobutton{View Solution}}'
                print '\\end{frame}'
                print '\n'
            #elif line.strip() == "":
            #    print '\\linebreak'
            else:
                print line[:-1]
        elif envStack[-1] == 'kdlexample':
            if re.match('^\s*\\\\end{kdlexample}',line):
                envStack.pop()
                print '\\end{kdlexample}'
                print '\\end{frame}'
                print '\n'
            #elif line.strip() == "":
            #    print '\\linebreak'
            else:
                print line[:-1]
        elif envStack[-1] == 'kdlsol':
            if re.match('^\s*\\\\end{kdlsol}',line):
                envStack.pop()
                print '\\end{kdlsol}'
                print '\n\n\n\\hyperlink{'+practicelabel+ \
                    '}{\\beamergotobutton{Go Back to Practice Problem}}'
                print '\\end{frame}'
                print '\n'
            else:
                print line[:-1]
        elif envStack[-1] == 'blurb':
            # This first match handles one blurb
            # after another.
            if re.match('^}\\\\blurb',line):
                print line[:-1]
            elif re.match('^}',line):
                envStack.pop()
                print '}\n'
            else:
                print line[:-1]
        elif envStack[-1] == 'equation':
            print line[:-1]
            if re.match('^\s*\\\\end{equation}',line):
                envStack.pop()
        elif envStack[-1] == 'lstlisting':
            if re.match('^\s*\\\\end{lstlisting}',line):
                envStack.pop()
                print '\\end{lstlisting}'
                if not blurbframe:
                    print '\\end{frame}'
                    print '\n'
            else:
                print line[:-1]
        elif envStack[-1] == 'spec':
            if re.match('^\s*\\\\end{spec}',line):
                envStack.pop()
                print '\\end{spec}'
                if not blurbframe:
                    print '\\end{frame}'
                    print '\n'
            else:
                print line[:-1]
        elif envStack[-1] == 'itemize':
            if re.match('^\s*\\\\begin{itemize}',line):
                envStack.append('itemize')
                print line[:-1]
            elif re.match('^\s*\\\\end{itemize}',line):
                envStack.pop()
                if len(envStack) == 0:
                    print '\\end{itemize}'
                    if not blurbframe:
                        print '\\end{frame}'
                        print '\n'
                else:
                    print line[:-1]
            else:
                print line[:-1]
        elif envStack[-1] == 'enumerate': 
            if re.match('^\s*\\\\begin{enumerate}',line):
                envStack.append('enumerate')
                print line[:-1]
            elif re.match('^\s*\\\\end{enumerate}',line):
                envStack.pop()
                if len(envStack) == 0:
                    print '\\end{enumerate}'
                    if not blurbframe:
                        print '\\end{frame}'
                        print '\n'
                else:
                    print line[:-1]
            else:
                print line[:-1]
    
    # At this point we are looking for our next environment to 
    # to process. When we find one below we'll add it to the 
    # envStack so we remember where we are.
    elif re.match('^\s*\\\\(sub){0,1}section.*',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        g = re.match('^\s*\\\\(sub){0,1}section(.*)',line)
        heading = g.group(2)
        print line[:-1]
    elif re.match('^\s*\\\\newsection.*',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        g =  re.match('^\s*\\\\newsection(.*)',line)
        heading = g.group(1)
        print '\\subsection'+g.group(1)
    elif re.match('^\s*\\\\newchapter.*',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        g =  re.match('^\s*\\\\newchapter(.*)',line)
        heading = g.group(1)
        print '\\section'+g.group(1)
    elif re.match('^\s*\\\\slideheading{([^}]*)}',line):
        g = re.match('^\s*\\\\slideheading{([^}]*)}',line)
        heading = g.group(1)
    elif re.match('^\s*\\\\begin{figure}',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        print '\\begin{frame}[fragile,allowpagebreaks]'
        print line[:-1]
        envStack.append('figure')
    elif re.match('^\s*\\\\begin{wrapfigure}',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        print '\\begin{frame}[fragile,allowpagebreaks]'
        print '\\begin{figure}'
        envStack.append('wrapfigure')
    elif re.match('^\s*\\\\begin{kdlexercise}',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        print '\\begin{frame}[fragile,allowframebreaks]'
        #print '\\frametitle{Practice Problem ' + str(chapter)+"."+str(practice) + ' }'
        print '\\heading{' + heading + '}\n'
        print '\\begin{kdlexercise}'
        # this extra print was added because labels apparently caused 
        # problems. They indented the 1st line inside an example or 
        # practice problem.
        print
        practice += 1
        envStack.append('kdlexercise')
    elif re.match('^\s*\\\\begin{kdlexample}',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False
        # This should be done everywhere the if blurbframe code above
        # is done. I'm cheating here.
        if equationframe:
            print '\\end{frame}'
            print '\n'
            equationframe = False

        print '\\begin{frame}[fragile,allowframebreaks]'
        #print '\\frametitle{Example ' + str(chapter) + "." + str(example) + '}'
        print '\\heading{' + heading + '}\n'
        print '\\begin{kdlexample}'
        # this extra print was added because labels apparently caused 
        # problems. They indented the 1st line inside an example or 
        # practice problem.
        print
        example+=1
        envStack.append('kdlexample')
    elif re.match('^\s*\\\\kdlsolution{.*}',line):
        if blurbframe:
            print '\\end{itemize}'
            print '\\end{frame}'
            print '\n'
            blurbframe = False

        g = re.match('^\s*\\\\kdlsolution{(.*)}',line)
        practicelabel = g.group(1)
        print '\\begin{frame}[fragile,allowframebreaks] % found a solution'
        print '\\label{'+practicelabel+'Solution}'
        #print '\\frametitle{Example ' + str(chapter) + "." + str(example) + '}'
        print line[:-1]
        envStack.append('kdlsol')
    elif re.match('^\s*\\\\begin{lstlisting}',line):
        envStack.append('lstlisting')
        if not blurbframe:
            print '\\begin{frame}[fragile,allowframebreaks]'
            print '\\heading{'+heading+'}'
        print line[:-1]
    elif re.match('^\s*\\\\begin{spec}',line):
        envStack.append('spec')
        if not blurbframe:
            print '\\begin{frame}[fragile,allowframebreaks]'
            print '\\heading{'+heading+'}'
        print line[:-1]
    elif re.match('^\s*\\\\blurb{',line):
        envStack.append('blurb')
        if not blurbframe:
            print '\\begin{frame}[fragile,allowframebreaks]'
            print '\\heading{'+heading+'}'  
            print '\\begin{itemize}'

        blurbframe = True
        print line[:-1]
    elif re.match('^\s*\\\\begin{equation}',line):
        envStack.append('equation')
        if not equationframe:
            print '\\begin{frame}[fragile,allowframebreaks]'
            print '\\heading{'+heading+'}'  

        equationframe = True
        print line[:-1]
    else:
        g = re.match('^\s*\\\\begin{(enumerate|itemize)}',line)
        if g:
            if not blurbframe:
                print '\\begin{frame}[fragile,allowframebreaks]'
                print '\\heading{'+heading+'}'
            print line[:-1]
            envStack.append(g.group(1))
    line = sys.stdin.readline()
