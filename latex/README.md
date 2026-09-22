# Como compilar el informe:

### Compila en .out/main.pdf
`latexmk -pdf main.tex`

### Limpia auxiliares de .out/ (deja el PDF)
`latexmk -c`

### Limpia todo, incluido el PDF
`latexmk -C`

### Compila los diagramas .puml de figures/ a .pdf (mismo nombre)
`plantuml -tpdf figures/*.puml`