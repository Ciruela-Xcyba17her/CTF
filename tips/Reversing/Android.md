# Tips related to Android

## apktools
APKの展開  
`apktool d XXX.apk`  
APKの作成  
`apktool e -o XXX.apk APP_DIR` 

## apkファイルに署名する 
署名鍵作成  
`keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000`  
署名する  
```jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore XXX.apk alias_name```

## classes.dexの抽出とjarへの変換
```bash
# extract-jar.sh
cp $1 tmp.zip 1>/dev/null
echo "[+] unzipping..."
unzip -d tmp tmp.zip 1>/dev/null
echo "[+] dex2jar processing..."
~/tools/dex2jar-2.0/d2j-dex2jar.sh -o $1.jar ./tmp/classes.dex 1>/dev/null
echo "[+] removing tmp directory..."
rm tmp.zip 1>/dev/null
rm -r tmp 1>/dev/null
echo "[+] Done!"
```
```bash
extract-jar.sh XXX.apk
```

## *.smaliファイルの書き換え
### Logcatへの出力

```java
//javaでは
Log.d("log-tag", string);
```

```smali
# smali、数値v9を出力する場合
const-string v8, "log-tag"

invoke-static {v1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;
move-result-object v9

invoke-static {v8, v9}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
```

```smali
# smali、String型v9を出力する場合
const-string v8, "log-tag"

invoke-static {v8, v9}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
``型