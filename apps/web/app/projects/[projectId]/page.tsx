import Link from "next/link";

import { ProjectActions } from "@/app/components/project-actions";
import { ProjectJobs } from "@/app/components/project-jobs";
import { ProjectStems } from "@/app/components/project-stems";
import { ProjectTimeline } from "@/app/components/project-timeline";
import {
  fetchProject,
  fetchProjectDownloadTargets,
  fetchProjectJobs,
  fetchProjectStems,
  fetchProjectTimeline,
  fetchUsers
} from "@/lib/api";
import type { PlanCode } from "@/lib/types";

const planLimitsByCode: Record<PlanCode, { stemsPerJob: number; activeJobs: number }> = {
  free: { stemsPerJob: 2, activeJobs: 1 },
  solo: { stemsPerJob: 4, activeJobs: 2 },
  pro: { stemsPerJob: 6, activeJobs: 5 }
};

type ProjectDetailPageProps = {
  params: Promise<{
    projectId: string;
  }>;
};

export default async function ProjectDetailPage({ params }: ProjectDetailPageProps) {
  const { projectId } = await params;
  const [project, jobs, stems, downloadTargets, timeline, users] = await Promise.all([
    fetchProject(projectId),
    fetchProjectJobs(projectId),
    fetchProjectStems(projectId),
    fetchProjectDownloadTargets(projectId),
    fetchProjectTimeline(projectId),
    fetchUsers()
  ]);
  const safeJobs = jobs || [];
  const safeStems = stems || [];
  const safeDownloadTargets = downloadTargets || [];
  const safeTimeline = timeline || [];
  const safeUsers = users || [];

  if (!project) {
    return (
      <main className="shell">
        <section className="panel stack">
          <p className="error-text">Erro ao carregar projeto.</p>
          <Link href="/" className="secondary-link">
            Voltar para projetos
          </Link>
        </section>
      </main>
    );
  }

  const projectUser = safeUsers.find((user) => user.id === project.user_id) ?? null;
  const activePlanCode = projectUser?.active_plan_code ?? "free";
  const planLimits = planLimitsByCode[activePlanCode];

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
            <p>{projectUser ? `${projectUser.display_name} (${projectUser.email})` : project.user_id}</p>
          </div>
          <div>
            <span className="detail-label">Plano ativo</span>
            <p>{activePlanCode}</p>
          </div>
          <div>
            <span className="detail-label">Limites do plano</span>
            <p>
              Ate {planLimits.stemsPerJob} stems por job e ate {planLimits.activeJobs} jobs ativos
            </p>
          </div>
        </div>
      </section>

      {!jobs ? <p className="error-text">Erro ao carregar jobs.</p> : null}
      {!timeline ? <p className="error-text">Erro ao carregar timeline.</p> : null}
      {!stems ? <p className="error-text">Erro ao carregar stems.</p> : null}
      {!downloadTargets ? <p className="error-text">Erro ao carregar links de download.</p> : null}
      {!users ? <p className="error-text">Erro ao carregar usuarios.</p> : null}

      <ProjectActions project={project} />
      <ProjectTimeline events={safeTimeline} />
      <ProjectJobs projectId={project.id} jobs={safeJobs} />
      <ProjectStems stems={safeStems} downloadTargets={safeDownloadTargets} />
    </main>
  );
}
