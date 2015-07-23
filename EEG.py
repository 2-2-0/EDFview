#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  EEG.py
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

import struct

# talking about the brain...
class Channel ():
	label = ""
	transducer = ""
	physical_dimension = ""
	physical_minimum = 0
	physical_maximum = 0
	digital_minimum = 0
	digital_maximum = 0
	
	pre_filtering = ""
	samples_per_record = 0
	reserved = ""


# your mind is your most important asset
class EEG ():
	header_format = ('@8s80s80s8s8s8s44s8s8s4s')
	header_length = struct.calcsize (header_format)

	data = []
	records = []
	channels = []
	
	patient_id = ""
	recording_id = ""
	start_date = ""
	start_time = ""
	
	reserved = ""
	
	header_bytes = 0
	data_records = -1
	data_duration = 0
	signal_channels = 0
	
	samples_per_record = 0
	digital_minimum = 0
	digital_maximum = 0
	
	# open your mind, there's much to be understood about it
	def open (self, filename):
		## FILE STREAM
		fstream = open (filename, 'rb')
		
		## HEADER
		data = struct.unpack (self.header_format, fstream.read (self.header_length))
		# basic info
		self.patient_id = data [1].rstrip ()
		self.recording_id = data [2].rstrip ()
		self.start_date = data [3]
		self.start_time = data [4]
		
		self.header_bytes = int (data [5])
		self.reserved = data[6]
		self.data_records = int (data [7])
		self.data_duration = int (data [8])
		self.signal_channels = int (data [9])
		
		#channels info
		self.channels = []
		for i in xrange (self.signal_channels):
			c = Channel ()
			self.channels.append (c)
			
		for i in xrange (self.signal_channels):
			self.channels [i].label = fstream.read (16).rstrip ()
			
		for i in xrange (self.signal_channels):
			self.channels [i].transducer = fstream.read (80).rstrip ()
			
		for i in xrange (self.signal_channels):
			self.channels [i].physical_dimension = fstream.read (8)
			
		for i in xrange (self.signal_channels):
			self.channels [i].physical_minimum = int (fstream.read (8))
			
		for i in xrange (self.signal_channels):
			self.channels [i].physical_maximum = int (fstream.read (8))
			
		for i in xrange (self.signal_channels):
			self.channels [i].digital_minimum = int (fstream.read (8))
			
		for i in xrange (self.signal_channels):
			self.channels [i].digital_maximum = int (fstream.read (8))
			
		for i in xrange (self.signal_channels):
			self.channels [i].pre_filtering = fstream.read (80).rstrip ()
			
		for i in xrange (self.signal_channels):
			self.channels [i].samples_per_record = int (fstream.read (8))
			
		for i in xrange (self.signal_channels):
			self.channels [i].reserved = fstream.read (32).rstrip ()

	
		# read records
		self.samples_per_record = int (self.channels [0].samples_per_record)
		self.digital_maximum = int (self.channels [0].digital_maximum)
		self.digital_minimum = int (self.channels [0].digital_minimum)
		
		total_count = 0
		
		self.records = []

		# give it some time...
		for h in xrange (self.data_records):
			signals = []
			for i in xrange (self.signal_channels):
				#print "Signal: "+str (i)
				
				samples = []
				for j in xrange (self.samples_per_record):
					y = int (struct.unpack ('@H', fstream.read (2)) [0])
					samples.append (y)
					total_count+= 1

				signals.append (samples)
			self.records.append (signals)
			#print h

		print "Total samples: "+str (total_count)
		fstream.close ()
			
		return 0

	# no use of having a brain if you don't use it...
	def consoleInfo (self):
		print "[EEG basic info]"
		print "Patient id: "+self.patient_id
		print "Recording id: "+self.recording_id
		print "Start date: "+self.start_date
		print "Start time: "+self.start_time
		
		print "Header bytes: "+str (self.header_bytes)
		print "Data records: "+str (self.data_records)
		print "Data duration: "+str (self.data_duration)
		print "Signal channels: "+str (self.signal_channels)
	
	def channelsInfo (self):
		for i in xrange (self.signal_channels):
			self.channelInfo (i)
			print 
	
	def channelInfo (self, channel_index):
		channel = self.channels [channel_index]
		print str (channel_index)+" "+channel.label+"\t"+channel.transducer \
		+" "+channel.physical_dimension+":"+str (channel.physical_minimum)+"/" \
		+str (channel.physical_maximum)+"  "+str (channel.digital_minimum)+"/" \
		+str (channel.digital_maximum)+" |  "+str (channel.samples_per_record)
			
	def channelDetailInfo (self, channel_index):
		channel = self.channels [channel_index]
		print "[Channel "+str (channel_index)+" info]"
		print "Label: "+channel.label
		print "Transducer: "+channel.transducer
		print "Physical dimension: "+channel.physical_dimension
		print "Physical minimum: "+channel.physical_minimum
		print "Physical maximum: "+channel.physical_maximum
		print "Digital minimum: "+channel.digital_minimum
		print "Digital maximum: "+channel.digital_maximum
		print "Pre-filtering: "+channel.pre_filtering
		print "Samples per record: "+channel.samples_per_record
		
	def electrodesList (self):
		for channel in self.channels:
			print channel.label
