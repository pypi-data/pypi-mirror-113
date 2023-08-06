from setuptools import setup

setup(
     name="crawl-web-page-script",  
     version="2.0.3",                          
     py_modules=["webcrawl_pack"],
     python_requires='>=3.6, <4',  
     install_requires=[
          'requests',
      ],             
)