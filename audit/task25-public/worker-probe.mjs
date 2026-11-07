import assert from 'node:assert/strict';

// Observe the actual public page's native Worker. Chromium pauses the original
// script before execution so instrumentation can wrap native Blob methods.
// The deployed HTML, generated Worker script and file bytes are left intact.
export async function observeWorker(browser, action) {
  const events = [], errors = [], pending = new Set(), breakpoints = new Map();
  const binding = '__edb251WorkerTrace';
  const instrumentation = `(() => {
    const slice = Blob.prototype.slice;
    Blob.prototype.slice = function(start, end) {
      ${binding}(JSON.stringify({event:'slice',start,end}));
      return slice.apply(this, arguments);
    };
    const read = Blob.prototype.arrayBuffer;
    Blob.prototype.arrayBuffer = function() {
      ${binding}(JSON.stringify({event:'read-start',size:this.size}));
      return read.call(this).finally(() => ${binding}(JSON.stringify({event:'read-end'})));
    };
    return true;
  })()`;
  const unlisten = browser.onEvent(message => {
    if (message.method === 'Runtime.bindingCalled' && message.params.name === binding) {
      events.push(JSON.parse(message.params.payload));
    }
    let operation;
    if (message.method === 'Target.attachedToTarget' && message.params.targetInfo.type === 'worker') {
      const session = message.params.sessionId;
      operation = (async () => {
        await browser.call('Network.enable', {}, session);
        await browser.call('Runtime.enable', {}, session);
        await browser.call('Runtime.addBinding', {name: binding}, session);
        await browser.call('Debugger.enable', {}, session);
        const mark = await browser.call('Debugger.setInstrumentationBreakpoint', {instrumentation:'beforeScriptExecution'}, session);
        breakpoints.set(session, mark.breakpointId);
        await browser.call('Runtime.runIfWaitingForDebugger', {}, session);
      })();
    } else if (message.method === 'Debugger.paused' && breakpoints.has(message.sessionId)) {
      const session = message.sessionId;
      operation = (async () => {
        const result = await browser.call('Debugger.evaluateOnCallFrame', {
          callFrameId:message.params.callFrames[0].callFrameId, expression:instrumentation, returnByValue:true,
        }, session);
        assert.equal(result.result.value, true);
        await browser.call('Debugger.removeBreakpoint', {breakpointId:breakpoints.get(session)}, session);
        breakpoints.delete(session);
        await browser.call('Debugger.resume', {}, session);
      })();
    }
    if (operation) {
      pending.add(operation);
      operation.catch(error => errors.push(error.message)).finally(() => pending.delete(operation));
    }
  });
  await browser.call('Target.setAutoAttach', {autoAttach:true,waitForDebuggerOnStart:true,flatten:true,filter:[{type:'worker'},{exclude:true}]});
  try {
    await action();
    await Promise.allSettled([...pending]);
    assert.deepEqual(errors, []);
    const slices = events.filter(row => row.event === 'slice').map(({start,end}) => [start,end]);
    const reads = events.filter(row => row.event === 'read-start');
    let active = 0, peak = 0;
    for (const row of events) {
      if (row.event === 'read-start') peak = Math.max(peak, ++active);
      if (row.event === 'read-end') active--;
      assert.ok(active >= 0);
    }
    assert.equal(active, 0);
    return {slices, read_sizes:reads.map(row=>row.size), peak_reads_in_flight:peak, read_count:reads.length};
  } finally {
    unlisten();
    await browser.call('Target.setAutoAttach', {autoAttach:false,waitForDebuggerOnStart:false,flatten:true});
  }
}
