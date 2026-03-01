## System Design – SOLID Principles in C++

This repository demonstrates **SOLID design principles** using simple, focused **C++ examples**.  
Each principle has:

- **Clean implementation** that follows the principle
- **Violation example** that shows what to avoid
- **Diagram (`.png`)** to visualize the design

The goal is to give you small, realistic snippets you can quickly read, run, and adapt.

### Repository structure

- `CPP/`
  - `SRP/`
    - `SRP.cpp` – Single Responsibility Principle (correct)
    - `SRP_voilated.cpp` – SRP violation
    - `SRP_principal.png` – SRP class diagram
  - `OCP/`
    - `OCP.cpp` – Open/Closed Principle (correct)
    - `ocp_voilated.cpp` – OCP violation
    - `OCP.png` – OCP diagram
  - `LSP/`
    - `LSP.cpp` – Liskov Substitution Principle (correct)
    - `LSP_voilate.cpp` – LSP violation
    - `LSP.png` – LSP diagram

### Principles overview

- **SRP (Single Responsibility Principle)**  
  A class should have **only one reason to change**.  
  In this repo:
  - `SRP.cpp` splits responsibilities into:
    - **`ShoppingCart`** – manages products and totals
    - **`ShoppingCartPrinter``** – prints invoices
    - **(optionally) persistence / storage classes**
  - `SRP_voilated.cpp` shows the opposite, where one class takes on too many roles.

- **OCP (Open/Closed Principle)**  
  Software entities should be **open for extension, closed for modification**.  
  In this repo:
  - `OCP.cpp` defines a `Persistence` abstraction with multiple implementations (`SQLPersistence`, `MongoPersistence`, `FilePersistence`) so you can add new storage types **without touching existing client code**.
  - `ocp_voilated.cpp` uses conditionals/switches and needs changes in existing code whenever a new storage type is added.

- **LSP (Liskov Substitution Principle)**  
  Subtypes must be **substitutable** for their base types without breaking behavior.  
  In this repo:
  - `LSP_voilate.cpp` models accounts where some subclasses throw exceptions or break expectations when used through the base type.
  - `LSP.cpp` refactors the hierarchy into:
    - `DepositOnlyAccount`
    - `WithdrawableAccount`
    - Concrete types like `SavingAccount`, `CurrentAccount`, `FixedTermAccount`
    so that each class can safely be used via the correct abstraction.

### How to build and run (Windows / g++)

You can compile each example independently. From the repo root:

- **SRP (correct)**:
  - `cd CPP/SRP`
  - `g++ SRP.cpp -std=c++11 -o srp`
  - `./srp` (or `srp.exe` on Windows)

- **SRP (violation)**:
  - `cd CPP/SRP`
  - `g++ SRP_voilated.cpp -std=c++11 -o srp_violation`
  - `./srp_violation`

- **OCP (correct)**:
  - `cd CPP/OCP`
  - `g++ OCP.cpp -std=c++11 -o ocp`
  - `./ocp`

- **OCP (violation)**:
  - `cd CPP/OCP`
  - `g++ ocp_voilated.cpp -std=c++11 -o ocp_violation`
  - `./ocp_violation`

- **LSP (correct)**:
  - `cd CPP/LSP`
  - `g++ LSP.cpp -std=c++11 -o lsp`
  - `./lsp`

- **LSP (violation)**:
  - `cd CPP/LSP`
  - `g++ LSP_voilate.cpp -std=c++11 -o lsp_violation`
  - `./lsp_violation`

Adjust compiler flags as needed for your toolchain (e.g., `clang++` instead of `g++`).

### Requirements

- **C++11 or later** compatible compiler (e.g., `g++`, `clang++`, MSVC)
- A terminal or shell (PowerShell, CMD, Bash, etc.)

### License

This project is licensed under the terms described in `LICENSE`.

