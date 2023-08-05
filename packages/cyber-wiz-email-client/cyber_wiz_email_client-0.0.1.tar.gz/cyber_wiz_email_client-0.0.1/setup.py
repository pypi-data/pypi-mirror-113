from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cyber_wiz_email_client',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='Client to communicate with email cyber-wiz',
    url='https://gitlab.com/aswin.cv/cyber-wiz-email-client',
    license='unlicense',
    py_modules=['cyber_wiz_api', 'exception'],
    package_dir={'': 'src'},
    author='Cyber Wiz',
    author_email='info@cyber-wiz.com',
    install_requires=[
        'requests',
    ],
    zip_safe=False
)
