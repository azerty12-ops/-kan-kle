1. **Add Authentication Middleware (`src/bot/main.py`)**
   - Import `TypeHandler` and `ApplicationHandlerStop` from `telegram.ext`.
   - Read `ALLOWED_USER_ID` from environment variables.
   - Create an asynchronous `auth_middleware` function that compares `update.effective_user.id` against `ALLOWED_USER_ID`.
   - If unauthorized, raise `ApplicationHandlerStop()` to halt update processing.
   - Register the `auth_middleware` using `TypeHandler(Update, auth_middleware)` with `group=-1` in the `main` function.

2. **Update `.env.example`**
   - Add `ALLOWED_USER_ID` variable so users know to configure it.

3. **Create Security Journal (`.jules/sentinel.md`)**
   - Document the critical vulnerability of exposing a personal assistant bot without authorization.
   - Document the fix pattern (using `TypeHandler` and `ApplicationHandlerStop` for global middleware).

4. **Verify Syntax and Complete Pre-commit Steps**
   - Run `python -m py_compile src/bot/main.py` to verify syntax.
   - Call `pre_commit_instructions` tool to ensure proper testing, verification, review, and reflection are done.

5. **Submit PR**
   - Submit the change with a descriptive commit message indicating it's a critical security fix.
