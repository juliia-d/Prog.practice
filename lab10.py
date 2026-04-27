import cv2
import numpy as np
import time
import threading
import multiprocessing as mp
from pathlib import Path

def blur_image(image_path):
    img = cv2.imread(image_path)
    blurred = cv2.GaussianBlur(img, (15, 15), 0)
    out_path = Path(image_path).stem + "_blur.jpg"
    cv2.imwrite(out_path, blurred)

def process_sequential(images):
    for img in images:
        blur_image(img)

def process_threading(images):
    threads = []
    for img in images:
        t = threading.Thread(target=blur_image, args=(img,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def process_multiprocessing(images):
    processes = []
    for img in images:
        p = mp.Process(target=blur_image, args=(img,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

def create_test_images(n=4):
    test_images = []
    for i in range(n):
        img = np.random.randint(0, 256, (400, 400, 3), dtype=np.uint8)
        filename = f"test_img_{i}.jpg"
        cv2.imwrite(filename, img)
        test_images.append(filename)
    return test_images

if __name__ == "__main__":
    images = create_test_images(4)
    
    start = time.time()
    process_sequential(images)
    seq_time = time.time() - start
    
    start = time.time()
    process_threading(images)
    thread_time = time.time() - start
    
    start = time.time()
    process_multiprocessing(images)
    proc_time = time.time() - start
    
    print(f"Послідовно: {seq_time:.2f} с")
    print(f"Потоки: {thread_time:.2f} с")
    print(f"Процеси: {proc_time:.2f} с")
