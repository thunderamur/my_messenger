from setuptools import setup, find_packages


setup(
    name="MyMessenger",
    version='0.2.2',
    description="Study project of chat based on JSON IM protocol",
    long_description="Study project of chat based on JSON IM protocol with python3 and PyQt5",
    author="Ramil Minnigaliev",
    author_email="minnigaliev-r@yandex.ru",
    url="https://github.com/thunderamur/my_messenger",
    license='MIT',
    keywords=['chat PyQt 5', 'jim chat'],
    packages=find_packages('src'),
    package_dir={'my_messenger': 'src/my_messenger'},
    python_requires='>=3.5',
    install_requires=[
        "PyQt5>=5.9",
        "SQLAlchemy>=1.1",
    ],
    extras_require={
        'test': ["pytest>=3.2",
                 "pytest-cov>=2.5",
                 "pytest-sugar>=0.9",],
    },
    entry_points={
        'gui_scripts': [
            'mm-client-qt5 = my_messenger.client_gui:main',
        ],
        'console_scripts': [
            'mm-client = my_messenger.client_console:main',
            'mm-server = my_messenger.server:main'
        ]
    },
)