export const eventStatus = {
    programmed: '🟩 À venir',
    cancelled: '🟥 Annulé',
    rescheduled: '🟧 Reporté',
    full: '🟨 Complet',
    movedOnline: '🟦 Déplacé en ligne'
};

export function getEventStatus(event) {
    if (new Date(event.date + 'Z') < new Date())
        return '⬛ Terminé';
    if (eventStatus[event.status])
        return eventStatus[event.status];
}