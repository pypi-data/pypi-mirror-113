from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='navmenu',
    version='0.2.1',
    description='A library to create multilevel menus for chatbots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rashidsh',
    author_email='mail@rashidsh.ru',
    url='https://github.com/rashidsh/navmenu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    tests_require=[
        'pytest',
    ],
)
