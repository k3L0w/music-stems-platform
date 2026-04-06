"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiBaseUrl } from "@/lib/api";
import type { Project, UploadTarget } from "@/lib/types";

type ProjectActionsProps = {
  project: Project;
};

export function ProjectActions({ project }: ProjectActionsProps) {
  const router = useRouter();
  const [uploadTarget, setUploadTarget] = useState<UploadTarget | null>(null);
  const [isGeneratingTarget, setIsGeneratingTarget] = useState(false);
  const [isCompletingUpload, setIsCompletingUpload] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [completeForm, setCompleteForm] = useState({
    objectKey: project.source_object_key ?? "",
    sourceFilename: project.source_filename,
    sourceContentType: project.source_content_type ?? "audio/wav",
    sourceSizeBytes: project.source_size_bytes?.toString() ?? ""
  });

  async function handleGenerateUploadTarget() {
    setIsGeneratingTarget(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const response = await fetch(`${apiBaseUrl}/projects/${project.id}/upload-target`, {
        method: "POST"
      });
      const payload = (await response.json().catch(() => null)) as UploadTarget | { detail?: string } | null;
      if (!response.ok) {
        throw new Error(
          payload && "detail" in payload ? payload.detail ?? "Falha ao gerar upload target." : "Falha ao gerar upload target."
        );
      }

      const target = payload as UploadTarget;
      setUploadTarget(target);
      setCompleteForm((current) => ({
        ...current,
        objectKey: target.object_key
      }));
      setSuccessMessage("Upload target mockado gerado com sucesso.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erro inesperado ao gerar upload target.");
    } finally {
      setIsGeneratingTarget(false);
    }
  }

  async function handleCompleteUpload(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsCompletingUpload(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const response = await fetch(`${apiBaseUrl}/projects/${project.id}/upload-complete`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          object_key: completeForm.objectKey,
          source_filename: completeForm.sourceFilename || null,
          source_content_type: completeForm.sourceContentType || null,
          source_size_bytes: completeForm.sourceSizeBytes ? Number(completeForm.sourceSizeBytes) : null
        })
      });

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
        throw new Error(payload?.detail ?? "Nao foi possivel confirmar o upload.");
      }

      setSuccessMessage("Upload confirmado com sucesso.");
      router.refresh();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erro inesperado ao confirmar upload.");
    } finally {
      setIsCompletingUpload(false);
    }
  }

  return (
    <section className="panel stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Upload mockado</p>
          <h2>Acoes de upload</h2>
        </div>
        <button type="button" onClick={handleGenerateUploadTarget} disabled={isGeneratingTarget}>
          {isGeneratingTarget ? "Gerando..." : "Gerar upload target"}
        </button>
      </div>

      {uploadTarget ? (
        <div className="code-block">
          <p>
            <strong>Object key:</strong> {uploadTarget.object_key}
          </p>
          <p>
            <strong>URL:</strong> {uploadTarget.upload_url}
          </p>
          <p>
            <strong>Metodo:</strong> {uploadTarget.upload_method}
          </p>
          <p>
            <strong>Expira em:</strong> {uploadTarget.expires_in_seconds}s
          </p>
        </div>
      ) : null}

      <form className="stack" onSubmit={handleCompleteUpload}>
        <div className="field-grid">
          <label className="field">
            <span>Object key</span>
            <input
              value={completeForm.objectKey}
              onChange={(event) =>
                setCompleteForm((current) => ({ ...current, objectKey: event.target.value }))
              }
              required
            />
          </label>

          <label className="field">
            <span>Arquivo</span>
            <input
              value={completeForm.sourceFilename}
              onChange={(event) =>
                setCompleteForm((current) => ({ ...current, sourceFilename: event.target.value }))
              }
            />
          </label>

          <label className="field">
            <span>Content-Type</span>
            <input
              value={completeForm.sourceContentType}
              onChange={(event) =>
                setCompleteForm((current) => ({ ...current, sourceContentType: event.target.value }))
              }
            />
          </label>

          <label className="field">
            <span>Tamanho em bytes</span>
            <input
              type="number"
              min="0"
              value={completeForm.sourceSizeBytes}
              onChange={(event) =>
                setCompleteForm((current) => ({ ...current, sourceSizeBytes: event.target.value }))
              }
            />
          </label>
        </div>

        <div className="actions">
          <button type="submit" disabled={isCompletingUpload || !completeForm.objectKey}>
            {isCompletingUpload ? "Confirmando..." : "Confirmar upload"}
          </button>
        </div>
      </form>

      {successMessage ? <p className="success-text">{successMessage}</p> : null}
      {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
    </section>
  );
}
