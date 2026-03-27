import soma
import subtrai
import multiplica
import divide

n1 = float(input("Digite o primeiro número: "))
n2 = float(input("Digite o segundo número: "))
operador = input("Digite a operação (+, -, *, /): ")

if operador == "+":
    resultado = soma.somaf(n1, n2)
    print("Resultado:", resultado)

elif operador == "-":
    resultado = subtrai.subtraif(n1, n2)
    print("Resultado:", resultado)

elif operador == "*":
    resultado = multiplica.multiplicaf(n1, n2)
    print("Resultado:", resultado)

elif operador == "/":
    resultado = divide.dividef(n1, n2)
    print("Resultado:", resultado)
    
elif operador == "**":
    resultado = potencia.potenciaf(n1, n2)
    print("Resultado:", resultado)
    
else:
    print("Operador inválido")
