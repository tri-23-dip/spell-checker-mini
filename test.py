from corrector import SpellChecker

def run_demo():
    checker = SpellChecker()

    while True:
        text = input("\nEnter text (or 'quit'): ")
        if text.lower() == "quit":
            break

        errors = checker.check_text(text)
        if not errors:
            print("All words correct!")
        else:
            print("Errors found:")
            for word, suggestions in errors.items():
                print(f"{word} -> {[s[0] for s in suggestions]}")

        print("Auto-corrected:", checker.auto_correct(text))


if __name__ == "__main__":
    run_demo()