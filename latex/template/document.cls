%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --------------------------------------------------------
% You may modify 'document.cls' file according to your
% needs and preferences. This LaTeX2e class file defines 
% the document layout and behavior.
% --------------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------
% Class configuration
%----------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{template/document}[24/02/2026 Document LaTeX2e class]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}}
\ProcessOptions\relax
\LoadClass{extarticle}
\AtEndOfClass{\RequirePackage{microtype}}

%----------------------------------------------------------
% Required packages
%----------------------------------------------------------

\RequirePackage[utf8]{inputenc}
\RequirePackage{etoolbox}
\RequirePackage[framemethod=tikz]{mdframed}
\RequirePackage{xifthen}
\RequirePackage{array} 
\RequirePackage{iflang}
\RequirePackage{fontawesome5}
\RequirePackage{ragged2e}
\RequirePackage{subcaption}
\RequirePackage{balance}

%----------------------------------------------------------
% Custom packages (location/name)
%----------------------------------------------------------

\RequirePackage{template/languages}
\RequirePackage{template/environments}

%----------------------------------------------------------
% Optional-, extra- packages
%----------------------------------------------------------

% \RequirePackage[switch]{lineno}
% \RequirePackage{adforn}
% \RequirePackage{fontawesome5}
% \RequirePackage{chemfig}
% \RequirePackage{circuitikz}
% \RequirePackage{matlab-prettifier}
% \RequirePackage{longtable}
% \RequirePackage{supertabular}
% \RequirePackage{setspace}
% \RequirePackage{lipsum}
% \RequirePackage{pbalance}
% \RequirePackage{afterpage}
% \RequirePackage{sidecap}
% \RequirePackage[switch]{lineno}

%----------------------------------------------------------
% Fonts
%----------------------------------------------------------

\RequirePackage[T1]{fontenc}
\RequirePackage[notextcomp]{stix2}
\RequirePackage{FiraSans}
\RequirePackage[scaled=0.80]{FiraMono}
\RequirePackage{roboto-mono}

%----------------------------------------------------------
% Figures
%----------------------------------------------------------

\RequirePackage{graphicx}
\RequirePackage{here}
\RequirePackage{float}
\RequirePackage{stfloats} 

%----------------------------------------------------------
% Tables
%----------------------------------------------------------

\RequirePackage{adjustbox}
\RequirePackage[most,many]{tcolorbox}
\RequirePackage{colortbl}
\RequirePackage{booktabs}
\AtBeginEnvironment{tabular}{\small\sffamily}
\newcommand{\tabletext}[1]{{\fontsize{7}{9}\vskip2pt\sffamily\itshape\selectfont#1}}

%----------------------------------------------------------
% Geometry setup
%----------------------------------------------------------

\RequirePackage[
    left=1.25cm,
    right=1.25cm,
    top=2cm,
    bottom=2cm,
    headsep=0.75cm,
    % showframe
]{geometry}

%----------------------------------------------------------
% Equation above/below skip
%----------------------------------------------------------

\newlength{\eqskip}\setlength{\eqskip}{9pt}
\expandafter\def\expandafter\normalsize\expandafter{%
	\normalsize%
	\setlength\abovedisplayskip{\eqskip-\baselineskip}%
	\setlength\belowdisplayskip{\eqskip-\baselineskip}%
	\setlength\abovedisplayshortskip{\eqskip-\baselineskip}%
	\setlength\belowdisplayshortskip{\eqskip}%
}

%----------------------------------------------------------
% Color template
%----------------------------------------------------------

\RequirePackage{xcolor}
% \definecolor{themecolor}{rgb}{0.11, 0.15, 0.33}  % Navy (#1D2554)
%\definecolor{themecolor}{rgb}{0.39, 0.26, 0.00} % Bronce
% \definecolor{themecolor}{rgb}{0.35, 0.10, 0.25} % Ciruela

\definecolor{themecolor}{rgb}{0.17, 0.30, 0.09} % Verde
% \definecolor{themecolor}{rgb}{0.38, 0.10, 0.08} % Ladrillo

% \definecolor{themecolor}{rgb}{0.12, 0.3, 0.17}  % Green
% \definecolor{themecolor}{rgb}{0.0, 0.2, 0.4}    % Blue
% \definecolor{themecolor}{rgb}{0.4, 0.26, 0.13}  % Brown



%----------------------------------------------------------
% URLs style
%----------------------------------------------------------

\RequirePackage{url}
\RequirePackage{xurl}
\renewcommand\UrlFont{\selectfont}

%----------------------------------------------------------
% Hyperref setup
%----------------------------------------------------------

\RequirePackage[colorlinks=true,allcolors=themecolor]{hyperref}
\RequirePackage{cleveref}
\RequirePackage{bookmark}

% New commands for figure-, table-, code- cross references
\newcommand{\figref}[1]{\hyperref[#1]{\figlabel~\ref*{#1}}}
\newcommand{\figsref}[1]{\hyperref[#1]{\figslabel~\ref*{#1}}}
\newcommand{\tabref}[1]{\hyperref[#1]{\tablabel~\ref*{#1}}}
\newcommand{\coderef}[1]{\hyperref[#1]{\captionlabelcode~\ref*{#1}}}
\newcommand{\equref}[1]{\hyperref[#1]{\eqlabel~\ref*{#1}}}

%----------------------------------------------------------
% Items
%----------------------------------------------------------

\RequirePackage{enumitem}
\setlist{noitemsep}

%----------------------------------------------------------
% Header and footer (first page)
%----------------------------------------------------------

\RequirePackage[bottom,hang,flushmargin,ragged]{footmisc}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\pagestyle{fancy}

% New commands
\newcommand{\footerfont}{\normalfont\sffamily\fontsize{8}{9}\selectfont}
\newcommand{\journalname}[1]{\def\@journalname{#1}}
\newcommand{\footerlogo}[1]{\def\@footerlogo{#1}}
\newcommand{\journal}[1]{\def\@journal{#1}}
\newcommand{\theday}[1]{\def\@theday{#1}}
\newcommand{\vol}[1]{\def\@vol{#1}}
\newcommand{\no}[1]{\def\@no{#1}}

% First page style
\fancypagestyle{firststyle}{
    \fancyhead[L]{}
    \fancyhead[C]{}
    \fancyhead[R]{}
    \fancyfoot[C]{}
    \fancyfoot[L]{
        % Insertar el logo centrado verticalmente respecto al texto
        {\ifx\@footerlogo\undefined\else
            \adjustbox{valign=c}{\includegraphics[height=18pt]{\@footerlogo}}%
            \hspace{3pt}% Espacio entre logo y texto
        \fi}
        % Nombre de la organización y otros datos
        \begin{tabular}{@{}l@{}}
            {\ifx\@journalname\undefined\else\footerfont\bfseries\@journalname\hspace{8pt}\fi}
            {\ifx\@theday\undefined\else\footerfont\@theday\hspace{8pt}\fi}
            {\ifx\@vol\undefined\else\footerfont{Vol.~}\@vol\hspace{8pt}\fi}
            {\ifx\@no\undefined\else\footerfont{No.~}\@no\hspace{8pt}\fi}
        \end{tabular}
    }
}

% Head and foot rule
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

%----------------------------------------------------------
% Header and footer 
%----------------------------------------------------------

% Fancy head
\fancyhead[RO,LE]{\ifx\@title\undefined\else\footerfont\@title\fi}
\fancyhead[RE,LO]{\ifx\@journal\undefined\else\footerfont\@journal\fi}

% Fancy foot
\fancyfoot[C]{\footerfont\thepage\textendash\pageref{LastPage}}

%----------------------------------------------------------
% Dropcap (lettrine)
%----------------------------------------------------------

\RequirePackage{lettrine}
\newcommand{\dropcapfont}{\color{themecolor}\bfseries}
\newcommand{\dropcap}[1]{\lettrine[lines=2,lraise=0,findent=2pt, nindent=0em]{{\fontsize{27}{24}\dropcapfont{#1}}}{}}

%----------------------------------------------------------
% Abstract style
%----------------------------------------------------------

% Abstract text style new commands
\newcommand{\keywords}[1]{\def\@keywords{#1}}
\newcommand{\abstracttitle}[1]{\def\@abstracttitle{#1}}
\newcommand{\absfont}{\color{black}\normalfont\sffamily\linespread{1}\fontsize{8.5}{11}\selectfont}
\newcommand{\absheadfont}{\color{themecolor}\normalfont\sffamily\fontsize{9}{11}\selectfont}
\newcommand{\keywordsfont}{\normalfont\sffamily\itshape\linespread{1}\fontsize{7.8}{9}\selectfont}
\newcommand{\keywordheadfont}{\normalfont\sffamily\fontsize{7.8}{9}\selectfont\bfseries}

% Abstract definition
\def\xabstract{abstract}
\long\def\abstract#1\end#2{
    \def\two{#2}\ifx\two\xabstract
    \long\gdef\theabstract{\ignorespaces#1}
    \def\go{\end{abstract}}
\else
    #1\end{#2}
    \gdef\theabstract{\vskip12pt 
    \vskip12pt}
    \let\go\relax\fi
\go}

% Abstract style 
\newcommand{\formatabstract}{%
    \begin{tcolorbox}[colback=themecolor!13, arc=3pt, boxrule=0pt, left=6pt, right=6pt, top=6pt, bottom=6pt, before skip=0pt, after skip=0pt]
        \ifx\@keywords\undefined
            \absheadfont\bfseries\@abstracttitle\vskip0.5em\absfont\theabstract\vskip10pt
        \else
            \absheadfont\bfseries\@abstracttitle\vskip0.5em\absfont\theabstract\vskip10pt
            \keywordsfont\keywordname\hspace{0.1em}\keywordsfont\@keywords
        \fi
    \end{tcolorbox}
}

%----------------------------------------------------------
% Title style
%----------------------------------------------------------

\RequirePackage{titling}
\RequirePackage[explicit]{titlesec}

% Title commands
\newcommand{\dates}[1]{\def\@dates{#1}}
\newcommand{\doctype}[1]{\def\@doctype{#1}}
\newcommand{\logo}[1]{\def\@logo{#1}}
\newcommand{\titlefont}{\bfseries\color{themecolor}\fontsize{18}{22}\sffamily\selectfont}

\renewcommand{\@maketitle}{
    \bgroup
        \noindent
        \ifx\@logo\undefined
            \begin{minipage}[c]{1\textwidth}
                {\ifx\@doctype\undefined\vskip-20pt\else\vskip-22pt\RaggedRight\sffamily\bfseries\@doctype\par\fi}
                {\RaggedRight\titlefont\@title\par\vskip8pt}
            \end{minipage}
        \else
            \begin{minipage}[c]{0.75\textwidth}
                {\ifx\@doctype\undefined\vskip-20pt\else\vskip-22pt\RaggedRight\sffamily\bfseries\@doctype\par\fi}
                {\RaggedRight\titlefont\@title\par\vskip8pt}
            \end{minipage}%
            \hfill
            \begin{minipage}[c]{0.25\textwidth}
                \raggedleft
                \includegraphics[width=\linewidth]{\@logo}
            \end{minipage}
        \fi

        \par\vskip0pt

        {\normalsize\sffamily\RaggedRight\@author\par}
        {\ifx\@dates\undefined\vskip18pt\else\vskip10pt\fontsize{7pt}{8pt}\RaggedRight\sffamily\selectfont\@dates\par\vskip18pt\fi}
    \egroup
    % Solo dibuja la caja del abstract si el documento define uno (main.tex)
    \ifdef{\theabstract}{\formatabstract}{}
    \vskip18pt
}

%----------------------------------------------------------
% Front-Matter information (after page) 
%----------------------------------------------------------

\RequirePackage{afterpage}

\newcommand{\docinfo}[1]{\def\@docinfo{#1}}
\let\@docinfo\@empty
\newcommand{\@corres}{}
\let\@corres\@empty

\newcommand{\corres}[1]{%
  \g@addto@macro\@corres{%
    \par\hspace*{1em} #1\par
  }%
}

\appto{\maketitle}{
  \afterpage{
    % Check if there is content to print
    \ifx\@corres\empty
      \ifx\@docinfo\empty
        % Case 1: Both empty, nothing is done
      \else
        % Case 2: Only docinfo defined
        \begin{figure}[b!]
            \footnotesize\sffamily
            \footnoterule
            \@docinfo
            \vspace{-0.2\baselineskip}
        \end{figure}
      \fi
    \else
      % \@corres has content.
      \ifx\@docinfo\empty
        % Case 3: Only corres defined
        \begin{figure}[b!]
            \footnotesize\sffamily
            \footnoterule
            \@corres
            \vspace{-0.2\baselineskip}
        \end{figure}
      \else
        % Case 4: Both are defined
        \begin{figure}[b!]
            \footnotesize\sffamily
            \footnoterule
            \@corres
            \vskip8pt
            \@docinfo
            \vspace{-0.2\baselineskip}
        \end{figure}
      \fi
    \fi
  }
}

%----------------------------------------------------------
% Affiliation setup
%----------------------------------------------------------

\RequirePackage{authblk}

\setlength{\affilsep}{10pt}
\renewcommand\Authfont{\normalfont\sffamily\fontsize{9}{11}}
\renewcommand\Affilfont{\sffamily\itshape\fontsize{7.5}{9}\selectfont}
\renewcommand\AB@affilnote[1]{\textsuperscript{\sffamily#1}}
\renewcommand\AB@authnote[1]{\textsuperscript{\sffamily#1}}
% \renewcommand\AB@affilsepx{; \protect\Affilfont}

\renewcommand\Authand{\ignorespaces\andlanguage}
\renewcommand\Authands{\ignorespaces\andlanguage}

%----------------------------------------------------------
% Section style
%----------------------------------------------------------

\setcounter{secnumdepth}{5}

\titleformat{\section}
    {\color{themecolor}\sffamily\large\bfseries}
    {\thesection.}
    {0.5em}
    {\MakeUppercase{#1}}
    []

\titleformat{name=\section,numberless}[block]
    {\color{themecolor}\sffamily\large\bfseries}
    {}
    {0em}
    {\tikz\draw[themecolor, fill=themecolor] (0,0) rectangle (1.25ex, 1.25ex); \hspace{2.5pt}{\MakeUppercase{#1}}}
    []
  
\titleformat{\subsection}[block]
    {\sffamily\bfseries}
    {\thesubsection.}
    {0.5em}
    {#1}     
    []
  
\titleformat{\subsubsection}[block] % You may change it to "runin"
    {\small\sffamily\bfseries\itshape}
    {\thesubsubsection.}
    {0.5em}
    {#1} % If using runin, change #1 to '#1. ' (space at the end)
    []    
  
\titleformat{\paragraph}[runin]
    {\small\bfseries}
    {}
    {0em}
    {#1} 
  
\titlespacing*{\section}{0pc}{3ex \@plus4pt \@minus3pt}{5pt}
% \titlespacing*{\subsection}{0pc}{2.5ex \@plus3pt \@minus2pt}{2pt}
% \titlespacing*{\subsubsection}{0pc}{2ex \@plus2.5pt \@minus1.5pt}{2pt}
% \titlespacing*{\paragraph}{0pc}{1.5ex \@plus2pt \@minus1pt}{12pt}

%----------------------------------------------------------
% Table of Contents
%----------------------------------------------------------

\newlength{\tocsep} 
% Sets the indentation of the sections in the table of contents
\setlength\tocsep{1.5pc} 

\usepackage{titletoc}
\contentsmargin{0cm}

\titlecontents{section}[\tocsep]
    {\addvspace{4pt}\sffamily\selectfont\bfseries}
    {\contentslabel[\thecontentslabel]{\tocsep}}
    {}
    {\hfill\thecontentspage}
    []

\titlecontents{subsection}[3pc]
    {\addvspace{4pt}\small\sffamily\selectfont}
    {\contentslabel[\thecontentslabel]{\tocsep}}
    {}
    {\ \titlerule*[.5pc]{.}\ \thecontentspage}
    []

\titlecontents*{subsubsection}[3pc]
    {\footnotesize\sffamily\selectfont}
    {}
    {}
    {}
    [\ \textbullet\ ]

%----------------------------------------------------------
% Figure-, Table-, Listings/Minted- caption style
%----------------------------------------------------------

\RequirePackage{caption}
\RequirePackage{subcaption}

% Figure
\captionsetup[figure]{format=plain, labelsep=period, textfont={small}, justification=centering, labelfont={small,bf,sf}}

% Table
\captionsetup*[table]{labelfont={small,bf,sf},textfont={small},position=below,aboveskip=0pt,labelsep=period}

% Listings and minted
\captionsetup[lstlisting]{font=small, labelfont={bf,sf}, aboveskip=0pt, belowskip=9pt, position=below, textfont=small, labelsep=period}
\renewcommand\lstlistingname{\captionlabelcode}
\renewcommand\lstlistlistingname{\captionlabelcode}

%----------------------------------------------------------
% Listings style
%----------------------------------------------------------

\RequirePackage{listings}
\newenvironment{code}{\captionsetup{type=lstlisting}}{}

% Defined colors for listings environment

% Listings style
\definecolor{codegreen}{rgb}{0.169, 0.302, 0.090}
\definecolor{codegray}{rgb}{0.113, 0.145, 0.329}
\definecolor{codepurple}{rgb}{0.416, 0.239, 0.604}
\definecolor{backcolour}{rgb}{0.894, 0.910, 0.882}
\definecolor{codeorange}{rgb}{1.000, 0.498, 0.000}
\definecolor{codeblue}{rgb}{0.184, 0.365, 0.698}
\definecolor{graphite}{rgb}{0.25, 0.25, 0.25}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codeorange},
    keywordstyle=\color{codeblue},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codegreen},
    basicstyle=\robotomono\scriptsize\color{graphite},
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    xleftmargin=1.5em,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2,
    lineskip=1.5pt,
}
\lstset{style=mystyle}

%----------------------------------------------------------
% Minted setup
%----------------------------------------------------------

\usepackage{minted}
\usemintedstyle{lovelace} % lovelace, tango, stata-light
\renewcommand{\theFancyVerbLine}{\scriptsize\textcolor{black}{\arabic{FancyVerbLine}}}
\definecolor{codeback}{RGB}{248, 248, 248} 
\setminted{
	frame=single,
	breaklines,
	numbersep=5pt,
    xleftmargin=1.8em,
	fontsize=\small,
	bgcolor=codeback,
}

%----------------------------------------------------------
% Inlinecode definition
%----------------------------------------------------------

\NewDocumentCommand{\inlinecode}{v}{%
  \tcbox[
	boxrule=0.4pt,          
	arc=1pt,                
	colback=gray!15,        
	colframe=gray!30,        
	coltext=themecolor,         
	left=1pt, right=1pt,    
	top=1pt, bottom=1pt,      
	boxsep=0pt,             
	fontupper=\ttfamily\small,
	valign=center,
    nobeforeafter,
    box align=base
  ]{#1}%
}

%----------------------------------------------------------
% Colors for 3-Coloring
%----------------------------------------------------------

\definecolor{grafo_azul}{HTML}{79A2F2}
\definecolor{grafo_verde}{HTML}{7BB35C}
\definecolor{grafo_naranja}{HTML}{FFB366}

\newcommand{\col}[1]{_{\scriptscriptstyle\textcolor{#1}{\blacksquare}}}

%----------------------------------------------------------
% BibLaTeX
%----------------------------------------------------------

\RequirePackage{csquotes}
\RequirePackage[
	backend=biber,
	style=ieee,
	sorting=ynt,
	citestyle=numeric-comp
]{biblatex}

\addbibresource{references.bib}

%----------------------------------------------------------

\endinput