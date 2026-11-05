"""Exercise the production ICO packer with a separate PNG reader and Windows consumer."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import zlib
import binascii
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('independent_ico_reader',ROOT/'tests/helpers/ico_reader.py')
reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)

def chunk(kind,value):return struct.pack('>I',len(value))+kind+value+struct.pack('>I',binascii.crc32(kind+value)&0xffffffff)
def png(size):
    rows=[]
    for y in range(size):
        row=bytearray([0])
        for x in range(size):row.extend([255,0,0,0 if x==y==0 else 255])
        rows.append(bytes(row))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',size,size,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')

class Task20IndependentFormats(unittest.TestCase):
    def test_production_encoder_exports_six_frames_read_by_independent_reader_and_windows(self):
        sizes=[16,32,48,64,128,256]
        frames=[{'size':n,'png':base64.b64encode(png(n)).decode()} for n in sizes]
        output=subprocess.check_output(['node','tests/helpers/ico_fixture.mjs'],cwd=ROOT,input=json.dumps(frames).encode(),timeout=30)
        with tempfile.TemporaryDirectory(prefix='edb-independent-ico-') as temp:
            path=Path(temp)/'packed.ico';path.write_bytes(base64.b64decode(output,validate=True));result=reader.inspect(path)
        self.assertEqual([x['width'] for x in result['frames']],sizes)
        self.assertTrue(all(x['corner_alpha']==0 and x['center']==[255,0,0,255] for x in result['frames']))
        self.assertEqual(result['native_windows_reader'],os.name=='nt')
        if os.name=='nt':self.assertEqual([x['windows_dimensions'] for x in result['frames']],[[n,n] for n in sizes])

if __name__=='__main__':unittest.main()
