export default function FirstLiveHarvestPage() {
  const steps = [
    "RAIN-EVENT WATCH","EVENT ACTIVATION","PRE-EVENT SITE CHECK","FIRST-FLUSH DIVERSION",
    "CONTROLLED COLLECTION","LIVE MEASUREMENT + VIDEO","SAMPLE IDENTIFICATION",
    "CHAIN OF CUSTODY","QMS / LAB HANDOFF","BATCH + SEAL","DMRV EVENT PACKAGE",
    "EVIDENCE RECONCILIATION","ANCHOR CANDIDATE","ASSURANCE REVIEW",
    "PREMIUM-CONDITION DECISION","REGULATORY / PRODUCT RELEASE GATE"
  ];

  return (
    <main style={{maxWidth: 1100, margin: "0 auto", padding: "48px 24px", fontFamily: "Arial, sans-serif"}}>
      <header style={{borderBottom: "1px solid #ddd", paddingBottom: 24}}>
        <p style={{fontSize: 13, letterSpacing: 1.5, fontWeight: 700}}>S13 · EMPIRICAL EVENT CONTROL</p>
        <h1 style={{fontSize: 40, margin: "8px 0"}}>First Live Harvest & Evidence Event</h1>
        <p style={{fontSize: 18, lineHeight: 1.6, maxWidth: 820}}>
          The first repository-defined sequence permitted to receive genuine field observations.
          No live harvest is claimed until the authorized physical event actually occurs.
        </p>
        <div style={{display: "flex", gap: 10, flexWrap: "wrap"}}>
          <Badge>READY FOR AUTHORIZED EXECUTION</Badge>
          <Badge>NO LIVE EVENT CLAIMED</Badge>
          <Badge>FAIL-CLOSED</Badge>
        </div>
      </header>
      <section style={{marginTop: 28, padding: 20, border: "1px solid #ddd", borderRadius: 12}}>
        <strong>Evidence boundary</strong>
        <p style={{lineHeight: 1.6}}>
          This surface is an execution control. It does not create rainfall, harvest, laboratory, premium-condition,
          regulatory, ESG/GHG or investor evidence. Forecasts remain forecasts and blockchain anchors prove package integrity only.
        </p>
      </section>
      <section style={{marginTop: 32}}>
        <h2>Controlled event sequence</h2>
        <ol style={{display: "grid", gap: 12, paddingLeft: 28}}>
          {steps.map((step, index) => (
            <li key={step} style={{padding: 14, border: "1px solid #ddd", borderRadius: 9}}>
              <strong>{index + 1}. {step}</strong>
            </li>
          ))}
        </ol>
      </section>
      <section style={{marginTop: 32, padding: 20, background: "#f7f7f7", borderRadius: 12}}>
        <h2>Gate discipline</h2>
        <p style={{lineHeight: 1.6}}>
          Site identity, authorization, source provenance, measurement integrity, first-flush evidence,
          video linkage, custody/QMS lineage, traceability and methodology must reconcile before dependent states advance.
        </p>
        <p style={{fontFamily: "monospace"}}>forecast ≠ observation · rainfall ≠ premium · anchor ≠ verification · harvest ≠ release</p>
      </section>
    </main>
  );
}
function Badge({children}: {children: React.ReactNode}) {
  return <span style={{fontSize: 12, fontWeight: 700, padding: "7px 10px", border: "1px solid #bbb", borderRadius: 999}}>{children}</span>;
}
