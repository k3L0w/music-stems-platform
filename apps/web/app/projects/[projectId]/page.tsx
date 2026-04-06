import Link from "next/link";
import { notFound } from "next/navigation";

import { ProjectActions } from "@/app/components/project-actions";
import { ProjectJobs } from "@/app/components/project-jobs";
import { ProjectStems } from "@/app/components/project-stems";
import {
  fetchProject,
  fetchProjectDownloadTargets,
  fetchProjectJobs,
  fetchProjectStems
} from "@/lib/api";

type ProjectDetailPageProps = {
  params: Promise<{
    projectId: string;
  }>;
};

export default async function ProjectDetailPage({ params }: ProjectDetailPageProps) {
  const { projectId } = await params;

  try {
    const [project, jobs, stems, downloadTargets] = await Promise.all([
      fetchProject(projectId),
      fetchProjectJobs(projectId),
      fetchProjectStems(projectId),
      fetchProjectDownloadTargets(projectId)
    ]);

    return (
      <main className="shell">
        <section className="hero">
          <div>
            <p className="eyebrow">Projeto</p>
            <h1>{project.name}</h1>
            <p className="muted">
              Status atual: <strong>{project.status}</strong>
            </p>
          </div>
          <Link href="/" className="secondary-link">
            Voltar para projetos
          </Link>
        </section>

        <section className="panel stack">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Resumo</p>
              <h2>Dados do projeto</h2>
            </div>
          </div>

          <div className="details-grid">
            <div>
              <span className="detail-label">ID</span>
              <p className="mono">{project.id}</p>
            </div>
            <div>
              <span className="detail-label">Arquivo</span>
              <p>{project.source_filename}</p>
            </div>
            <div>
              <span className="detail-label">Object key</span>
              <p className="mono">{project.source_object_key ?? "Ainda nao confirmado"}</p>
            </div>
            <div>
              <span className="detail-label">Content-Type</span>
              <p>{project.source_content_type ?? "-"}</p>
            </div>
            <div>
              <span className="detail-label">Tamanho</span>
              <p>{project.source_size_bytes ?? "-"}</p>
            </div>
            <div>
              <span className="detail-label">Usuario</span>
              <p className="mono">{project.user_id}</p>
            </div>
          </div>
        </section>

        <ProjectActions project={project} />
        <ProjectJobs projectId={project.id} jobs={jobs} />
        <ProjectStems stems={stems} downloadTargets={downloadTargets} />
      </main>
    );
  } catch (error) {
    if (error instanceof Error && error.message.includes("404")) {
      notFound();
    }

    throw error;
  }
}
