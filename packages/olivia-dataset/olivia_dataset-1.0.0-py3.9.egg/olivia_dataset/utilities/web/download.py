import requests
import requests.cookies
import os

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def cookie_enabled_download(url: str, output_filepath: str, chunk_size: int = 4096) -> None:
    """
    This method enables downloading while simulating cookies being present. It is prepared
    using the code-segments in [https://wasi0013.com/2019/10/04/how-to-download-a-file-from-a-website-link-using-python-script-or-code-snippet/](https://wasi0013.com/2019/10/04/how-to-download-a-file-from-a-website-link-using-python-script-or-code-snippet/).

    Parameters
    ----------
    url: `str`, required
        The path to the online file to be downloaded

    output_filepath: `str`, required
        The output filepath, in which the file will be saved

    chunk_size: `int`, optional (default=4096)
        The chunk size for downloading
    """
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Connection": "keep-alive",
    }
    s = requests.Session()
    cookie = requests.cookies.create_cookie('COOKIE_NAME', 'COOKIE_VALUE')
    s.cookies.set_cookie(cookie)

    try:
        with s.get(url, stream=True, headers=headers) as r:
            with open(output_filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)
        logger.info(f"the file is downloaded to {output_filepath}")
    except Exception as e:
        logger.error(f"download has failed due to the following error: {e}")
