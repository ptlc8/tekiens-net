from flask import Blueprint

from .. import api


socials = {
    'web': {
        'name': 'Site web',
        'display': 'Site web',
        'link': 'https://{0}',
        'placeholder': 'tekiens.net'
    },
    'telegram': {
        'name': 'Telegram',
        'display': 'Telegram',
        'link': 'https://t.me/{0}',
        'placeholder': '+wtd86pl51'
    },
    'twitter': {
        'name': 'Twitter',
        'display': 'Twitter @{0}',
        'link': 'https://twitter.com/{0}',
        'placeholder': 'Tekiens'
    },
    'discord': {
        'name': 'Discord',
        'display': 'Discord',
        'link': 'https://discord.gg/{0}',
        'placeholder': 'ml51rbn113'
    },
    'instagram': {
        'name': 'Instagram',
        'display': 'Instagram @{0}',
        'link': 'https://instagram.com/{0}',
        'placeholder': 'super_asso'
    },
    'email': {
        'name': 'Email',
        'display': '{0}',
        'link': 'mailto:{0}',
        'placeholder': 'contact@tekiens.net'
    },
    'links': {
        'name': 'Liens',
        'display': 'Liens',
        'link': 'https://{0}',
        'placeholder': 'tekiens.net/links'
    },
    'facebook': {
        'name': 'Facebook',
        'display': 'Facebook',
        'link': 'https://facebook.com/{0}',
        'placeholder': 'profile.php?id=518651113'
    },
    'linkedin': {
        'name': 'LinkedIn',
        'display': 'LinkedIn',
        'link': 'https://linkedin.com/{0}',
        'placeholder': 'company/tekiens'
    },
    'youtube': {
        'name': 'YouTube',
        'display': 'YouTube',
        'link': 'https://youtube.com/{0}',
        'placeholder': '@tekiens-net'
    },
    'tiktok': {
        'name': 'TikTok',
        'display': 'TikTok',
        'link': 'https://tiktok.com/{0}',
        'placeholder': '@tekiens'
    },
}


def parse_social(social):
    id = social.split(':')[0]
    id = id if id in socials else 'web'
    value = social.split(':', 1)[-1]
    return {
        'id': id,
        'display': socials[id]['display'].format(value),
        'link': socials[id]['link'].format(value),
        'value': value
    }


blueprint = Blueprint('socials', __name__)

@blueprint.route('', methods=['GET'])
def get_socials():
    return api.success(socials)