export default function IllovedizaFuerzaPage() {
  const layers = [
    ["17 + 2", "Autonomous communities / cities"],
    ["50", "Provinces"],
    ["8,132", "Municipal reporting nodes"],
    ["∞", "Observation records over time"],
  ];

  const domains = [
    "Rainfall & prediction",
    "Atmospheric moisture",
    "Weather & air quality",
    "Remote sensing",
    "Water/QMS",
    "DMRV",
    "ESG/GHG",
    "Institutional reporting",
  ];

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-6 py-10 text-slate-100">
      <section className="rounded-3xl border border-white/10 bg-slate-950/80 p-8 shadow-2xl">
        <div className="mb-3 text-xs font-semibold uppercase tracking-[0.28em] text-cyan-300">
          Secondary Institutional Pilot · Spain
        </div>
        <h1 className="text-4xl font-semibold tracking-tight md:text-6xl">
          Illovediza Fuerza
        </h1>
        <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-300">
          Whole-of-Spain environmental evidence mapping: every autonomous community,
          province and municipality becomes a reporting node while physical deployment,
          measured evidence and Premium RainWater production remain independently gated.
        </p>

        <div className="mt-8 grid gap-4 md:grid-cols-4">
          {layers.map(([value, label]) => (
            <div key={label} className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
              <div className="text-3xl font-semibold">{value}</div>
              <div className="mt-2 text-sm text-slate-400">{label}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-6 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-7">
          <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Node hierarchy</div>
          <div className="mt-5 flex flex-wrap items-center gap-2 text-sm">
            {["Spain", "Autonomous Community / City", "Province", "Municipality", "Authorized Field Site", "Observation Node"].map((item, i) => (
              <span key={item} className="rounded-full border border-cyan-300/20 bg-cyan-300/5 px-3 py-2">
                {i + 1}. {item}
              </span>
            ))}
          </div>
          <p className="mt-6 text-sm leading-7 text-slate-400">
            A municipal node is a reporting boundary, not evidence that a collector,
            sensor, laboratory or harvest operation exists there.
          </p>
        </div>

        <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-7">
          <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Reporting domains</div>
          <div className="mt-5 grid grid-cols-2 gap-2">
            {domains.map((domain) => (
              <div key={domain} className="rounded-xl bg-white/[0.04] px-3 py-3 text-sm text-slate-300">
                {domain}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mt-6 grid gap-6 md:grid-cols-3">
        <article className="rounded-3xl border border-white/10 bg-slate-950/70 p-7">
          <div className="text-xs uppercase tracking-[0.2em] text-emerald-300">Evidence</div>
          <h2 className="mt-3 text-xl font-semibold">REPORTABLE → VERIFIED</h2>
          <p className="mt-3 text-sm leading-7 text-slate-400">
            Provenance, timestamp, coordinates, units, methodology, quality and reconciliation
            remain mandatory before promotion.
          </p>
        </article>
        <article className="rounded-3xl border border-white/10 bg-slate-950/70 p-7">
          <div className="text-xs uppercase tracking-[0.2em] text-violet-300">Blockchain</div>
          <h2 className="mt-3 text-xl font-semibold">Integrity, not truth</h2>
          <p className="mt-3 text-sm leading-7 text-slate-400">
            Evidence roots may be anchored for auditability. The chain does not establish
            water quality, environmental truth or regulatory approval.
          </p>
        </article>
        <article className="rounded-3xl border border-white/10 bg-slate-950/70 p-7">
          <div className="text-xs uppercase tracking-[0.2em] text-amber-300">Premium RainWater</div>
          <h2 className="mt-3 text-xl font-semibold">Physical gate required</h2>
          <p className="mt-3 text-sm leading-7 text-slate-400">
            Rain event, first flush, collection, custody, QMS, batch, seal, DMRV and
            regulatory/product-release evidence are required.
          </p>
        </article>
      </section>

      <section className="mt-6 rounded-3xl border border-white/10 bg-gradient-to-br from-cyan-950/40 to-slate-950 p-7">
        <div className="text-xs uppercase tracking-[0.2em] text-cyan-300">Programme relationship</div>
        <div className="mt-4 grid gap-6 md:grid-cols-2">
          <div>
            <h2 className="text-xl font-semibold">Global Lagos → Dubai</h2>
            <p className="mt-2 text-sm leading-7 text-slate-400">Reference/proof pilot and cross-continental network architecture.</p>
          </div>
          <div>
            <h2 className="text-xl font-semibold">Illovediza Fuerza</h2>
            <p className="mt-2 text-sm leading-7 text-slate-400">Spain-wide institutional replication and municipal reporting grid.</p>
          </div>
        </div>
        <div className="mt-6 border-t border-white/10 pt-5 text-sm text-slate-500">
          Status: DESIGNED FOR CONTROLLED IMPLEMENTATION · Administrative coverage does not imply physical deployment.
        </div>
      </section>
    </main>
  );
}
