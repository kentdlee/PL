class LaTeX_Converter:
    
    def __init__(self):
        self.chapterNum = -1
    
    def makeTitle(self, title, level):
        if level == 0:
            titleChar = "="
        elif level == 1:
            titleChar = "-"
        elif level == 2:
            titleChar = "="
        elif level == 3:
            titleChar = "*"
        else:
            titleChar = "+"
            
        text = title + "\n" + (titleChar * len(title)) + "\n"
        
        if level == 0 or level == 1:
            text = "\n"+(titleChar * len(title)) + "\n" + text
             
        return text
        
    
    def skipEnv(self, infile):
        
        ch = infile.read(1)
        text = ch
        braceCount = 1
        
        while ch!="{":
            ch = infile.read(1)
            text += ch
            
        
        while braceCount>0:
            ch = infile.read(1)
            if ch == "{":
                braceCount+=1
            if ch == "}":
                braceCount-=1
            text += ch
            
            
        return text
    
    def parse(self, infile):
    
        state = 1
        text = ""
        word = ""
        indent = ""
        done = False
        exerciseNum = 0
        figureNum = 0
        sectionNum = 0
        solutionNum = 0
        exampleNum = 0
        language = "cpp"
        
        while not done:
            #print("DEBUG: State = ", state)
            ch = infile.read(1)
            if ch == '':
                print("DEBUG: Finished")
                #print(text)
                done = True
            elif state == 1:
                if ch == '%':
                    state = 4
                elif ch == "\\":
                    word = ch
                    state = 2
                elif ch == '}':
                    #print("FOUND END OF ENV WITH TEXT")
                    #print(text)
                    done = True
                elif ch == "$":
                    mathtext = ""
                    ch = infile.read(1)
                    while ch!="$":
                        mathtext+=ch
                        ch = infile.read(1)
                    text += ":math:`"+mathtext
                    text = text.strip()+"`"
                elif ch == '`':
                    ch = infile.read(1)
                    if ch == '`':
                        text += '"'
                    else:
                        text += '`' + ch
                elif ch == '[':
                    subtext = self.parse(infile).strip()
                    text += '[' + subtext + ']'
                elif ch == ']':
                    done = True
                elif ch == '{':
                    text += self.parse(infile)
                elif ch == "\n" and len(text) > 1 and text[-1] == "\n" and text[-2] == "\n":
                    pass
                else:
                    if ch == '*':
                        ch = "\*"
                    text += ch
            elif state == 2:
                word += ch
                if word == "\\{":
                    state = 1
                elif word == "\\}":
                    state = 1
                elif word == '\\[':
                    mathtxt = ""
                    while len(mathtxt) < 2 or mathtxt[-2:] != "\\]":
                        mathtxt += infile.read(1)
                        
                    mathtxt = mathtxt[:-2]
                    
                    text += "\n\n.. math::\n  " + mathtxt + "\n"
                    state = 1
                elif word == '\\(':
                    mathtxt = ""
                    while len(mathtxt) < 2 or mathtxt[-2:] != "\\)":
                        mathtxt += infile.read(1)
                        
                    mathtxt = mathtxt[:-2]
                    
                    text += "\n\n.. math::\n  " + mathtxt + "\n"
                    state = 1
                elif word == '\\documentclass{':
                    subtext = self.parse(infile).strip()
                    #print("DEBUG", word, "subtext:", subtext)
                    #print(text)
                    state = 1
                elif word == '\\usepackage{':
                    subtext = self.parse(infile).strip()
                    #print("DEBUG",word,'subtext: ',subtext)
                    #print(text)
                    state = 1
                    
                elif word == "\\label{":
                    subtext = self.parse(infile).strip()
                    #text += ".. _"+subtext+":\n"
                    state = 1
                    
                elif word == "\\ref{":
                    subtext = self.parse(infile).strip()
                    #text += subtext+"_"
                    state = 1
                    
                elif word == "\\pageref{":
                    subtext = self.parse(infile).strip()
                    #text += subtext+"_"
                    state = 1
                    
                elif word == "\\underline{":
                    subtext = self.parse(infile).strip()
                    text += ":underline:`" + subtext + "`"
                    state = 1
                    
                elif word == "\\title{":
                    subtext = self.parse(infile).strip()
                    #print("DEBUG", word, "subtext:", subtext)
                    #text += self.makeTitle(subtext,0)
                    state = 1
                    
                elif word == "\\include{":
                    filename = self.parse(infile).strip()
                    print("PROCESSING", filename)
                    #print("DEBUG", word, "subtext:", subtext)
                    text += "   " + filename + ".rst\n"
                    
                    subfile = open(filename+".tex","r")
                    subfiletext = self.parse(subfile)
                    subrstfile = open(filename+".rst","w")
                    subrstfile.write(subfiletext)
                    subfile.close()
                    state = 1
                    
                elif word == "\\pagestyle{":
                    subtext = self.parse(infile)
                    #print("DEBUG",word,'subtext: ',subtext)
                    state = 1     
                    
                elif word == "\\lstset":
                    subtext = self.skipEnv(infile)
                    #print("DEBUG",word,'subtext: ',subtext)
                    state = 1 
                    
                elif word == "\\setcounter{":
                    subtext = self.parse(infile)
                    subtext2 = self.skipEnv(infile)
                    #print("DEBUG",word,"subtext: ", subtext, "subtext2:",subtext2)
                    state = 1    
    
                elif word == "\\fancyplain{":
                    subtext = self.parse(infile)
                    subtext2 = self.skipEnv(infile)
                    #print("DEBUG",word,"subtext: ", subtext, "subtext2:",subtext2)
                    state = 1 
                    
                elif word == "\\blurb{":
                    subtext = self.parse(infile)
                    text += subtext
                    state=1
                    
                elif word == "\\\\":
                    state = 1
                    
                elif word == "\=":
                    state = 1
                    
                elif word == "\\newline":
                    state = 1
                    
                elif word == "\\newenvironment":
                    subtext = self.skipEnv(infile)
                    subtext2 = self.skipEnv(infile)
                    subtext3 = self.skipEnv(infile)
                    #print("DEBUG",word,"subtext: ", subtext, "subtext2:",subtext2)
                    state = 1  
                
                elif word == "\\makeindex":
                    state = 1
                    
                elif word == "\\maketitle":
                    state = 1
                    
                elif word == "\\thispagestyle":
                    subtext = self.skipEnv(infile)
                    state = 1
                    
                elif word == "\\pagestyle":
                    subtext = self.skipEnv(infile)
                    state = 1
                    
                elif word == "\\frontmatter":
                    state = 1
                    
                elif word == "\\mainmatter":
                    state = 1
                    
                elif word == "\\tableofcontents":
                    text += self.makeTitle("Contents",2) + "\n.. toctree::\n   :maxdepth: 4\n\n"
                    state = 1
                    
                elif word == "\\setcounter":
                    subtext = self.skipEnv(infile)
                    subtext = self.skipEnv(infile)
                    state = 1       
                
                elif word == "\\index":
                    self.skipEnv(infile)
                    state = 1
                    
                    
                elif word == "\\%":
                    text += "%"
                    state = 1
                    
                elif word == "\\$":
                    text += "$"
                    state = 1
    
                elif word == "\\#":
                    text += "#"
                    state = 1
    
                elif word == "\\|":
                    text += "|"
                    state = 1
                
                elif word == "\\&":
                    text += "&"
                    state = 1
                    
                elif word == "\\_":
                    text += "_"
                    state = 1
                
                elif word == "\\backmatter":
                    state = 1
                    
                elif word == "\\newpage":
                    state = 1
                    
                elif word == "\\chapter{":
                    subtext = self.parse(infile)
                    self.chapterNum += 1
                    text += self.makeTitle("Chapter "+str(self.chapterNum) + ": "+subtext,0)
                    exerciseNum = 0
                    solutionNum = 0
                    state = 1
    
                elif word == "\\newchapter{":
                    subtext = self.parse(infile)
                    self.chapterNum += 1
                    text += self.makeTitle("Chapter "+str(self.chapterNum) + ": "+subtext,0)
                    exerciseNum = 0
                    solutionNum = 0
                    state = 1
                    
                elif word == "\\bibliography":
                    self.skipEnv(infile)
                    state = 1
                    
                elif word == "\\bibliographystyle":
                    self.skipEnv(infile)
                    state = 1
                    
                elif word == "\\newsection{":
                    subtext = self.parse(infile)
                    sectionNum+=1
                    text += self.makeTitle(subtext,1)
                    state=1
                    
                elif word == "\\subsubsection{":
                    subtext = self.parse(infile)
                    text += self.makeTitle(subtext, 3)
                    state = 1
     
                elif word == "\\subsubsection*{":
                    subtext = self.parse(infile)
                    text += self.makeTitle(subtext, 3)
                    state = 1                
    
                elif word == "\\cite{":
                    subtext = self.parse(infile)
                    #text += "["+subtext+"]_"
                    state = 1
                    
                elif word == "\\subsection*{":
                    subtext = self.parse(infile)
                    text += self.makeTitle(subtext,2)
                    state=1
    
                elif word == "\\subsection{":
                    subtext = self.parse(infile)
                    text += self.makeTitle(subtext,2)
                    state=1
                    
                elif word == "\\practice":
                    text += "practice problem "
                    state = 1  
    
                elif word == "\\Practices":
                    text += "Practice problems "
                    state = 1
                
                elif word == "\\printindex":
                    state = 1
                    
                elif word == "\\slidebreak":
                    state = 1
                    
                elif word == "\\Huge":
                    state = 1
                    text += self.parse(infile)
                    done = True
    
                elif word == "\\huge":
                    state = 1
                    text += self.parse(infile)
                    done = True
                    
                elif word == "\\small":
                    state = 1
                    text += self.parse(infile)
                    done = True
                
                elif word == "\\scriptsize":
                    state = 1         
    
                elif word == "\\slideheading":
                    self.skipEnv(infile)
                    state = 1
                    
                elif word == "\\centering":
                    state = 1
                    
                elif word == "\\noindent":
                    state = 1
                    
                elif word == "\\author":
                    subtext = self.skipEnv(infile)
                    state = 1
                    
                elif word == "\\item":
                    text += indent + itemchar
                    state = 1
                    
                elif word == "\\kdlsolution{":
                    subtext = self.parse(infile)
                    solutionNum += 1
                    text += ".. _exercise" + str(self.chapterNum) + "-" + str(solutionNum) + ":\n\n"
                    text += self.makeTitle("Solution to Practice Problem "+str(self.chapterNum) + "." + str(solutionNum),2)
                    state = 1
                    
                elif word == "\\begin{":
                    subtext = self.parse(infile)
                    if subtext == "document":
                        pass
                    elif subtext == "itemize":
                        indent += "  "
                        itemchar = "* "
                    elif subtext == "spec":
                        indent += "  "
                        itemchar = "* "
                    elif subtext == "enumerate":
                        indent += "  "
                        itemchar = '#. '
                    elif subtext == "kdlsol":
                        pass
                    elif subtext == "wrapfigure":
                        self.skipEnv(infile);
                        self.skipEnv(infile);
                        self.skipEnv(infile);
                    elif subtext == "equation":
                        eqn = ""
                        line = infile.readline().strip()
                        while line != "\end{equation}":
                            eqn += line
                            line = infile.readline().strip()
                        text += "\n\n.. math::\n  " + eqn + "\n"
                        state = 1
                        
                    elif subtext == "figure":
                        ch = infile.read(1)
                        while ch!="\n": # skip anything else on this line
                            ch = infile.read(1)  
                    elif subtext == "kdlexercise":
                        exerciseNum += 1
                        subtext = self.parse(infile)
                        text += "\n.. container:: exercise\n\n" 
                        
                        newtext = "  **Practice " + str(self.chapterNum) + "." + str(exerciseNum) + "**\n\n  "
                        
                        for sc in subtext.strip():
                            if sc == "\n":
                                newtext += "\n  "
                            else:
                                newtext += sc
                                
                        text += newtext
                        
                        text += "\n\n  :ref:`You can check your answer(s) here.<exercise"+str(self.chapterNum)+"-"+str(exerciseNum)+">`\n\n"
                        
                        state = 1
                    
                    elif subtext == "quote":
                        quotetext = self.parse(infile)
                        text += "    " + quotetext
                        state = 1
                        
                    elif subtext == "kdlexample":
                        exampleNum += 1
                        
                        text += self.makeTitle("Example " + str(self.chapterNum)+"."+str(exampleNum), 2)
                        
                    elif subtext == "lstlisting":
                        infile.readline() # skip rest of line
                        subtext = ''
                        
                        while len(subtext) < 15 or subtext[-16:] != "\\end{lstlisting}":
                            subtext += infile.read(1)
                        subtext = subtext[:-16]
                        text += "\n.. code-block:: " + language + "\n\n  "
                        for sc in subtext:
                            if sc == "\n":
                                text += "\n  "
                            else:
                                text += sc
                                
                        state = 1                          
                        
                    elif subtext == "center":
                        pass 
                    else:
                        print("UNHANDLED BEGIN of", subtext)
                    state = 1
                    
                elif word == "\\end{":
                    subtext = self.parse(infile).strip()
                    if subtext == "document":
                        pass
                    elif subtext == "itemize":
                        indent = indent[:-2]
                    elif subtext == "spec":
                        indent = indent[:-2]
                    elif subtext == "enumerate":
                        indent = indent[:-2]
                    elif subtext == "wrapfigure":
                        pass
                    elif subtext == "figure":
                        pass
                    elif subtext == "center":
                        pass
                    elif subtext == "kdlsol":
                        pass       
                    elif subtext == "kdlexample":
                        pass
                    elif subtext == "kdlexercise":
                        done = True
                    elif subtext == "lstlisting":
                        done = True
                    elif subtext == "quote":
                        done = True
                    else:
                        print("UNHANDLED END of", subtext)
                    state = 1
                    
                elif word == "\\includegraphics[":
                    self.parse(infile)
                    ch = infile.read(1)
                    subtext = self.parse(infile).strip()
                    if subtext[-3:].lower() == "pdf":
                        subtext = subtext[:-3] + "png"
                    text += "\n.. container:: figboxright\n"
                    text += "\n   .. figure:: " + subtext + "\n"
                    state = 1
                    
                elif word == "\\includegraphics{":
                    subtext = self.parse(infile).strip()
                    if subtext[-3:].lower() == "pdf":
                        subtext = subtext[:-3] + "png"
                    text += "\n.. container:: figboxright\n"
                    text += "\n   .. figure:: " + subtext + "\n"
                    state = 1
                    
                elif word == "\\caption{":
                    subtext = self.parse(infile).strip()
                    figureNum += 1
                    text += "      **Fig. "+str(self.chapterNum) + "." + str(figureNum) + ": " + subtext+"**\n"
                    state=1
                    
                elif word == "\\scshape":
                    state = 1
    
                elif word == "\\sf":
                    state = 1
                    
                elif word == "\\bf":
                    subtext = self.parse(infile).strip()
                    text += "**" + subtext + "**"
                    done = True
                                
    
                elif word == "\\em":
                    subtext = self.parse(infile).strip()
                    text += "*" + subtext + "*"
                    done = True
                    
                elif word == "\\verb":
                    fc = infile.read(1)
                    ch = infile.read(1)
                    while ch!=fc:
                        text+=ch
                        ch = infile.read(1)
                        
                    state=1
                    
                elif word == "\\texttt":
                    subtext = self.skipEnv(infile)[1:-1].strip()              
                    text += "``"+subtext+"``"
                    state=1
                    
                    
                else:
                    if len(word) > 20:
                        print("FOUND UNKNOWN FORMATTING COMMAND", word)
                        done = True
                        
            elif state == 3:
                # inside a new environment
                subtext = self.parse(infile)
                text += subtext
                
            elif state == 4:
                # ignore comments
                if ch == '\n':
                    state = 1
                    
        return text
            

def main():
    file = open("ProgrammingLanguages.tex","r")
    outfile = open("index.rst","w")

    converter = LaTeX_Converter()
    
    text = converter.parse(file)
    #print("Text Returned In Main")
    #print(text)
    outfile.write(text)
    outfile.close()
    #ch = file.read(1)
    
    #while ch!="":
        #print(ch)
        
        #ch = file.read(1)
        
if __name__ == "__main__":
    main()