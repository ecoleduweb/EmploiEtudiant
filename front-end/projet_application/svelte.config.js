import adapter from "@sveltejs/adapter-node"
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte"

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://kit.svelte.dev/docs/integrations#preprocessors
    // for more information about preprocessors
    preprocess: vitePreprocess(),
    //C'est l'option qui active les runes de Svelte 5 dans votre projet.
    /*Les runes sont la nouvelle syntaxe de réactivité de Svelte 5. Ce sont des mots-clés spéciaux qui commencent par $ :
        compilerOptions: {
        runes: true
    },
   */

    kit: {
        // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
        // If your environment is not supported or you settled on a specific environment, switch out the adapter.
        // See https://kit.svelte.dev/docs/adapters for more information about adapters.
        adapter: adapter(),
    },
}

export default config
