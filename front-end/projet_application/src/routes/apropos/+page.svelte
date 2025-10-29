<script lang="ts">
    import APropos from "../../Components/Common/APropos.svelte"
</script>

<main>
    <section class="about-section">
        <div class="about-container">
            <h1 class="page-title">
                <span class="text-white">À PROPOS DU</span>
                <span class="text-green">PORTAIL</span>
            </h1>
            <span class="radiant"></span>
            
            <div class="about-content">
                <APropos />
            </div>
        </div> 
    </section>
</main>

<style scoped>
    main {
        min-height: 80vh;
        width: 100%;
    }

    .about-section {
        display: flex;
        justify-content: center;
        padding: 2rem;
    }

    .about-container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }

    .page-title {
        margin: 30px 0 20px 0;
        font-size: 2.5vw;
    }

    .text-white {
        color: white;
        margin-right: 0.5rem;
    }

    .text-green {
        color: #00ad9a;
    }

    .radiant {
        display: block;
        width: 100%;
        height: 16px;
        background: linear-gradient(270deg, #bb2534, #b2243d, #a72348, #a02250);
        margin-bottom: 30px;
    }

    .about-content {
        margin-top: 2rem;
        padding: 0 1rem;
    }

    @media (max-width: 768px) {
        .page-title {
            font-size: 7vw;
            margin-left: 1vw;
        }

        .about-section {
            padding: 1rem;
        }

        .radiant {
            width: 98vw;
            margin-left: -1rem;
        }
    }

    @media (min-width: 1024px) {
        .about-section {
            padding: 4rem 6rem;
        }
    }
</style>