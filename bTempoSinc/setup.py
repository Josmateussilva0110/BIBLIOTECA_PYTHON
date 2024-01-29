from setuptools import setup
with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='TempoSinc',
    version='0.0.5',
    license='MIT License',
    author='RaiLeal/JoseMateus',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='temposinc.gerencia@gmail.com',
    keywords='TempoSinc',
    description=u'Previsão de tempo',
    packages=['TempoSinc'],
    install_requires=['requests', 'pandas', 'geopy', 'matplotlib'],)