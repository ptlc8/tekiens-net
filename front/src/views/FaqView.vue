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
                Le but de ce site est de centraliser les informations concernant les associations et les événements de
                l'école.
                <h3>C'est quoi Archives ?</h3>
                <a target="_blank" href="https://archive.tekiens.net">archives.tekiens.net</a> est une section de la
                plateforme qui conserve des informations historiques sur les associations, les cours, les photos, etc.
                Cela permet de suivre l'évolution de la vie étudiante et de donner aux élèves l'accès aux anciens
                documents.
            </article>
            <article id="use">
                <h2>Utilisation de la plateforme</h2>
                <h3>Comment ajouter une association à mon calendrier ?</h3>
                Tekiens.net propose un flux calendrier(iCal) et RSS pour les évènements, que ce soit pour une ou toutes
                les associations.
                Pour que les évènements apparaissent automatiquement dans votre calendrier, vous devez ajouter le lien
                trouvable sur la page d'une association ou "Événements" (exemple pour ATILLA:
                tekiens.net/assos/atilla/events.ics) dans votre application de calendrier.
                <br />Voici quelques liens utiles pour savoir comment ajouter un calendrier iCal dans différents
                logiciels/outils :
                <ul>
                    <li>
                        Calendrier <a href="mail.etu.cyu.fr">mail.etu.cyu.fr</a> : En allant dans "Calendrier"-> l'icone
                        paramètre à côté de <b>"Calendriers"</b> -> <b>"Ajouter Calendrier Externe"</b> -> <b>"Ajouter
                            un calendrier externe (autre)"</b> -> <b>"Abonnement iCAL"</b> -> Mettez le lien ics
                        (exemple: https://tekiens.net/events.ics)
                    </li>
                    <li><a href="https://support.google.com/calendar/answer/37100?hl=fr">Google Calendar</a></li>
                    <li>
                        <a href="https://support.microsoft.com/fr-fr/office/importer-des-calendriers-dans-outlook-8e8364e1-400e-4c0f-a573-fe76b5a2d379">Outlook</a>
                    </li>
                    <li><a href="https://support.mozilla.org/en-US/kb/creating-new-calendars">Thunderbird</a></li>
                    <li><a href="https://support.apple.com/fr-fr/guide/calendar/icl1022/mac">Calendar</a> (Mac OS) </li>
                    <li>
                        Moodle/<a href="cours.cyu.fr">cours.cyu.fr</a> : Aller dans votre calendrier et tout en bas de
                        la page cliquer sur <b>"Importer ou exporter des calendriers"</b> -> <b>"Importer un
                            calendrier"</b> puis remplir les champs, bien sélectionner <b>"URL d'un calendrier"</b> et
                        mettre la mise à jour sur <b>"Chaque heure"</b>
                    </li>
                    <li><a href="https://support.apple.com/fr-fr/guide/iphone/iph3d1110d4/ios">Iphone</a></li>
                    <li>
                        <u>Android</u> : le plus simple est d'ajouter le calendrier à votre agenda Google, la
                        synchronisation se fera ensuite automatiquement.
                    </li>
                </ul>
                <h3>Comment puis-je ajouter mon association sur tekiens.net ?</h3>
                Pour ajouter votre association sur tekiens.net, vous devez contacter le bureau de l'association
                <RouterLink to="/assos/atilla">Atilla</RouterLink>.
                La plateforme n'est actuellement dédiée qu'aux associations de CY Tech.
                <h3>Puis-je utiliser l'API tekiens.net pour mes projets ?</h3>
                Oui, l'API est publique et vous pouvez l'utiliser pour vos projets.
                Consultez la <a target="_blank" href="https://gitlab.com/ptlc8/tekiens-net/-/blob/new/api.md">documentation de l'API</a> pour
                obtenir les détails techniques.
            </article>
            <article id="contribute">
                <h2>Contribution et support</h2>
                <h3>Comment puis-je contribuer au projet ?</h3>
                Nous accueillons volontiers les contributions !
                Consultez notre page GitLab pour trouver des opportunités d'aide.
                Vous pouvez soumettre des suggestions, des rapports de bugs ou même proposer des améliorations.
                <br />
                Vous êtes intéressés pour découvrir le code, ou vous voulez simplement participer à l'amélioration de la
                plateforme ?
                Rejoignez nous en CY307 ou sur les internets, ou encore sur le <a href="https://discord.gg/yx7ectUSUV" target="_blank">serveur Discord</a>!
                <h3 id="repo">Comment puis-je trouver le code source de tekiens.net ?</h3>
                Le code source est disponible sur <a href="https://gitlab.atilla.org/tekiens-net/tekiens-net" target="_blank">le dépôt public GitLab</a>.
                Vous pouvez le cloner, le fork, et contribuer sur la page du projet.
                <h3>Comment puis-je signaler un problème ou un bug ?</h3>
                Si vous rencontrez un problème ou un bug, veuillez créer un rapport sur notre page GitLab dans la
                section des problèmes ou sur le serveur Discord d'Atilla.
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
