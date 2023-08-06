from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='SNPerr',
    version="0.0.1",
    url='https://github.com/j3551ca/DiVirusity',
    author='Jessica Caleta',
    author_email='jessica.caleta@alumni.ubc.ca',
    packages=['SNPerr'],
    description="Determine read depth and variant frequency thresholds to distinguish seq errors from true SNPs. \
    Simulates effect of changing per-site read depth and variant frequency on accuracy of genetic diversity",
    install_requires=['numpy',
    'scipy.stats',
    'pandas',
    'matplotlib.pyplot'
    ],
    license='MIT',
    # We will also need a readme eventually (there will be a warning)
    #long_description=open('README.txt').read(),
    python_requires='>=3.6'
)
