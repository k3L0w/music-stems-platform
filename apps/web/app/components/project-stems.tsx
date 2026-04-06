import type { GeneratedStem, StemDownloadTarget } from "@/lib/types";

type ProjectStemsProps = {
  stems: GeneratedStem[];
  downloadTargets: StemDownloadTarget[];
};

export function ProjectStems({ stems, downloadTargets }: ProjectStemsProps) {
  const downloadTargetsByStemId = new Map(
    downloadTargets.map((target) => [target.stem_id, target])
  );

  return (
    <section className="panel stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Saida</p>
          <h2>Stems gerados</h2>
        </div>
      </div>

      {stems.length === 0 ? (
        <p className="muted">Nenhum stem disponivel para este projeto.</p>
      ) : (
        <div className="stack">
          {stems.map((stem) => (
            <article key={stem.id} className="list-card stack">
              <div className="inline-between">
                <strong>{stem.stem_type}</strong>
                <span className="mono">{stem.id}</span>
              </div>
              <p className="muted mono">{stem.file_key}</p>
              {downloadTargetsByStemId.has(stem.id) ? (
                <div className="stack">
                  <a
                    href={downloadTargetsByStemId.get(stem.id)?.download_url}
                    target="_blank"
                    rel="noreferrer"
                    className="secondary-link"
                  >
                    Abrir link mockado
                  </a>
                  <p className="muted">
                    Metodo {downloadTargetsByStemId.get(stem.id)?.download_method} expira em{" "}
                    {downloadTargetsByStemId.get(stem.id)?.expires_in_seconds}s
                  </p>
                </div>
              ) : (
                <p className="muted">Link de download ainda nao disponivel.</p>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
