# Custom Practice Template

Copy this entire folder to `custom_practice/<company>/<your_problem_name>/`.

1. Replace `solve` in `solution.py` with the desired function signature and implementation stub.
2. Add visible `Case` entries in `test_cases.py`.
3. If the function needs input construction or output normalization, add a small adapter in
   `run_tests.py` and pass that adapter to `run_cli` instead of `solve`.
4. Run `python3 custom_practice/<company>/<your_problem_name>/run_tests.py`.

Keep the copied practice standard-library-only unless the actual interview environment guarantees
additional packages.
