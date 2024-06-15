# M3U8 Downloader

This script downloads and combines .ts video segments from an M3U8 playlist into a single video file using `ffmpeg`. The script handles the download of the M3U8 file, parses it to get the segment URLs, downloads the segments concurrently, and then combines them into a single output file.

## Requirements

- Python 3.x
- `requests` library
- `ffmpeg`

## Installation

1. Install the required Python library:

   ```
   pip install requests
   ```

2. Download and install `ffmpeg` from [ffmpeg.org](https://ffmpeg.org/download.html). Make sure `ffmpeg` is accessible from your system's PATH or note its installation path.

## Usage

1. Set the `m3u8_url` to the URL ending with `.m3u8`.
2. Set the `ffmpeg_path` to the path of the `ffmpeg` executable on your system.
3. Run the script.

```python
m3u8_url = 'YOUR_M3U8_URL'
# enter ffmpeg path
ffmpeg_path = 'PATH_TO_FFMPEG'

download_m3u8(m3u8_url, output_filename, ffmpeg_path)
```

## Example

```python
m3u8_url = 'https://example.com/path/to/your/playlist.m3u8'
# enter ffmpeg path
ffmpeg_path = 'E:\\ffmpeg\\bin\\ffmpeg.exe'

now = datetime.now()
suffix = now.strftime("%Y%m%d_%H%M%S")
output_filename = f'output_{suffix}.mp4'

download_m3u8(m3u8_url, output_filename, ffmpeg_path)
```

## How It Works

1. **Download the .m3u8 file:** The script downloads the M3U8 file specified by the `m3u8_url`.
2. **Parse the .m3u8 file:** The script parses the M3U8 file to extract URLs of the .ts video segments.
3. **Create a temporary directory:** A temporary directory is created to store the downloaded .ts segments.
4. **Download .ts segments concurrently:** The script uses `ThreadPoolExecutor` to download .ts segments concurrently for faster performance.
5. **Combine .ts segments:** Once all segments are downloaded, they are combined into a single file using `ffmpeg`.
6. **Cleanup:** Temporary files and directories are deleted after the final output file is created.

## Note

- Ensure the `ffmpeg` path is correct.
- The output filename will include a timestamp to ensure uniqueness.
- The script will print progress messages to the console.
