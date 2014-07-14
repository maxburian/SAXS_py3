from setuptools import setup
try:
    import py2exe
except:
    print "No py2exe here"
 

 
 

setup(
    name="SAXS",
    version="0",
    packages=["SAXS"],
    package_data={"SAXS": ["schema.json","LeashRequestSchema.json","LeashResultSchema.json","NetworkSchema.json"]},
    author="Christian Meisenbichler",
    author_email="chmberg@gmail.com",
    description="Tools for analysing SAXS Data",
    install_requires=["numpy","scipy", "matplotlib","jsonschema", "bitarray"," watchdog","sphinxcontrib-programoutput"],
    license="Proprietary",
    entry_points = {
        'console_scripts': [
            'saxsconverter = SAXS:convert',
            'saxsdog = SAXS:saxsdog',
            'plotchi=SAXS:plotchi',
            'saxsdogserver = SAXS:saxsdogserver',
            'saxsleash =SAXS:saxsleash',
            'saxsfeeder=SAXS:saxsfeeder',
            "saxsnetconf=SAXS.gennetconf"
            ]
        
    }
)
 