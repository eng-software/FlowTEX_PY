''' 
  TesteFlowTEX.py

    Created: 23/04/2021 12:30:00
    Author: henrique.coser
'''
import serial, serial.tools.list_ports, time
import TexNet

# Get the COM port
Ports = serial.tools.list_ports.comports()

if(len(Ports) == 0):
    print("[ERROR] Nenhuma porta serial encontrada!")
    exit()

#Cria o menu das portas seriais
TargetPort = None
optionNumber = 1
print("Portas seriais disponíveis:")
for Port in Ports:
    StringPort = str(Port)
    print("  -> ",optionNumber," : Porta: {}".format(StringPort))
    optionNumber = optionNumber + 1
    
print("Digite o numero da opção para selecionar a porta serial:")
serialOpt = int(input()) - 1

#Extrai o nome da porta em função da opção selecionada
TargetPort = str(Ports[serialOpt]).split(" ")[0]

#Instancia um objeto TexNET abrindo a porta serial selecionada
flowTex = TexNet.TexNet(TargetPort)
nleituras = 0

#Vai imprimir a cada 0,5s as informações lidas do sensor
while(True):    
    try:        
        print("-------------------------------------------------------------")
        print("Leitura FlowTEX nº",nleituras)
        print(flowTex.getVersion())
        print(flowTex.getSerialNumber())
        print(flowTex.getModel())
        print("{:10.2f}".format(flowTex.getFlow()),"Sccm")
        print("{:10.2f}".format(flowTex.getTemperature()),"°C")
        print("-------------------------------------------------------------")
        print(" ")
        nleituras = nleituras + 1
    except:
        pass

    time.sleep(0.5)

