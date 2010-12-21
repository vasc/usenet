
from nntplib import NNTP, NNTPDataError
import yencdecode
import zlib
import os


class NNTPExtensions(NNTP):
    def xzver(self, start, end, file=None):
        """Process an XZVER command (optional compressed "xover" alternative) Arguments:        - start: start of range
        - end: end of range
        Returns:
        - resp: server response if successful
	        - list: list of (art-nr, subject, poster, date,
	                         id, references, size, lines)"""

        resp, lines = self.longcmd('XZVER ' + start + '-' + end, file)
        if resp.startswith("224 "):
            info = yencdecode.decode_from_lines(lines)
            #encoded_data = open(info['tmpfilename'], 'r').read()
            #os.remove(info['tmpfilename'])

            encoded_data = info['data']
            decoded_lines = zlib.decompress(encoded_data, -15).splitlines()
   	        #decoded_lines = open(info['tmpfilename'], 'r').read().splitlines()
        else: decoded_lines = lines
        xover_lines = []
        for line in decoded_lines:
            elem = line.split("\t")
            try:
                xover_lines.append((elem[0],
                                    elem[1],
                                    elem[2],
                                    elem[3],
                                    elem[4],
                                    elem[5].split(),
                                    elem[6],
                                    elem[7]))
            except IndexError:
                raise NNTPDataError(line)
        return resp,xover_lines

