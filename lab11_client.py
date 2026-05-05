import socket
import json
import cv2
import numpy as np
import sys

def send_request(req_dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 25002))
    sock.sendall(json.dumps(req_dict).encode())
    
    if req_dict.get('action') == 'bw_image':
        data = b''
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            data += chunk
        sock.close()
        return data
    else:
        data = sock.recv(65536).decode()
        sock.close()
        return json.loads(data)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'bw':
        req = {
            'action': 'bw_image',
            'url': 'https://ornella.club/231-sobaka-taksa.html'
        }
        img_data = send_request(req)
        img_array = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            cv2.imshow('Black and White', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            with open('bw_output.jpg', 'wb') as f:
                f.write(img_data)
        else:
            print("Failed to decode image")
    else:
        req = {'action': 'fetch', 'url': 'https://example.com', 'regex': '<title>.*</title>'}
        resp = send_request(req)
        print('Headers:', resp.get('headers', {}))
        print('Matched lines:', resp.get('matched_lines', []))
