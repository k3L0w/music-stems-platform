import type {
  GeneratedStem,
  ProcessingJob,
  Project,
  ProjectTimelineEvent,
  StemDownloadTarget,
  UserSummary
} from "./types";

type ApiErrorResponse = {
  error: string;
  message: string;
  status: number;
};

type ApiResult<T> = {
  data: T | null;
  error: string | null;
  message: string | null;
  status: number | null;
};

const apiBaseUrl =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000";

async function parseApiErrorResponse(response: Response): Promise<ApiErrorResponse> {
  const fallbackMessage = `API request failed with status ${response.status}.`;

  try {
    const payload = (await response.json()) as {
      error?: string;
      message?: string;
      detail?: string;
    };

    return {
      error: payload.error ?? "api_error",
      message: payload.message ?? payload.detail ?? fallbackMessage,
      status: response.status
    };
  } catch (error) {
    return {
      error: "api_error",
      message: fallbackMessage,
      status: response.status
    };
  }
}

export async function parseApiError(response: Response): Promise<ApiErrorResponse> {
  return parseApiErrorResponse(response);
}

export function getApiErrorMessage(
  payload: { message?: string | null; detail?: string | null } | null,
  fallback: string
): string {
  return payload?.message ?? payload?.detail ?? fallback;
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<ApiResult<T>> {
  try {
    const response = await fetch(`${apiBaseUrl}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {})
      },
      cache: "no-store"
    });

    if (response.status >= 400) {
      const apiError = await parseApiErrorResponse(response);
      console.error("API ERROR", apiError);
      return {
        data: null,
        error: apiError.error,
        message: apiError.message,
        status: apiError.status
      };
    }

    if (response.status === 204) {
      return {
        data: undefined as T,
        error: null,
        message: null,
        status: response.status
      };
    }

    return {
      data: (await response.json()) as T,
      error: null,
      message: null,
      status: response.status
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unexpected API failure.";
    console.error("API ERROR", { error: "network_error", message, status: null });
    return {
      data: null,
      error: "network_error",
      message,
      status: null
    };
  }
}

export async function fetchProjects(): Promise<Project[] | null> {
  const result = await apiFetch<Project[]>("/projects");
  return result.data;
}

export async function fetchProject(projectId: string): Promise<Project | null> {
  const result = await apiFetch<Project>(`/projects/${projectId}`);
  return result.data;
}

export async function fetchProjectJobs(projectId: string): Promise<ProcessingJob[] | null> {
  const result = await apiFetch<ProcessingJob[]>(`/projects/${projectId}/jobs`);
  return result.data;
}

export async function fetchProjectStems(projectId: string): Promise<GeneratedStem[] | null> {
  const result = await apiFetch<GeneratedStem[]>(`/projects/${projectId}/stems`);
  return result.data;
}

export async function fetchProjectDownloadTargets(
  projectId: string
): Promise<StemDownloadTarget[] | null> {
  const result = await apiFetch<StemDownloadTarget[]>(`/projects/${projectId}/download-targets`);
  return result.data;
}

export async function fetchUsers(): Promise<UserSummary[] | null> {
  const result = await apiFetch<UserSummary[]>("/users");
  return result.data;
}

export async function fetchProjectTimeline(projectId: string): Promise<ProjectTimelineEvent[] | null> {
  const result = await apiFetch<ProjectTimelineEvent[]>(`/projects/${projectId}/timeline`);
  return result.data;
}

export { apiBaseUrl };
