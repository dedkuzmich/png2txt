# Png2txt
Assume that you already have ShareX that saves all screenshots in `C:\Users\lol19\Pictures\ShareX`.
This folder should contain subfolders `2023-08`, `2023-09`, `...`, `2023-12` with PNG files inside.

Take a screenshot in Sharex with hotkey Win + Shift + E.



## 1. Install Tesseract 
Install [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) in `C:\Program Files\Tesseract-OCR`.
Add `C:\Program Files\Tesseract-OCR` to your system PATH. You should be able to run Tesseract from anywhere.

Use `tesseract.exe` (run PowerShell as admin):
```ps
PS C:\Users\lol19\Desktop> tesseract "IMAGE.PNG" "Text" -l ukr+eng
```
File Text.txt will contain a text from "IMAGE.PNG".



## 2. Install Png2txt
Copy this repo in `C:\Users\lol19\Pictures\ShareX\png2txt`.

Install all dependencies:
```ps
PS C:\Users\lol19\Pictures\ShareX\png2txt\bin> pip install -r requirements.txt
```

Ensure that `png2txt.py` works:
```ps 
PS C:\Users\lol19\Pictures\ShareX\png2txt\bin> python png2txt.py -h 
```

Compile `png2txt.py`:
```ps
PS C:\Users\lol19\Pictures\ShareX\png2txt\bin> pyinstaller --onefile png2txt.py
```

Ensure that `dist` folder has been created and it contains file `png2txt.exe`:
```ps
PS C:\Users\lol19\Pictures\ShareX\png2txt\bin\dist> png2txt.exe -h
```

Add `C:\Users\lol19\Pictures\ShareX\png2txt\bin\dist` to your system PATH. You should be able to run Png2txt from anywhere.


## 3. Usage examples
You can: 
* Set languages:
```ps
PS C:\Users\lol19\Desktop> png2txt -l "eng"
PS C:\Users\lol19\Desktop> png2txt -l "ukr+eng"
```

* Set folder and PNG:
```ps
PS C:\Users\lol19\Desktop> png2txt -d "C:\Users\lol" -f "kek.png"
```

* Use verbose mode:
```ps
PS C:\Users\lol19\Desktop> png2txt -v
```

* Use default params (last modified ShareX folder + last created PNG):
```ps
PS C:\Users\lol19\Desktop> png2txt
```
