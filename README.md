# Jaiho91 MOD APK

Custom casino app with Jazpays payment gateway.

## Features
- ✅ Package rename (apna brand)
- ✅ Custom logo
- ✅ Jazpays payment gateway (MD5 signature)
- ✅ Original games intact
- ✅ Auto-build via GitHub Actions

## One-Click Build

1. Fork this repo
2. Go to **Actions** → **Build MOD APK**
3. Click **Run workflow** → paste APK download URL
4. Wait 5 min → download your MOD APK

## Manual Build (PC)

```bash
# Requirements: Java 8+
python3 build.py original.apk --package "com.yourbrand.game" --name "Your Casino"
```

## Payment Gateway

| Item | Value |
|------|-------|
| Gateway | Jazpays |
| Merchant | 100222099 |
| Endpoint | `https://api.jazpays.com/v1/create` |

**Flow:** User clicks deposit → amount dialog → Jazpays URL → browser pay → callback
