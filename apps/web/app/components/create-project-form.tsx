"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiBaseUrl, getApiErrorMessage, parseApiError } from "@/lib/api";
import type { UserSummary } from "@/lib/types";

type CreateProjectFormProps = {
  users: UserSummary[];
};

export function CreateProjectForm({ users }: CreateProjectFormProps) {
  const router = useRouter();
  const defaultUserId = users[0]?.id ?? "";
  const [formData, setFormData] = useState({
    userId: defaultUserId,
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
        const payload = await parseApiError(response);
        setErrorMessage(getApiErrorMessage(payload, "Nao foi possivel criar o projeto."));
        return;
      }

      setFormData({
        userId: defaultUserId,
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

  const selectedUser = users.find((user) => user.id === formData.userId) ?? null;

  return (
    <form className="stack" onSubmit={handleSubmit}>
      <div className="field-grid">
        <label className="field">
          <span>Usuario</span>
          <select
            name="userId"
            value={formData.userId}
            onChange={(event) => setFormData((current) => ({ ...current, userId: event.target.value }))}
            required
            disabled={users.length === 0}
          >
            {users.length === 0 ? <option value="">Nenhum usuario disponivel</option> : null}
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.display_name} ({user.email})
              </option>
            ))}
          </select>
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

      {selectedUser ? (
        <p className="muted">
          Plano ativo: <strong>{selectedUser.active_plan_code}</strong> | Perfil:{" "}
          <strong>{selectedUser.role}</strong>
        </p>
      ) : null}

      <div className="actions">
        <button type="submit" disabled={isSubmitting || users.length === 0 || !formData.userId}>
          {isSubmitting ? "Criando..." : "Criar projeto"}
        </button>
      </div>

      {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
    </form>
  );
}
