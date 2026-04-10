## System Design – SOLID & Design Patterns (C++ & Python)

This repository demonstrates **SOLID design principles** and **classic design patterns** using simple, focused **C++ and Python examples**.  
Most principles/patterns include:

- **Clean implementation** that follows the principle
- **Violation example** that shows what to avoid
- **Diagram (`.png`)** to visualize the design

The goal is to give you small, realistic snippets you can quickly read, run, and adapt in either C++ or Python.

### Repository structure (C++)

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

### Repository structure (Python)

- `Design_principle/`
  - `Strategy_design_pattern/`
    - `StrategyDesignPattern.py` – Strategy pattern with robot behaviors (walk/talk/fly)
  - `Factory_designn_pattern/`
    - `SimpleFactory.py` – Simple Factory for burgers
    - `FactoryMethod.py` – Factory Method with multiple burger brands
    - `AbstractFactory.py` – Abstract Factory producing burgers + garlic bread
- `Food_delivery_app/`
  - `Food_delivery.py` – Food delivery system design example (customers, restaurants, orders, delivery)
- `Google_docs/`
  - `Document_editor.py` – Document editor example (composite + persistence abstraction)

### SOLID principles (C++)

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
### Design patterns (Python)

- **Strategy pattern (`StrategyDesignPattern.py`)**
  - `Robot` composes three behaviors: `WalkableRobot`, `TalkableRobot`, `FlyableRobot`.
  - Concrete strategies like `NormalWalk`, `NoWalk`, `NormalTalk`, `NoTalk`, `NormalFly`, `NoFly` can be combined to build different robot types (`CompanionRobot`, `WorkerRobot`) without changing their code.

- **Simple Factory (`SimpleFactory.py`)**
  - `BurgerFactory` decides which `Burger` implementation (`BasicBurger`, `StandardBurger`, `PremiumBurger`) to build based on a string type.

- **Factory Method (`FactoryMethod.py`)**
  - `BurgerFactory` is an abstraction implemented by `SinghBurger` and `KingBurger`.
  - Each factory creates its own family of burgers (regular vs wheat variants) while clients depend only on the factory interface.

- **Abstract Factory (`AbstractFactory.py`)**
  - `MealFactory` can create multiple related products: `Burger` and `GarlicBread`.
  - `SinghBurger` and `KingBurger` produce matching burger + garlic bread combinations (normal vs wheat).

- **Document editor (`Document_editor.py`)**
  - Uses a composite-style `Document` made of `DocumentElement` implementations (`TextElement`, `ImageElement`, `NewLineElement`, `TabSpaceElement`).
  - `DocumentEditor` provides a simple API to build a document and delegates persistence to a `Persistence` abstraction (`FileStorage`, `DBStorage` placeholder).

### How to build and run

- **C++ examples (Windows / g++)**
  - Use the commands under `SOLID_design_principal/` as shown above (e.g. `g++ SRP.cpp -std=c++11 -o srp`).
  - Run with `./name` (Linux/macOS) or `.\name.exe` (Windows PowerShell).

- **Python examples**
  - Requires **Python 3.10+** (for the `|` union type hints).
  - From the repo root:

```powershell
cd Design_principle/Strategy_design_pattern
python StrategyDesignPattern.py

cd ../Factory_designn_pattern
python SimpleFactory.py
python FactoryMethod.py
python AbstractFactory.py

cd ../../Google_docs
python Document_editor.py
```

Adjust interpreter/paths as needed (e.g., `python3` on Linux/macOS).

### Requirements

- **C++11 or later** compatible compiler (e.g., `g++`, `clang++`, MSVC)
- **Python 3.10+** interpreter
- A terminal or shell (PowerShell, CMD, Bash, etc.)

### License

This project is licensed under the terms described in `LICENSE`.
