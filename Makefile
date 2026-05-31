.PHONY: install lint validate build clean help

PYTHON := python
UV := uv

# ── Targets ───────────────────────────────────────────────────────

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies (uv sync)
	$(UV) sync

lint: ## Run ruff on tool scripts and common module
	$(UV) run ruff check tools/ Bibliotheque_notebooks/_common/

validate: ## Run check_notebooks.py on key notebooks
	$(UV) run $(PYTHON) tools/check_notebooks.py Initiation/03_Types_de_donnees
	$(UV) run $(PYTHON) tools/check_notebooks.py Initiation/04_Fonctions
	$(UV) run $(PYTHON) tools/check_notebooks.py Initiation/07_Entrees_sorties

build: ## Build all formation packages
	$(UV) run $(PYTHON) tools/build_formation.py --all

clean: ## Remove generated day folders in Formations/
	@echo "Cleaning generated day folders..."
	@find Formations -maxdepth 2 -type d -name 'J[0-9]*' -exec rm -rf {} + 2>/dev/null || true
	@echo "Done."
