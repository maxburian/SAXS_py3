from setuptools import setup


 

 
 

setup(
    name="SAXS",
    version="0",
    packages=["SAXS"],
    package_data={"SAXS": ["schema.json"]},
    author="Christian Meisenbichler",
    author_email="chmberg@gmail.com",
    description="Tools for analysing SAXS Data",
    license="Proprietary",
    entry_points = {
        'console_scripts': [
            'saxsconverter = SAXS:convert',
            'saxsdog = SAXS:saxsdog',
            'plotchi=SAXS:plotchi']
        
    }
)
 