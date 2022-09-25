#! /usr/bin/env python
"""
ulpack
"""
import sys
import socket
import traceback
import logging

class ULPacketFormatError(Exception):
    """ULPacketFormatError"""
    pass
class ULPackageFormatError(Exception):
    """ULPackageFormatError"""
    pass
class ULPackagePrefixFormatError(ULPackageFormatError):
    """ULPackagePrefixFormatError"""
    pass
class ULPackageSuffixFormatError(ULPackageFormatError):
    """ULPackageSuffixFormatError"""
    pass
class ULPacketHeadFormatError(ULPacketFormatError):
    """ULPacketHeadFormatError"""
    pass
class ULPacketBodyFormatError(ULPacketFormatError):
    """ULPacketBodyFormatError"""
    pass

class ULPacket(object):
    """
        A class of one ul_pack, providing functionalities: parsing from and saving to an 
        string object,enumerating fields, accessing field value according to field name, etc.
        """
    def __init__(self, head="\r\n", body=""):
        self._fields    = []
        self._dict      = {}
        self._headParse(head)
        self._bodyParse(body)

    ## The separator between a field and its value
    def getFieldValueSep(self):
        """getFieldValueSep"""
        return ' : '
    
    fieldValueSep = property(getFieldValueSep, doc="The separator between a field and its value")

    ## The separator between records
    def getRecordSep(self):
        """getRecordSep"""
        return '\r\n'
    
    recordSep = property(getRecordSep, doc="The separator between records")

    ## head part of ulpack
    def getHead(self):
        """getHead"""
        recordList = []

        for name in self._fields:
            recordList.append(name + self.fieldValueSep + self._dict[name])
        recordList.append(self.recordSep)

        return self.recordSep.join(recordList)
    
    
    def setHead(self, head):
        """setHead"""
        self._headParse(head)
    head = property(getHead, setHead, doc="The head part of an ul_pack")

    ## body part of ulpack
    def getBody(self):
        """getBody"""
        return self._body
    def setBody(self, body):
        """setBody"""
        self._bodyParse(body)
    body = property(getBody, setBody, doc="The body part of an ul_pack")

    ## field name list of ulpack
    def getFields(self):
        """getFields"""
        return self._fields[:]
    fields = property(getFields, doc="The field name list of an ul_pack")

    ## set the order of head fields in ulpack
    def setfieldorder(self, permutator):
        """setfieldorder"""
        fields = permutator(self._fields)
        assert(len(fields) == len(self._fields))
        for f in fields: assert f in self._dict

        self._fields = fields

    ## get body domains in ulpack's Body
    def getBodyDomains(self):
        """getBodyDomains"""
        ret = []
        if not 'Body' in self._dict:return ret
        parts = self._dict['Body'].split('+')
        for part in parts:
            key = ''
            value = 0
            for c in part:
                if c >= '0' and c <= '9':
                    value = value * 10 + ord(c)-ord('0')
                else:
                    key += c
            ret.append((key, value))
        return ret

    def getDomain(self, domain):
        """getDomain"""
        domains = self.getBodyDomains()
        offset = 0
        for name, length in domains:
            if name == domain: return self.body[offset:offset + length]
            offset += length
        return None

    ## a helper function to parse head
    def _headParse(self, head):
        records = head.split(self.recordSep)
        if len(records) < 2 or records[-1] != '' or records[-2] != '':
            raise ULPacketHeadFormatError
        del records[-2:]

        self._fields    = []
        self._dict      = {}
        for rec in records:
            try:
                (field, value) = rec.split(self.fieldValueSep, 1)
            except ValueError:
                raise ULPacketHeadFormatError
            else:
                self._fields.append(field)
                self._dict[field] = value

    ## a helper function to parser body
    def _bodyParse(self, body):
        self._body = body

    ## judge a head field exist or not
    def __contains__(self, field):
        return field in self._dict

    ## get a head field
    def __getitem__(self, field):
        return self._dict[field]

    ## set a head field
    def __setitem__(self, field, value):
        if field not in self._dict:
            self._fields.append(field)
        self._dict[field] = value

    ## delete a head field
    def __delitem__(self, field):
        del self._dict[field]
        self._fields = [f for f in self._fields if f != field]

    ## enumerate all head fields
    def __iter__(self):
        return self._dict.__iter__()

    def __eq__(self, other):
        if not isinstance(other, ULPacket):
            return False
        if self._dict != other._dict or self.body != other.body:
            return False
        return True

    ## serialize ulpack to a string
    def __repr__(self):
        headSize = len(self.head)
        bodySize = len(self.body)
        dummy    = ULPackage()
        prefix = ' '.join([dummy.startFlag, str(headSize), str(bodySize)])
        padding = dummy.prefixLen - len(prefix)
        if padding > 0:# padding with '@'s
            prefix = prefix + ' ' + dummy.paddingByte * (padding - 1)
            prefixChars = list(prefix)
            prefixChars[-1] = '\0'
            prefix = ''.join(prefixChars)

        return prefix + self.head + self.body + dummy.endFlag

    def stdout(self):
        """stdout"""
        sys.stdout.write(self.__repr__())

class ULPackage(object):
    """
        A class for parsing ULPacket from a file-like object.
        """
    ## The length of prefix before an ul_pack
    def getPrefixLen(self):
        """getPrefixLen"""
        return 20
    prefixLen = property(getPrefixLen, doc="The length of prefix before an ul_pack")

    ## The padding byte used in prefix
    def getPaddingByte(self):
        """getPaddingByte"""
        return '@'
    paddingByte = property(getPaddingByte, doc="The padding byte used in prefix")

    ## The start flag before a pack
    def getStartFlag(self):
        """getStartFlag"""
        return '~BUF!'
    startFlag = property(getStartFlag, doc="The start flag before a pack")

    ## The end flag after a pack
    def getEndFlag(self):
        """getEndFlag"""
        return '~EOF!'
    endFlag  = property(getEndFlag, doc="The end flag after a pack")

    ## A helper function to parse prefix part of ulpack
    def _prefixFormatCheck(self, prefix):
        prefixList = prefix.split(' ')
        if len(prefixList) not in range(3, 5): raise ULPackagePrefixFormatError
        if prefixList[0] != self.startFlag:   raise ULPackagePrefixFormatError
#                if len(prefixList) == 4 and prefixList[3] != '@'*len(prefixList[3]):
#                        raise ULPackagePrefixFormatError
        headSize, bodySize = tuple(map(int, prefix.split(' ')[1:3]))
        if headSize < 0 or bodySize < 0: raise ULPackagePrefixFormatError

    ## A helper function to parse suffix part of ulpack
    def _suffixFormatCheck(self, suffix):
        if suffix != self.endFlag: raise ULPackageSuffixFormatError

    ## constructor
    def __init__(self, file=None):
        """constructor"""
        self.count = None
        ULPackage.parse(self, file)

    ## parse method
    def parse(self, file):
        """parse"""
        if hasattr(self, "file") and self.file != file:
            self.count = None
        self.file = file

    ## read next ulpack from file-like object
    def next(self):
        """next"""
        if self.file is None:
            return None
        prefix = self.file.read(self.prefixLen)
        if len(prefix) == 0:
            return None
        prefix = prefix.rstrip('\0')
        self._prefixFormatCheck(prefix)

        headSize, bodySize = tuple(map(int, prefix.split(' ')[1:3]))
        headStr = self.file.read(headSize)
        bodyStr = self.file.read(bodySize)

        suffix = self.file.read(len(self.endFlag))
        self._suffixFormatCheck(suffix)

        return ULPacket(headStr, bodyStr)

    ## iterate all ulpack from file-like object
    def __iter__(self):
        while True:
            packet = self.next()
            if packet is None:
                break
            yield packet

    def reset(self):
        """reset"""
        curpos = None
        if self.file:
            curpos = self.file.tell()
            # self.file.seek(0, 0L)
        return curpos

    ## length of ulpackage
    # @return - return number of ulpack in package
    def __len__(self):
        if self.count:
            return self.count
        count = 0
        while True:
            next = self.next()
            if next is None:break
            count += 1
        self.reset()
        self.count = count
        return count

class ULPack(object):
    'send ulpack'
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.is_connected = False
        self.connect()

    def connect(self):
        """connect"""
        try:
            self.sock = socket.create_connection((self.ip, self.port))
            self.is_connected = True
        except:
            logging.error(traceback.format_exc())
            pass

    def send(self, packet):
        """send"""
        for i in range(1, 2):
            if self.is_connected == False:
                self.connect()
            try:
                sent = self.sock.send(str(packet))
                if sent == 0:
                    logging.warning("send packet info " + str(i) + " times failed " + str(packet))
                    self.close()
                    continue
                return True
                '''package = ULPackage()
                package.parse(self.sock.makefile())
                #print package
                if package.next()['Response'].upper() == 'OK': 
                    #print "login fifo successfully."
                    return True'''
            except:
                logging.error("send fifo error retry[%d] err[%s]" % (i, traceback.format_exc()))
                self.close()
        return False	
	
    def close(self):
        """close"""
        try:
            self.is_connected = False
            self.sock.shutdown(socket.SHUT_WR)
            self.sock.close()
            self.sock = None
        except:
            logging.error(traceback.format_exc())



def dict_to_ulpack(d):
    """dict_to_ulpack"""
    def inner_dict_to_ulpack(dic, ulpacket, parent_name):
        """inner_dict_to_ulpack"""
        for key, value in dic.iteritems():
            if type(value) == dict:
                #use '_' to connect the child name with the parent level
                inner_dict_to_ulpack(value, ulpacket, parent_name + key + '_')
            else:
                ulpacket[parent_name + key] = str(value)
    packet = ULPacket()
    inner_dict_to_ulpack(d, packet, '')
    return packet

# if __name__ == '__main__':

#     packet = ULPacket()

#     packet["Url"] = "www.baidu.com/"

#     packet.body = "abcdefg"
#     packet.head = "Url : www.google.com/\r\nIntime : 32000000\r\n\r\n"

#     packet2 = ULPacket()
#     packet2["Url"] = "www.google.com/"
#     packet2["Intime"] = "32000000"
#     packet2.body = 'abcdefg'
#     print('packet==packet2 is ', packet == packet2)

#     packet.setfieldorder(sorted)
#     for field in packet:
#        print(packet[field])

#     if len(sys.argv) != 3:
#         sys.exit(0)

#     inpack          = open(sys.argv[1], 'r')
#     package         = ULPackage()
#     package.parse(inpack)
#     for packet in package:
#        print(packet["Url"])

#     inpack.close()
#     inpack          = open(sys.argv[1], 'r')
#     outpack         = open(sys.argv[2], 'w')
#     i = 0
#     for packet in ULPackage(inpack):
#         packet["Url"] = str(i)
#         i += 1
#         outpack.write("packet")
