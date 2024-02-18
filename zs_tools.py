import zstandard
import struct
import yaml
import oead


def zs_compress(data):
	return zstandard.compress(data, level=10)


def zs_decompress(data):
	return zstandard.decompress(data)



class SARC:
	def __init__(self, data: bytes):
		self.reader = oead.Sarc(zs_decompress(data))
		self.writer = oead.SarcWriter.from_sarc(self.reader)
		oead.SarcWriter.set_endianness(self.writer, oead.Endianness.Little) # Switch uses Little Endian
	
	
	def repack(self):
		return zs_compress(self.writer.write()[1])



class BYAML:
	def __init__(self, data, compressed=False):
		self.compressed = compressed
		if self.compressed:
			data = oead.Bytes(zs_decompress(data))
		
		data[0x2:0x4] = (4).to_bytes(2, 'little')
		self.info = oead.byml.from_binary(data)


	def repack(self):
		data = oead.byml.to_binary(self.info, False, 4) # BYAML version 4 is the highest this library supports, but still works

		if self.compressed:
			data = zs_compress(data)
		
		return data
