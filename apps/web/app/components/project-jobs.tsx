"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiBaseUrl } from "@/lib/api";
import type { ProcessingJob, ProcessingJobStatus, StemType } from "@/lib/types";

type ProjectJobsProps = {
  projectId: string;
  jobs: ProcessingJob[];
};

const availableStems: StemType[] = ["vocals", "drums", "bass", "guitar", "piano", "other"];
const statusOptions: ProcessingJobStatus[] = ["running", "succeeded", "failed"];

export function ProjectJobs({ projectId, jobs }: ProjectJobsProps) {
  const router = useRouter();
  const [provider, setProvider] = useState("htdemucs_6s");
  const [selectedStems, setSelectedStems] = useState<StemType[]>(["vocals", "drums"]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isCreatingJob, setIsCreatingJob] = useState(false);
  const [updatingJobId, setUpdatingJobId] = useState<string | null>(null);

  function toggleStem(stem: StemType) {
    setSelectedStems((current) =>
      current.includes(stem) ? current.filter((item) => item !== stem) : [...current, stem]
    );
  }

  async function handleCreateJob(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsCreatingJob(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const response = await fetch(`${apiBaseUrl}/projects/${projectId}/jobs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          provider,
          requested_stems: selectedStems
        })
      });

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
        throw new Error(payload?.detail ?? "Nao foi possivel criar o job.");
      }

      setSuccessMessage("Job criado com sucesso.");
      router.refresh();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erro inesperado ao criar job.");
    } finally {
      setIsCreatingJob(false);
    }
  }

  async function handleUpdateStatus(jobId: string, status: ProcessingJobStatus) {
    setUpdatingJobId(jobId);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const response = await fetch(`${apiBaseUrl}/jobs/${jobId}/status`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ status })
      });

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
        throw new Error(payload?.detail ?? "Nao foi possivel atualizar o status do job.");
      }

      setSuccessMessage(`Job atualizado para ${status}.`);
      router.refresh();
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Erro inesperado ao atualizar o status do job."
      );
    } finally {
      setUpdatingJobId(null);
    }
  }

  return (
    <section className="panel stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Processamento</p>
          <h2>Jobs do projeto</h2>
        </div>
      </div>

      <form className="stack" onSubmit={handleCreateJob}>
        <div className="field-grid">
          <label className="field">
            <span>Provider</span>
            <input value={provider} onChange={(event) => setProvider(event.target.value)} required />
          </label>
        </div>

        <div className="field">
          <span>Requested stems</span>
          <div className="checkbox-grid">
            {availableStems.map((stem) => (
              <label key={stem} className="check">
                <input
                  type="checkbox"
                  checked={selectedStems.includes(stem)}
                  onChange={() => toggleStem(stem)}
                />
                <span>{stem}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="actions">
          <button type="submit" disabled={isCreatingJob || selectedStems.length === 0}>
            {isCreatingJob ? "Criando..." : "Criar job"}
          </button>
        </div>
      </form>

      <div className="stack">
        {jobs.length === 0 ? (
          <p className="muted">Nenhum job criado para este projeto.</p>
        ) : (
          jobs.map((job) => (
            <article key={job.id} className="list-card stack">
              <div className="inline-between">
                <div>
                  <strong>{job.provider}</strong>
                  <p className="muted mono">{job.id}</p>
                </div>
                <span className={`status-badge status-${job.status}`}>{job.status}</span>
              </div>

              <p className="muted">Stems: {job.requested_stems.join(", ")}</p>

              <div className="actions">
                {statusOptions.map((status) => (
                  <button
                    key={status}
                    type="button"
                    className="secondary-button"
                    disabled={updatingJobId === job.id}
                    onClick={() => handleUpdateStatus(job.id, status)}
                  >
                    {updatingJobId === job.id ? "Atualizando..." : `Marcar como ${status}`}
                  </button>
                ))}
              </div>
            </article>
          ))
        )}
      </div>

      {successMessage ? <p className="success-text">{successMessage}</p> : null}
      {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
    </section>
  );
}
