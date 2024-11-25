export const eventStatus = {
    programmed: '🟩 À venir',
    cancelled: '🟥 Annulé',
    rescheduled: '🟧 Reporté',
    full: '🟨 Complet',
    movedOnline: '🟦 Déplacé en ligne'
};

export function getEventStatus(event, real = false) {
    if (real || ['cancelled', 'rescheduled'].includes(event.status))
        return eventStatus[event.status];
    let date = Date.parse(event.date + 'Z');
    if (new Date(date + (event.duration ?? 0) * 60 * 1000) < new Date())
        return '⬛ Terminé';
    if (date < new Date())
        return '🟪 En cours';
    if (eventStatus[event.status])
        return eventStatus[event.status];
    return event.status;
}