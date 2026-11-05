# Passphrase Generator

Canonical route: `passphrase-generator/index.html`.

6–12 words per phrase, 1–10 phrases, output including separating line breaks ≤4,096 characters. Cryptographic rejection sampling chooses each word independently; repeats are valid. English wordlist: <a href="https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt" rel="noopener noreferrer" target="_blank">Electronic Frontier Foundation / Joseph Bonneau</a>, attributed under <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener noreferrer" target="_blank">CC BY 4.0</a>. Dice codes removed in the local JavaScript wrapper; words/order unchanged. No EFF endorsement. No automatic generation, downloads, stored secrets or logs. Clipboard/extension access and memory erasure are outside this tool’s control; site password rules vary.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/PASSPHRASE_GENERATOR_VERIFICATION.json`.
