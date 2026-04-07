export type ProjectStatus = "draft" | "uploaded" | "processing" | "completed" | "failed";

export type ProcessingJobStatus = "queued" | "running" | "succeeded" | "failed";

export type StemType = "vocals" | "drums" | "bass" | "guitar" | "piano" | "other";

export type PlanCode = "free" | "solo" | "pro";

export type UserRole = "customer" | "admin";

export type Project = {
  id: string;
  user_id: string;
  name: string;
  source_filename: string;
  source_object_key: string | null;
  source_content_type: string | null;
  source_size_bytes: number | null;
  status: ProjectStatus;
  created_at: string;
};

export type ProcessingJob = {
  id: string;
  project_id: string;
  provider: string;
  requested_stems: StemType[];
  status: ProcessingJobStatus;
  created_at: string;
};

export type GeneratedStem = {
  id: string;
  project_id: string;
  processing_job_id: string;
  stem_type: StemType;
  file_key: string;
  created_at: string;
};

export type UploadTarget = {
  project_id: string;
  object_key: string;
  upload_url: string;
  upload_method: string;
  upload_headers: Record<string, string>;
  expires_in_seconds: number;
};

export type StemDownloadTarget = {
  stem_id: string;
  stem_type: StemType;
  file_key: string;
  download_url: string;
  download_method: string;
  expires_in_seconds: number;
};

export type UserSummary = {
  id: string;
  email: string;
  display_name: string;
  role: UserRole;
  active_plan_code: PlanCode;
};
