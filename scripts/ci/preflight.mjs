import assert from 'node:assert/strict';
import fs from 'node:fs';
import {findBrowser, launchBrowser} from '../tool-tests/browser.mjs';
// An explicit CI selection must not silently fall back to the developer's Edge.
assert.ok(process.env.EDB_TEST_BROWSER, 'Set EDB_TEST_BROWSER to the installed pinned Chromium executable.');
assert.ok(fs.existsSync(process.env.EDB_TEST_BROWSER), 'Configured Chromium executable is missing.');
const executable = findBrowser(process.env.EDB_TEST_BROWSER);
assert.ok(executable, 'Required browser unavailable.');
let browser;
try {
  browser = await launchBrowser(executable);
  assert.equal(await browser.evaluate('6 * 7'), 42);
  console.log(JSON.stringify({status:'PASS', browser:browser.version}));
} finally {
  if (browser) await browser.close();
}
