# Project source collection

This folder contains selected source files from my Python and C++ work folders, organized by language and purpose.

## What's here

- `python/apps/desktop/` — digital clock, stopwatch, and weather app.
- `python/games/` — chess experiments and an animal hangman game.
- `python/practice/codewars/` — kata solutions grouped by kyu level.
- `python/practice/toi-zero/` — TOI-ZERO practice solutions grouped by problem ID.
- `python/practice/misc/` — smaller Python exercises.
- `cpp/` — small apps, games, sorting, linked-list exercises, and experiments.

## Running the examples

These are independent learning projects, not one combined application. Many C++ files have their own `main()` function and should be compiled separately. For example:

```sh
g++ cpp/apps/base36-converter.cpp -o base36-converter
```

Python apps may need third-party libraries. The chess projects use Tkinter or Pygame; the desktop examples use PyQt5; and some chess versions use `python-chess`. Install only the packages required by the project you want to run.

The weather app expects an OpenWeatherMap key in the `OPENWEATHERMAP_API_KEY` environment variable. Do not put keys in source files or commit them.

## Notes

- Only non-empty source files and required small data files were copied.
- Executables, build folders, virtual environments, caches, editor settings, and empty placeholders were left out.
- These files are learning work and are not all tested or complete. Check each source before relying on it.
