import os
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def download_ts_segment(ts_url, temp_dir, i):
    print(f"Downloading {ts_url}")
    ts_response = requests.get(ts_url)
    ts_filename = os.path.join(temp_dir, f"segment_{i}.ts")
    with open(ts_filename, 'wb') as f:
        f.write(ts_response.content)
    print(f"Downloaded {ts_filename}")

def download_m3u8(url, output_name, ffmpeg_path):
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Download the .m3u8 file
    response = requests.get(url)
    m3u8_content = response.text

    # Step 2: Parse the .m3u8 file to get the .ts segment URLs
    base_url = os.path.dirname(url)
    # Get the missing part of the URL from the .m3u8 URL
    missing_part = url.split('/')[-2]
    ts_urls = [urljoin(base_url, f"{missing_part}/{line.strip()}") for line in m3u8_content.split('\n') if line and not line.startswith('#')]

    # Step 3: Create a temporary directory for storing .ts files
    temp_dir = os.path.join(current_dir, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Step 4: Download .ts segments concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, ts_url in enumerate(ts_urls):
            futures.append(executor.submit(download_ts_segment, ts_url, temp_dir, i))
            print(f"Downloading {ts_url}")
        for future in futures:
            future.result()  # Wait for each download to complete

    # Step 5: Combine the .ts segments into a single file using ffmpeg
    ts_files = [os.path.join(temp_dir, f"segment_{i}.ts") for i in range(len(ts_urls))]
    ts_list_file = os.path.join(temp_dir, 'tslist.txt')
    with open(ts_list_file, 'w') as f:
        for ts_file in ts_files:
            f.write(f"file '{ts_file}'\n")
    output_file = os.path.join(current_dir, output_name)
    os.system(f"{ffmpeg_path} -f concat -safe 0 -i {ts_list_file} -c copy {output_file}")
    
    # Step 6: Cleanup temporary .ts files and directory
    os.remove(ts_list_file)
    for ts_file in ts_files:
        os.remove(ts_file)
        print(f"Removed {ts_file}")
    os.rmdir(temp_dir)
    print(f"Removed temporary directory {temp_dir}")

    print(f"Download and combination complete. Output file: {output_file}")

# enter url end with .m3u8
m3u8_url = ''
# enter ffmpeg path
ffmeg_path = 'E:\\ffmpeg\\bin\\ffmpeg.exe'

now = datetime.now()
suffix = now.strftime("%Y%m%d_%H%M%S")
output_filename = f'output_{suffix}.mp4'

download_m3u8(m3u8_url, output_filename, ffmeg_path)
