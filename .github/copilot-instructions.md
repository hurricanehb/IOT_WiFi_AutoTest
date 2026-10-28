# PyAutoTest Repository Instructions

## Architecture Placement

- Treat `core/libs/` as the product-domain capability layer. Add code there only when its primary owner is a product domain such as Android, miniAP, or printer, and place it under that product's directory.
- Do not create technology-oriented or infrastructure-oriented directories under `core/libs/`, including `models`, `contracts`, `lab_equipment`, `drivers`, or generic `common` groupings. A device being used by product tests does not by itself make the device integration a product domain.
- Put cross-product infrastructure and laboratory integrations in `core/utils/` when they provide reusable transport, device-control, environment, or framework support. Keep product-independent interfaces in `core/contracts/`, structured-data loaders in `core/testdata_loader/`, and executable utilities in `tools/`.
- Co-locate small configuration dataclasses with the module that owns and consumes their behavior. Do not create a new directory solely to hold one small model or one implementation file.
- Before adding a module or directory, inspect the target directory's documented responsibility and nearby siblings, then state its owning domain. If no product owner can be named, do not place it in `core/libs/`.
- Prefer an existing module over a new package until multiple cohesive modules require a package boundary. Do not introduce speculative directories for possible future expansion.
- Do not reorganize unrelated existing code merely because it predates these rules. Apply the rules to the requested change and directly affected files.
- After moving modules, update every import, remove obsolete source and cache-only directories, verify no old import path remains, run a fresh-interpreter import, run the focused unit tests, and collect affected pytest modules.

## Reuse Before Adding

- Before adding a parameter, fixture, helper, test-data profile, YAML key, or configuration entry, search for an existing item that can satisfy the same test purpose.
- Decide reuse by test intent and behavior, not by case name or incidental value differences. If two scenarios validate the same capability, prefer one shared configuration and align nonessential values such as passwords.
- Express necessary scenario differences through existing function arguments or case metadata before creating another configuration entry.
- Add a new parameter or configuration only when an existing abstraction cannot represent a behaviorally distinct requirement. State that requirement in the name or description.
- When consolidating configuration, update every reference, remove obsolete entries, and keep case prerequisites consistent with the effective shared data.
- After changes, validate that structured data loads successfully, all referenced IDs resolve, old IDs have no remaining references, and affected pytest modules still collect.
