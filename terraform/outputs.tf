output "service_url" {
  description = "URL pública del servicio Cloud Run"
  value       = google_cloud_run_v2_service.la_figa.uri
}

output "artifact_registry_url" {
  description = "URL base del repositorio Artifact Registry"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/la-figa"
}

output "docker_build_and_push" {
  description = "Comandos para construir y subir la imagen Docker"
  value       = <<-EOT
    # 1. Autenticarse en Artifact Registry
    gcloud auth configure-docker ${var.region}-docker.pkg.dev

    # 2. Construir la imagen
    docker build -t ${var.region}-docker.pkg.dev/${var.project_id}/la-figa/la-figa:latest .

    # 3. Subir la imagen
    docker push ${var.region}-docker.pkg.dev/${var.project_id}/la-figa/la-figa:latest
  EOT
}

output "service_account_email" {
  description = "Email del Service Account usado por Cloud Run"
  value       = google_service_account.la_figa_sa.email
}

output "chroma_gcs_bucket" {
  description = "Bucket GCS donde ChromaDB persiste los artículos entre reinicios"
  value       = google_storage_bucket.chroma_db.name
}
