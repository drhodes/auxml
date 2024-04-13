



#!/usr/bin/env python
from livereload import Server, shell
server = Server()
server.watch('./examples/auxml-src/webpage.xml', shell('make webpage'))
server.watch('./examples/macro-definitions/webpage-macros.xml', shell('make webpage'))
server.serve(root='/tmp/webpage/output.html')


