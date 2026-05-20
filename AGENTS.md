# AI Agent Customization Guide - Python Learning/Utilities Project

## Project Overview
This is a personal Python learning and utilities workspace containing educational scripts and calculator applications. The project demonstrates foundational Python concepts through practical examples.

## Project Structure

| File | Purpose |
|------|---------|
| `draft.py` | Educational content - Python basics, data types, functions, and profit calculations |
| `profit.py` | Tax calculator - computes net profit based on income and tax brackets |
| `Web scraping.py` | Web scraping example with graceful fallback from requests/BeautifulSoup to urllib |
| `Калькулятор (n!) log_b(x).py` | Scientific calculator - factorial and logarithm computations |
| `Калькулятор простий -1.py` | Basic calculator - addition, subtraction, multiplication, division |

## Language & Conventions

- **Primary Language**: Ukrainian (both code comments and user-facing text)
- **Scripts**: Interactive CLI applications with menu-driven interfaces
- **Python Version**: Python 3.x

## Common Patterns

### 1. Error Handling & Validation
- Division by zero protection in calculators
- Input type validation (converting strings to float/int)
- Mathematical domain validation (e.g., negative factorials, zero in logarithms)
- Graceful error messages displayed to users

### 2. User Input & Menus
- Use `input()` with Ukrainian prompts
- Menu-driven loops with `while True`
- Input validation before processing
- Provide clear exit options (usually option 5 or similar)

### 3. Interactive Programs
All scripts follow this general structure:
```python
def main():
    print("=== Program Title ===")
    while True:
        print("\nMenu options...")
        # Get user input
        # Validate input
        # Process and display results
```

## Development Guidelines

### When Adding Features
1. **Maintain Ukrainian UX** - Keep all user-facing text in Ukrainian
2. **Validate Early** - Check user input types and mathematical domain before calculations
3. **Clear Feedback** - Use formatted strings (f-strings) for informative output
4. **Exit Gracefully** - Always provide a clean exit option from loops
5. **Comment in Ukrainian** - Maintain consistency with existing code

### Common Modifications
- **Adding calculator operations**: Add function, add menu option, integrate into main loop
- **Improving input validation**: Use try-except with meaningful Ukrainian error messages
- **Testing edge cases**: Negative numbers, zero, very large numbers, non-numeric input

## Dependencies
- Standard library: `math`, `urllib.request`
- Optional: `requests`, `beautifulsoup4` (with fallback in Web scraping.py)

## Tips for AI Agents
- Always preserve Ukrainian language in user interfaces and comments
- Test new code with edge cases (0, negative numbers, very large values)
- Use docstrings for complex functions (Ukrainian or English both acceptable)
- Format currency/financial output with 2 decimal places when relevant
- When modifying calculators, verify mathematical accuracy with domain constraints
