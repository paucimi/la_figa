# ─── APIs necesarias ─────────────────────────────────────────────────────────
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
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

# ─── Service Account para Cloud Run ──────────────────────────────────────────
resource "google_service_account" "la_figa_sa" {
  account_id   = "la-figa-cloudrun"
  display_name = "La Figa — Cloud Run Service Account"
  description  = "Identidad del servicio Cloud Run. Tiene acceso a Vertex AI."
}

# Vertex AI User: puede llamar a modelos Gemini y Text Embeddings
resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.la_figa_sa.email}"
}

# Permite leer imágenes de Artifact Registry
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

    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/la-figa/la-figa:${var.image_tag}"

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
        # Permite usar CPU fuera de las peticiones (útil para ChromaDB)
        cpu_idle = true
      }

      # Vertex AI — no necesita API key, usa el Service Account adjunto (ADC)
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

      # Directorios efímeros en Cloud Run
      env {
        name  = "CHROMA_DIR"
        value = "/tmp/chroma_db"
      }
      env {
        name  = "SESSIONS_DIR"
        value = "/tmp/sessions"
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
