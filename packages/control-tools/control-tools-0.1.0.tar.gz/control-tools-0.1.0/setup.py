from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='control-tools',
    version='0.1.0',
    description='Useful tools to make an automated actions script ',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Badreddine bencherki',
    author_email='badrbencherki@gmail.com',
    keywords=['bot', 'control', 'clock','timer',],
    url='https://github.com/badre2dine/control-tools',
    download_url='https://pypi.org/project/control-tools/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)