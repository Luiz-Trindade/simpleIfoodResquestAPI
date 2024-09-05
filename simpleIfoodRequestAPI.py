"""
    
        ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗             
        ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝             
        ███████╗██║██╔████╔██║██████╔╝██║     █████╗               
        ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝               
        ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗             
        ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝             
                                                                
        ██╗███████╗ ██████╗  ██████╗ ██████╗                       
        ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗                      
        ██║█████╗  ██║   ██║██║   ██║██║  ██║                      
        ██║██╔══╝  ██║   ██║██║   ██║██║  ██║                      
        ██║██║     ╚██████╔╝╚██████╔╝██████╔╝                      
        ╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚═════╝                       
                                                                
        ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗
        ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
        ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   
        ██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
        ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   
        ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
                                                                
         █████╗ ██████╗ ██╗                                        
        ██╔══██╗██╔══██╗██║                                        
        ███████║██████╔╝██║                                        
        ██╔══██║██╔═══╝ ██║                                        
        ██║  ██║██║     ██║                                        
        ╚═╝  ╚═╝╚═╝     ╚═╝      
    
    Copyright (C) <2024>  <Luiz Gabriel Magalhães Trindade>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

#Importação de bibliotecas
import requests, json
from os import system, name as nameOS

#Variáveis
#Variáveis do cliente
clientId        = ""
clientSecret    = ""
#variáveis importantes
accessToken     = ""
merchantID      = ""
catalogID       = ""

#Função para conseguir o merchant ID
def getMerchantList():
    # URL da API
    url = "https://merchant-api.ifood.com.br/merchant/v1.0/merchants"

    # Cabeçalhos da requisição
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    # Fazendo a requisição GET
    response = requests.get(
        url, 
        headers=headers
    )

    # Verificando a resposta
    if response.status_code == 200:
        print("Dados recebidos com sucesso:")
        # print(response.json())

        for element in response.json():
            for key in element:
                size = int(13 - len(key))
                print(f"{key}{' '*size} ----> {element[key]}")
            print("-"*60)
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)

#Função para selecionar o Merchant ID com o qual será trabalhado
def selectMerchantID():
    global merchantID

    getMerchantList()
    merchantID = input("Merchant ID: ")
    print("Merchant selecionado com sucesso!")

#Função para conseguir um  código de acesso(access token)
def getAccessToken():
    global accessToken, clientId, clientSecret
    # URL do endpoint de autenticação
    url = "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token"

    # Dados do formulário
    data = {
        "grantType": "client_credentials",
        "clientId": f"{clientId}",
        "clientSecret": f"{clientSecret}",
        "authorizationCode": "",
        "authorizationCodeVerifier": "",
        "refreshToken": ""
    }

    # Configuração dos cabeçalhos da requisição
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Fazendo a requisição POST
    response = requests.post(
        url, headers=headers, 
        data=data
    )

    # Verificando a resposta
    if response.status_code == 200:
        #print("Token obtido com sucesso!")
        #print("Resposta:", response.json())
        responseJson = response.json()
        accessToken = responseJson.get("accessToken")

    else:
        print(f"Falha na autenticação. Código de status: {response.status_code}")
        print("Resposta:", response.json())

#Função para adicionar um produto novo
def adicionarProduto():
    global accessToken, merchantID

    # URL do endpoint da API do iFood
    url = "https://merchant-api.ifood.com.br/catalog/v2.0/merchants/4c7e54cd-3062-4b63-a53d-d63c9bccddbe/products"

    #Variáveis de interação
    nomeProduto         = input("Nome do produto: ")
    descricaoProduto    = input("Descrição para o produto: ")
    infoProduto         = input("Informação adicional: ")
    codigoExterno       = input("Código externo: ")
    imagem64            = input("Imagem em base64: ")

    # Dados do produto
    product_data = {
        "name": f"{nomeProduto}",
        "description": f"{descricaoProduto}",
        "additionalInformation": f"{infoProduto}",
        "externalCode": f"{codigoExterno}",
        "image": f"{imagem64}",
        "serving": "SERVES_1",
        "dietaryRestrictions": ["ORGANIC", "VEGAN"],
        "ean": "1234567890123",
        "weight": {
            "quantity"  : 500,
            "unit"      : "g"
        },
        "multipleImages": []
    }

    # Configuração dos cabeçalhos da requisição
    headers = {
        "Authorization" : f"Bearer {accessToken}",
        "Content-Type"  : "application/json",
        "Accept"        : "application/json"
    }

    # Fazendo a requisição POST
    response = requests.post(
        url.format(merchantId=merchantID), 
        headers=headers, 
        data=json.dumps(product_data)
    )

    # Verificando a resposta
    if response.status_code == 201:
        print("\nProduto criado com sucesso!")
        #print("Resposta:", response.json())
    else:
        print(f"Falha ao criar produto. Código de status: {response.status_code}")
        print("Resposta:", response.json())

#Função para listar produtos
def listarProdutos():    
    # URL da API
    url = f"https://merchant-api.ifood.com.br/catalog/v2.0/merchants/{merchantID}/products"
    params = {
        'limit': 200,
        'page': 0
    }

    # Cabeçalhos da requisição
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {accessToken}'
    }

    # Fazendo a requisição GET
    response = requests.get(
        url, 
        headers=headers, 
        params=params
    )

    # Verificando o status e conteúdo da resposta
    if response.status_code == 200:
        data = response.json()
        print("Dados recebidos com sucesso:\n")
        # print(data)
        for item in data["elements"]:
            for key in item:
                size = int(21 - len(key))
                print(f"{key}{' '*size} ----> {item[key]}")
            print("-"*60)
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)

#Função para listar categorias
def listarCatalogos():
    global accessToken
    # URL do endpoint
    url = f"https://merchant-api.ifood.com.br/catalog/v2.0/merchants/{merchantID}/catalogs"
    # Cabeçalhos da requisição
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    # Fazendo a requisição GET
    response = requests.get(
        url, 
        headers=headers
    )

    # Verificando a resposta
    if response.status_code == 200:
        print("Dados recebidos com sucesso!")
        #print(response.json()) 
        for element in response.json():
            for key in element:
                size = int(10 - len(key))
                print(f"{key}{' '*size} ----> {element[key]}")
            print("-"*60)
    else:
        print(f"Erro ao fazer requisição: {response.status_code}")
        print(response.text)


def selecionarCatalogo():
    global catalogID
    catalogID = input("Catálogo ID: ")

#Função para criar um item, que é associar um produto a uma categoria
def criarItem():
    global merchantID, accessToken
    
    # URL do endpoint para criar um item
    url = f"https://merchant-api.ifood.com.br/catalog/v2.0/merchants/{merchantID}/items"
    headers = {
        "Accept"        : "application/json",
        "Content-Type"  : "application/json",
        "Authorization" : f"Bearer {accessToken}",
    }

    # Coletar dados do usuário
    idProduto           = input("ID do produto: ")
    idCategoria         = input("ID da categoria: ")
    nomeProduto         = input("Nome que o produto será vendido: ")
    externalCode        = input("External code: ")
    aditionalInfo       = input("Informação adicional: ")
    descricaoProduto    = input("Descrição: ")
    precoProduto        = float(input("Preço (R$): "))

    # Dados do item (exemplo)
    data = {
        "item": {
            "id": idProduto, 
            "type": "DEFAULT",  
            "categoryId": idCategoria,  
            "status": "AVAILABLE",  
            "price": {
                "value": precoProduto,  
                "originalValue": precoProduto,  
                "scalePrices": [] 
            },
            "externalCode": "",  
            "index": 0,  
            "productId": idProduto,  
            "shifts": [
                {
                    "startTime": "00:00",
                    "endTime": "23:59",
                    "monday": "true",
                    "tuesday": "true",
                    "wednesday": "true",
                    "thursday": "true",
                    "friday": "true",
                    "saturday": "true",
                    "sunday": "true"
                }
            ],
            "tags": [
                "FROSTY"
            ],  
            "contextModifiers": []  
        },
        "products": [
            {
                "id": idProduto,
                "name": nomeProduto,
                "externalCode": externalCode,  
                "description": descricaoProduto,
                "additionalInformation": aditionalInfo,
                "imagePath": "",
                "ean": "1234567890123",
                "serving": "SERVES_1",
                "dietaryRestrictions": ['VEGAN', 'ORGANIC'],
                "tags": [
                    "FROSTY"
                ],
                "quantity": 0,
                "optionGroups": []
            }
        ],
        "optionGroups": [],
        "options": []
    }

    # Criando o item
    response = requests.put(
        url, 
        headers=headers, 
        json=data
    )

    print(response.status_code)

    if response.status_code == 200:
        print("Item criado com sucesso e associado às categorias!")
    else:
        print(f"Erro ao criar item: {response.status_code}")
        print(response.text)


def listarCategorias():
    global merchantID, accessToken, catalogID
    # URL para listar categorias
    url = f"https://merchant-api.ifood.com.br/catalog/v2.0/merchants/{merchantID}/catalogs/{catalogID}/categories?includeItems=true"
    
    # Cabeçalhos da requisição
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "accept": "application/json"
    }
    
    # Enviando a requisição GET
    response = requests.get(
        url, 
        headers=headers
    )
    
    # Verificando a resposta
    if response.status_code == 200:
        print("Categorias listadas com sucesso!")
        #print(response.json())
    
        for element in response.json():
            for key in element:
                size = int(12 - len(key))
                print(f"{key}{' '*size} ----> {element[key]}")
            print("-"*60)

    else:
        print(f"Erro ao listar categorias: {response.status_code}")
        print(response.text)

#função de limpra a tela dependendo do tipo de sistema operacional
def limparTela():
    if nameOS == "nt":
        system("cls")
    elif nameOS == "posix":
        system("clear")
    else:
        pass

#Função principal
def main():
    global clientId, clientSecret

    clientId        = input("Informe o clientID: ")
    clientSecret    = input("Informe o clientSecret: ")
    limparTela()

    while True:
        getAccessToken()

        print("""\n

        ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗             
        ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝             
        ███████╗██║██╔████╔██║██████╔╝██║     █████╗               
        ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝               
        ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗             
        ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝             
                                                                
        ██╗███████╗ ██████╗  ██████╗ ██████╗                       
        ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗                      
        ██║█████╗  ██║   ██║██║   ██║██║  ██║                      
        ██║██╔══╝  ██║   ██║██║   ██║██║  ██║                      
        ██║██║     ╚██████╔╝╚██████╔╝██████╔╝                      
        ╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚═════╝                       
                                                                
        ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗
        ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
        ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   
        ██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
        ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   
        ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
                                                                
         █████╗ ██████╗ ██╗                                        
        ██╔══██╗██╔══██╗██║                                        
        ███████║██████╔╝██║                                        
        ██╔══██║██╔═══╝ ██║                                        
        ██║  ██║██║     ██║                                        
        ╚═╝  ╚═╝╚═╝     ╚═╝      

        Copyright (C) <2024>  <Luiz Gabriel Magalhães Trindade>

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
        """)

        print("-"*60)
        print("""
        Adicionar produto    ---->   1
        Listar produtos      ---->   2
        Listar merchants     ---->   3
        Selecionar merchant  ---->   4
        Listar catálogos     ---->   5
        Selecionar catálogo  ---->   6
        Listar categorias    ---->   7
        Criar um item        ---->   8
        Sair                 ---->   e
        """)
        print("-"*60)

        #Código de operações
        codigo = input("        * Digite um código de operação: ")

        if codigo == "e":
            print("""\n
        
        ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗             
        ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝             
        ███████╗██║██╔████╔██║██████╔╝██║     █████╗               
        ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝               
        ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗             
        ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝             
                                                                
        ██╗███████╗ ██████╗  ██████╗ ██████╗                       
        ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗                      
        ██║█████╗  ██║   ██║██║   ██║██║  ██║                      
        ██║██╔══╝  ██║   ██║██║   ██║██║  ██║                      
        ██║██║     ╚██████╔╝╚██████╔╝██████╔╝                      
        ╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚═════╝                       
                                                                
        ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗
        ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
        ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   
        ██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
        ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   
        ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
                                                                
         █████╗ ██████╗ ██╗                                        
        ██╔══██╗██╔══██╗██║                                        
        ███████║██████╔╝██║                                        
        ██╔══██║██╔═══╝ ██║                                        
        ██║  ██║██║     ██║                                        
        ╚═╝  ╚═╝╚═╝     ╚═╝            

        Copyright (C) <2024>  <Luiz Gabriel Magalhães Trindade>

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.\n
            """)
            exit()

        elif codigo == "1":
            if len(merchantID) == 0:
                selectMerchantID()
            adicionarProduto()

        elif codigo == "2":
            if len(merchantID) == 0:
                selectMerchantID()
            listarProdutos()

        elif codigo == "3":
            getMerchantList()

        elif codigo == "4":
            selectMerchantID()

        elif codigo == "5":
            if len(merchantID) == 0:
                selectMerchantID()
            listarCatalogos()

        elif codigo == "6":
            selecionarCatalogo()

        elif codigo == "7":
            if len(merchantID) == 0:
                selectMerchantID()
            listarCategorias()

        elif codigo == "8":
            if len(merchantID) == 0:
                selectMerchantID()
            criarItem()

        else:
            pass
        
        input("Precione ENTER para continuar...")

        #limparTela()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        limparTela()
        print("""\n
        
        ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗             
        ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝             
        ███████╗██║██╔████╔██║██████╔╝██║     █████╗               
        ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝               
        ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗             
        ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝             
                                                                
        ██╗███████╗ ██████╗  ██████╗ ██████╗                       
        ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗                      
        ██║█████╗  ██║   ██║██║   ██║██║  ██║                      
        ██║██╔══╝  ██║   ██║██║   ██║██║  ██║                      
        ██║██║     ╚██████╔╝╚██████╔╝██████╔╝                      
        ╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚═════╝                       
                                                                
        ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗
        ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
        ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   
        ██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
        ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   
        ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
                                                                
         █████╗ ██████╗ ██╗                                        
        ██╔══██╗██╔══██╗██║                                        
        ███████║██████╔╝██║                                        
        ██╔══██║██╔═══╝ ██║                                        
        ██║  ██║██║     ██║                                        
        ╚═╝  ╚═╝╚═╝     ╚═╝      

        Copyright (C) <2024>  <Luiz Gabriel Magalhães Trindade>

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.\n
        """)
        exit()
