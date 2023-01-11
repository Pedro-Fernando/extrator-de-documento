# ocr
# extrator-de-documento

Download dados de treinamento do tesseract
~~~cmd
wget -O ./tessdata/por.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata?raw=true
wget -O ./tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata?raw=true
~~~
deve ser instalado a linguagem em português
~~~cmd
 sudo apt-get install tesseract-ocr-por
~~~