import type { ProjectTimelineEvent } from "@/lib/types";

type ProjectTimelineProps = {
  events: ProjectTimelineEvent[];
};

function formatTimestamp(timestamp: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short"
  }).format(new Date(timestamp));
}

export function ProjectTimeline({ events }: ProjectTimelineProps) {
  return (
    <section className="panel stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Timeline</p>
          <h2>Fluxo do projeto</h2>
        </div>
      </div>

      {events.length === 0 ? (
        <p className="muted">Nenhum evento disponivel para este projeto.</p>
      ) : (
        <div className="stack">
          {events.map((event, index) => (
            <article key={`${event.type}-${event.timestamp}-${index}`} className="list-card stack">
              <div className="inline-between">
                <strong>{event.title}</strong>
                <span className="muted">{formatTimestamp(event.timestamp)}</span>
              </div>
              <p className="muted">{event.description}</p>
              <p className="mono">{event.type}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
