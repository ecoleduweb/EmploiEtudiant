# Web application

## Environnement

Before starting the app, create a .env file and add the required fields. Alternativately, the file can be found on Discord, in #front-end.

## Developing

Once you've created a project and installed dependencies with `npm install` (make sure you're in the /projet_application directory), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
