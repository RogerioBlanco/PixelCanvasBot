#!/usr/bin/env python

import locale
import time


class I18n(object):

    @staticmethod
    def get(key, inline='false'):
        if (inline == 'true'):
            return I18n._all[I18n._locale][key]
        else:
            return '[' + time.strftime("%H:%M:%S") + '] ' + I18n._all[I18n._locale][key]

    _all = {
        'en_GB': {
            'exit': 'Bye!',
            'colors.round': '{rgba} colors rounded by {diff_min} ({name}).',
            'chunk.blind.east': 'This bot may be blind for all pixels east of {x}.',
            'chunk.blind.south': 'This bot may be blind for all pixels south of {y}.',
            'chunk.load': 'Loading chunk ({x}, {y})...',

            'error.try_again': 'Oh no, an error occurred. Trying again.',
            'error.proxy': 'Oh no, you are using a proxy.',
            'error.token': 'Oh no, a new token is required. Please open pixelcanvas.io and paint a pixel.',
            'error.rate_limit': 'Oh no, you tried too hard! Rate limit exceeded.',
            'error.connection': 'Connection broke :(',

            'paint.has_painted': 'Have you painted a pixel in pixelcanvas.io? y/n:',
            'paint.user': 'You painted {color} at {x},{y}.',
            'paint.ally': 'Somebody updated {x},{y} with {color} [ALLY].',
            'paint.outside': 'Somebody updated {x},{y} with {color} [OUTSIDE TEMPLATE].',
            'paint.enemy': 'Somebody updated {x},{y} with {color} [ENEMY].',
            'paint.wait': 'Waiting {seconds} seconds.',
            'progress': 'Total active pixel count: {total}. Correct pixels: {correct}. Incorrect pixels: {incorrect}. Progress: {progress}%.',


            'websocket.closed': 'Websocket closed.',
            'websocket.opened': 'Websocket opened.',

            'strategy.left_right_top_bottom': 'Drawing from left to right, from top to bottom.',
            'strategy.right_left_top_bottom': 'Drawing from right to left, from top to bottom.',
            'strategy.top_bottom_left_right': 'Drawing from top to bottom, from left to right.',
            'strategy.bottom_top_left_right': 'Drawing from bottom to top, from left to right.',
            'strategy.auto_select': 'Invalid strategy "{strategy}". Defaulting to strategy "spiral".',

            'external.load_cache': 'Loading cached image.',
            'external.generating': 'Generating converted image here: {path}.',
            'external.saved_cache': 'Saved image cache file, loading now...',
            'qr_created': 'QR Code successfully saved here: {path}.',

            # Arguments
            '--image': 'The image to draw. Quantizes colors to the palette as defined in colors.py so the bot can draw correctly.',
            '--fingerprint': 'Your fingerprint. See README.md for instructions on how to retrieve it.',
            '--start_x': 'The x coordinate at which to start drawing.',
            '--start_y': 'The y coordinate at which to start drawing.',
            '--colors_ignored': 'Any colors listed here, if contained within the quantized image, will be treated as transparent for the purposes of drawing.',
            '--colors_not_overwrite': 'The colors listed here will not be overwritten if they appear on the canvas where the image is being drawn.',
            '--draw_strategy': 'Optional draw strategy. Choose from the strategy list [linear, p_linear, qf, randomize, status, sketch, radiate, spiral] default: randomize.',
            '--mode_defensive': 'Put the bot in daemon mode (run in background). This will run forever.',
            '--proxy_url': 'Proxy url with port. ex: url:port . DEPRECATED',
            '--proxy_auth': 'Proxy authentication. ex: user:pass . DEPRECATED',
            '--round_sensitive': 'Color rounding sensitivity. This number must be > 0. ex: 3.',
            '--image_brightness': 'Change image brightness. Supports negative values. ex: 15 or -15.',
            '--detect_area_min_range': 'Supports negative values ex: 3000 or -3000.',
            '--detect_area_max_range': 'Supports negative values ex: 3000 or -3000.',
            '--QR_text': 'url or some text.',
            '--QR_scale': 'QR code pixel width.',
            '--xreversed': 'Draw from right to left. Set to True or False (default False).',
            '--yreversed': 'Draw from bottom to top. Set to True or False (default False).',
            '--point_x': 'Target x coordinate for strategies that radiate from a single point, such as radiate and spiral; defaults to center.',
            '--point_y': 'Target y coordinate for strategies that radiate from a single point, such as radiate and spiral; defaults to center.',
            '--prioritized': 'Sorts the order in which pixels are placed so that pixels that are more opaque in the source image are given priority over the more transparent pixels; allows for establishing strategic hotspots in a template.',
            '--notify': 'Send a system notification if a captcha is encountered by the bot. Notification remains for 30 seconds or until dismissed.',
            '--output_file': 'Output the logs to this file. (default: logfile.log).',
            '--locale': 'The language to use. Choose from [en_GB, fr_FR].',

            # Colors
            'white': 'white',
            'gainsboro': 'bright grey',
            'grey': 'grey',
            'nero': 'black',
            'carnation pink': 'pink',
            'red': 'red',
            'orange': 'orange',
            'brown': 'brown',
            'yellow': 'yellow',
            'conifer': 'conifer',
            'green': 'green',
            'dark turquoise': 'turquoise',
            'pacific blue': 'navy blue',
            'blue': 'blue',
            'violet': 'violet',
            'purple': 'purple',
        },

        'fr_FR': {
            'exit': 'Au revoir!',
            'colors.round': '{rgba} colors rounded by {diff_min} ({name}).',
            'chunk.blind.east': 'Il se pourrait que ce bot ne puisse pas voir à l\'est de {x}.',
            'chunk.blind.south': 'Il se pourrait que ce bot ne puisse pas voir au sud de {y}.',
            'chunk.load': 'Je charge chunk ({x}, {y})...',

            'error.try_again': 'Oh la! Une erreur est survenue. J\'essaie encore de le faire.',
            'error.proxy': 'Oh la! Tu utilises un proxy.',
            'error.token': 'J\'ai besoin d\'une nouvelle zone de texte. Merci d\'ouvrir pixelcanvas.io et poser un pixel.',
            'error.rate_limit': 'J\'ai envoyé trop de requêtes.',
            'error.connection': 'La connexion s\'est brisé prématurément.',

            'paint.has_painted': 'Est-ce que tu as posé un pixel sur pixelcanvas.io? y/n:',
            'paint.user': 'Tu as peint le pixel {x},{y} en {color}.',
            'paint.ally': 'Un(e) ami(e) a peint le pixel {x},{y} en {color}.',
            'paint.outside': 'Quelqu\'un a peint le pixel {x},{y} en {color} (en dehors de la modèle).',
            'paint.enemy': 'Un(e) ennemi(e) a peint le pixel {x},{y} en {color}.',
            'paint.wait': 'J\'attends {seconds} secondes.',
            'progress': 'Tous pixels: {total}. Pixels corrects: {correct}. Pixels incorrects: {incorrect}. Avancement: {progress}%.',

            'websocket.closed': 'Websocket s\'est fermé.',
            'websocket.opened': 'Websocket s\'est ouvert.',

            'strategy.left_right_top_bottom': 'Je dessine de gauche à droite, de haut en bas.',
            'strategy.right_left_top_bottom': 'Je dessine de droite à gauche, de haut en bas.',
            'strategy.top_bottom_left_right': 'Je dessine de haut en bas, de gauche à droite.',
            'strategy.bottom_top_left_right': 'Je dessine de bas en haut, de gauche à droite.',
            'strategy.auto_select': 'Stratégie erronée "{strategy}". J\'utilise la stratégie "spiral".',

            'external.load_cache': 'Je charge l\'image de la mémoire-cache.',
            'external.generating': 'Je crée l\'image transformée ici : {path}.',
            'external.saved_cache': 'J\'ai mis l\'image en mémoire-cache, je le charge...',
            'qr_created': 'Le code QR est sauvegardé ici : {path}.',

            # Arguments
            '--image': 'L\'image à peindre. Corriger les couleurs de l\'image (comme défini en colors.py) pour que le bot puisse peindre.',
            '--fingerprint': 'Ton empreinte digitale. Voir README.md pour des instructions sur la façon de l\'obtenir.',
            '--start_x': 'La coordonnée X à laquelle commencer à peindre.',
            '--start_y': 'La coordonnée Y à laquelle commencer à peindre',
            '--colors_ignored': 'Ces couleurs seront ignorées.',
            '--colors_not_overwrite': 'Ces couleurs ne seront pas écrasés.',
            '--draw_strategy': 'Stratégie optionnelle. Choisir parmi [linear, p_linear, qf, randomize, status, sketch, radiate, spiral] la stratégie par défaut: randomize.',
            '--mode_defensive': 'La façon défensive.',
            '--proxy_url': 'L\'URL de proxy avec le port. ex: url:port . DEPRECATED',
            '--proxy_auth': 'L\'authentification de proxy. ex: user:pass . DEPRECATED',
            '--round_sensitive': 'La sensibilité à l\'arrondi des couleurs. Ce nombre doit être > 0. ex: 3.',
            '--image_brightness': 'Changer la luminosité de l\'image. ex: 15 or -15.',
            '--detect_area_min_range': 'Supporter les nombres négatifs. ex: 3000 or -3000.',
            '--detect_area_max_range': 'Supporter les nombres négatifs. ex: 3000 or -3000.',
            '--QR_text': 'URL ou texte.',
            '--QR_scale': 'La largeur de pixels du code QR.',
            '--xreversed': 'Dessiner de droite à gauche. Mettre True (Vrai) or False (Faux) (le valeur par défaut: False (Faux)).',
            '--yreversed': 'Dessiner de bas en haut. Mettre True (Vrai) or False (Faux) (le valeur par défaut: False (Faux)).',
            '--point_x': 'La coordonnée X pour des stratégies qui rayonne autor d\'un endroit, comme "radiate" et "spiral"; (le valeur par défaut: le centre de la modèle).',
            '--point_y': 'La coordonnée Y pour des stratégies qui rayonne autor d\'un endroit, comme "radiate" et "spiral"; (le valeur par défaut: le centre de la modèle).',
            '--prioritized': 'Peindre des pixels plus paques le premier.',
            '--notify': 'Envoyer-toi un notification quand le bot a besoin d\'une nouvelle zone de texte.',
            '--output_file': 'Écrire le journal d\'événements dans ce fichier.',
            '--locale': 'La langue à utiliser. Choisir parmi [en_GB, fr_FR].',

            # Colors
            'white': 'blanc',
            'gainsboro': 'gris clair',
            'grey': 'gris',
            'nero': 'noir',
            'carnation pink': 'rose',
            'red': 'rouge',
            'orange': 'orange',
            'brown': 'marron',
            'yellow': 'jaune',
            'conifer': 'vert clair',
            'green': 'vert',
            'dark turquoise': 'turquoise',
            'pacific blue': 'bleu marine',
            'blue': 'bleu',
            'violet': 'violet',
            'purple': 'violet foncé',
        },

        'pt_BR': {
            'exit': 'Ate Logo!',
            'colors.round': '{rgba} colors rounded by {diff_min} ({name})',
            'chunk.blind.east': 'Esse bot pode não ler pixels ao leste de {x}',
            'chunk.blind.south': 'Esse bot pode não ler pixels ao sul de {y}',
            'chunk.load': 'Carregando chunk ({x}, {y})...',

            'error.try_again': 'Ocorreu um erro. Tentando novamente.',
            'error.proxy': 'Ops! Parece que voce esta usando um Proxy',
            'error.token': 'Um token é necessario. Abra pixelcanvas.io e pinte um pixel',
            'error.rate_limit': 'Oh nao! Limite de tentativas excedido',
            'error.connection': 'Erro de conexao :(',

            'paint.has_painted': 'Voce pintou um pixel no pixelcanvas.io? y(sim)/n(nao):',
            'paint.user': 'Voce pintou {x},{y} com {color}',
            'paint.ally': 'Alguem pintou {x},{y} com {color} [ALIADO]',
            'paint.outside': 'Alguem pintou {x},{y} com {color} [FORA DO TEMPLATE]',
            'paint.enemy': 'Alguem pintou {x},{y} com {color} [INIMIGO]',
            'paint.wait': 'Esperando {seconds} segundos',
            'progress': 'Total de pixels: {total}. Pixels corretos: {correct}. Pixels incorretos: {incorrect}. Progresso: {progress}%.',


            'websocket.closed': 'Websocket fechado',
            'websocket.opened': 'Websocket aberto',

            'strategy.left_right_top_bottom': 'Desenha da esquerda para a direita, de cima para baixo',
            'strategy.right_left_top_bottom': 'Desenha da direita para a esquerda, de cima para baixo',
            'strategy.top_bottom_left_right': 'Desenha de cima para baixo, da esquerda para a direita',
            'strategy.bottom_top_left_right': 'Desenha de baixo para cima, da esquerda para a direita',
            'strategy.auto_select': 'Estrategia invalida "{strategy}". Automaticamente selecionando "spiral"',

            'external.load_cache': 'Carregndo imagem em cache',
            'external.generating': 'Gerando imagem convertida em: {path}',
            'external.saved_cache': 'Imagem salva no cache, carregando...',
            'qr_created': 'QR code salvo em: {path}',

            # Argumentos
            '--image': 'Imagem a ser desenhada.Converte automaticamente para as cores do Canvas.',
            '--fingerprint': 'Sua fingerprint. Veja README.md (em ingles)para instrucoes de como configurar.',
            '--start_x': 'Coordenada X do topo esquerdo do desenho',
            '--start_y': 'Coordenada Y do topo esquerdo do desenho',
            '--colors_ignored': 'Cores escolhidas serão tratadas como transparentes pelo bot.',
            '--colors_not_overwrite': 'As cores escolhidas não serão sobrepostas no Canvas.',
            '--draw_strategy': 'Estrategia de desenho. Escolha da lista de estrategias [linear, p_linear, qf, randomize, status, sketch, radiate, spiral] default: randomize',
            '--mode_defensive': 'Ativa o modo demoniaco (roda em segundo plano). Isso irá durar para sempre.',
            '--proxy_url': 'url do Proxy e porta. Ex: url:porta . DEPRECATED',
            '--proxy_auth': 'Autenticacao do Proxy. Ex: usuario:senha . DEPRECATED',
            '--round_sensitive': 'Sensibilidade da cor. O valor deve ser > 0. Ex: 3',
            '--image_brightness': 'Altera o brilho da imagem. Suporta valores negativos. Ex: 15 ou -15',
            '--detect_area_min_range': 'Suporta valores negativos. Ex: 3000 ou -3000',
            '--detect_area_max_range': 'Suporta valores negativos. Ex: 3000 ou -3000',
            '--QR_text': 'link ou texto para gerar o QR code',
            '--QR_scale': 'Proporcao do QR code',
            '--xreversed': 'Desenha da direita para a esquerda. Definir com \'True\'(verdadeiro) ou \'False\'(falso) (Por padrão: falso)',
            '--yreversed': 'Desenha de baixo para cima. Definir com \'True\'(verdadeiro) ou \'False\'(falso) (Por padrão: falso)',
            '--point_x': 'Ponto de partida para coordenadas X em estrategias que partem de um unico ponto, como radial e spiral. (Por padrão: do centro)',
            '--point_y': 'Ponto de partida para coordenadas Y em estrategias que partem de um unico ponto, como radial e spiral. (Por padrão: do centro)',
            '--prioritized': 'Prioriza pixels baseado no nível de transparencia do template, pixels com maior transpareencia são pintados primeiro pelo bot; permite definir pontos estrategicos no template',
            '--notify': 'Enviar uma notificação de sistema quando o bot detecta um Captcha. A notificação dura 30 segundos, ou até ser removida.',
            '--output_file': 'Arquivo de logs. (Por padrão: logfile.log)',
            '--locale': 'Língua a usar. Escolha entre [en_GB, fr_FR, pt_BR].',

            # Colors
            'white': 'branco',
            'gainsboro': 'cinza claro',
            'grey': 'cinza escuro',
            'nero': 'preto',
            'carnation pink': 'rosa',
            'red': 'vermelho',
            'orange': 'laranja',
            'brown': 'marrom',
            'yellow': 'amarelo',
            'conifer': 'verde claro',
            'green': 'verde escuro',
            'dark turquoise': 'turquesa',
            'pacific blue': 'azul marinho',
            'blue': 'azul',
            'violet': 'violeta',
            'purple': 'roxo',
        },
    }

    _locale = locale.getdefaultlocale()[0]
    try:
        _all[_locale]
    except KeyError:
        _locale = 'en_GB'
