1. Lets analyze file
```
file hi.docm
```

```
strings "qupiya{" hi.docm
```

2. Convert **.docm** to **.zip** and then unzip to one folder 

 * Use **nano** to convert file
 * Use **unzip** to unzip and add **-d <dir_name>**
```
unzip hi.zip -d unzip
```

3. Fast searching with **grep**

```
grep -r "qupiya{" unzip
```
grep: unzip/word/vbaProject.bin: binary file matches

Flag founded on this way but grep cannot read binary.

4. Finish

```
strings unzip/word/vbaProject.bin
```
Flag: **qupiya{korgalgan_macros}**

