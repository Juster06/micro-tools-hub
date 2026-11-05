# Passphrase Generator

## Task 19.1 public verification

The deployed source from PR #34 / `7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/PASSPHRASE_GENERATOR_RELEASE_VERIFICATION.json` and `audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 19 development notes

Canonical route: `passphrase-generator/index.html`.

6–12 words per phrase, 1–10 phrases, output including separating line breaks ≤4,096 characters. Cryptographic rejection sampling chooses each word independently; repeats are valid. English wordlist: <a href="https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt" rel="noopener noreferrer" target="_blank">Electronic Frontier Foundation / Joseph Bonneau</a>, attributed under <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener noreferrer" target="_blank">CC BY 4.0</a>. Dice codes removed in the local JavaScript wrapper; words/order unchanged. No EFF endorsement. No automatic generation, downloads, stored secrets or logs. Clipboard/extension access and memory erasure are outside this tool’s control; site password rules vary.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/PASSPHRASE_GENERATOR_VERIFICATION.json`.
