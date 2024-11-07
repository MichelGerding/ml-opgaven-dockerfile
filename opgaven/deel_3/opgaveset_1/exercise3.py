import matplotlib.pyplot as plt
import sys

from uitwerkingen import *


# HELPER FUNCTIES
def plot_matrix(data):
    plt.figure()
    plt.matshow(data)
    plt.show()

print ("Laden van de data...")
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()
labels = ['T-shirt/topje', 'Broek', 'Pullover', 'Jurk', 'Jas', 'Sandalen', 'Shirt', 'Sneaker', 'Tas', 'Lage laars'] 
print ("Done.")

# ===============  OPGAVE 0 ======================
print ("")
print ("Ophalen van het opgeslagen model")

model = load_model()

# ===============  OPGAVE 1 ======================
print ("Bepalen van de confusion matrix van het getrainde netwerk.")

pred = np.argmax(model.predict(test_images), axis=1)
conf_mtx = conf_matrix(test_labels, pred)

print ("De confusion matrix:") 
print (conf_mtx)

if (len(sys.argv)>1 and sys.argv[1]=='skip') :
    print ("Tekenen slaan we over")
else:
    plot_matrix(conf_mtx)
  

print ("Bepalen van de tp, tn, fp, fn")
metrics = conf_els(conf_mtx.numpy(), labels)
print (metrics)
print ("Bepalen van de scores:")
scores = conf_data(metrics)
print (scores)

print ("Klaar... 💪")