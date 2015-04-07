#!/usr/bin/python
# -*- coding: latin_1 -*-

# =========={ INICIO DE LA LICENCIA DE ESTE SOFTWARE }==========
#
#  Copyright (c) 2005-2006, Manuel Lorenzo Frieiro
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#  * Neither the name of the Manuel Lorenzo Frieiro nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# =========={ FIN DE LA LICENCIA DE ESTE SOFTWARE }==========


# Información del módulo
#========================
# Desde la versión 0.3 este módulo deja de considerarse un módulo opcional y pasa a ser obligatorio siendo variable el nivel de registro
    
__module_name__ = 'Logging Module'
__module_version__ = '0.3.1'
__module_date__ = '2007/03/21'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo encargado de los registros del bot.'

# Módulos necesarios
#====================

import re
import time
import codecs

# Variables Globales
#====================
CTCP = '\001'

# Clases
#========

class logger:
    # Constructores de la clase:
    def __init__(self, loglevel, code, logFileChannel, logFileDcc, logFileDebug, logFileIrc, logFilePrivate):
	 self.loglevel = int(loglevel)
	 self.code = code
	 self.logFiles = {}
	 self.logFiles['CHANNEL'] = logFileChannel
	 self.logFiles['DCC'] = logFileDcc
	 self.logFiles['DEBUG'] = logFileDebug
	 self.logFiles['IRC'] = logFileIrc
	 self.logFiles['PRIVATE'] = logFilePrivate
         return
    # Métodos
    #---------
    # log: graba los datos pasados como parámetro en el fichero de tipo X si el nivel de log es igual o superior al citado en el fichero de configuración
    def log(self, level, type, data):
         if level <= self.loglevel:
              if not self.logFiles.has_key(type):
	           self.log(0, 'DEBUG', u'Se ha intentado registrar datos con \"tipo\" incorrecto.')
		   self.log(0, 'DEBUG', u'Nivel: %i' % level)
		   self.log(0, 'DEBUG', u'Tipo: %s' % type)
		   self.log(0, 'DEBUG', u'Datos: %s' % data)
	      else:
	           outputLine = u''
		   if type == 'CHANNEL':
		        outputLine += data
		   elif type == 'DCC':
		        outputLine += data
	           elif type == 'DEBUG':
		        outputLine += data
	           elif type == 'IRC':
		        outputLine += data
		   elif type == 'PRIVATE':
		        outputLine += data
		   if outputLine != '':
		        outputLine += '\n'
			outputLine = '(%s) %s' % (time.strftime('%a %d/%m/%Y %H:%M:%S', time.localtime()), outputLine)
			try:
			     outputHandle = codecs.open(self.logFiles[type], 'a', self.code)
			     outputHandle.write(outputLine)
			     outputHandle.close()
			except IOError, descError:
			     print u'(%s) Error de Entrada/Salida en %s [%s]' % (time.strftime('%a %d/%m/%Y %H:%M:%S', time.localtime()), self.logFiles[type], descError)
         return True
    # parseIrcData: A partir de una línea de texto procedente del servidor de IRC envía los datos al tipo de registro indicado
    def parseIrcData(self, textLine):
	 if re.search('^ERROR', textLine):
	      self.log(1, 'IRC', u'[ERROR] %s' % re.search('(:+.*$)', textLine).group()[1:])
	 elif re.search('^:[^ ]+![^ ]+@[^ ]+ ', textLine) != None:
	      if re.search('^[^ ]+ PRIVMSG', textLine) != None:
	           regExpElements = re.search('^:(?P<sender>[^ ]+) [^ ]+ (?P<target>[^ ]+) :(?P<message>.*)$', textLine)
		   if re.search('^%s.*%s$' % (CTCP, CTCP), regExpElements.group('message')) != None:
		        ctcpEval = re.search('^%s(?P<type>[^ ]+)(?P<data>.*%s)$' % (CTCP, CTCP), regExpElements.group('message'))
			if ctcpEval.group('type') == 'ACTION':
			     data = u'[%s] * %s%s' % (regExpElements.group('target'), regExpElements.group('sender'), ctcpEval.group('data'))
			else:
			     data = u'[%s] %s envía un CTCP %s (parámetros:%s)' % (regExpElements.group('target'), regExpElements.group('sender'), ctcpEval.group('type'), ctcpEval.group('data'))
	           else:
	                data = u'[%s] <%s> %s' % (regExpElements.group('target'), regExpElements.group('sender'), regExpElements.group('message'))
		   if re.search('^#.*$', regExpElements.group('target'), re.I):
		        self.log(1, 'CHANNEL', data)
		   else:
		        self.log(1, 'PRIVATE', data)
	      elif re.search('^[^ ]+ NOTICE', textLine) != None:
	           regExpElements = re.search('^:(?P<sender>[^ ]+) [^ ]+ (?P<target>[^ ]+) :(?P<message>.*)$', textLine)
	           data = u'[%s] -%s- %s' % (regExpElements.group('target'), regExpElements.group('sender'), regExpElements.group('message'))
		   if re.search('^@*#.*$', regExpElements.group('target'), re.I):
		        self.log(1, 'CHANNEL', data)
		   else:
		        self.log(1, 'PRIVATE', data)
	      elif re.search('^[^ ]+ JOIN', textLine) != None:
	           regExpElements = re.search('^:(?P<nick>[^ ]+) [^ ]+ :(?P<channel>.*)$', textLine)
	           self.log(0, 'CHANNEL', u'[%s] Join >> %s' % (regExpElements.group('channel'), regExpElements.group('nick')))
	      elif re.search('^[^ ]+ PART', textLine) != None:
	           if re.search(' :.*$', textLine) != None:
		        regExpElements = re.search('^:(?P<nick>[^ ]+) [^ ]+ (?P<channel>[^ ]+) :(?P<message>.*)$', textLine)
	                self.log(1, 'CHANNEL', u'[%s] Part >> %s (%s)' % (regExpElements.group('channel'), regExpElements.group('nick'), regExpElements.group('message')))
	           else:
		        regExpElements = re.search('^:(?P<nick>[^ ]+) [^ ]+ (?P<channel>[^ ]+).*$', textLine)
	                self.log(1, 'CHANNEL', u'[%s] Part >> %s' % (regExpElements.group('channel'), regExpElements.group('nick')))
	      elif re.search('^[^ ]+ QUIT', textLine) != None:
	           regExpElements = re.search('^:(?P<nick>[^ ]+) [^ ]+ :(?P<message>.*)$', textLine)
	           self.log(1, 'CHANNEL', u'Quit >> %s (%s)' % (regExpElements.group('nick'), regExpElements.group('message')))
	      elif re.search('^[^ ]+ KICK', textLine) != None:
	           regExpElements = re.search('^:(?P<kicker>[^ ]+) [^ ]+ (?P<channel>[^ ]+) (?P<target>[^ ]+) :(?P<reason>.*)$', textLine)
	           self.log(1, 'CHANNEL', u'[%s] Kick >> %s expulsa a %s {%s}' % (regExpElements.group('channel'), regExpElements.group('kicker'), regExpElements.group('target'), regExpElements.group('reason')))
	      elif re.search('^[^ ]+ MODE', textLine) != None:
	           if re.search('^:[^ ]+ [^ ]+ [^ ]+ [^ ]+ .+$', textLine) != None:
		        regExpElements = re.search('^:(?P<sender>[^ ]+) [^ ]+ (?P<channel>[^ ]+) (?P<modes>[^ ]+) (?P<targets>.+)$', textLine)
	                self.log(1, 'CHANNEL', u'[%s] Modo >> %s fija modo %s %s' % (regExpElements.group('channel'), regExpElements.group('sender'), regExpElements.group('modes'), regExpElements.group('targets')))
		   else:
		        regExpElements = re.search('^:(?P<sender>[^ ]+) [^ ]+ (?P<channel>[^ ]+) (?P<modes>[^ ]+)', textLine)
	                self.log(1, 'CHANNEL', u'[%s] Modo >> %s fija modo %s' % (regExpElements.group('channel'), regExpElements.group('sender'), regExpElements.group('modes')))
	      elif re.search('^[^ ]+ TOPIC', textLine) != None:
	           regExpElements = re.search('^:(?P<nick>[^ ]+) [^ ]+ (?P<channel>[^ ]+) :(?P<topic>.+)$', textLine)
	           self.log(1, 'CHANNEL', u'[%s] Topic >> %s cambia topic a %s' % (regExpElements.group('channel'), regExpElements.group('nick'), regExpElements.group('topic')))
	      elif re.search('^[^ ]+ INVITE', textLine) != None:
	           regExpElements = re.search('^:(?P<sender>[^ ]+) [^ ]+ (?P<target>[^ ]+) :(?P<channel>.+)$', textLine)
	           self.log(1, 'PRIVATE', u'[%s] Invite >> %s te invita a entrar en %s' % (regExpElements.group('target'), regExpElements.group('sender'), regExpElements.group('channel')))
	      elif re.search('^[^ ]+ NICK', textLine) != None:
	           regExpElements = re.search('^:(?P<nick>[^ ]+) [^ ]+ :(?P<newnick>[^ ]+)$', textLine)
	           self.log(1, 'CHANNEL', u'Nick >> %s se cambia el nick a %s' % (regExpElements.group('nick'), regExpElements.group('newnick')))
	 elif re.search('^:', textLine) != None:
	      self.log(1, 'IRC', u'%s' % re.search(' +(.*$)', textLine).group()[1:])
	 return
    # version: devuelve el nombre y version del módulo
    def version(self):
	 return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
