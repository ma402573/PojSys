#!/usr/bin/env python
# coding: utf-8


python serveur.py 6000 & xterm -e sh -c 'printf client | netcat -w 1 localhost 6000 > result'