// Playwright only supplies Chromium. All interactions use the existing CDP harness.
const fs = require('node:fs');
const {chromium} = require('playwright');
const executable = chromium.executablePath();
if (!fs.statSync(executable).isFile()) throw Error('Pinned Chromium is missing; run the documented install command.');
if (process.argv.includes('--github-env')) {
  if (!process.env.GITHUB_ENV || /[\r\n]/.test(executable)) throw Error('Invalid GitHub environment file or executable path.');
  fs.appendFileSync(process.env.GITHUB_ENV, `EDB_TEST_BROWSER=${executable}\n`);
} else console.log(executable);
