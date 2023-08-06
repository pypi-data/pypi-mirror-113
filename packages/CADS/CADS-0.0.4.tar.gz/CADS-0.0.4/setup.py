from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='CADS',
      version='0.0.4',
      description='Python Package to add new download services to Copernicus and make easier managing voluminous data requests.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/CADS",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      zip_safe=False,
      platforms='OS Independent',
      python_requires='>=3.6',

      include_package_data=True,
      package_data={
        'CADS': ['DATA/LOGO.gif', 'Database/CMEMS_Database.json', 'Database/CMEMS_Databaseselvar.json', 'Database/datasets_MY.pdf','Script/CMEMS_Database.json','Script/FTPsubsetMO.py']

      },

      install_requires=[
        'netCDF4>=1.4.2',
        'ftputil>=3.4',
        'motuclient>=1.8.1',
        'csv342>=1.0.0', 
        'pandas>=0.23.4', 
        'xarray>=0.11.0',
        'json5>=0.9.1',
        'h5py>=2.10.0',
        'h5netcdf>=0.8.0'
        
      ],
      
      packages=find_packages(),

      entry_points={
        'console_scripts':['CADS = CADS.__main__:main']
        
      },

      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
