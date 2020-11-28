import cv2
import numpy as np
#from matplotlib import pyplot as plt
import socket
import sys
import binascii
import struct
import time
#from PIL import Image


def bufferToMat(length, imagebuffer):
    if length == 200*150*2:
        #print('bufferToMat found mosaic data')
        #vis = np.zeros((150, 200), np.uint16)
        #h,w = vis.shape
        #vis2 = cv.CreateMat(h, w, cv.CV_32FC3)
        #vis0 = cv.frombuffer(image_stream.read())
        num_images = 1
        rows = 150
        cols = 200
        #data = numpy.frombuffer(image_stream.read(), dtype=numpy.int16)
        #print (imagebuffer)
        #print('bufferToMat setting up numpy var type')
        dt = np.int16
        #print('bufferToMat setting up numpy var byte order')
        #dt = dt.newbyteorder("<")
        #print('bufferToMat creating numpy var from buffer')
        data = np.frombuffer(bytes(imagebuffer), dtype=dt)
        #print('bufferToMat created numpy var')
        data = data.reshape(num_images, rows, cols, 1)            
        #print('bufferToMat reshaped numpy var')
        #image = cv2.frombuffer(data)
        #print('bufferToMat created image')
        return data
    if length == 320*240*2:
        num_images = 1
        rows = 240
        cols = 320
        dt = np.int16
        data = np.frombuffer(bytes(imagebuffer), dtype=dt)
        data = data.reshape(num_images, rows, cols, 1)            
        return data
    return 0


#img = cv2.imread('watch.jpg',cv2.IMREAD_GRAYSCALE)
#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#def get_constants(prefix):
#    """Create a dictionary mapping socket module constants to their names."""
#    return dict( (getattr(socket, n), n)
#                 for n in dir(socket)
#                 if n.startswith(prefix)
#                 )

class irCamera_SeekMosaic:

    def __init__(self, portnumber):
        #def openconnection(self, portnumber):
        #print('openconnection called')
   
        # Create a TCP/IP socket
        self.connection = socket.create_connection(('localhost', portnumber))
        #print('openconnection done, connection ')
        #print(self.connection)




    def recv_timeout(self, requestedLength,timeout):
        #print('recv_timeout(..,%d,..) entered' %requestedLength)
        #make socket non blocking
        self.connection.setblocking(0)
        #print('recv_timeout set socket to non-blocking')
        
        #total data partwise in an array
        total_data=bytearray(0);
        #print('total_data initialized to:')
        #print(total_data)
        data='';
        
        #beginning time
        #print('recv_timeout getting time mark')
        begin=time.time()
        #print('recv_timeout got time mark')
        while 1:
            #print('recv_timeout loop top')
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
            
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
            
            #recv something
            try:
                data = self.connection.recv(requestedLength - len(total_data))
                if data:
                    print('recv_timeout received data len=%d' % len(data))
                    if requestedLength == len(data):
                        total_data = data
                        break;
                    else:
                        print('partial data read: %d bytes' %len(data))
                        if len(total_data) == 0:
                            total_data = data
                        else:
                            total_data += data
                        #print('total_data is now:')
                        #print(total_data)
                    print('now have %d bytes' % len(total_data))
                    if len(total_data) >= requestedLength:
                        break;
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #print('recv_timeout sleeping')
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
            #print('recv_timeout loop bottom')
        
        #join all parts to make final string
        #print('recv_timeout exiting')
        #print(total_data)
        #return ''.join(total_data)
        return total_data


    def read(self):
        #print('imread called')
        #print(self.connection)
        image = 0
        try:    
            self.connection.sendall(b'THERM')
            amount_received = 0
            #print('calling recv_timeout')
            data = self.recv_timeout(4, 30)
            #print('back from recv_timeout; data=')
            #print(data)
            #image_len = struct.unpack('<L', self.connection.read(4))[0]
            image_len = struct.unpack('<I', data)[0]
            #print('unpacked struct')
            fullBuffer = []
            amount_expected = image_len
            #print('Buffer is %d bytes' % image_len)

            imagedata = self.recv_timeout(image_len, 30)
            #print('imagedata is')
            #print(imagedata)

            #print('imagedata bufferlen is %d bytes' % len(imagedata))
            
            # Construct a stream to hold the image data and read the image
            # data from the connection
            #image_stream = io.BytesIO()
            #image_stream.write(self.connection.read(image_len))

            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            #image_stream.seek(0)

            image = bufferToMat(image_len, imagedata)
            #print('Image is %dx%d' % image.size)
            image.verify()
            #print('Image is verified')
        except:
            pass

        #print('imread done')
        frame = image[0]
        if frame is None:
            return False, frame
        return True, frame


                
            
    def release(self):
        #finally:
        print >>sys.stderr, 'closing socket'
        self.connection.close()

    


    
