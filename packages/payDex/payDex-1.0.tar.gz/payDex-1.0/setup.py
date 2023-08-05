from distutils.core import setup
setup(
  name = 'payDex',         
  packages = ['payDex'],   
  version = '1.0',      
  license='MIT',        
  description = 'pay Dex, paiement in cameroun base on payUnit',   
  author = 'fredex',                   
  author_email = 'freddyviany@gmail.com',      
  url = 'https://github.com/freddy-viany/payDex',   
  download_url = 'https://github.com/freddy-viany/payDex/archive/refs/tags/v1.0.tar.gz',    
  keywords = ['payDex', 'PAIEMENT', 'CAMEROUN', 'DJANGO'],   
  install_requires=[            # I get to this in a second   
          'requests',
          'uuid',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
