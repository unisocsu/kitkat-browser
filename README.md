# KitKat Browser

An experimental, non-Chromium browser project targeting Android 4.4 (API 19), investigating whether Mozilla Gecko/GeckoView can be adapted to run on KitKat.

## Goal

- Android minimum API: 19
- Browser engine: Mozilla Gecko (not Chromium)
- Language/UI: Java + XML where practical
- Build environment: GitHub Actions; no Android Studio required locally
- Output: downloadable APK artifacts once a compatible engine build is available

## Reality check

Changing `minSdkVersion` alone does not make a modern Gecko build compatible with Android 4.4. Native dependencies, NDK/toolchain versions, Android APIs, graphics, TLS, and GeckoView's Java API may all require changes. The first milestone is a reproducible source compatibility audit; it is not yet an APK build.

A successful build also does not guarantee that current websites will work. Android 4.4 lacks modern platform APIs and current security support, and old engine builds can have serious security limitations.

## Milestones

1. Audit candidate Gecko source revisions for Android minimum SDK and build-tool constraints.
2. Select a baseline and document concrete API 19 blockers.
3. Build the smallest feasible Gecko/GeckoView target in CI.
4. Add a Java/XML browser shell and produce an APK artifact.
5. Test startup, navigation, JavaScript, CSS, certificates/TLS, and memory usage on an API 19 device.

## License

This repository's own code will be licensed separately as it is added. Mozilla Gecko and related components retain their respective upstream licenses.