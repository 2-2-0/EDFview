#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  EDFview.py
#  
#  Copyright 2015 220 <220@WKH>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# care for your brain and it will care for you
import EEG, EEGGraph
import pygame

# change here to use other file
initial_filename = "test.edf"

# change these to use another resolution
screen_width = 800
screen_height = 600

def initGraph ((w, h), caption):
	canvas = pygame.display.set_mode ((w, h))
	pygame.display.set_caption (caption)
	pygame.init ()
	pygame.font.init ()
	return canvas
	
def initFont ():
	pygame.font.init ()
	font = pygame.font.SysFont ("monospace", 8, False, False)
	return font

def main():
	print "EDFview, by 220 @ WKH"
	print "EEG & EEGGraph libs also by 220"
	
	canvas = initGraph ((screen_width, screen_height), "EDFview")
	font = initFont ()
	
	offset = 0
	
	eeg = EEG.EEG ()
	print "loading file..."
	eeg.open (initial_filename)
	eeg.consoleInfo ()

	egraph = EEGGraph.EEGGraph (screen_width, screen_height, eeg.signal_channels)
	
	active = True
	while (active):
		canvas.fill ((0, 0, 0))
		egraph.graph (canvas, eeg, offset)
		pygame.display.update ()
		
		cmd = raw_input ("cmd> ")
		if cmd.isdigit ():
			d = int (cmd)
			egraph.toggleSignal(d)

		elif cmd=="c":
			eeg.channelsInfo ()
		elif cmd=="i":
			eeg.consoleInfo ()
		elif cmd=="t":
			eeg.transducersList ()
		elif cmd=="d":
			egraph.displaysList ()


		elif cmd=="j":
			offset = 0
			print str (offset)+"/"+str (eeg.data_records)
		elif cmd=="z":
			if offset>0: offset-= 1
			print str (offset)+"/"+str (eeg.data_records)
		elif cmd=="x":
			if offset<eeg.data_records-1: offset+= 1
			print str (offset)+"/"+str (eeg.data_records)
			
		elif cmd=="a":
			if offset>0: offset-= 10
			print str (offset)+"/"+str (eeg.data_records)
		elif cmd=="s":
			if offset<eeg.data_records-10: offset+= 10
			print str (offset)+"/"+str (eeg.data_records)
			
		elif cmd=="q":
			if offset>0: offset-= 100
			print str (offset)+"/"+str (eeg.data_records)
		elif cmd=="w":
			if offset<eeg.data_records-100: offset+= 100
			print str (offset)+"/"+str (eeg.data_records)
			
		elif cmd=="Q":
			active = False
		elif cmd=="h":
			print "[c] EEG info  [s] signal channels  [t] transducers list  [d] displays list"
			print "[z/x] prev/next  [a/s] (prev/next)*10   [q/w] (prev/next)*100 [j] jump to top"
			print "[Q] quit"

	
	pygame.font.quit ()
	pygame.quit ();
	return 0

if __name__ == '__main__':
	main()

