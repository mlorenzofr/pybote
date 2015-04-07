#!/usr/bin/python
# -*- coding: latin_1 -*-

# =========={ INICIO DE LA LICENCIA DE ESTE SOFTWARE }==========
#
#  Copyright (c) 2005, Manuel Lorenzo Frieiro
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

__module_name__ = 'pyBOTe'
__module_version__ = '0.3.0r1'
__module_date__ = '2007/03/01'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Bot de IRC para desarrollar diferentes funciones.'

# Módulos necesarios
# ===================

import getopt
import sys
import getpass
import os
import signal
import ConfigParser

# Ruta de los módulos adicionales del bot
sys.path.append('%s%smodules' % (os.path.dirname(sys.argv[0]), os.sep))
import botFerrolterra

# Funciones
#===========

# Usage: Muestra la ayuda del programa
def usage():
    print 'Uso: %s [OPCIONES]' % sys.argv[0]
    print '%s\n' % __module_description__
    print '*** Opciones disponibles ***\n'
    print '\t-c, --config\t\tIndica los canales en los que entrará el bot. Los canales deben ir separados por una coma (,)'
    print '\t-v, --version\t\tMuestra la versión del script.'
    print '\t-h, --help\t\tMuestra este mensaje de ayuda.\n'
    return

# createDaemon: Crea un fork del proceso padre y cierra las salidas standard para que el BOT funcione como un daemon
def createDaemon(logdir):
    initDir = os.path.abspath(logdir)
    pid = os.fork()
    if pid == 0:
         os.setsid()
         signal.signal(signal.SIGHUP, signal.SIG_IGN)
         pid = os.fork()
         if pid == 0:
	      # Guarrería de eliminar el chdir pero si no me da errores al abrir fichero referenciados
	      # en el fichero de configuración como '.'
              # os.chdir(os.sep)
              os.umask(0)
         else:
              os._exit(0)
    else:
         os._exit(0)
    sys.stdin = open('/dev/null', 'r')
    sys.stdout = open('%s%sout.log' % (initDir, os.sep), 'a')
    sys.stderr = open('%s%serr.log' % (initDir, os.sep), 'a')
    return

# main: función principal
def main():
    configFile = ''
    try:
         opts, args = getopt.getopt(sys.argv[1:], 'c:vh', ['config=', 'version', 'help'])
    except getopt.GetoptError:
         usage()
	 sys.exit(1)
    for opt, arg in opts:
         if opt in ['-v', '--version']:
	      print '%s versión %s' % (sys.argv[0], __module_version__)
	      print '%s' % __module_description__
	      sys.exit()
	 if opt in ['-h', '--help']:
	      usage()
	      sys.exit()
	 if opt in ['-c', '--config']:
	      configFile = arg
    if configFile == '':
         print 'Debe especificarse un fichero de configuración para el bot.'
	 sys.exit(2)
    if not os.path.isfile(configFile):
         print 'No se ha podido abrir el fichero %s.' % configFile
	 sys.exit(3)
    generalConfig = ConfigParser.ConfigParser()
    generalConfig.read(configFile)
    if generalConfig.getboolean('general', 'daemon'):
         createDaemon(generalConfig.get('general', 'logdir'))
    generalConfig = ''
    botObject = botFerrolterra.botFerrolterra(configFile)
    if botObject.getPassword() == '':
         botObject.setPassword(getpass.getpass('Introduce contraseña del nick: '))
    botObject.start()
    return

if __name__ == '__main__':
    main()
