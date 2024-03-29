# Png2txt
Png2txt is a wrapper over the Tesseract-OCR. It’s designed to extract text from the latest screenshot made with ShareX. 


## Before we proceed
Assume that you already have [ShareX](https://getsharex.com/) that saves screenshots in `%USERPROFILE%\Pictures\ShareX`.
This folder should contain subfolders `2023-08`, `2023-09`, `...`, `2023-12` with PNG files inside.

Take a screenshot in Sharex with hotkey Win + Shift + E.


## 1. Install Tesseract
Install [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) in `C:\Program Files\Tesseract-OCR`.
Add `C:\Program Files\Tesseract-OCR` to your system PATH. You should be able to run Tesseract from anywhere.

Use `tesseract.exe` (run PowerShell as admin):
```ps
PS C:\Users\lol19\Desktop> tesseract "IMAGE.png" "EXAMPLE" -l ukr+eng
```
File "EXAMPLE.txt" will contain an extracted text from "IMAGE.png".


## 2. Install Png2txt
Copy this repo to `%USERPROFILE%\Pictures\ShareX\png2txt`.

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

Add `%USERPROFILE%\Pictures\ShareX\png2txt\bin\dist` to your system PATH. You should be able to run Png2txt from anywhere.


## 3. Usage examples
You can: 
* Set languages:
```ps
PS C:\Users\lol19\Desktop> png2txt -l "eng"
PS C:\Users\lol19\Desktop> png2txt -l "ukr+eng"
```

* Set folder and PNG:
```ps
PS C:\Users\lol19\Desktop> png2txt -d "C:\abc\def" -f "kek.png"
```

* Use verbose mode:
```ps
PS C:\Users\lol19\Desktop> png2txt -v
```

* Use default params (last modified ShareX folder + last created PNG):
```ps
PS C:\Users\lol19\Desktop> png2txt
```

## 4. Add more languages
You can find language packs [here](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files/1467229f37bb073850344fc4c1d06b7b199e4f73).
Copy .traineddata file to `C:\Program Files\Tesseract-OCR\tessdata`.


