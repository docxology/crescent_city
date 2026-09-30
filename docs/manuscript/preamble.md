# LaTeX Preamble

```latex
% Core mathematics
\usepackage{amsmath}
\usepackage{amssymb}

% Document layout — minimal margins
\usepackage{geometry}
\geometry{margin=0.6in,top=0.7in,bottom=0.7in}
\usepackage{float}
\usepackage{graphicx}
\usepackage{caption}
\captionsetup{font=small,labelfont=bf,labelsep=period,justification=justified}

% Tables
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}

% Typography and formatting
\usepackage{microtype}
\usepackage{xcolor}

% Cross-references and citations — all links red
\usepackage{hyperref}
\definecolor{linkred}{RGB}{180,0,30}
\hypersetup{
  colorlinks=true,
  linkcolor=linkred,
  citecolor=linkred,
  urlcolor=linkred,
  filecolor=linkred,
  anchorcolor=linkred,
  menucolor=linkred,
  runcolor=linkred
}
\usepackage[capitalise,noabbrev]{cleveref}
\usepackage{natbib}
\bibpunct{(}{)}{;}{a}{,}{,}

% Better paragraph spacing
\setlength{\parskip}{4pt plus 1pt minus 1pt}
\setlength{\parindent}{0pt}

% Slightly tighter section spacing
\usepackage[compact]{titlesec}
\titlespacing*{\section}{0pt}{12pt plus 2pt minus 2pt}{6pt plus 1pt minus 1pt}
\titlespacing*{\subsection}{0pt}{8pt plus 2pt minus 2pt}{4pt plus 1pt minus 1pt}

% Header / footer
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\itshape Crescent City, California}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
```
