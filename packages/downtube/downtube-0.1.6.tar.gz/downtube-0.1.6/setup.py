# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['downtube']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9.1,<0.10.0',
 'click>=8.0.1,<9.0.0',
 'pytube>=10.9.2,<11.0.0',
 'tqdm>=4.61.2,<5.0.0',
 'youtube-search>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['dtube = downtube.main:main']}

setup_kwargs = {
    'name': 'downtube',
    'version': '0.1.6',
    'description': 'A simple yet powerful youtube downloader built in python',
    'long_description': "# DownTube\n## `Downtube` : A simple CLI for downloading youtube videos in video/audio format\n\nNOTE: I dont support downloading stuff illegally, be sure to use it for legal purposes and creative commons licensed videos only\n\n## Install\n\n```\npip3 install downtube \n```\n\n## Dependencies\n+ `click` \n+ `click_help_colors`\n+ `pytube`\n+ `tqdm`\n+ `youtube_search`\n\n## Built with\n+ `Python 3.9.6` \n\n## Supported Platforms:\n\n+ Operating System = Cross-Platform\n\n## How to use\n\nOpen powershell for Windows or Terminal for Linux/Mac and  and type ```dtube```\n\nIf the following result comes, then you have successfully installed downtube on your system\n\n```bash\n\n  Download Youtube Videos fast and easily with DownTube\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  config  Setup your default video resolution\n  dayt    Download Audio by Search\n  dlal    Download Audio by URL\n  dlvl    Download Video by URL\n  dlyt    Download Video by Search\n  init    Initialize downtube to get started\n```\n\nelse, try the above steps again!\n\n#### Setup\n\nFirst you need to setup downtube for yourself\n\nProcedure:\n\n- Run `dtube config -dr <resolution>`to set your preferred default video resolution for download. You can check options for resolutions by executing `dtube config`\n\n- Now you are set up to use downtube\n\n**Most of the time only 360p and 720p videos support audio, so they are recommended over any other resolution**\n\n##### Download video from search terms :\n\n```\ndtube dlyt {Search Terms} -r {resolution(optional)}\n```\n\nFor example:\n\n```\ndtube dlyt Despacito_Song -r 360p\n```\nThe first result from your search terms will be downloaded to your current folder\n\nGiving a resolution is completely optional. If you dont provide it, the video will be downloaded in your default resolution.\n\n**Most of the time only 360p and 720p videos support audio, so they are recommended over any other resolution**\n\n##### Download video from URL\n\n```\ndtube dlvl {Video URL} -r {resolution(optional)}\n```\n\nFor example:\n\n```\ndtube dlvl 'https://www.youtube.com/watch?v=kJQP7kiw5Fk' -r 360p\n```\nThe video redirected by your url will be downloaded to your current folder\n\nGiving a resolution is completely optional. If you dont provide it, the video will be downloaded in your default resolution.\n\n**Most of the time only 360p and 720p videos support audio, so they are recommended over any other resolution**\n\n##### Download audio from Search Terms\n\n```\ndtube dayt {Search Terms}\n```\n\nFor example:\n\n```\ndtube dayt Despacito_Song\n```\nThe first result from your search terms will be downloaded to your current folder in AUDIO format\n\n##### Download audio from URL\n\n```\ndtube dlat {Video URL}\n```\n\nFor example:\n\n```\ndtube dlal 'https://www.youtube.com/watch?v=kJQP7kiw5Fk\n```\nThe video redirected by your url will be downloaded to your current folder in AUDIO format\n\n##### --dir flag\n\nThe dir flag ensures that your file is downloaded in the Downloads directory of your computer\n\nFor e.g.\n\n```bash\ndtube dlvl https://youtu.be/kJQP7kiw5Fk -d\n```\n\nThe above command sets your download location as C://Downloads for windows and /home/user/Downloads for Linux/Mac. The same flag applies for `dlyt`, `dayt` and `dlal`.\n### Developers\n- [Arghya Sarkar](https://github.com/arghyagod-coder)\n\n### Current Release- 0.1.6\n\n#### Whats new?\n\n- Custom directory options and default directory awesome\n- Better handling of errors\n\n### Developer Tools\n\n- [Visual Studio Code](https://github.com/microsoft/vscode)\n\n- [Python 3.9.6](https://python.org)\n\n- [Git](https://git-scm.com)\n\n- [Python Poetry](https://python-poetry.org/)\n\n## License\n\nLicense © 2021-Present Arghya Sarkar\n\nThis repository is licensed under the MIT license. See [LICENSE](https://github.com/arghyagod-coder/downtube/blob/main/LICENSE) for details.\n\n## Special Notes\n\n- Contribution is appreciated! \n- If you see anything uncomfortable or not working, file an issue in [the issue page](https://github.com/arghyagod-coder/downtube/issues). Issues aren't ignored by the developers\n- Thanks for seeing my project!",
    'author': 'Arghya Sarkar',
    'author_email': 'arghyasarkar.nolan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arghyagod-coder/downtube',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
