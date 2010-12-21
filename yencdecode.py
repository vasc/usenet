#!/usr/bin/python
import yenc
import re
import uuid
import os
import tempfile

def find_values(keys, string):
    results = {}
    for k in keys:
        m = re.search('k'+r'=([^\s\n\r]*)')
        results[k] = m.group(0)
    return results

def decode_from_lines(lines):
    info = {}
    if re.match('=ybegin ', lines[0]):
        m = re.match('name=([^\s]*)', lines[0])
        if m: info['filename'] = m.group(1)
        info['uuid'] = uuid.uuid4().hex
        m = re.match('part=(\d*)', lines[0])
        if m: info['part'] = int(m.group(1))
        m = re.match('total=(\d*)', lines[0])
        if m: info['total'] = int(m.group(1))
    else: raise Exception("First line must be start with '=ybegin ' (%s)" % lines[0])
    if re.match('=yend', lines[-1]):
        m = re.match('crc32=([^\s]*)', lines[-1])
        if m: info['crc32'] = m.group(1)
    if re.match("=ypart ", lines[1]):
        data = lines[2:-1]
    else: data = lines[1:-1]
    #fenc = open(info['uuid']+'.yenc', "w")
    data = '\n'.join(data)
    #fenc.write(data)
    #fenc.close()
    file_encoded = tempfile.NamedTemporaryFile(delete=False)
    file_encoded.write(data)
    file_encoded.close()

    file_decoded = tempfile.NamedTemporaryFile(delete=False)
    file_decoded.close()

    yenc.decode(str(file_encoded.name), str(file_decoded.name))

    info['data'] = open(file_decoded.name, 'r').read()
    file_decoded.close()

    #info['tmpfilename'] = info['uuid'] + '.tmp'
    #yenc.decode(info['uuid']+'.yenc', info['tmpfilename'])
    #os.remove(info['uuid']+'.yenc')
    return info

