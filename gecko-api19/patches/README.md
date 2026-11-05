# Patches on top of Gecko esr115

`gecko/` is a git submodule pinned to an upstream commit of mozilla/gecko-dev (branch esr115).
We cannot push to upstream, so our own edits live here as `git format-patch` files and are applied
before building:

    git -C gecko am ../gecko-api19/patches/*.patch

To make a new patch: commit inside `gecko/` locally, run `git -C gecko format-patch -N -o ../gecko-api19/patches`,
then reset the submodule back to the pinned commit.

No patches exist yet; the first candidates will come from the first configure/compile failures.
