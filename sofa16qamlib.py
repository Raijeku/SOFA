import numpy as np
def modulate(inputs): #Entran los indices (0,15) y retorna los símbolos (coordenadas)
    modulated=[]
    dic_index_to_syms={'0':-3-3j,'1':-3-1j,'2':-3+3j,'3':-3+1j, #Código Grey
                       '4':-1-3j,'5':-1-1j,'6':-1+3j,'7':-1+1j,
                       '8':3-3j,'9':3-1j,'10':3+3j,'11':3+1j,
                       '12':1-3j,'13':1-1j,'14':1+3j,'15':1+1j}
    syms_str=list(map(str,inputs))
    for i in range (0,len(inputs)):
        modulated.append(dic_index_to_syms[syms_str[i]])    
    
    return(np.array(modulated))
def demodulate(inputs): #Entran los símbolos (coordenadas) y retorna los indices (0,15)
    A_mc=np.array([-3-3j,-3-1j,-3+3j,-3+1j,
                   -1-3j,-1-1j,-1+3j,-1+1j,
                    3-3j, 3-1j, 3+3j, 3+1j,
                    1-3j, 1-1j, 1+3j, 1+1j])
    corrected=[]
    for j in np.arange(0,len(inputs),1):
            minp=np.abs(A_mc-inputs[j])
            indexm=list(minp).index(np.min(minp))
            corrected.append(A_mc[indexm])
            
    demodulated=[]
    dic_syms_to_index={'(-3-3j)':0,'(-3-1j)':1,'(-3+3j)':2,'(-3+1j)':3,
                       '(-1-3j)':4,'(-1-1j)':5,'(-1+3j)':6,'(-1+1j)':7,
                       '(3-3j)':8,'(3-1j)':9,'(3+3j)':10,'(3+1j)':11,
                       '(1-3j)':12,'(1-1j)':13,'(1+3j)':14,'(1+1j)':15}
    syms_str=list(map(str,corrected))
    for i in range (0,len(corrected)):
        demodulated.append(dic_syms_to_index[syms_str[i]])    
    
    return(demodulated)

def noiselnl(syms_tx,SNR,phin,rot): #Agregación de ruido linea y no lineal
    
    #syms_tx: señal sin ruido
    #SNR: relación señal a ruido (cantidad de ruido lineal) (0,~40)
    #phin: ruido de fase (0, ~10)
    #rot: rotación a la constelación en grados
    
    num_sym=len(syms_tx)#Cantidad de simbolos de la constelación
    sign_power = np.var(syms_tx)  #Se calcula la potencia de la señal ideal #Relación señal-a-ruido deseada
    Es_No = 10**(SNR/10.0)        #Relación señal-a-ruido en decibeles
    N0 = sign_power/Es_No         #Potencia del ruido
    sigma = np.sqrt(N0/2)         #Distribución gausiana siguiendo la potencia del ruido
    ni = np.random.normal(scale= sigma, size = len(syms_tx)) #Ruido aleatorio para la componente In-Phase
    nq = np.random.normal(scale= sigma, size = len(syms_tx)) #Ruido aleatorio para la componente Quadrature
    
    n = ni + 1j*nq #Ruido total
    sig_rx=syms_tx+n
    
    phi = phin*(np.pi/180)*np.random.randn(1,num_sym)  #Ruido de fase
    sig_no = sig_rx*np.exp(1j*phi)
    
    phn=(rot*np.pi)/180
    sig_no=sig_no*np.exp(1j*phn)  #rotación
    
    return(sig_no[0])

def biterr(rx, tx): #Entran los indices (0,15) y retorna cantidad de bits diferentes (errores)
    rx_bit=[]
    tx_bit=[]
    for i in range (0,len(rx)):
        rx_bit.append(f'{rx[i]:04b}')
        tx_bit.append(f'{tx[i]:04b}')
        
    str_rx=''.join(list(map(str,rx_bit)))
    str_tx=''.join(list(map(str,tx_bit)))
    return(sum ( str_rx[i] != str_tx[i] for i in range(len(str_rx))))