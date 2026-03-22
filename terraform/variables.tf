variable "project_id" {
  description = "Google Cloud Project ID (el que tiene los 300€ de crédito)"
  type        = string
}

variable "region" {
  description = "Región de Google Cloud donde se desplegará todo"
  type        = string
  default     = "europe-west1"
}

variable "image_tag" {
  description = "Tag de la imagen Docker en Artifact Registry"
  type        = string
  default     = "latest"
}

variable "newspaper_name" {
  description = "Nombre del periódico"
  type        = string
  default     = "la_figa"
}

variable "gemini_model" {
  description = "Modelo Gemini a usar vía Vertex AI"
  type        = string
  default     = "gemini-2.5-flash"
}

variable "language" {
  description = "Idioma de los artículos y respuestas"
  type        = string
  default     = "español"
}

variable "chroma_gcs_bucket" {
  description = "Nombre del bucket GCS para ChromaDB persistente. Si se deja vacío se genera como '{project_id}-la-figa-chroma'"
  type        = string
  default     = ""
}
