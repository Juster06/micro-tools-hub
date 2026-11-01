(() => {
  'use strict';
  const byId = id => document.getElementById(id);
  const input = byId('toolInput'), output = byId('toolOutput'), mode = byId('toolMode');
  const run = byId('runBtn'), copy = byId('copyBtn'), download = byId('downloadBtn');
  const error = byId('toolError'), status = byId('toolStatus');
  let revision = 0, busy = false;
  const tell = message => { status.textContent = message; };
  function invalidate() {
    revision++;
    output.value = '';
    copy.disabled = download.disabled = true;
    error.hidden = true;
    error.textContent = '';
  }
  input.addEventListener('input', () => { invalidate(); tell('Input changed. Run again for a current result.'); });
  mode.addEventListener('change', () => { invalidate(); tell('Operation changed. Run again.'); });
  if (window.EDB_TOOL.isScaffold === false) {
    byId('scaffoldNotice').hidden = true;
    tell('Ready. Results stay in this browser tab.');
  }
  run.addEventListener('click', async () => {
    if (busy) return;
    invalidate();
    const current = revision;
    busy = true;
    run.disabled = true;
    try {
      if (input.value.length > 100000) throw new Error('Input is too large. Limit: 100,000 code units.');
      if (!window.EDB_TOOL.allowEmpty && !input.value.trim()) throw new Error('Enter input first.');
      const result = await window.EDB_TOOL.run(input.value, {mode:mode.value});
      if (current !== revision) return;
      if (result === undefined) throw new Error('The implementation returned no result.');
      output.value = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
      copy.disabled = download.disabled = output.value.length === 0;
      tell('Result updated.');
    } catch (problem) {
      if (current === revision) {
        error.textContent = problem instanceof Error ? problem.message : 'The tool could not process this input.';
        error.hidden = false;
        tell('No result. Review the error and input.');
      }
    } finally {
      busy = false;
      run.disabled = false;
    }
  });
  byId('clearBtn').addEventListener('click', () => {
    invalidate(); input.value = ''; mode.selectedIndex = 0;
    tell('Cleared.'); input.focus();
  });
  copy.addEventListener('click', async () => {
    if (copy.disabled) return;
    const current = revision, value = output.value;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(value);
      if (current === revision) tell('Result copied.');
    } catch {
      if (current === revision) {
        output.focus(); output.select();
        tell('Automatic copy unavailable. Output selected; press Ctrl+C (or ⌘C).');
      }
    }
  });
  download.addEventListener('click', () => {
    if (download.disabled) return;
    try {
      const url = URL.createObjectURL(new Blob([output.value], {type:'text/plain;charset=utf-8'}));
      const link = document.createElement('a');
      link.href = url; link.download = window.EDB_META.id + '-output.txt';
      document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      tell('Text download requested.');
    } catch { tell('Download unavailable. Copy the result instead.'); }
  });
})();
