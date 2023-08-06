import re

class validatorPCTE(): 
    def senha(self, senha1, senha2):
        """
            DESCRIPTIONS:
                -> método para validar o campo SENHA
        """
        if len(senha1) < 6:
            return False
        if senha1 != senha2:
            return False
        if len(senha1) > 20:
            return False
        if senha1.isdigit():
            return False
        if senha1 == senha2:
            return True


    def cpf(self, cpf):
        """
            DESCRIPTIONS:
                -> método para validar CPF, através do cálculo disponibilizado pelo Ministério da Fazenda
        """
        # testes
        if (len(cpf) > 11 or len(cpf) < 11):
            print(f"CPF inválido pela quantidade {len(cpf)} de caracteres.")
            return False
        else:
            cont = 0
            for i in cpf[1:]:
                if i == cpf[0]:
                    cont += 1
            if cont == 10:
                print("CPF inválido!")
                return False
                
        # validação do primeiro dígito
        cont = 10
        resultado = 0
        for i in cpf[0:9]:
            resultado += int(i) * cont # realiza a multiplicação dos numeros, exceto o que vem após o - 
            cont -= 1
        resultado = resultado * 10 % 11 # resto do calculo tem que ser igual o penultimo numero do cpf
        if resultado != int(cpf[9]): # verifica se o numero é diferente do penultimo número do cpf
            print("CPF inválido!")
            return False
        else: # validação do segundo dígito
            cont = 11
            resultado = 0
            for i in cpf[0:10]: 
                resultado += int(i) * cont # realiza a multiplicação dos números, exceto o ultimo número 
                cont -= 1
            resultado = resultado * 10 % 11 # resto do calculo tem que ser igual o ultimo numero do cpf
            if resultado == int(cpf[10]): # verifica se o numero é igual do penultimo número do cpf
                return True
            else:
                print("CPF inválido!") 
                return False # retorna False se for diferente
    

    def telefone(self, numero):
        """
            DESCRIPTIONS:
                -> método para validar número de telefone com a ajuda da biblioteca RE
        """
        padrao = "([1-9]{2})?([0-9]{2})([0-9]{4,5})([0-9]{4})" # número padrão de telefone
        resultado = re.search(padrao, numero) # realiza a comparação se o parâmetro 'numero' se encaixa com a variavel 'padrao'
        if not resultado: # retorna um valor booleano True or False
            print("número de telefone inválido.")
            return False
        #print('+{}({}){}-{}'.format(resultado.group(1),  resultado.group(2), resultado.group(3), resultado.group(4)))
