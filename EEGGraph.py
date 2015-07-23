#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  EEGGraph.py
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

import pygame

def rmap (x, imin, imax, omin, omax):
	return (x-imin)*(omax-omin) / (imax-imin)+omin


color_tables = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
				(255, 127, 0), (255, 0, 127), (0, 255, 127), (127, 255, 0), (0, 127, 255), (127, 0, 255),
				(255, 127, 127), (127, 255, 127), (127, 127, 255), (255, 255, 127), (255, 127, 255), (127, 255, 255),
				(255, 127, 64), (255, 64, 127), (64, 255, 127), (127, 255, 64), (64, 127, 255), (127, 64, 255),
				(255, 64, 64), (64, 255, 64), (64, 64, 255), (255, 255, 64), (255, 64, 255), (64, 255, 255),
				(255, 255, 255), 
				]


# your mind is a system, feed it proper information
class EEGGraph ():
	active_signals = []
	
	screen_width = 0
	screen_height = 0
	
	def __init__ (self, screen_width, screen_height, signal_channels):
		self.screen_width = screen_width
		self.screen_height = screen_height
		
		for i in xrange (0, signal_channels):
			self.active_signals.append ((i, True))
	
	def toggleSignal (self, signal_index):
		t = self.active_signals [signal_index]
		nt = (t [0], not t [1])
		
		print "signal "+str (signal_index)+" display now "+str (nt [1])
		self.active_signals [signal_index] = nt
		
		
	def graph (self, canvas, eeg, record_offset, stacked=False):
		columns = self.screen_width/eeg.samples_per_record
		row_height = self.screen_height
		
		for record_index in xrange (0, columns):
			if record_offset+record_index<len(eeg.records):
				record = eeg.records [record_offset+record_index]
				if record_index==0: pygame.draw.rect (canvas, (0, 8, 32), (record_index*eeg.samples_per_record, 0, eeg.samples_per_record, self.screen_height))
				self.graphRecord (canvas, record, eeg.digital_minimum, eeg.digital_maximum, record_index*eeg.samples_per_record, stacked)
			
		return canvas
	
	# your brain will speak to you using whatever you feed it... be nice
	def graphRecord (self, canvas, record, dmin, dmax, offset_x, stacked=False):
		visible_rows = 0
		for signal in self.active_signals:
			if signal [1]==True: visible_rows+= 1
		
		if stacked==True:
			row_height = self.screen_height/visible_rows
		else:
			row_height = self.screen_height
		
		color_index = 0		
		pygame.draw.line (canvas, (0, 127, 255), (offset_x, 0), (offset_x, self.screen_height))
		
		row = 0
		signal_index = 0
		for signal in record:
			active_signal = self.active_signals [signal_index]
			signal_index+= 1
			
			l = len (color_tables)-1
			c = color_tables [color_index % l]
			color_index+= 1
			
			if active_signal[1]==True:
				x = offset_x
				lastx = 0
				lasty = 0

				for sample in signal:
					y = rmap (sample, dmin, dmax, 0, row_height)
					if stacked==True:
						y+= row*row_height
					
					if (lastx == 0): lastx = x
					if (lasty == 0): lasty = y
					pygame.draw.line (canvas, c, (lastx, lasty), (x, y))
					
					lastx = x
					lasty = y
					x+= 1
				row+= 1

	def displaysList (self):
		for item in self.active_signals:
			print item
			
# no need to get sentimental, here... end of code
