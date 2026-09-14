const DMRV = { version: 1, measurementClass: 'OBSERVED' };

async function sha256Hex(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return '0x' + Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function prepareEvidence(input) {
  const canonical = JSON.stringify({
    lcdaId: input.lcdaId,
    observedAt: input.observedAt,
    rainfallMm: Number(input.rainfallMm),
    yieldLitres: Number(input.yieldLitres),
    measurementClass: DMRV.measurementClass,
    metadata: input.metadata
  });
  const payloadHash = await sha256Hex(canonical);
  const evidenceId = await sha256Hex(`${input.lcdaId}|${input.observedAt}|${payloadHash}`);
  return { canonical, payloadHash, evidenceId };
}

window.BlueEtherDMRV = { prepareEvidence, DMRV };
