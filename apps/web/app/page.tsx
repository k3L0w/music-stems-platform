import Link from "next/link";

import { CreateProjectForm } from "@/app/components/create-project-form";
import { fetchProjects } from "@/lib/api";

export default async function HomePage() {
  const projects = await fetchProjects();

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">MVP web</p>
          <h1>Music Stems Platform</h1>
          <p className="hero-copy">
            Interface minima para operar o fluxo principal da API sem depender do Swagger.
          </p>
        </div>
      </section>

      <section className="panel stack">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Criacao</p>
            <h2>Novo projeto</h2>
          </div>
        </div>
        <CreateProjectForm />
      </section>

      <section className="panel stack">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Projetos</p>
            <h2>Lista de projetos</h2>
          </div>
        </div>

        {projects.length === 0 ? (
          <p className="muted">Nenhum projeto encontrado na API.</p>
        ) : (
          <div className="stack">
            {projects.map((project) => (
              <article key={project.id} className="list-card">
                <div className="inline-between">
                  <div>
                    <h3>{project.name}</h3>
                    <p className="muted">{project.source_filename}</p>
                  </div>
                  <span className={`status-badge status-${project.status}`}>{project.status}</span>
                </div>
                <p className="muted mono">{project.id}</p>
                <div className="actions">
                  <Link href={`/projects/${project.id}`} className="secondary-link">
                    Abrir detalhe
                  </Link>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
