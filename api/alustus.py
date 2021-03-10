"""
Käyttää opintopolku moduulia ja tekee tietokannan, ei ole varmaankaan viimeinen versio, taikka se mikä päivittyy viikon välein, mutta toimiva.
"""
if __name__ == "__main__":
    import tietokanta
    from opintopolku import opintopolku
    import asetukset
    import os

    db = tietokanta.Database(asetukset.palvelin, asetukset.kayttaja, asetukset.salasana, asetukset.tietokanta)

    db.query(
        """
            CREATE TABLE IF NOT EXISTS `kurssit` (
            `id` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
            `nimi` VARCHAR(200) NOT NULL COLLATE 'latin1_swedish_ci',
            `kieli` VARCHAR(30) NOT NULL COLLATE 'latin1_swedish_ci',
            `kuvaus` VARCHAR(500) NOT NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
            `opintopisteet` INT(11) UNSIGNED NOT NULL DEFAULT '0',
            `koulu` VARCHAR(100) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',
            `osaamiset` VARCHAR(500) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',
            PRIMARY KEY (`id`) USING BTREE
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    )
    db.query("TRUNCATE kurssit")
    opintopolku.hakuTyokaluYksinkertainen()
    for i, j in opintopolku.objs.items():
        db.query(j.sqlYksinkertainen())
    path = os.path.dirname(os.path.abspath(__file__))
    fo_api_ini = open(path+"/api.ini", "w")
    fo_api_ini.write("""
[uwsgi]\n
module = wsgi:app\n
master = true\n
processes = 2\n
virtualenv = {path}\n
socket = api.sock\n
chmod-socket = 666\n
vacuum = true\n
\n
die-on-term = true
    """.format(path=path))
    fo_api_ini.close()
    fo_wsgi_py = open(path+"/wsgi.py", "w")
    fo_wsgi_py.write("""from api import app\n
\n
if __name__ == "__main__":\n
    app.run()""")
    fo_wsgi_py.close()