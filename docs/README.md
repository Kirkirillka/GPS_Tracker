# Project Documentation

## Description

Welcome to the documentation!

The documentation based on [arc42](http://arc42.org) suggested template.

The following sections are available:

1. [Introduction and Motivation](01_01_introduction.md)
2. [Solution strategy](02_01_architecture_constraints.md)
3. [Contex and Scope](03_01_context_and_scope.md)
4. [Solution Strategy](04_01_solution_strategy.md)
5. [Building Blocks](05_01_building_blocks.md)
6. [Deployment View](07_01_deployment_view.md)
7. [Crosscutting concepts](08_01_crosscutting_concepts.md)
8. [Architecture Decisions](09_00_architecture_decisions.md)
9. [Risk and Technical Debts](11_01_risk_and_debt.md)
10. [Glossary](12_00_glossary.md)

Also, you can find out more detailed information on the sections:

- About System Components - [link](components/README.md)
- About Using Data structures - [link](data_structures/README.md)
- Description of Protocols and Interfaces - [link](interfaces/README.md)
- Diagrams and Schemes - [link](schemes/README.md)
- About System Launching - #TODO: 
- About System Testing - [link](testing/README.md)


## Usage

Generate a PDF file:

```bash
pandoc *.md -H disable_float.tex -o "Performance analysis framework for base station placement using IEEE 802.11.pdf"
```
