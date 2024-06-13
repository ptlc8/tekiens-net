<script>
import { RouterLink } from 'vue-router';
</script>

<template>
    <section class="with-nav">
        <nav>
            <a href="#general">Informations générales</a>
            <a href="#use">Utilisation de la plateforme</a>
            <a href="#contribute">Contribution et support</a>
        </nav>
        <article>
            <article id="general">
                <h2>Informations générales</h2>
                <h3>Qu'est-ce que tekiens.net et quel est son objectif ?</h3>
                Tekiens.net est le site de la vie étudiante de CY Tech. (anciennement eistiens.net)
                <br />
                Le but de ce site est de centraliser les informations concernant les associations et les événements de l'école.
                <h3>C'est quoi Archives ?</h3>
                <a target="_blank" href="https://archive.tekiens.net">archives.tekiens.net</a> est une section de la plateforme qui conserve des informations historiques sur les associations, les cours, les photos, etc.
                Cela permet de suivre l'évolution de la vie étudiante et de donner aux élèves l'accès aux anciens documents.
            </article>
            <article id="use">
                <h2>Utilisation de la plateforme</h2>
                <h3>Comment puis-je ajouter mon association sur tekiens.net ?</h3>
                Pour ajouter votre association sur tekiens.net, vous devez contacter le bureau de l'association <RouterLink to="/assos/atilla">Atilla</RouterLink>.
                La plateforme n'est actuellement dédiée qu'aux associations de CY Tech.
                <h3>Puis-je utiliser l'API tekiens.net pour mes projets ?</h3>
                Oui, l'API est publique et vous pouvez l'utiliser pour vos projets.
                Consultez la <a target="_blank" href="https://gitlab.com/ptlc8/tekiens-net/-/blob/new/api.md">documentation de l'API</a> pour obtenir les détails techniques.
            </article>
            <article id="contribute">
                <h2>Contribution et support</h2>
                <h3>Comment puis-je contribuer au projet ?</h3>
                Nous accueillons volontiers les contributions !
                Consultez notre page GitLab pour trouver des opportunités d'aide.
                Vous pouvez soumettre des suggestions, des rapports de bugs ou même proposer des améliorations.
                <br />
                Vous êtes intéressés pour découvrir le code, ou vous voulez simplement participer à l'amélioration de la plateforme ?
                Rejoignez nous en CY307 ou sur les internets !
                <h3 id="repo">Comment puis-je trouver le code source de tekiens.net ?</h3>
                Le code source est disponible sur <a href="https://gitlab.com/ptlc8/tekiens-net" target="_blank">le dépôt public GitLab</a>.
                Vous pouvez le cloner, le fork, et contribuer sur la page du projet.
                <h3>Comment puis-je signaler un problème ou un bug ?</h3>
                Si vous rencontrez un problème ou un bug, veuillez créer un rapport sur notre page GitLab dans la section des problèmes ou sur le serveur Discord d'Atilla.
                Décrivez le problème de manière détaillée, en incluant si possible les étapes pour le reproduire.
                Notre équipe examinera rapidement votre rapport.
            </article>
        </article>
    </section>
</template>

<style lang="scss" scoped>
section.with-nav {
    display: flex;
    flex-direction: row;

    nav {
        display: flex;
        flex-direction: column;
        border-left: 1px solid #555;
        margin: 1em;
        height: fit-content;
        position: sticky;
        top: 1em;
    
        a {
            padding: 1em
        }
        
        @media (max-width: 600px) {
            display: none;
        }
    }
}

h3 {
    color: #555;
}
</style>