# CI/CD Toolkit for Instabase

A Python package to migrate Instabase applications between different environments (e.g., Dev → Prod).

## Supported Flows

| Flow | CLI Command | Description |
|------|-------------|-------------|
| Normal Flow | `promote-solution` | Migrate flow-based solutions |
| Solution Builder Flow | `promote-sb-solution` | Migrate Solution Builder projects |
| Build App | `promote-build-solution` | Migrate Build apps |

## Installation

### From GitHub Release

```bash
pip install https://github.com/samyak-ib/ci-cd-toolkit-for-NW/releases/download/vX.X.X/cicd_aihub-X.X.X-py3-none-any.whl
```

### From Source

```bash
git clone https://github.com/samyak-ib/ci-cd-toolkit-for-NW.git
cd ci-cd-toolkit-for-NW
pip install -e .
```

## Required Secrets

When using this toolkit in GitHub Actions, configure the following secrets in your repository:

### API Authentication

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `SOURCE_HOST_URL` | Source (Dev) Instabase host URL (e.g., `https://dev.instabase.com`) | ✅ Yes |
| `SOURCE_TOKEN` | Source (Dev) API token | ✅ Yes |
| `TARGET_HOST_URL` | Target (Prod) Instabase host URL (e.g., `https://prod.instabase.com`) | ✅ Yes |
| `TARGET_TOKEN` | Target (Prod) API token | ✅ Yes |

### mTLS Certificates (Optional)

If your Instabase environments require mutual TLS (mTLS) authentication, add these secrets:

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `MTLS_SOURCE_CERT_CONTENT` | Source (Dev) certificate PEM file content | If mTLS enabled |
| `MTLS_SOURCE_KEY_CONTENT` | Source (Dev) private key PEM file content | If mTLS enabled |
| `MTLS_TARGET_CERT_CONTENT` | Target (Prod) certificate PEM file content | If mTLS enabled |
| `MTLS_TARGET_KEY_CONTENT` | Target (Prod) private key PEM file content | If mTLS enabled |

### Proxy Configuration (Optional)

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `PROXY_HOST` | Proxy server hostname | If using proxy |
| `PROXY_PORT` | Proxy server port | If using proxy |
| `PROXY_USER` | Proxy username | If proxy requires auth |
| `PROXY_PASSWORD` | Proxy password | If proxy requires auth |

## Environment Variables

The toolkit reads the following environment variables at runtime:

### API Configuration
- `SOURCE_HOST_URL` - Source Instabase host URL
- `SOURCE_TOKEN` - Source API token
- `TARGET_HOST_URL` - Target Instabase host URL
- `TARGET_TOKEN` - Target API token

### mTLS Certificate Paths
- `MTLS_SOURCE_CERT` - Path to source certificate PEM file
- `MTLS_SOURCE_KEY` - Path to source private key PEM file
- `MTLS_TARGET_CERT` - Path to target certificate PEM file
- `MTLS_TARGET_KEY` - Path to target private key PEM file

> **Note:** In GitHub Actions, the workflow writes certificate content from secrets to temporary files and sets these environment variables to point to those files.

## Workflow Setup

### Step 1: Add Secrets to Your Repository

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each secret listed above

### Step 2: Setup mTLS Certificates in Workflow

Add this step to your GitHub Actions workflow after checkout:

```yaml
- name: Setup mTLS certificates
  run: |
    mkdir -p $RUNNER_TEMP/certs
    echo "${{ secrets.MTLS_SOURCE_CERT_CONTENT }}" > $RUNNER_TEMP/certs/source_cert.pem
    echo "${{ secrets.MTLS_SOURCE_KEY_CONTENT }}" > $RUNNER_TEMP/certs/source_key.pem
    echo "${{ secrets.MTLS_TARGET_CERT_CONTENT }}" > $RUNNER_TEMP/certs/target_cert.pem
    echo "${{ secrets.MTLS_TARGET_KEY_CONTENT }}" > $RUNNER_TEMP/certs/target_key.pem
    chmod 600 $RUNNER_TEMP/certs/*.pem
    
    # Export paths for subsequent steps
    echo "MTLS_SOURCE_CERT=$RUNNER_TEMP/certs/source_cert.pem" >> $GITHUB_ENV
    echo "MTLS_SOURCE_KEY=$RUNNER_TEMP/certs/source_key.pem" >> $GITHUB_ENV
    echo "MTLS_TARGET_CERT=$RUNNER_TEMP/certs/target_cert.pem" >> $GITHUB_ENV
    echo "MTLS_TARGET_KEY=$RUNNER_TEMP/certs/target_key.pem" >> $GITHUB_ENV
```

### Step 3: Use CLI Commands

```yaml
- name: Fetch Latest App Data
  run: |
    promote-solution --compile_solution --download_solution

- name: Migrate to Target
  run: |
    promote-solution --promote_solution_to_target
```

## CLI Reference

### promote-solution

Migrate flow-based solutions.

```bash
promote-solution [OPTIONS]

Options:
  --compile_solution        Compile the solution on source
  --download_solution       Download the solution from source
  --promote_solution_to_target  Upload solution to target
  --upload_dependencies     Upload dependencies to target
  --publish_advanced_app    Publish as advanced app on target
  --create_deployment       Create deployment on target
```

### promote-sb-solution

Migrate Solution Builder projects.

```bash
promote-sb-solution [OPTIONS]

Options:
  --compile_solution        Compile the solution on source
  --download_solution       Download the solution from source
  --promote_solution_to_target  Upload solution to target
  --upload_dependencies     Upload dependencies to target
  --publish_advanced_app    Publish as advanced app on target
  --create_deployment       Create deployment on target
```

### promote-build-solution

Migrate Build apps.

```bash
promote-build-solution [OPTIONS]

Options:
  --compile_solution        Compile the solution on source
  --download_solution       Download the solution from source
  --create_build_project    Create build project on target
  --rebuild                 Rebuild the project on target
  --publish_build_app       Publish build app on target
  --create_deployment       Create deployment on target
  --delete_build            Delete the build project
```

## Example Workflows

See the `workflows/` directory for complete workflow examples:

- [`commit_and_fetch.yml`](workflows/commit_and_fetch.yml) - Fetch latest code from source environment
- [`merge_and_migrate.yml`](workflows/merge_and_migrate.yml) - Migrate to target environment

## Architecture

```
┌─────────────────────┐                      ┌─────────────────────┐
│   SOURCE (Dev)      │                      │   TARGET (Prod)     │
│                     │                      │                     │
│  HOST: SOURCE_      │    Download          │  HOST: TARGET_      │
│        HOST_URL     │  ─────────────────>  │        HOST_URL     │
│  TOKEN: SOURCE_     │                      │  TOKEN: TARGET_     │
│         TOKEN       │     Upload           │         TOKEN       │
│  CERT: MTLS_        │  <─────────────────  │  CERT: MTLS_        │
│        SOURCE_*     │                      │        TARGET_*     │
└─────────────────────┘                      └─────────────────────┘
```

## Development

### Running Tests

```bash
pip install -e ".[test]"
pytest
```

### Building the Package

```bash
pip install build
python -m build
```

This creates a wheel file in `dist/` that can be distributed.

## License

Internal use only.
