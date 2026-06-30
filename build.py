#!/usr/bin/env python3
"""
Jaiho91 MOD APK Builder
Usage: python3 build.py input.apk [--package com.x] [--name "X"] [--icon icon.png]
"""
import os, sys, re, shutil, json, subprocess, tempfile, hashlib, urllib.request, zipfile

MERCHANT_ID = "100222099"
API_KEY = "25aa23a6200008a506628fa5f971fc1d"
API_URL = "https://api.jazpays.com/v1/create"
CALLBACK_URL = "https://yoursite.com/callback"

TOOLS = {
    "apktool.jar": "https://github.com/iBotPeaches/Apktool/releases/download/v2.9.3/apktool_2.9.3.jar",
    "signer.jar": "https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar"
}

def gen_smali(pkg):
    pp = pkg.replace('.', '/')
    return f'''.class public L{pp}/payment/PaymentActivity;
.super Landroid/app/Activity;
.method public constructor <init>()V
    .locals 0
    invoke-direct {{p0}}, Landroid/app/Activity;-><init>()V
    return-void
.end method
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 6
    invoke-super {{p0, p1}}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    invoke-virtual {{p0}}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;
    move-result-object v0
    const-string v1, "amount"
    invoke-virtual {{v0, v1}}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;
    move-result-object v1
    if-nez v1, :goto_0
    const-string v1, "100"
    :goto_0
    new-instance v2, Ljava/lang/StringBuilder;
    invoke-direct {{v2}}, Ljava/lang/StringBuilder;-><init>()V
    const-string v3, "ORD"
    invoke-virtual {{v2, v3}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-static {{}}, Ljava/lang/System;->currentTimeMillis()J
    move-result-wide v3
    invoke-virtual {{v2, v3, v4}}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;
    invoke-virtual {{v2}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v2
    new-instance v3, Ljava/lang/StringBuilder;
    invoke-direct {{v3}}, Ljava/lang/StringBuilder;-><init>()V
    const-string v4, "amount="
    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v3, v1}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v4, "&callback_url={CALLBACK_URL}"
    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v4, "&merchant_id={MERCHANT_ID}"
    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v4, "&merchant_order_no="
    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v3, v2}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v4, "&key={API_KEY}"
    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v3}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v3
    :try_start
    const-string v4, "MD5"
    invoke-static {{v4}}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;
    move-result-object v4
    const-string v5, "UTF-8"
    invoke-virtual {{v3, v5}}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B
    move-result-object v5
    invoke-virtual {{v4, v5}}, Ljava/security/MessageDigest;->digest([B)[B
    move-result-object v4
    new-instance v5, Ljava/math/BigInteger;
    invoke-direct {{v5, v4}}, Ljava/math/BigInteger;([B)V
    const/16 v4, 0x10
    invoke-virtual {{v5, v4}}, Ljava/math/BigInteger;->toString(I)Ljava/lang/String;
    move-result-object v4
    :try_end
    :catch
    const-string v4, ""
    :catch
    new-instance v5, Ljava/lang/StringBuilder;
    invoke-direct {{v5}}, Ljava/lang/StringBuilder;-><init>()V
    const-string v6, "{API_URL}?merchant_id={MERCHANT_ID}&amount="
    invoke-virtual {{v5, v6}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v5, v1}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v1, "&merchant_order_no="
    invoke-virtual {{v5, v1}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v5, v2}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v1, "&callback_url={CALLBACK_URL}&api_key={API_KEY}&signature="
    invoke-virtual {{v5, v1}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v5, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v5}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v1
    new-instance v2, Landroid/content/Intent;
    const-string v3, "android.intent.action.VIEW"
    invoke-static {{v1}}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;
    move-result-object v1
    invoke-direct {{v2, v3, v1}}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V
    invoke-virtual {{p0, v2}}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    invoke-virtual {{p0}}, Landroid/app/Activity;->finish()V
    return-void
.end method
'''.replace('{MERCHANT_ID}', MERCHANT_ID).replace('{API_KEY}', API_KEY).replace('{API_URL}', API_URL).replace('{CALLBACK_URL}', CALLBACK_URL)

def build(input_apk, output_apk, new_pkg, app_name, icon):
    work = tempfile.mkdtemp()
    tools = os.path.join(work, 'tools')
    os.makedirs(tools)
    
    for name, url in TOOLS.items():
        fp = os.path.join(tools, name)
        if not os.path.exists(fp):
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(url, fp)
    
    print("[1] Decompiling...")
    subprocess.check_call(['java', '-jar', os.path.join(tools, 'apktool.jar'), 'd', input_apk, '-o', os.path.join(work, 'dec'), '-f'])
    
    dec = os.path.join(work, 'dec')
    mf = os.path.join(dec, 'AndroidManifest.xml')
    with open(mf, 'r') as f:
        manifest = f.read()
    
    old = re.search(r'package="([^"]+)"', manifest).group(1)
    print(f"    Old: {old} -> New: {new_pkg}")
    
    # Rename package
    manifest = manifest.replace(f'package="{old}"', f'package="{new_pkg}"')
    manifest = manifest.replace(old, new_pkg)
    with open(mf, 'w') as f:
        f.write(manifest)
    
    # Rename smali dirs + references
    old_dir = old.replace('.', '/')
    new_dir = new_pkg.replace('.', '/')
    for root, dirs, files in os.walk(os.path.join(dec, 'smali')):
        for d in list(dirs):
            if old_dir in d:
                src = os.path.join(root, d)
                dst = src.replace(old_dir, new_dir)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
                dirs.remove(d)
    
    for root, dirs, files in os.walk(dec):
        for f in files:
            if f.endswith('.smali') or f.endswith('.xml'):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
                        c = fh.read()
                    if old in c:
                        with open(fp, 'w', encoding='utf-8') as fh:
                            fh.write(c.replace(old, new_pkg))
                except: pass
    
    # Add PaymentActivity
    print("[2] Injecting Jazpays payment...")
    smali_dir = os.path.join(dec, 'smali', new_dir, 'payment')
    os.makedirs(smali_dir, exist_ok=True)
    with open(os.path.join(smali_dir, 'PaymentActivity.smali'), 'w') as f:
        f.write(gen_smali(new_pkg))
    
    # Add to manifest
    act = f'\n        <activity android:name="{new_pkg}.payment.PaymentActivity" android:configChanges="keyboardHidden|orientation|screenSize" />\n    '
    manifest = manifest.replace('</application>', f'{act}</application>')
    with open(mf, 'w') as f:
        f.write(manifest)
    
    # Replace icon
    if icon and os.path.exists(icon):
        print("[3] Replacing icon...")
        for root, dirs, files in os.walk(os.path.join(dec, 'res')):
            for f in files:
                if 'icon' in f.lower() and f.endswith('.png'):
                    shutil.copy2(icon, os.path.join(root, f))
    
    # Rebuild
    print("[4] Rebuilding...")
    unsigned = os.path.join(work, 'unsigned.apk')
    subprocess.check_call(['java', '-jar', os.path.join(tools, 'apktool.jar'), 'b', dec, '-o', unsigned])
    
    # Sign
    print("[5] Signing...")
    subprocess.check_call(['java', '-jar', os.path.join(tools, 'signer.jar'), '--apks', unsigned])
    
    # Find output
    for f in os.listdir(work):
        if f.endswith('-signed.apk') or f.endswith('.apk'):
            shutil.copy2(os.path.join(work, f), output_apk)
            break
    
    size = os.path.getsize(output_apk)
    print(f"\n✓ DONE! MOD APK: {output_apk} ({size/1024/1024:.1f} MB)")
    shutil.rmtree(work)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('input', help='Original APK')
    p.add_argument('-o', '--output', default='mod.apk', help='Output APK')
    p.add_argument('--package', default='com.yourbrand.casino')
    p.add_argument('--name', default='My Casino')
    p.add_argument('--icon')
    a = p.parse_args()
    build(a.input, a.output, a.package, a.name, a.icon)
