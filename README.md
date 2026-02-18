# stepmaniamaker

ffmpeg
```
winget install Gyan.FFmpeg
```


## cmd
### install
```
python -m venv .venv &&
.venv\Scripts\activate &&
pip install -r requirements.txt
```

### command
```
.venv\Scripts\activate &&
python main.py ^
    --song "Cheap Thrills" ^
    --artist "Sia" ^
    --has-video 1 ^
    --url "https://youtu.be/BKfXlF3t1Ic?si=HohJBYEEvak4wXZC" ^
    --output "C:\Games\StepMania 5\Songs\Nightcores" 
```

## bash

### install
```
python -m venv .venv &&
source .venv/Scripts/activate &&
pip install -r requirements.txt
```

### command
```
source .venv/Scripts/activate &&
python main.py \
    --song "Cheap Thrills" \
    --artist "Sia" \
    --has-video 1 \
    --url "https://youtu.be/BKfXlF3t1Ic?si=HohJBYEEvak4wXZC" \
    --output "C:\Games\StepMania 5\Songs\Nightcores" 
```