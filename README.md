# KitKat Browser

An experimental, non-Chromium browser project targeting Android 4.4 (API 19), investigating whether Mozilla Gecko/GeckoView can be adapted to run on KitKat.

## Goal

- Android minimum API: 19
- Browser engine: Mozilla Gecko (not Chromium)
- Language/UI: Java + XML where practical
- Build environment: GitHub Actions; no Android Studio required locally
- Output: downloadable APK artifacts once a compatible engine build is available

## Compatibility findings (October 2026)

- **Current GeckoView is not a realistic API 19 target.** Mozilla's current GeckoView documentation says GeckoView requires Android 8.0 (API 26) or later. See [Mozilla's GeckoView system requirements](https://wiki.mozilla.org/Mobile/GeckoView) and [Mozilla bug 1982312, which raised GeckoView's minimum SDK to 26](https://bugzilla.mozilla.org/show_bug.cgi?id=1982312).
- **Older GeckoView builds did run on older Android versions, but that is not equivalent to current web compatibility.** Mozilla's historical [bug 1567115](https://bugzilla.mozilla.org/show_bug.cgi?id=1567115) documents GeckoView on Android 4.4 and a workaround for a dependency crash. That old engine is not a safe long-term browser for modern internet use and will lack years of web-platform and security fixes.
- Therefore the next meaningful experiment is to identify the newest historical GeckoView artifact that can at least start on API 19, then separately test its JavaScript, CSS, TLS/certificate handling, and stability. This is an investigation, not a claim that modern websites will work.

Changing `minSdkVersion` alone does not make a modern Gecko build compatible with Android 4.4. Native dependencies, NDK/toolchain versions, Android APIs, graphics, TLS, and GeckoView's Java API may all require changes. The current audit workflow only downloads build configuration; it does not compile Gecko or create an APK.

A successful build also does not guarantee that current websites will work. Android 4.4 is an obsolete platform, and using an old browser engine for sensitive browsing carries serious security risks.

## Milestones

1. Identify the newest historical GeckoView candidate that may run on API 19.
2. Build a minimal Java/XML browser shell against that candidate in GitHub Actions.
3. Produce an APK artifact and test installation/startup on an API 19 device.
4. Test navigation, JavaScript, CSS, certificates/TLS, and memory usage; document unsupported features and security limitations.

## License

This repository's own code will be licensed separately as it is added. Mozilla Gecko and related components retain their respective upstream licenses.
