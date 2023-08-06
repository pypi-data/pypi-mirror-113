#
# Copyright (c) 2020, Hyve Design Solutions Corporation.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are 
# met:
#
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in the 
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of Hyve Design Solutions Corporation nor the names 
#    of its contributors may be used to endorse or promote products 
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY HYVE DESIGN SOLUTIONS CORPORATION AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, 
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
# HYVE DESIGN SOLUTIONS CORPORATION OR CONTRIBUTORS BE LIABLE FOR ANY 
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS 
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
import os, struct
from .. mesg.ipmi_app import GetDeviceID
from .. mesg.ipmi_storage import GetFruAreaInfo, ReadFru, WriteFru
from .. util import checksum
from .. util.exception import PyCmdsExcept, PyCmdsArgsExcept
from . _consts import TupleExt, CHASSIS_TYPES
from . _common import do_command, get_sdr_repo, str2int, conv_time

FRU_BUF_SIZE = 32
AREA_NAMES = {'c': 'Chassis', 'b': 'Board', 'p': 'Product'}

def _fru_get_common(self, fru_id, area_size):
    if area_size < 8:
        raise PyCmdsExcept('FRU size is too small to have a common header.', -1)

    data = self.intf.issue_cmd(ReadFru, fru_id, 0, 8)
    if data[0] != 8:  
        raise PyCmdsExcept('Failed to get FRU common header.', -1)

    data = data[1:]

    hdr = struct.unpack('B' * 8, data)
    offset_c = hdr[2]
    offset_b = hdr[3]
    offset_p = hdr[4]
    
    return (offset_c, offset_b, offset_p)

def _fru_get_area(self, fru_id, offset, area_size, area_name):
    if area_size < offset * 8 + 2:
        raise PyCmdsExcept('FRU size is too small to have a {0} Info Area.'.format(area_name), -1)

    # Area Format Version, Area Length
    data = self.intf.issue_cmd(ReadFru, fru_id, offset * 8, 2)
    if data[0] != 2:  
        raise PyCmdsExcept('Failed to get {0} Info Area Length.'.format(area_name), -1)

    data = data[1:]
    area_len = data[1]

    # xx Info Area
    read_count = area_len * 8 - 2
    read_offset = offset * 8 + 2    
    ret = b''

    if area_size < read_offset + read_count:
        raise PyCmdsExcept('FRU size is too small to have a {0} Info Area.'.format(area_name), -1)

    while read_count > 0:
        if read_count > 255:
            read_size = 255
        else:
            read_size = read_count

        data = self.intf.issue_cmd(ReadFru, fru_id, read_offset, read_size)
        read_offset += data[0]
        read_count -= data[0]
        ret += data[1:]

    return ret

def _fru_get_field(data, idx):
    field_len = data[idx] & 0x3f
    field_end = idx+field_len+1
    if field_len == 0 or field_end >= len(data):
        return (0, b'') 
    field = data[idx+1:field_end]
    return (field_len, field)

def _fru_print_chassis_type(self, title, chs_type):
    self.print('  {0:24}: {1}'.format(title, CHASSIS_TYPES.get(chs_type, chs_type)))

def _fru_print_field(self, title, field):
    self.print('  {0:24}: {1}'.format(title, field.decode('latin_1')))

def _fru_print_all_fields(self, data, area_name, titles, idx_s):
    idx = idx_s
    count = 1
    start = data[idx]
    while start != 0xc1:
        field_len, field = _fru_get_field(data, idx)

        if field_len > 0:
            _fru_print_field(self, area_name + ' ' + titles.get(count, 'Extra'), field)

        idx += field_len + 1
        count += 1
        if idx >= len(data): return
        start = data[idx]

def _fru_print_chassis(self, fru_id, offset, area_size):
    area_name = AREA_NAMES['c']

    # Retrieve the Chassis Info Area
    data = _fru_get_area(self, fru_id, offset, area_size, area_name)    

    titles = TupleExt(('Type', 'Part Number', 'Serial Number'))
    # Print Chassis Type
    chs_type = data[0]
    _fru_print_chassis_type(self, area_name + ' ' + titles[0], chs_type)

    # Print other fields
    _fru_print_all_fields(self, data, area_name, titles, 1)

def _fru_print_board_time(self, title, mfg_time):
    t1 = struct.unpack('B' * 3, mfg_time)
    mtime = (((t1[2] << 8) + t1[1]) << 8) + t1[0]
    ts = mtime * 60 + 820454400
    self.print('  {0:24}: {1}'.format(title, conv_time(ts)))

def _fru_print_board(self, fru_id, offset, area_size):
    area_name = AREA_NAMES['b']

    # Retrieve the Board Info Area
    data = _fru_get_area(self, fru_id, offset, area_size, area_name)    

    titles = TupleExt(('Mfg. Time', 'Manufacturer', 'Product Name', 'Serial Number',
                       'Part Number', 'FRU File ID',))

    # Print Mfg. Date / Time
    mfg_time = data[1:4]
    _fru_print_board_time(self, area_name + ' ' + titles[0], mfg_time)

    # Print other fields
    _fru_print_all_fields(self, data, area_name, titles, 4)

def _fru_print_product(self, fru_id, offset, area_size):
    area_name = AREA_NAMES['p']

    # Retrieve the Board Info Area
    data = _fru_get_area(self, fru_id, offset, area_size, area_name)    

    titles = TupleExt(('none', 'Manufacturer', 'Name', 'Part Number', 'Version',
                       'Serial Number', 'Asset Tag', 'FRU File ID',))

    # Print product fields
    _fru_print_all_fields(self, data, area_name, titles, 1)

def _fru_print_one(self, fru_id, area_size):
    offset_c, offset_b, offset_p = _fru_get_common(self, fru_id, area_size)
    if offset_c != 0:  _fru_print_chassis(self, fru_id, offset_c, area_size)
    if offset_b != 0:  _fru_print_board(self, fru_id, offset_b, area_size)
    if offset_p != 0:  _fru_print_product(self, fru_id, offset_p, area_size)

def _fru_print(self, argv):
    title = 'FRU Device Description'
    req_id = -1
    if len(argv) > 1:
        req_id = str2int(argv[1])

    # Print BMC FRU
    if req_id < 1:
        t1 = self.intf.issue_cmd(GetDeviceID)
        if t1[5] & 8:  
            # BMC has FRU device
            area_size, _ = self.intf.issue_cmd(GetFruAreaInfo, 0)
            if area_size == 0:  
                raise PyCmdsExcept('The area size of the FRU device with ID 0 is zero.', -1)
            self.print('{0:26}: {1}'.format(title, 'Builtin FRU Device (ID 0)'))
            _fru_print_one(self, 0, area_size)
            self.print()
        else:
            self.print('BMC does not have a FRU device.')

    # Print FRUs of other devices
    if req_id == 0:  return
    sdr_repo = get_sdr_repo(self)

    flag = False
    for sdr1 in sdr_repo[0x11]:
        fru_id = sdr1[1]
        if (fru_id == 0) or (req_id != -1 and req_id != fru_id):  continue
        if sdr1[2] & 0x80 == 0:  continue

        area_size, _ = self.intf.issue_cmd(GetFruAreaInfo, fru_id)
        if area_size == 0:  
            self.print('The area size of the FRU device with ID {0} is zero.'.format(fru_id))
            continue

        fru_name = sdr1[11:].decode('latin_1')
        self.print('{0:26}: {1} (ID {2})'.format(title, fru_name, fru_id))

        # Logical FRU
        _fru_print_one(self, fru_id, area_size)
        self.print()
        flag = True

    if not flag and req_id != -1:
        self.print('Cannot find FRU ID {0} from SDR.'.format(req_id))

def _fru_read(self, fru_id, fru_file, area_size):
    offset = 0
    with open(fru_file, 'wb') as out_file:
        while offset < area_size:
            data = self.intf.issue_cmd(ReadFru, fru_id, offset, FRU_BUF_SIZE)
            count = data[0]
            out_file.write(data[1:])
            offset += count        

    self.print('Done')

def _fru_write(self, fru_id, fru_file, area_size):
    file_size = os.stat(fru_file).st_size
    if area_size < file_size:
        raise PyCmdsExcept('ERROR: The input file size {0} is bigger than the target FRU area size {1}.'
                            .format(file_size, area_size), -1)

    self.print('Size to Write    : {0} bytes'.format(file_size))

    offset = 0
    with open(fru_file, 'rb') as in_file:
        while offset < area_size:
            chunk = in_file.read(FRU_BUF_SIZE)
            if not chunk:  break
            count, = self.intf.issue_cmd(WriteFru, fru_id, offset, chunk)
            offset += count

def _fru_read_write(self, argv):
    if len(argv) < 3:
        raise PyCmdsArgsExcept(1)

    fru_file = argv[2]
    fru_id = str2int(argv[1])
    if fru_id == -1:
        raise PyCmdsArgsExcept(3, 0, argv[1])

    area_size, _ = self.intf.issue_cmd(GetFruAreaInfo, fru_id)
    if area_size == 0:  
        raise PyCmdsExcept('The area size of the FRU device with ID {0} is zero.'.format(fru_id), -1)
    
    # print fru size
    self.print('Fru Size         : {0} bytes'.format(area_size))

    if argv[0] == 'write':
        _fru_write(self, fru_id, fru_file, area_size)
    else:
        _fru_read(self, fru_id, fru_file, area_size)

def _fru_edit_imp(self, fru_id, area_size, sec, sec_idx, sec_str):
    # get the offset of the area
    offset_c, offset_b, offset_p = _fru_get_common(self, fru_id, area_size)
    if ((sec == 'c' and offset_c == 0) or (sec == 'b' and offset_b == 0) 
        or (sec == 'p' and offset_p == 0)):
        raise PyCmdsExcept(
            'ERROR: the offset of area {0} is zero in the Common Header.'.format(
             AREA_NAMES[sec]))

    if sec == 'c': 
        offset = offset_c
        start_offset = 1
    elif sec == 'b': 
        offset = offset_b
        start_offset = 4
    elif sec == 'p': 
        offset = offset_p
        start_offset = 1
    
    # retrive the data of the area
    data = _fru_get_area(self, fru_id, offset, area_size, AREA_NAMES[sec]) 

    # seek the field to be edited
    curr_idx = 0
    get_field_len = lambda data, idx: data[idx] & 0x3f
    field_len = get_field_len(data, start_offset)
    while curr_idx < sec_idx:
        start_offset += field_len + 1
        if data[start_offset] == 0xc1:
            raise PyCmdsExcept('The index: {0} is out of range in the {1} Info Area.'.format(
                               sec_idx, AREA_NAMES[sec]), -1)

        field_len = get_field_len(data, start_offset)
        curr_idx += 1

    if len(sec_str) == field_len:
        # the length of the value doesn't change
        data_new = (data[:start_offset+1] + sec_str.encode('latin_1') 
                    + data[start_offset+1+field_len:-1])
    elif len(sec_str) < field_len:
        # the length of the value becomes shorter
        diff = field_len - len(sec_str)
        type_len = data[start_offset] - diff 
        data_new = (data[:start_offset] 
                    + type_len.to_bytes(1, byteorder='little') 
                    + sec_str.encode('latin_1')
                    + data[start_offset+1+field_len:-1]) 
        # padding
        data_new += b'\x00' * diff
    else:
        # the length of the value becomes longer
        # this needs to check the total length
        diff = len(sec_str) - field_len
        unused = len(data) - data.rfind(b'\xc1') - 2

        if diff > unused or len(sec_str) > 63:
            raise PyCmdsExcept('ERROR: Input string {0} is too long.'.sec_str)
        type_len = data[start_offset] + diff 
        data_new = (data[:start_offset] 
                    + type_len.to_bytes(1, byteorder='little') 
                    + sec_str.encode('latin_1')
                    + data[start_offset+1+field_len:-1-diff]) 

    # adding the first two bytes
    area_len = int((len(data_new) + 3) / 8)
    data_new = b'\x01' + area_len.to_bytes(1, byteorder='little') + data_new

    # calculate checksum
    data_new += checksum(data_new)

    # write fru
    total_bytes = len(data_new) 
    offset *= 8
    while total_bytes > 0:
        if total_bytes >= FRU_BUF_SIZE:
            to_write = FRU_BUF_SIZE
        else:
            to_write = total_bytes

        count, = self.intf.issue_cmd(WriteFru, fru_id, offset, data_new[:to_write])
        total_bytes -= to_write
        if not total_bytes: break
        offset += count 
        data_new = data_new[to_write:]

def _fru_edit(self, argv):
    #edit <fru id> field <section> <index> <string>
    if len(argv) < 6:
        raise PyCmdsArgsExcept(1)

    fru_id = str2int(argv[1])
    if fru_id == -1:
        raise PyCmdsArgsExcept(3, 0, argv[1])

    area_size, _ = self.intf.issue_cmd(GetFruAreaInfo, fru_id)
    if area_size == 0:  
        raise PyCmdsExcept('The area size of the FRU device with ID {0} is zero.'.format(fru_id), -1)

    if argv[2] != 'field':
        raise PyCmdsArgsExcept(3, 0, argv[2])

    sec = argv[3]
    if sec not in ('c', 'b', 'p'):        
        raise PyCmdsArgsExcept(2, 0, sec)

    sec_idx = str2int(argv[4])
    if sec_idx == -1:
        raise PyCmdsArgsExcept(3, 0, argv[4])

    sec_str = argv[5]
    
    _fru_edit_imp(self, fru_id, area_size, sec, sec_idx, sec_str)

def help_fru(self, argv=None, context=0):
    self.print('FRU Commands:')
    self.print('    print   [<fru_id>]')
    self.print('    read    <fru id> <file name>')
    self.print('    write   <fru id> <file name>')
    self.print('    edit <fru id> field <section(c,b,p)> <index> <string>')
    self.print('    help')

FRU_CMDS = {
    'print': _fru_print,
    'read': _fru_read_write,
    'write': _fru_read_write,
    'edit': _fru_edit,
    'help': help_fru, 
}

def do_fru(self, argv):
    do_command(self, argv, help_fru, FRU_CMDS)
