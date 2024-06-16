from os import system
from time import sleep
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider



cloud_config = {
    'secure_connect_bundle': 'secure-connect-bdnr-database.zip'
}

auth_provider = PlainTextAuthProvider(
    "msPtPsTroupwzIgveKpSvZWh",
    "qZdaUaazThqftr.cSMd,fGnaPCY2Xelbz2W+NJxBOExb1Sl0AtGaZ2aDBk9im.TM+cpZPp,5JNFuRPn11gO-yoQ4e_06tGOOfPYccrJeBWZjE5dYr+kgSrjDh_4.t9m7"
)

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)


def find_vendedor():
    print("|Carregando vendedores...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    result = [row for row in session.execute(f"SELECT * FROM mercadolivre.vendedor;")]

    print("|Vendedores cadastrados")
    for i in range(len(result)):
        print(f"|{i+1} - {result[i].id}")
        print(f"|Nome: {result[i].nome}")
        print(f"|CNPJ: {result[i].cnpj}")

    try:
        r = int(input("|Selecione o vendedor: "))
        return result[r-1]
    except: pass

def find_usuario():
    print("|Carregando usuarios...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    result = [row for row in session.execute(f"SELECT * FROM mercadolivre.usuario;")]

    print("|Usuario cadastrados")
    for i in range(len(result)):
        print(f"|{i+1} - {result[i].id}")
        print(f"|Nome: {result[i].nome}")
        print(f"|Favoritos: {0 if not result[i].favoritos else len(result[i].favoritos)}")

    try:
        r = int(input("|Selecione o usuario: "))
        u = result[r-1]
        return {
            "id": u.id,
            "nome": u.nome,
            "favoritos": [] if u.favoritos is None else u.favoritos
        }
    except: pass

def selecionar_produtos(produtos: list = None):
    print("|Carregando produtos...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    if produtos is None:
        produtos = [row for row in session.execute(f"SELECT * FROM mercadolivre.produto;")]
    else:
        produtos = [[*session.execute(f"SELECT * FROM mercadolivre.produto where id = {id};")][0] for id in produtos]
    
    print("|Produtos")
    for i in range(len(produtos)):
        print(f"|{i+1} - {produtos[i].id}")
        print(f"|Nome: {produtos[i].nome}")
        print(f"|Descricao: {produtos[i].descricao}")
        print(f"|Valor: {produtos[i].valor}")
    
    try:
        selecionados = [int(n)-1 for n in input("|Selecione os produtos e separe com vírgulas(2, 5, 7, 8): ").split(",")]
        return [produtos[i] for i in selecionados]
    except: pass

def search_produto(nome: str):
    print("|Carregando produtos...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    produtos = [row for row in session.execute(f"SELECT * FROM mercadolivre.produto;")]
    produtos = [p for p in produtos if nome.lower() in p.nome.lower()]

    print("|Produtos encontrados")
    for p in produtos:
        print(f"|{p.id}")
        print(f"|Nome: {p.nome}")
        print(f"|Descricao: {p.descricao}")
        print(f"|Valor: {p.valor}")

def find_compra(data: str):
    print("|Carregando usuarios...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    usuarios = [row for row in session.execute(f"SELECT * FROM mercadolivre.usuario;")]

    print("|Usuario cadastrados")
    for i in range(len(usuarios)):
        print(f"|{i+1} - {usuarios[i].id}")
        print(f"|Nome: {usuarios[i].nome}")
        print(f"|Favoritos: {0 if not usuarios[i].favoritos else len(usuarios[i].favoritos)}")
    
    try:
        usuario = usuarios[int(input("|Selecione o usuario: "))-1]
    except: return

    print(f"|Compras do usuário {usuario.nome}")
    compras = [] if not usuario.compras else [c for c in usuario.compras if str(c.data) == data]
    for i in range(len(compras)):
        print(f"|{i+1} - {compras[i].id}")
        print(f"|Nome: {usuario.nome}")
        print(f"|Valor: {compras[i].valor}")
        print(f"|Data: {compras[i].data}")
        print(f"|Produtos: {0 if not compras[i].produtos else len(compras[i].produtos)}")


def main():
    EXECUTANDO = True
    while EXECUTANDO:
        print("|Menu Principal      |")
        print("|1 - Insert Usuário  |")
        print("|2 - Insert Produto  |")
        print("|3 - Insert Vendedor |")
        print("|4 - Insert Compra   |")
        print("|5 - Update Usuario  |")
        print("|6 - Search Produto  |")
        print("|7 - Delete Compra   |")
        print("|0 - Sair            |")

        entrada = int(input("|Opção: "))
        system("cls")
        if entrada == 1:# Insert Usuário
            print("|Insira os dados do usuario")
            print("|Carregando...", end="\r")
            session = cluster.connect()
            print(" "*100, end="\r")
            session.execute(f"""INSERT INTO mercadolivre.usuario (id, nome, favoritos)
                            VALUES (uuid(), '{input('|Nome: ')}', {'{}'});""")
       
        elif entrada == 2:# Insert Produto
            print("|Insira os dados do produto")
            print("|Carregando...", end="\r")
            session = cluster.connect()
            print(" "*100, end="\r")
            session.execute(f"""INSERT INTO mercadolivre.produto (id, nome, descricao, valor, vendedor_id)
                            VALUES (
                                uuid(),
                                '{input('|Nome: ')}',
                                '{input('|Descrição: ')}',
                                {float(input('|valor: '))},
                                {find_vendedor().id}
                            );""")
        
        elif entrada == 3:# Insert Vendedor
            print("|Insira os dados do vendedor")
            print("|Carregando...", end="\r")
            session = cluster.connect()
            print(" "*100, end="\r")
            session.execute(f"""INSERT INTO mercadolivre.vendedor (id, cnpj, nome, produtos)
                            VALUES (
                                uuid(),
                                '{input('|CNPJ: ')}',
                                '{input('|Nome: ')}',
                                {'{}'}
                            );""")
        
        elif entrada == 4:# Insert Compra
            print("|Insira os dados da compra")
            print("|Carregando...", end="\r")
            session = cluster.connect()
            print(" "*100, end="\r")

            print("|Selecione os produtos")
            produtos = selecionar_produtos()
            total = sum([p.valor for p in produtos])
            print("|Insira os dados da compra")
            session.execute(f"""INSERT INTO mercadolivre.compra (id, usuario_id, valor, data, produtos)
                            VALUES (
                                uuid(),
                                {find_usuario()['id']},
                                {total},
                                '{input('|Data(aaaa-mm-dd): ')}',
                                {{{', '.join([str(p.id) for p in produtos])}}}
                            );""")
        
        elif entrada == 5:# Update Usuario
            usuario = find_usuario()
            if input("|Deseja alterar o nome?(sim/não): ").strip().upper() == "SIM":
                usuario["nome"] = input("|Insira o nome: ")
            
            if input("|Deseja adicionar produtos aos favoritos?(sim/não): ").strip().upper() == "SIM":
                fav = []
                for np in selecionar_produtos():
                    if np not in usuario["favoritos"]:
                        fav.append(str(np.id))
                usuario["favoritos"] = fav

            if input("|Deseja remover produtos dos favoritos?(sim/não): ").strip().upper() == "SIM":
                remover = [str(f.id) for f in selecionar_produtos(usuario["favoritos"])]
                usuario["favoritos"] = [fav for fav in usuario["favoritos"] if fav not in remover]
            
            print("|Atualizando usuário...", end="\r")
            session = cluster.connect()
            print(" "*100, end="\r")
            session.execute(f"""UPDATE mercadolivre.usuario
                            SET nome = '{usuario['nome']}',
                                favoritos = {{{', '.join([str(f) for f in usuario['favoritos']])}}}
                            WHERE id = {usuario['id']};""")
            print("|Usuario atualizado")
        
        elif entrada == 6:# Search Produto
            nome = input("|Nome do produto: ")
            search_produto(nome)
        
        elif entrada == 7:# Delete Compra
            find_compra(input("|Data da compra(aaaa-mm-dd): "))
        
        else: EXECUTANDO = False
    print("|Saindo...")
main()