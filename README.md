# Multiversion Timestamp Ordering Protocol

## How To Run
Jalankan
```
run.bat
```
### Test Case
Terdapat 3 skenario yang diuji pada laporan
1. Read, Write Normal (tc1.txt)
2. Rollback (tc2.txt)
3. Overwrite dan Cascading Rollback (tc3.txt)

Setiap file _test case_ terdapat di folder in, setiap skenario dapat diuji dengan mengubah file _test case_ pada run.bat

### run.bat
```
python src/main.py in/<nama-file-tc>.txt
```
atau dapat menjalankan langsung perintah di atas pada terminal
## Link
https://github.com/darwix/mvto
