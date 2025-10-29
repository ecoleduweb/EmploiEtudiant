<script>
    import Button from "../Inputs/Button.svelte"
    import LargeButton from "../Inputs/LargeButton.svelte"

</script>
<div class="about-text">
    <p class="text-welcome">Bienvenue sur le portail d'offres d'emploi du Cégep!
                    En collaboration avec des étudiants en Techniques de l'informatique et sous la responsabilité de l'enseignant Antoine Chagnon-Michaud,
                    le Cégep de Rivière-du-Loup a développé un nouveau Portail d'offres d'emploi. Celui-ci a pour objectif d'afficher 
                    les offres d'emploi destinées à nos élèves actuels ou qui ont obtenu leur diplôme récemment.
                    Veuillez noter que les entreprises sont responsables de la qualité du français dans leurs offres d'emploi respectives.</p>
    <LargeButton
        text="Consulter toutes les offres"
        onClick={() => window.location.href = "/"} />
</div>
<style>
      .text-welcome
    {
        color: white;
        font-size: 1.5rem;
        margin-top: 20px;
        text-align: justify;
    }
    .about-text {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;
    }
</style>