from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider



class BD:
    def __init__(self):
        self.cloud_config = {
            'secure_connect_bundle': 'secure-connect-bdnr-database.zip'
        }

        self.auth_provider = PlainTextAuthProvider(
            "msPtPsTroupwzIgveKpSvZWh",
            "qZdaUaazThqftr.cSMd,fGnaPCY2Xelbz2W+NJxBOExb1Sl0AtGaZ2aDBk9im.TM+cpZPp,5JNFuRPn11gO-yoQ4e_06tGOOfPYccrJeBWZjE5dYr+kgSrjDh_4.t9m7"
        )

        cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider)
        self.bd = cluster.connect()

        row = self.bd.execute("select release_version from system.local").one()
        if row: pass
            # print(row[0])
        else:
            print("A conexão falhou.")
    
    def usuario_collection(self):
        return self.bd.execute("SELECT * FROM Usuario")
    
    def produto_collection(self):
        return self.bd.execute("SELECT * FROM Produto")
    
    def vendedor_collection(self):
        return self.bd.execute("SELECT * FROM Vendedor")
    
    def compra_collection(self):
        return self.bd.execute("SELECT * FROM Compra")