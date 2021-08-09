# Import community modules.
import os
import sys
from setuptools import setup,find_packages


if __name__=='__main__':

  # Run only as sudo/root user.
  if not os.geteuid()==0:
    print('Run this command as sudo/root user.')
    sys.exit(1)

  # Setup configuration.
  setup(
    classifiers=[
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: OS Independent'
    ],
    python_requires='==2.7.*,==3.6.*,==3.7.*,==3.8.*,==3.9.*',
    package_dir={'':'source'},
    # packages=['sloopengine'],
    packages=find_packages(where='source'),
    install_requires=[
      'subprocess32==3.5.4',
      'requests==2.26.0',
      'validators==0.18.2',
      'termcolor==1.1.0'
    ],
    entry_points={
      'console_scripts':[
        'sloopengine=sloopengine:cli'
      ]
    },
    data_files=[
      ('/opt/sloopengine',[]),
      ('/opt/sloopengine/data',[]),
      ('/opt/sloopengine/log',[
        'source/sloopengine/log/main.log'
      ]),
      ('/opt/sloopengine/conf',[
        'source/sloopengine/conf/main.conf',
        'source/sloopengine/conf/credential.conf'
      ])
    ],
    url='https://github.com/sloopstash/sloopengine-cli',
    project_urls={
      'Source':'https://github.com/sloopstash/sloopengine-cli',
      'Issues':'https://github.com/sloopstash/sloopengine-cli/issues'
    },
    zip_safe=True
  )
