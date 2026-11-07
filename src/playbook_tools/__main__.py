"""Point d'entrée « python -m playbook_tools » (équivalent de la commande playbook-check)."""

import sys

from playbook_tools.check import main

sys.exit(main())
