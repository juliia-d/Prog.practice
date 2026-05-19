import requests
import cv2
import numpy as np
import sys

BASE_URL = "http://localhost:8000"

def send_request(req_dict):
    response = requests.post(f"{BASE_URL}/", json=req_dict)
    
    if req_dict.get('action') == 'bw_image':
        return response.content
    else:
        return response.json()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'fetch':
            url = input("Enter URL: ")
            regex = input("Enter regex (optional): ")
            req = {'action': 'fetch', 'url': url}
            if regex:
                req['regex'] = regex
            resp = send_request(req)
            print('Headers:', resp.get('headers', {}))
            print('Matched lines:', resp.get('matched_lines', []))
        
        elif sys.argv[1] == 'bw':
            url = input("Enter image URL: ")
            req = {'action': 'bw_image', 'url': url}
            img_data = send_request(req)
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                cv2.imshow('Black and White', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                save = input("Save image? (y/n): ")
                if save.lower() == 'y':
                    filename = input("Filename (default: bw_output.jpg): ")
                    if not filename:
                        filename = 'bw_output.jpg'
                    with open(filename, 'wb') as f:
                        f.write(img_data)
            else:
                print("Failed to decode image")
        
        elif sys.argv[1] == 'wiki':
            print("\nWikipedia Pageviews Stats")
            print("1. Top articles")
            print("2. Agent breakdown")
            print("3. Hourly stats (обробка hourly_encoded)")
            choice = input("Choose (1-3): ")
            
            if choice == '1':
                limit = input("Limit (default 20): ")
                limit = int(limit) if limit else 20
                req = {
                    'action': 'wiki_stats',
                    'query_type': 'top_articles',
                    'limit': limit
                }
                resp = send_request(req)
                print(f"\nTop {limit} articles:")
                for i, item in enumerate(resp, 1):
                    print(f"{i}. {item['title']}: {item['views']} views")
            
            elif choice == '2':
                req = {
                    'action': 'wiki_stats',
                    'query_type': 'agent_breakdown'
                }
                resp = send_request(req)
                print("\nAgent breakdown:")
                for item in resp:
                    print(f"{item['agent']}: {item['views']} views")
            
            elif choice == '3':
                print("\nОбробка hourly_encoded")
                print("Формат: YYYYMMDDHH")
                hour = input("Enter hour (leave empty for all hours): ")
                req = {
                    'action': 'wiki_stats',
                    'query_type': 'hourly_stats',
                    'hour': hour if hour else None
                }
                resp = send_request(req)
                print("\nHourly stats:")
                for item in resp:
                    print(f"{item['hour']}: {item['views']} views")
    
    else:
        print("Usage:")
        print("  python client.py fetch    - Fetch URL and find regex matches")
        print("  python client.py bw       - Convert image to black and white")
        print("  python client.py wiki     - Wikipedia pageviews stats")
