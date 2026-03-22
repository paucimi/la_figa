terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Opcional: guarda el estado en GCS para trabajo en equipo
  # backend "gcs" {
  #   bucket = "tu-bucket-tfstate"
  #   prefix = "la-figa/terraform.tfstate"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
