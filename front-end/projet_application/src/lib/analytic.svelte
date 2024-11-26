<script lang="ts">
  import { page } from '$app/stores'
  import { env } from "$env/dynamic/public"
  

  const measurementId = env.PUBLIC_PUBLIC_MEASUREMENT_ID

  console.log("Measurement ID:", measurementId); // Ajoutez cette ligne pour vérifier la valeur de measurementId

  $: {
    if (typeof gtag !== 'undefined') {
      console.log("gtag is defined"); // Vérifiez si gtag est défini
      gtag('config', measurementId, {
        page_title: document.title,
        page_path: $page.url.pathname,
      })
    } else {
      console.log("gtag is not defined"); // Vérifiez si gtag n'est pas défini
    }
  }
</script>

<svelte:head>
  <script
    async
    src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}>
  </script>
  <script>
    window.dataLayer = window.dataLayer || []

    function gtag() {
      dataLayer.push(arguments)
    }

    gtag('js', new Date())
    gtag('config', '${measurementId}')
  </script>
</svelte:head>