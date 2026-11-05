# Gecko esr115 import: status

- Source: mozilla/gecko-dev branch `esr115`, commit `ed296929c72f022818e0596bb3788498109e9dbb` (Firefox 115.26.0 ESR, July 2025), as submodule `gecko/`.
- Checked out size: about 3.3 GB (shallow history about 730 MB).

## What the source says about API levels (read from the tree, nothing compiled yet)
- `build/moz.configure/android-sdk.configure`: default min SDK is 21; **16 in GeckoView Lite mode**; overridable with `--with-android-min-sdk`.
- `python/mozboot/mozboot/android.py` pins NDK `r23c`.
- So an API 19 build looks configurable (Lite mode + `--with-android-min-sdk=19`), which is what `mozconfig.api19-arm` does.

## Not yet known / likely blockers
- Whether it configures and compiles at all with the pinned Rust/clang/NDK.
- Whether it starts on a real KitKat device (bionic/kernel assumptions, graphics, sandboxing).
- TLS: root certificates on API 19 are old; Gecko ships its own NSS roots, which should help, but this is untested.
- Security: esr115 stopped receiving upstream fixes after 2025, so this engine will not get new patches.
- A full Gecko Android build needs far more disk, RAM and time than a free GitHub runner or this sandbox. Plan on a strong local machine or a self-hosted runner.

## Existing files
The previous app/ and workflows (prebuilt GeckoView 70 route) are left untouched.
