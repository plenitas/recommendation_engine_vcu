# Recommendation Engine

This repository contains a very small demo website that shows how a simple
video recommendation system can work completely in the browser.  Users can be
selected from the landing page, then a video can be chosen.  Ten seconds into
playback the page will suggest another video based on the selected user's
preferences and prior watch history (stored in the browser's `localStorage`).

## Running locally

Open `site/index.html` in a web browser.  Because everything is client-side no
server is required.  The provided sample videos are pulled from
`sample-videos.com`, so an internet connection is needed for playback.

You can replace the entries in `site/js/app.js` with your own video URLs and
tags.  When new videos are added simply update the `videos` array.

## Updating your Codespace

If you wish to modify this project in a Codespace, clone the repository and
apply your changes.  Commit them with `git commit` and then push with
`git push`.
