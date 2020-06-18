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
```

### 実行コードの追加（関数）
EX1. Javaと対応するSmaliコード・その1
```Java
// Java
Log.d("log-tag", Arrays.toString(arrayOfByte));
```

```Smali
# smali
const-string v6, "log-tag"
invoke-static {v0}, Ljava/util/Arrays;->toString([Ljava/lang/Object;)Ljava/lang/String;
move-result-object v7
invoke-static {v6, v7}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
```

EX2. Javaと対応するSmaliコード・その2
```Java
// Java
private final SecretKey secretKey = new SecretKeySpec("IncrediblySecure".getBytes(), 0, 16, "AES");
```  

```Smali
### smali
new-instance v0, Ljavax/crypto/spec/SecretKeySpec;

const-string v1, "IncrediblySecure"

invoke-virtual {v1}, Ljava/lang/String;->getBytes()[B

move-result-object v1

const/4 v2, 0x0

const/16 v3, 0x10

const-string v4, "AES"

# v1(="IncrediblySecure")は[B型(byte[]型)
# v2(=0x0)はI型(int型)
# v3(=0x10)はI型(int型)
# v4(="AES")はLjava/lang/String;型(java.lang.Stringオブジェクト)
# 返り値はV型(void)
invoke-direct {v0, v1, v2, v3, v4}, Ljavax/crypto/spec/SecretKeySpec;-><init>([BIILjava/lang/String;)V

iput-object v0, p0, Les/o0i/challengeapp/nativemodule/ValidateFlagModule;->secretKey:Ljavax/crypto/SecretKey;
```

### Smali基本文法
[今日も朝から昼寝: smaliの文法まとめ](https://stpr18.blogspot.com/2015/11/smali.html)を参照するべし。
#### 型
| Javaでの型 | Smaliでの型 |
| ----------- | --------- |
| void | V |
| boolean | Z |
| byte | B |
| short | S |
| char | C |
| int | I |
| long | L |
| float | F |
| double | D |
#### クラス型
| Javaでの型 | Smaliでの型 |
| ----------- | --------- |
| java.lang.String | Ljava/lang/String; |
|  |  |
