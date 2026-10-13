# Computer Science Portfolio

A responsive React, TypeScript, and Vite portfolio for documenting a student's Computer Science work and learning. Candidate projects and bracketed profile fields are intentionally labeled; replace them only with details you can verify.

## Requirements

- Node.js 20.19+ or 22.12+ (for Vite 6)
- npm

## Run locally

```sh
npm install
npm run dev
```

Vite prints the local preview URL, usually `http://localhost:5173`.

## Edit portfolio content

Update `src/content.ts` to change your name, introduction, education, contact links, project write-ups, screenshots, learning, and achievements. Home, About, Projects, Learning, and Contact are separate hash-routed pages; project case studies use routes such as `#project/chess-game` and are generated from the shared project data. Put a real résumé file under `public/` and set `profile.resume` to its public path before showing the download link. Empty contact links stay as plain placeholders rather than broken buttons.

Self-study courses can be listed without certificates. Label them as independent learning and add the creator or provider, course link, topics completed, and any project or practice work. Do not imply a credential that was not awarded.

## Checks and production build

```sh
npm run typecheck
npm run build
npm run preview
```

The production files are written to `dist/`.

## Deploy

Build with `npm run build` and publish the contents of `dist/` to any static host that supports single-page applications. Configure the host to serve `index.html` for unknown paths. Because this site uses hash navigation, the project detail routes do not require server-side route rewrites. For GitHub Pages, set Vite's `base` in `vite.config.ts` to the repository path before building.

## Before publishing

- Replace profile placeholders and add only accurate personal and academic details.
- Add project source links and verify the documented behavior against the code.
- Replace candidate projects with completed work or keep the candidate label.
- Add evidence links for any achievement.
- Add a professional email, GitHub profile, and actual résumé only if you want them public.
- The reviewed local weather-app source has an API credential in the code. Rotate it and remove it from the source before publishing or sharing that project.
