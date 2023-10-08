# Spotibox

<img src="static/images/logo.png" align="right">

A collaborative, online jukebox based on [Spotify](https://open.spotify.com).

[Website](https://spotibox.epoc.fr/)

## Prerequisites

  - Python >= 3.8
  - A modern web browser
  - An SQLAlchemy-supported DBMS
  - (Optional, but recommended) A WSGI-capable web server

## Installation

  1. Clone this repo somewhere
  2. Copy `.env.local` to `.env`, then fill in the required/desired variables
  3. `pip install -r requirements-dev.txt`
  4. `flask db upgrade`
