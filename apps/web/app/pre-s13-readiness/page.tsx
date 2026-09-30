export default function PreS13ReadinessPage() {
  const procedures = [
    ["S12.1", "Site Authorization & Physical Identity", "SITE_AUTHORIZED"],
    ["S12.2", "Operator & Equipment Qualification", "QUALIFIED"],
    ["S12.3", "Weather/Telemetry Connector Qualification", "CONNECTOR_QUALIFIED"],
    ["S12.4", "Video Evidence Qualification", "VIDEO_QUALIFIED"],
    ["S12.5", "Measurement & Calibration Control", "MEASUREMENT_CONTROLLED"],
    ["S12.6", "First-Flush & Collection Procedure Qualification", "COLLECTION_CONTROLLED"],
    ["S12.7", "Sampling/Custody/QMS Qualification", "CUSTODY_QMS_READY"],
    ["S12.8", "Batch/Seal Traceability Qualification", "TRACEABILITY_READY"],
    ["S12.9", "DMRV Event Schema & Methodology Freeze", "SCHEMA_FROZEN"],
    ["S12.10", "Evidence Package Dry Run", "DRY_RUN_COMPLETE"],
    ["S12.11", "Anchor Workflow Dry Run", "ANCHOR_DRY_RUN_COMPLETE"],
    ["S12.12", "Exception/CAPA & Rollback Drill", "RECOVERY_TESTED"],
    ["S12.13", "External Assurance Evidence-Room Review", "ASSURANCE_READY"],
    ["S12.14", "Regulatory/Product Compliance Gate", "COMPLIANCE_REVIEWED"],
    ["S12.15", "Claims & Investor Surface Freeze", "CLAIMS_FROZEN"],
    ["S12.16", "Integrated Field Readiness Review", "INTEGRATED_READY"],
    ["S12.17", "Final Go/No-Go Authorization", "FIELD_AUTHORIZED"],
  ];

  return (
    <main style={{maxWidth: 1100, margin: "0 auto", padding: "48px 24px", fontFamily: "Arial, sans-serif"}}>
      <header style={{borderBottom: "1px solid #ddd", paddingBottom: 24, marginBottom: 28}}>
        <p style={{fontSize: 13, letterSpacing: 1.5, fontWeight: 700}}>S12 → S13 CONTROL GATE</p>
        <h1 style={{fontSize: 40, margin: "8px 0"}}>Pre-S13 Field Readiness</h1>
        <p style={{fontSize: 18, lineHeight: 1.6, maxWidth: 820}}>
          Institutional controls that must be implemented and tested before the first genuinely empirical live rainwater harvest evidence event.
        </p>
        <div style={{display: "flex", gap: 10, flexWrap: "wrap"}}>
          <Badge>PHYSICAL PRODUCTION: NOT RELEASED</Badge>
          <Badge>PRE-HARVEST CONTROL STATE</Badge>
          <Badge>FAIL-CLOSED</Badge>
        </div>
      </header>

      <section style={{background: "#f7f7f7", padding: 20, borderRadius: 12, marginBottom: 28}}>
        <strong>Evidence boundary</strong>
        <p style={{lineHeight: 1.6, marginBottom: 0}}>
          S12 readiness does not create rainfall observations, harvest measurements, laboratory results, premium-condition conclusions,
          regulatory approvals or product-release evidence. Synthetic records are control-test records only.
        </p>
      </section>

      <section>
        <h2>Required procedures</h2>
        <div style={{display: "grid", gap: 12}}>
          {procedures.map(([id, name, gate]) => (
            <article key={id} style={{border: "1px solid #ddd", borderRadius: 10, padding: 18, display: "grid", gridTemplateColumns: "80px 1fr auto", gap: 16, alignItems: "center"}}>
              <strong>{id}</strong>
              <div>
                <div style={{fontWeight: 700}}>{name}</div>
                <div style={{fontSize: 12, marginTop: 5, opacity: 0.7}}>Gate: {gate}</div>
              </div>
              <span style={{fontSize: 12, fontWeight: 700}}>CONTROL TO COMPLETE</span>
            </article>
          ))}
        </div>
      </section>

      <section style={{marginTop: 32, padding: 20, border: "1px solid #ddd", borderRadius: 12}}>
        <h2>Transition to S13</h2>
        <p style={{lineHeight: 1.6}}>
          S13 is the first controlled empirical field sequence. It may begin only after S12.17 human authorization.
        </p>
        <p style={{fontFamily: "monospace", lineHeight: 1.7}}>
          RAIN-EVENT WATCH → EVENT ACTIVATION → PRE-EVENT SITE CHECK → FIRST-FLUSH → CONTROLLED COLLECTION → LIVE MEASUREMENT + VIDEO → SAMPLE/CUSTODY → QMS/LAB → BATCH/SEAL → DMRV → ASSURANCE → RELEASE GATE
        </p>
      </section>
    </main>
  );
}

function Badge({children}: {children: React.ReactNode}) {
  return <span style={{fontSize: 12, fontWeight: 700, padding: "7px 10px", border: "1px solid #bbb", borderRadius: 999}}>{children}</span>;
}
