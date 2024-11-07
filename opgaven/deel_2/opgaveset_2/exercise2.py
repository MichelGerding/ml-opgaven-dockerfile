# MACHINE LEARNING OPGAVE WEEK 2

import numpy as np
from random import randint
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sys
import pickle

from uitwerkingen import *

# Helperfuncties die nodig zijn om de boel te laten werken
# Hier hoef je niets aan te veranderen, maar bestudeer de 
# code om een beeld te krijgen van de werking hiervan.

def initialize_random_weights(in_conn, out_conn):
    W = np.zeros((out_conn, 1 + out_conn))
    epsilon_init = 0.12
    W = np.random.rand(out_conn, 1+in_conn) * 2 * epsilon_init - epsilon_init
    return W

def display_data(X):
    m,n = X.shape
    for idx in range(0, m):
        plt.subplot(5, 5, idx+1)
        x = X[idx,:].reshape(20,20)
        plt.tick_params(which='both',left=False, bottom=False, top=False, labelleft=False, labelbottom=False)
        plt.imshow(x, cmap='gray', interpolation='nearest');

    plt.show()

itr = 1
def callbackF(Xi):
    global itr
    print (f"iteration {itr}")
    itr += 1


def nn_cost_function(Thetas, X, y):
    global input_layer_size, hidden_layer_size, num_labels
    size = hidden_layer_size * (1+input_layer_size) # +1 want de bias-node zit wel in de matrix
    Theta2 = Thetas[:size].reshape(hidden_layer_size, input_layer_size+1)
    Theta3 = Thetas[size:].reshape(num_labels, hidden_layer_size+1)
    J = compute_cost(Theta2, Theta3, X, y)
    grad1, grad2 = nn_check_gradients(Theta2, Theta3, X, y)
    return J, np.concatenate( (grad1.flatten(), grad2.flatten()) ) 


#Laden van de data en zetten van de variabelen.
with open ('week2_data.pkl','rb') as f:
    data = pickle.load(f)

X,y = data['X'], data['y']

#Zetten van belangrijke variabelen
m,n = X.shape # aantal datapunten in de trainingsset
input_layer_size  = 400;  # 20x20 input plaatjes van getallen
hidden_layer_size = 25;   # verborgen laag van 25 units
num_labels = 10;          # 10 labels, 1 tot en met 10
                          # let op: '0' wordt opgeslagen als label 10.


# ========================  OPGAVE 1 ======================== 
rnd = randint(0, X.shape[0])
print (f"Tekenen van data op regel {rnd}")
if (len(sys.argv)>1 and sys.argv[1]=='skip') :
    print ("Slaan we over")
else:
    hyp = y[rnd]
    if (hyp==10): hyp=0
    print (f"Dit zou een {hyp} moeten zijn.")
    plot_number(X[rnd,:])

input ("Druk op Return om verder te gaan...") 


# ========================  OPGAVE 2a ======================== 
print ("")
print ("Sigmoid-functie met een relatief groot negatief getal zou bijna 0 moeten zijn")
print (f"Sigmoid van -10 = {sigmoid(-10)}")

print ("Sigmoid-functie van 0 zou 0,5 moeten zijn.")
print (f"Sigmoid van 0 = {sigmoid(0)}")

print ("Sigmoid-functie met een relatief groot positief getal zou bijna 1 moeten zijn")
print (f"Sigmoid van 10 = {sigmoid(10)}")

print ("Simoid aangeroepen met 1×3 vector [-10, 0, 10]")
print (sigmoid(np.matrix( [-10, 0, 10] )))
print ("Simoid aangeroepen met 3×1 vector [-10, 0, 10]")
print (sigmoid(np.matrix( ([-10], [0], [10]) )))

input ("Druk op Return om verder te gaan...") 

# ========================  OPGAVE 2b ======================== 
print ("")
print ("Aanroepen van de methode predict_number met de y-vector")
print ("en het weergeven van de dimensionaliteit van het resultaat")
matr = get_y_matrix(y, m)
print (matr.shape)
print ("Dit zou (5000,10) moeten zijn.")
input ("Druk op Return om verder te gaan.")


# ========================  OPGAVE 2c ======================== 
print("")
print ("Zetten van initiële waarden van de Theta's.")
Theta2 = initialize_random_weights(input_layer_size, hidden_layer_size)
Theta3 = initialize_random_weights(hidden_layer_size, num_labels)

print ("Aanroepen van de methode predict_number")
pred = np.argmax(predict_number(Theta2,Theta3,X), axis=1).reshape(m,1)
cost = compute_cost(Theta2, Theta3, X, y)

print (f"De kosten die gemoeid zijn met de huidige waarden van Theta2 en Theta3 zijn {cost}")
print ("Dit zou zo rond de 7 moeten liggen.")
acc = np.count_nonzero([pred - y == 0])
print (f"Correct geclassificeerd: {acc}")
print (f"De huidige accuratessse van het netwerk is {100 * acc/ m} %")
input ("Druk op Return om verder te gaan.")

# ========================  OPGAVE 3 ======================== 
print ("")
print ("Aanroepen van de methode sigmoid_gradient met de waarden [-1, -0.5, 0, 0.5, 1 ]")
print (sigmoid_gradient(np.array([ [-1, -0.5, 0, 0.5, 1 ] ])))
print ("Dit zou als resultaat de volgende lijst moeten hebben")
print ("[ 0.19661193  0.23500371  0.25  0.23500371  0.19661193]")
input ("Druk op Return om verder te gaan...")

print ("")
print ("Aanroepen van de methode nn_check_gradients met initiële waarden van de Theta's.")
g1, g2 =  nn_check_gradients(Theta2, Theta3, X, y)
print (f"De totale som van de eerste gradiënt-matrix is {sum(g1)}")
print (f"De totale som van de tweede gradiënt-matrix is {sum(g2)}")
input ("Druk op Return om verder te gaan...")

# ========================  OPGAVE 4 ======================== 

init_params = np.concatenate( (Theta2.flatten(), Theta3.flatten()) )
args = (X, y)
print ("")
print ("Gebruik scipy.optimize.minimize om het netwerk te trainen...")
res = minimize(nn_cost_function, init_params, args=args, method='CG', callback=callbackF, jac=True, options={'maxiter':30,'disp':True})
size = hidden_layer_size * (input_layer_size+1) #voor de bias-node die wel in de matrix zit maar niet geplot moet worden
res_Theta2 = res['x'][:size].reshape(hidden_layer_size, input_layer_size+1)
res_Theta3 = res['x'][size:].reshape(num_labels, hidden_layer_size+1)

print ("Training compleet. ")

cost = compute_cost(res_Theta2, res_Theta3, X, y) 
print (f"De kosten die gemoeid zijn met de huidige waarden van Theta2 en Theta3 zijn {cost}")
print ("Dit zou een stuk lager moeten zijn dan in het begin.")

pred = np.argmax(predict_number(res_Theta2,res_Theta3,X), axis=1)+1
pred = pred.reshape(m,1)
acc = np.count_nonzero([pred - y == 0])
print (f"correct geclassificeerd: {acc}")
print (f"De huidige accuratessse van het netwerk is {100 * acc/ m} %")
print ("Dat zou een stuk hoger moeten zijn dan in het begin.")
print ("Plotten van de waarden van de gewichten in de verborgen laag (hidden layer)")

display_data(res_Theta2[:,1:]) 
