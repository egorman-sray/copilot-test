# Project Overview

This repository contains code for a microservice that preprocesses documents to be ingested by our bespoke data extraction service. It is built with Python and interacts directly with other GCP cloud services.

## Folder Structure

- `/ai_document_preproessor`: Contains the source code for the service.
- `/argocd`: Contains config yamls for ArgoCD.
- `/charts`: Contains config yamls for Helm.
- `/cicd`: Contains config yamls for our CICD pipelines (run via ArgoCD).
- `/tests`: Contains the unit and integration tests for the service.

## Libraries and Frameworks

- Python for the service usecase/business logic.
- PubSub queue for retrieving preprocess requests.
- GCS for retrieving and storing documents.

## Coding Standards

- Write clear, maintainable, and well-documented code.
- Write small, well-defined interfaces between adapters and business logic.
- Input and output adapters should not include any business logic.
- Use factory functions to ensure proper dependency injection.
- Include type hints and docstrings, and comments only when code is unclear.
- Write comprehensive unit and integration tests that cover base and edge cases.
- Never store secrets, credentials, or sensitive data in code or configuration files.

## Reviews

- You should include all changes that you think need to be made.
- Do not include a summary of the changes that were made.
- If you have no suggestions, keep your response simple (e.g. LGTM).
- Add a smiley face emoticon to the end of every sentence.

