"""Independent test-only ICO/PNG reader; Windows additionally uses the OS icon loader."""
import binascii
import ctypes
import json
import os
from pathlib import Path
import struct
import sys
import zlib

def png_pixels(data):
    assert data[:8]==b'\x89PNG\r\n\x1a\n'
    offset=8;compressed=[];width=height=None;ended=False
    while offset<len(data):
        length=struct.unpack_from('>I',data,offset)[0];kind=data[offset+4:offset+8];payload=data[offset+8:offset+8+length]
        assert offset+12+length<=len(data)
        assert binascii.crc32(kind+payload)&0xffffffff==struct.unpack_from('>I',data,offset+8+length)[0]
        if kind==b'IHDR':
            width,height,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',payload)
            assert width==height and width in [16,32,48,64,128,256]
            assert (depth,color,compression,filtering,interlace)==(8,6,0,0,0)
        elif kind==b'IDAT':compressed.append(payload)
        elif kind==b'IEND':
            assert not payload and offset+12==len(data);ended=True;break
        offset+=12+length
    assert ended and compressed and width
    expected=(width*4+1)*height;decoder=zlib.decompressobj();raw=decoder.decompress(b''.join(compressed),expected+1)
    assert len(raw)==expected and decoder.eof and not decoder.unconsumed_tail
    rows=[];stride=width*4
    def paeth(a,b,c):
        p=a+b-c;dist=[abs(p-a),abs(p-b),abs(p-c)];return [a,b,c][dist.index(min(dist))]
    for y in range(height):
        flag=raw[y*(stride+1)];assert flag<=4
        row=bytearray(raw[y*(stride+1)+1:(y+1)*(stride+1)]);up=rows[-1] if rows else bytes(stride)
        for x in range(stride):
            left=row[x-4] if x>=4 else 0;above=up[x];corner=up[x-4] if x>=4 else 0
            predictor=[0,left,above,(left+above)//2,paeth(left,above,corner)][flag]
            row[x]=(row[x]+predictor)&255
        rows.append(row)
    center=rows[height//2][(width//2)*4:(width//2)*4+4]
    return {'width':width,'height':height,'corner_alpha':rows[0][3],'center':list(center)}

def native_dimensions(path,size):
    from ctypes import wintypes as w
    user=ctypes.WinDLL('user32',use_last_error=True);gdi=ctypes.WinDLL('gdi32',use_last_error=True)
    class ICONINFO(ctypes.Structure):_fields_=[('fIcon',w.BOOL),('xHotspot',w.DWORD),('yHotspot',w.DWORD),('hbmMask',w.HANDLE),('hbmColor',w.HANDLE)]
    class BITMAP(ctypes.Structure):_fields_=[('bmType',w.LONG),('bmWidth',w.LONG),('bmHeight',w.LONG),('bmWidthBytes',w.LONG),('bmPlanes',w.WORD),('bmBitsPixel',w.WORD),('bmBits',ctypes.c_void_p)]
    user.LoadImageW.argtypes=[w.HINSTANCE,w.LPCWSTR,w.UINT,ctypes.c_int,ctypes.c_int,w.UINT];user.LoadImageW.restype=w.HANDLE
    user.GetIconInfo.argtypes=[w.HANDLE,ctypes.POINTER(ICONINFO)];user.GetIconInfo.restype=w.BOOL
    user.DestroyIcon.argtypes=[w.HANDLE];user.DestroyIcon.restype=w.BOOL
    gdi.GetObjectW.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p];gdi.GetObjectW.restype=ctypes.c_int
    gdi.DeleteObject.argtypes=[w.HANDLE];gdi.DeleteObject.restype=w.BOOL
    icon=user.LoadImageW(None,str(Path(path).resolve()),1,size,size,0x10)
    assert icon,'Windows independently rejected the ICO file'
    info=ICONINFO()
    try:
        assert user.GetIconInfo(icon,ctypes.byref(info));bitmap=BITMAP();assert gdi.GetObjectW(info.hbmColor or info.hbmMask,ctypes.sizeof(bitmap),ctypes.byref(bitmap))
        result=[bitmap.bmWidth,bitmap.bmHeight if info.hbmColor else bitmap.bmHeight//2]
        assert result==[size,size];return result
    finally:
        if info.hbmMask:gdi.DeleteObject(info.hbmMask)
        if info.hbmColor:gdi.DeleteObject(info.hbmColor)
        user.DestroyIcon(icon)

def inspect(path):
    data=Path(path).read_bytes();assert 6<len(data)<=1048576
    reserved,kind,count=struct.unpack_from('<HHH',data);assert (reserved,kind)==(0,1) and 1<=count<=6
    frames=[];ranges=[];seen=set()
    for i in range(count):
        width,height,colors,reserved,planes,depth,length,offset=struct.unpack_from('<BBBBHHII',data,6+16*i)
        width=width or 256;height=height or 256
        assert width==height and width not in seen;seen.add(width)
        assert (colors,reserved,planes,depth)==(0,0,1,32)
        assert offset>=6+16*count and offset+length<=len(data)
        assert not any(offset<b and offset+length>a for a,b in ranges);ranges.append((offset,offset+length))
        decoded=png_pixels(data[offset:offset+length]);assert decoded['width']==width
        if os.name=='nt':decoded['windows_dimensions']=native_dimensions(path,width)
        frames.append(decoded)
    return {'frames':frames,'bytes':len(data),'native_windows_reader':os.name=='nt','reader':'Independent stdlib ICO directory/PNG CRC/zlib/filter reader; Windows LoadImageW/GetIconInfo when on Windows.'}

if __name__=='__main__':print(json.dumps(inspect(sys.argv[1])))
