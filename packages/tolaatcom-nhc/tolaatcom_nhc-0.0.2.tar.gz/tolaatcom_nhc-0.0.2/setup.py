from distutils.core import setup


setup(
    name='tolaatcom_nhc',
    version='0.0.2',
    description='tolatcom module for scraping backend of net hamishpat app',
    url='https://github.com/tolaat-com/tolaatcom_nhc/archive/refs/tags/0.0.2.tar.gz',
    author='Andy Worms',
    author_email='andyworms@gmail.com',
    license='mit',
    packages=['tolaatcom_nhc'],
    install_requires=['Pillow==7.1.2', 'PyPDF2==1.26.0', 'qrcode==6.1', 'numpy==1.18.4'],
    data_files=[('tolaatcom_nhc', ['tolaatcom_nhc/Arimo-Bold.ttf', 'tolaatcom_nhc/tolaat-stamp.png'])],
    package_data={'tolaatcom_nhc': ['Arimo-Bold.ttf', 'tolaat-stamp.png']},
    zip_safe=False
)