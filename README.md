# Run imagee

## CPU image
Om de image te starten zonder gpu support kun je gebruik maken van het volgende commando 
```bash
docker run -p 8888:8888 -v /{LOCATIE_VAN_INGEVULDE_OPGAVEN}:/usr/ml-opgaven michelgerding/ml-opgave:cpu-latest
```

## GPU 
Voor support met de gpu moet de flag aangpast worden naar `:gpu-latest` en de parameter `--gpus=all` meegegven worden. dat resulteert in het volgende commando
hiervoor moeten cuda supported drivers geinstaleerd zijn.
```bash
docker run \
  -p 8888:8888 \
  -v /{LOCATIE_VAN_INGEVULDE_OPGAVEN}:/usr/ml-opgaven \
  --gpus=all \
  michelgerding/ml-opgave:gpu-latest
```

# Build image 
de image wordt automatisch gebuild op bij een push naar de main branch. 
Dit kan handmatig gedaan worden met het onderstaande commando. op basis van de build argument processor kan gekozen 
worden tussen cpu en gpu support.

```bash
docker build --build-args processor={cpu|gpu} .
```