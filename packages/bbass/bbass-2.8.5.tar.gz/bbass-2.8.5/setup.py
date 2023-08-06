from distutils.core import setup
setup(
  name = 'bbass',      
  packages = ['bbass'],
  version = '2.8.5', 
  license='MIT',   
  description = '🔊 an asynchronous music downloader to make your life‬ easy.', 
  author = 'PROgramJEDI',
  url = 'https://github.com/PROgramJEDI/bbass',  
  download_url = 'https://github.com/PROgramJEDI/bbass/archive/refs/tags/2.8.5.tar.gz', 
  keywords = ['music', 'youtube', 'music-downloader', 'asynchronous'], 
  install_requires=[        
          'chrome_bookmarks'
      ]
)