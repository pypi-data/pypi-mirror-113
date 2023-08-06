# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_shrinkwrap']

package_data = \
{'': ['*']}

install_requires = \
['curlify>=2.2.1,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'psutil>=5.8.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'uncurl>=0.0.11,<0.0.12']

entry_points = \
{'console_scripts': ['hsw = http_shrinkwrap.bin:main']}

setup_kwargs = {
    'name': 'http-shrinkwrap',
    'version': '0.1.0',
    'description': 'A command line tool to minimize curl http requests.',
    'long_description': '# http_shrinkwrap - Minimizes curl HTTP commands\n## In a nutshell\nhttp_shrinkwrap is a command line tool that removes all obsolete HTTP headers from a curl HTTP request.\n* All headers that have no apparent effect on the response obtained from the webserver are removed.\n* Long Cookies and some other header values are also shortened.  \n\nSince the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for minimizing the recreated browser requests in your shell.\nThe tool is written in python and based on [uncurl](https://github.com/spulec/uncurl).\n\n\n## Example\n### Example ipinfo\nturns this:\n\n```bash\ncurl \'https://ipinfo.io/\' -H \'authority: ipinfo.io\' -H \'cache-control: max-age=0\' -H \'dnt: 1\' -H \'upgrade-insecure-requests: 1\' -H \'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/534.16\' -H \'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\' -H \'sec-fetch-site: none\' -H \'sec-fetch-mode: navigate\' -H \'sec-fetch-user: ?1\' -H \'sec-fetch-dest: document\' -H \'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5\' -H \'sec-gpc: 1\' --compressed\n```\n\ninto this:\n\n```bash\ncurl -X GET -H \'user-agent: Mozilla/5.0\' https://ipinfo.io/\n```\n\n### Example heise.de\nturns this:\n\n```bash\ncurl \'https://www.heise.de/\'   -H \'authority: www.heise.de\'   -H \'cache-control: max-age=0\'   -H \'dnt: 1\'   -H \'upgrade-insecure-requests: 1\'   -H \'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/137.36\'   -H \'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\'   -H \'sec-fetch-site: none\'   -H \'sec-fetch-mode: navigate\'   -H \'sec-fetch-user: ?1\'   -H \'sec-fetch-dest: document\'   -H \'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5\'   -H \'cookie: wt_nv_s=1; wt3_sid=%3B288689636920174%3B589751618140993; wt_ttv2_e_288689636920174=meldung.newsticker.bottom.kommentarelesen*4439526%3ASmart%20Home%3A%20Innenminister%20planen%20Zugriff%20auf%20Daten%20von%20Alexa%20%26%20Co.**meldung.newsticker.bottom*******2*2*; wt_ttv2_c_288689636920174=meldung.newsticker.bottom.kommentarelesen*4428549%3AAntergos-Entwickler%20stellen%20Linux-Projekt%20ein**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4432329%3AEuropa-Wahl%3A%20Schwere%20Schlappe%20f%C3%BCr%20deutsche%20Koalitionsparteien%2C%20Erfolge%20f**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4436209%3AHuawei-Konflikt%3A%20China%20k%C3%BCndigt%20eigene%20schwarze%20Liste%20an**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4439526%3ASmart%20Home%3A%20Innenminister%20planen%20Zugriff%20auf%20Daten%20von%20Alexa%20%26%20Co.**meldung.newsticker.bottom*******2*2*; volumeControl_volumeValue=100; wt_nv=1; wt_ttv2_s_288689636920174=9700; wt_ttv2_s_288689636920174=9700; wt3_eid=%3B288689636920174%7C2155707251500935604%232159741754555500039%3B589751618140993%7C2155796048217456639%232155796801880162886\'   -H \'sec-gpc: 1\'   -H \'if-modified-since: Wed, 18 Nov 2020 21:57:08 GMT\'   --compressed\n```\n\ninto this:\n\n```bash\ncurl -X GET https://www.heise.de/\n```\n\n## Usage\nThere are tree main ways to invoke http_shrinkwrap `hsw`\n* By passing a `file` as an argument\n* Via piping a curl command from `stdin`\n* By calling `hsw` from insde `vim` (or `fc`)\n\nUse ```--bust``` to avoid having the web server refer the client back to the cache with a 304 by\nremoving the according headrs\n\n### Via file\n\thsw file_containing_curl_cmd\n\neg:\n* in Chrome/Mozilla dev tools > "copy request as curl" & paste to some_file\n* `hsw some_file`\n\n### Via stdin\npipe curl command to `hsw`\neg:\n* in Chrome/Mozilla dev tools > "copy request as curl"\n* `echo "curl http://foo.com -H \'some thing\'" | hsw`\n\nNote:\n* wrap the curl command in double quotes\n* this will not work if the curl command has single and double quotes or other sepcial chars. Use the file method in these cases.\n\n\n### From fc & vim\ngiven `export EDITOR="vim"`\n\n* in Chrome/Mozilla dev tools > "copy request as curl"\n* paste and execute curl command in terminal\n* run `fc`\n* now inside vim run `:%! hsw`\n* then save output if needed `:w outfile_name`\n\n\n## Install\n\tpip3 install -i https://test.pypi.org/simple/ http-shrinkwrap\n\n\n## Run without install\n\tgit clone https://github.com/zrthstr/http_shrinkwrap\n\tcd http_shrinkwrap\n\tpip install -r requirements.txt\n\t\n\techo \'some curl cmd \' | python -m http_shrinkwrap.bin\n\t# or\n\tpython -m http_shrinkwrap.bin some_file_containing_a_curl_cmd\n\n\n## Development\n\n### Debugging\n`export DEBUG=TRUE`\neven more info\n`export DEBUG=TRACE`\n\n### Testing\n\tmake test\n\n### License\nApache License 2.0\n\n### Develpement\nWritten by zrth1k@gmail.com\n\nThanks to [Lars Wirzenius](https://liw.fi/readme-review/) for reviewing the README!\n',
    'author': 'zrthstr',
    'author_email': 'zrth1k@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zrthstr/http_shrinkwrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
