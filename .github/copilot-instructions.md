# Copilot Instructions for Jintian's Personal Site

## Overview
This repository contains a simple static website template for GitHub Pages, designed for personal use. It does not rely on Jekyll, Ruby, or complex build tools, making it easy to maintain and update.

## Architecture
- **Main Components**: The site is structured into several key directories:
  - `about/`: Contains personal information and skills.
  - `blog/`: Hosts blog posts and notes, with each post in its own folder.
  - `projects/`: Showcases various projects with descriptions and links.
  - `contact/`: Provides contact information and links to social media.

- **Data Flow**: Content is primarily static, with HTML files serving as the main entry points. Each section (about, blog, projects, contact) is linked through a consistent navigation bar.

## Developer Workflows
- **Building**: The site can be deployed directly to GitHub Pages without any build step. Simply push changes to the repository.
- **Adding Blog Posts**: To add a new blog post, copy an existing folder under `blog/`, rename it, and update the `index.html` file within that folder.
- **Updating Content**: Modify the `README.md` and `index.md` files for site-wide information and personal details.

## Project-Specific Conventions
- **File Naming**: Use lowercase and hyphens for file names to maintain consistency and avoid issues with case sensitivity on different platforms.
- **Styling**: All styles are managed through a single CSS file located in `assets/css/styles.css`. Ensure any new styles are added here.

## Integration Points
- **External Dependencies**: The site uses a simple CSS framework for styling. Ensure that any external libraries are linked correctly in the HTML files.
- **JavaScript**: Any interactive features should be added to `assets/js/main.js`. This file is included in all pages.

## Examples
- **Blog Post Structure**: Each blog post should follow the structure found in `blog/experiment-notes/`.
- **Project Entry**: Projects should be documented in `projects/index.html`, following the format of existing entries.

## Conclusion
This guide should help AI agents understand the structure and workflows of this codebase, enabling them to assist effectively in maintaining and updating the site.