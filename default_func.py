import requests

ec_cred = {
    'url': 'https://sup-api-rmsv1.erental.com.br/api/',
    'key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiQ2xpZW50ZSIsIlNpc3RlbWEiOiJlSWQvR0NqaWlYMDV2SDJTVlFQV1dBPT0iLCJuYmYiOjE2NzgxMzM0MTcsImV4cCI6MTY4MTEzMzQxNywiaWF0IjoxNjc4MTMzNDE3fQ.TqOV6gAhHCkKDwGO-4BFvV4ZyngCZx3HyrHj2r8f0tU'
}


def default_get(url_end=''):
    req = requests.get(ec_cred['url']+url_end, headers= {'Authorization':'Bearer '+ec_cred['key']})
    if(req.status_code != 200):
        print('EC: ocorreu um erro na lista de '+url_end+'s')
        return False
    return req.json()['lista']


def lista_carros():
    #PUXAR LISTA DE CARROS
    carros_r = default_get('Grupo')
    if not carros_r:
        return {'success':False}

    #PUXAR LISTA DE LOJAS
    lojas_r = default_get('Loja')
    if not lojas_r:
        return {'success':False}

    #PUXAR PERIODOS
    periodos_r = default_get('Periodo')
    if not periodos_r:
        return {'success':False}

    #PUXAR QUILOMETRAGENS
    franquias_r = default_get('Franquia')
    if not franquias_r:
        return {'success':False}


    #PROCURA OS VEICULOS EM CADA LOJA
    lojas = []
    for loja in lojas_r:
        body = {'codLoja':loja['cod']}
        req = requests.post(ec_cred['url']+'Oferta', json=body, headers={'Authorization':'Bearer '+ec_cred['key']})
        if(req.status_code != 200):
            print(req)
            return {'success':False}
        ofertas = req.json()['lista']
        
        carros = []

        for oferta in ofertas:
            valores = []
            val_base = 0.0
            for valor in oferta['valores']:
                if valor['valor'] < val_base:
                    val_base = valor['valor']
                for periodo in periodos_r:
                    if periodo['qtd'] == valor['periodo']:
                        valor['periodo'] = periodo
                for km in franquias_r:
                    if km['qtd'] == valor['quilometragem']:
                        valor['quilometragem'] = km

                valores.append(valor)

            carro = None
            for carro_r in carros_r:
                if carro_r['cod'] == oferta['codigo']:
                    carro = {
                        "cod": carro_r['cod'],
                        "sgl": carro_r['sgl'],
                        "nom": carro_r['nom'],
                        "descricao": carro_r['dsc'],
                        "descricaoCompleta": oferta['descricao'],
                        "promocao": carro_r['promocao'],
                        "categoria": carro_r['categoria'],
                        "energizacao": carro_r['energizacao'],
                        "marca": carro_r['marca'],
                        "txtDetalhes": carro_r['txtDetalhes'],
                        "imgBase64": carro_r['imgBase64'],
                        "imgUrl": carro_r['imgUrl'],
                        "listaImgUrl": carro_r['listaImgUrl'],
                        "linkExterno": carro_r['linkExterno'],
                        "acessorios": carro_r['acessorios'],
                        "periodo": oferta['periodo'],
                        "quilometragem": oferta['quilometragem'],
                        "valores": valores,
                        "valorBase": val_base
                    }
            carros.append(carro)

        loja['carros'] = carros
        lojas.append(loja)


    #LISTAR PROTECOES
    protecoes = default_get('Protecao')
    if not protecoes:
        return {'success':False}

    return {'success':True, 'data':{'lojas':lojas, 'protecoes': protecoes}}
