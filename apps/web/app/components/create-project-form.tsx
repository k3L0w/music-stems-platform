"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiBaseUrl } from "@/lib/api";

const DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001";

export function CreateProjectForm() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    userId: DEFAULT_USER_ID,
    name: "",
    sourceFilename: "",
    sourceContentType: "audio/wav",
    sourceSizeBytes: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const response = await fetch(`${apiBaseUrl}/projects`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: formData.userId,
          name: formData.name,
          source_filename: formData.sourceFilename,
          source_content_type: formData.sourceContentType || null,
          source_size_bytes: formData.sourceSizeBytes ? Number(formData.sourceSizeBytes) : null
        })
      });

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
        throw new Error(payload?.detail ?? "Nao foi possivel criar o projeto.");
      }

      setFormData({
        userId: DEFAULT_USER_ID,
        name: "",
        sourceFilename: "",
        sourceContentType: "audio/wav",
        sourceSizeBytes: ""
      });
      router.refresh();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erro inesperado ao criar projeto.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="stack" onSubmit={handleSubmit}>
      <div className="field-grid">
        <label className="field">
          <span>Usuario</span>
          <input
            name="userId"
            value={formData.userId}
            onChange={(event) => setFormData((current) => ({ ...current, userId: event.target.value }))}
            required
          />
        </label>

        <label className="field">
          <span>Projeto</span>
          <input
            name="name"
            value={formData.name}
            onChange={(event) => setFormData((current) => ({ ...current, name: event.target.value }))}
            placeholder="Meu primeiro projeto"
            required
          />
        </label>

        <label className="field">
          <span>Arquivo</span>
          <input
            name="sourceFilename"
            value={formData.sourceFilename}
            onChange={(event) =>
              setFormData((current) => ({ ...current, sourceFilename: event.target.value }))
            }
            placeholder="musica.wav"
            required
          />
        </label>

        <label className="field">
          <span>Content-Type</span>
          <input
            name="sourceContentType"
            value={formData.sourceContentType}
            onChange={(event) =>
              setFormData((current) => ({ ...current, sourceContentType: event.target.value }))
            }
            placeholder="audio/wav"
          />
        </label>

        <label className="field">
          <span>Tamanho em bytes</span>
          <input
            name="sourceSizeBytes"
            type="number"
            min="0"
            value={formData.sourceSizeBytes}
            onChange={(event) =>
              setFormData((current) => ({ ...current, sourceSizeBytes: event.target.value }))
            }
            placeholder="10485760"
          />
        </label>
      </div>

      <div className="actions">
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Criando..." : "Criar projeto"}
        </button>
      </div>

      {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
    </form>
  );
}
