<script lang="ts">
  import { page } from '$app/stores'
  import { env } from "$env/dynamic/public"
  

  const measurementId: string | undefined = env.PUBLIC_PUBLIC_MEASUREMENT_ID;

  console.log("Measurement ID:", measurementId); 

  $: {
    if (typeof gtag !== 'undefined') {
      if (measurementId) {
      gtag('config', measurementId, {
        page_title: document.title,
        page_path: $page.url.pathname,
      })
        } else {
          console.warn('measurementId is not defined')
        }
    } else {
      console.warn('gtag is not defined')
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