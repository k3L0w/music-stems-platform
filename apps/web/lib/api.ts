import type { GeneratedStem, ProcessingJob, Project } from "./types";

const apiBaseUrl =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    cache: "no-store"
  });

  if (!response.ok) {
    const message = await readErrorMessage(response);
    throw new Error(`HTTP ${response.status}: ${message}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const data = (await response.json()) as { detail?: string };
    return data.detail ?? `API request failed with status ${response.status}.`;
  } catch {
    return `API request failed with status ${response.status}.`;
  }
}

export async function fetchProjects(): Promise<Project[]> {
  return apiFetch<Project[]>("/projects");
}

export async function fetchProject(projectId: string): Promise<Project> {
  return apiFetch<Project>(`/projects/${projectId}`);
}

export async function fetchProjectJobs(projectId: string): Promise<ProcessingJob[]> {
  return apiFetch<ProcessingJob[]>(`/projects/${projectId}/jobs`);
}

export async function fetchProjectStems(projectId: string): Promise<GeneratedStem[]> {
  return apiFetch<GeneratedStem[]>(`/projects/${projectId}/stems`);
}

export { apiBaseUrl };
