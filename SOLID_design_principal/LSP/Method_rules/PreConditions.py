from __future__ import annotations


class User:
    # Precondition: password must be at least 8 characters long
    def set_password(self, password: str) -> None:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long!")
        print("Password set successfully")


class AdminUser(User):
    # Weakened precondition: password must be at least 6 characters long
    def set_password(self, password: str) -> None:
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long!")
        print("Password set successfully")


def main() -> None:
    user: User = AdminUser()
    user.set_password("Admin1")  # Works fine: AdminUser allows shorter passwords


if __name__ == "__main__":
    main()

