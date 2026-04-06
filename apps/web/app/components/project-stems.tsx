import type { GeneratedStem } from "@/lib/types";

type ProjectStemsProps = {
  stems: GeneratedStem[];
};

export function ProjectStems({ stems }: ProjectStemsProps) {
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
            <article key={stem.id} className="list-card">
              <div className="inline-between">
                <strong>{stem.stem_type}</strong>
                <span className="mono">{stem.id}</span>
              </div>
              <p className="muted mono">{stem.file_key}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
