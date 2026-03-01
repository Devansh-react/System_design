## System Design – SOLID Principles in C++

This repository demonstrates **SOLID design principles** using simple, focused **C++ examples**.  
Each principle has:

- **Clean implementation** that follows the principle
- **Violation example** that shows what to avoid
- **Diagram (`.png`)** to visualize the design

The goal is to give you small, realistic snippets you can quickly read, run, and adapt.

### Repository structure

```
SOLID_design_principal/
├── SRP/
│   ├── SRP.cpp              – Single Responsibility Principle (correct)
│   ├── SRP_voilated.cpp     – SRP violation
│   └── SRP_principal.png    – SRP class diagram
├── OCP/
│   ├── OCP.cpp              – Open/Closed Principle (correct)
│   ├── ocp_voilated.cpp     – OCP violation
│   └── OCP.png              – OCP diagram
├── LSP/
│   ├── LSP.cpp              – Liskov Substitution Principle (correct)
│   ├── LSP_voilate.cpp      – LSP violation
│   ├── LSP.png              – LSP diagram
│   ├── Method_rules/        – Pre/Post condition rules
│   │   ├── PreConditions.cpp
│   │   └── PostConditions.cpp
│   ├── Property_rule/       – Invariant & history rules
│   │   ├── ClassInvariants.cpp
│   │   └── HistoryConstraint.cpp
│   └── Signature_rule/      – Return type, arguments, exceptions
│       ├── ReturnTypeRule.cpp
│       ├── MethodArgumentRule.cpp
│       └── ExceptionRule.cpp
├── ISP/
│   ├── Isp.cpp             – Interface Segregation Principle (correct)
│   ├── isp_voilated.cpp    – ISP violation
│   └── ISP.png             – ISP diagram
└── DIP/
    ├── Dip.cpp             – Dependency Inversion Principle (correct)
    ├── Dip_voilated.cpp    – DIP violation
    └── DIP.png             – DIP diagram
```

### Principles overview

- **SRP (Single Responsibility Principle)**  
  A class should have **only one reason to change**.  
  In this repo:
  - `SRP.cpp` splits responsibilities into:
    - **`ShoppingCart`** – manages products and totals
    - **`ShoppingCartPrinter`** – prints invoices
    - **`ShoppingCartStorage`** – persistence
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
  - **LSP subrules** (in `Method_rules/`, `Property_rule/`, `Signature_rule/`):
    - **PreConditions** – subclasses can weaken preconditions but not strengthen them
    - **PostConditions** – subclasses can strengthen postconditions but not weaken them
    - **ClassInvariants** – child classes must maintain or strengthen parent invariants
    - **HistoryConstraint** – subclasses must not introduce state changes the base class never allowed
    - **ReturnTypeRule** – return types must be identical or narrower (covariance)
    - **MethodArgumentRule** – method arguments must be identical or wider
    - **ExceptionRule** – subclasses should throw fewer or narrower exceptions

- **ISP (Interface Segregation Principle)**  
  Clients should not be forced to depend on interfaces they do not use.  
  In this repo:
  - `Isp.cpp` defines separate interfaces (`TwoDimensionalShape`, `ThreeDimensionalShape`) so 2D shapes implement only `area()` and 3D shapes implement `area()` and `volume()`.
  - `isp_voilated.cpp` forces all shapes into a single `Shape` interface with `volume()`, making 2D shapes throw exceptions for an irrelevant method.

- **DIP (Dependency Inversion Principle)**  
  High-level modules should not depend on low-level modules; both should depend on abstractions.  
  In this repo:
  - `Dip.cpp` uses a `Database` interface with dependency injection so `UserService` depends on the abstraction, not concrete `MySQLDatabase` or `MongoDBDatabase`.
  - `Dip_voilated.cpp` tightly couples `UserService` to both MySQL and MongoDB with separate methods for each.

### How to build and run (Windows / g++)

Compile each example independently. From the repo root:

**SRP**
```powershell
cd SOLID_design_principal/SRP
g++ SRP.cpp -std=c++11 -o srp
g++ SRP_voilated.cpp -std=c++11 -o srp_violation
```

**OCP**
```powershell
cd SOLID_design_principal/OCP
g++ OCP.cpp -std=c++11 -o ocp
g++ ocp_voilated.cpp -std=c++11 -o ocp_violation
```

**LSP**
```powershell
cd SOLID_design_principal/LSP
g++ LSP.cpp -std=c++11 -o lsp
g++ LSP_voilate.cpp -std=c++11 -o lsp_violation
```

**LSP subrules**
```powershell
cd SOLID_design_principal/LSP/Method_rules
g++ PreConditions.cpp -std=c++11 -o preconditions
g++ PostConditions.cpp -std=c++11 -o postconditions

cd ../Property_rule
g++ ClassInvariants.cpp -std=c++11 -o invariants
g++ HistoryConstraint.cpp -std=c++11 -o history

cd ../Signature_rule
g++ ReturnTypeRule.cpp -std=c++11 -o return_type
g++ MethodArgumentRule.cpp -std=c++11 -o method_arg
g++ ExceptionRule.cpp -std=c++11 -o exception_rule
```

**ISP**
```powershell
cd SOLID_design_principal/ISP
g++ Isp.cpp -std=c++11 -o isp
g++ isp_voilated.cpp -std=c++11 -o isp_violation
```

**DIP**
```powershell
cd SOLID_design_principal/DIP
g++ Dip.cpp -std=c++11 -o dip
g++ Dip_voilated.cpp -std=c++11 -o dip_violation
```

Run the executables with `./name` (Linux/macOS) or `.\name.exe` (Windows PowerShell).

Adjust compiler flags as needed for your toolchain (e.g., `clang++` instead of `g++`).

### Requirements

- **C++11 or later** compatible compiler (e.g., `g++`, `clang++`, MSVC)
- A terminal or shell (PowerShell, CMD, Bash, etc.)

### License

This project is licensed under the terms described in `LICENSE`.
