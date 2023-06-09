# chatgpt-clone-vue
Build ChatGPT in Vue
This repository contain chatgpt-clone-vue and flask-api

## Requirements

To run this application on your workstation, you must install :

-   node.js version 16.xx.xx
-   npm 8.xx.x
-   Vue Cli 5.x.xx
-   Vue 3

### Vue CLI

Run `npm install -g @vue/cli` or `yarn global add @vue/cli`

### Clone this repository

git clone https://github.com/Abdietou/chatgpt-clone.git

### Install dependencies

Run `npm install` to generate node_modules folder who contains dependencies.

## Developement server

Run `npm run serve` for a development server.

Navigate to `http://localhost:8080/`. The application will automatically reload if you change any of the source files.

## Running eslint [eslint](https://eslint.org/)

Run `npm run lint` for check js rules.

## Running prettier [prettier](https://prettier.io/)

Run `npm run prettier:check` for check your format code.

Run ` npm run prettier` for format the code.

## Build

Run `npm run build` for build this project, build files will be at the root of the project in the dist directory.


# flask-api

## Requirements

To run this application on your workstation, you must install :

-  Python 3.10.xx

## Create the virtual environment
```bash
$ python -m venv venv
```

## Activate the virtual environment
### Windows
```bash
$ venv\Scripts\activate
```

Or run this command for cmd.exe
```bash
$ venv\Scripts\activate.bat
```

### Linux or macOS
```bash
$ source venv/bin/activate
```

## Install dependencies
```bash
$ pip install -r requirements.txt
```

## Start Server
```bash
$ flask run
```

Or run this command 
```bash
$ python -m flask run
```