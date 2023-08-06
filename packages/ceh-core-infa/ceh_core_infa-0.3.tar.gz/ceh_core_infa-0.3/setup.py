from setuptools import setup, find_packages

requirements = ["yarl==1.6.3", "requests-oauthlib==1.3.0", "pandas==1.1.4", 'pydantic==1.8.1', "psycopg2-binary==2.8.6"]

setup(name='ceh_core_infa',
      version='0.3',
      description='Фреймворк для загрузки данных слоев IDL, BDM',
      packages=find_packages(),
      install_requires=requirements,
      author_email='dimapyrin@gmail.com',
      zip_safe=False)