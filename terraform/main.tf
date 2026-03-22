# ─── APIs necesarias ─────────────────────────────────────────────────────────
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# ─── Artifact Registry ───────────────────────────────────────────────────────
resource "google_artifact_registry_repository" "la_figa" {
  repository_id = "la-figa"
  location      = var.region
  format        = "DOCKER"
  description   = "Imágenes Docker del periódico multiagente La Figa"

  depends_on = [google_project_service.apis]
}

# ─── Bucket GCS para ChromaDB persistente ────────────────────────────────────
# Sin este bucket, ChromaDB vive en /tmp y se borra al reiniciar el contenedor.
# Cloud Run monta el bucket como un volumen FUSE en /mnt/chroma_db.
resource "google_storage_bucket" "chroma_db" {
  name                        = local.chroma_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false # protege contra borrado accidental con terraform destroy

  depends_on = [google_project_service.apis]
}

locals {
  # Si el usuario pasa un nombre de bucket lo usa; si no, lo genera automáticamente
  chroma_bucket_name = var.chroma_gcs_bucket != "" ? var.chroma_gcs_bucket : "${var.project_id}-la-figa-chroma"
}

# ─── Service Account para Cloud Run ──────────────────────────────────────────
resource "google_service_account" "la_figa_sa" {
  account_id   = "la-figa-cloudrun"
  display_name = "La Figa — Cloud Run Service Account"
  description  = "Identidad del servicio Cloud Run. Tiene acceso a Vertex AI y GCS."
}

# Vertex AI User: llama a modelos Gemini y Text Embeddings
resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.la_figa_sa.email}"
}

# Lectura/escritura en el bucket de ChromaDB
resource "google_storage_bucket_iam_member" "chroma_db_admin" {
  bucket = google_storage_bucket.chroma_db.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.la_figa_sa.email}"
}

# Lectura de imágenes en Artifact Registry
resource "google_project_iam_member" "artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.la_figa_sa.email}"
}

# ─── Cloud Run ───────────────────────────────────────────────────────────────
resource "google_cloud_run_v2_service" "la_figa" {
  name     = "la-figa"
  location = var.region

  template {
    service_account = google_service_account.la_figa_sa.email

    # 5 agentes en cadena pueden tardar varios minutos: 300s evita cortes de conexión
    timeout = "300s"

    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }

    # Volumen GCS montado como sistema de archivos (FUSE) → ChromaDB persistente
    volumes {
      name = "chroma-gcs"
      gcs {
        bucket    = google_storage_bucket.chroma_db.name
        read_only = false
      }
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/la-figa/la-figa:${var.image_tag}"

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
        cpu_idle = true
      }

      # ChromaDB apunta al bucket GCS montado → persiste entre reinicios
      volume_mounts {
        name       = "chroma-gcs"
        mount_path = "/mnt/chroma_db"
      }

      # Vertex AI — ADC automático vía Service Account adjunto
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "GOOGLE_CLOUD_LOCATION"
        value = var.region
      }
      env {
        name  = "GOOGLE_GENAI_USE_VERTEXAI"
        value = "1"
      }

      # ChromaDB apunta al mount GCS (no a /tmp efímero)
      env {
        name  = "CHROMA_DIR"
        value = "/mnt/chroma_db"
      }
      env {
        name  = "SESSIONS_DIR"
        value = "/tmp/sessions"
      }

      # Configuración editorial
      env {
        name  = "NEWSPAPER_NAME"
        value = var.newspaper_name
      }
      env {
        name  = "GEMINI_MODEL"
        value = var.gemini_model
      }
      env {
        name  = "LANGUAGE"
        value = var.language
      }

      ports {
        container_port = 8080
      }
    }
  }

  depends_on = [
    google_project_service.apis,
    google_artifact_registry_repository.la_figa,
    google_project_iam_member.vertex_ai_user,
    google_storage_bucket_iam_member.chroma_db_admin,
  ]
}

# Acceso público sin autenticación (como Render.com)
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = google_cloud_run_v2_service.la_figa.project
  location = google_cloud_run_v2_service.la_figa.location
  name     = google_cloud_run_v2_service.la_figa.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
