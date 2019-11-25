# Busca binária

# Lista base
lista_numerica = [0,1,2,3,4,5,6,7,8,9,10,11,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

# Função que encontra, caso existir, o indice do objeto procurado
def busca_binaria(lista_numerica, numero_a_ser_buscado):
    primeiro = 0
    ultimo = len(lista_numerica) -1

    while (primeiro <= ultimo) :
        meio = ((primeiro + ultimo) // 2)

        if (numero_a_ser_buscado == lista_numerica[meio]) :
            return lista_numerica.index(numero_a_ser_buscado) 
        else :
            if (numero_a_ser_buscado < lista_numerica[meio]) :
                ultimo = meio - 1
            else :
                primeiro = meio + 1
    return "Não encontrado"
            
print(lista_numerica)
entrada_numero_busca = int(input("Digite um número a ser procurado na lista acima :\n"))
print("Index : ", busca_binaria(lista_numerica, entrada_numero_busca))
