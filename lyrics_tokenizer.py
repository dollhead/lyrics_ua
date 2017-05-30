import tokenize_uk
import os

lyrics_folder = 'lyrics'
tokens_folder = 'tokens'
stop_list = ['Приспів']
punctuation = ',.:!?–)(-..."'
numbers = '0123456789'


def is_valid_token(token):
    return token not in stop_list and token not in punctuation and token not in numbers


def write_tokens_to_file(artist_tokens):
    if not os.path.exists(tokens_folder):
        os.makedirs(tokens_folder)

    for artist, tokens in artist_tokens.items():
        token_file_path = os.path.join(tokens_folder, artist + '.tok')
        with open(token_file_path, 'w', encoding='utf8') as file:
            file.write('\n'.join(tokens))


def get_all_artists_tokens(writeToFiles=True):
    artist_tokens = {}
    for directory in os.listdir(lyrics_folder):
        artist_tokens[directory] = []
        relative_dir_path = os.path.join(lyrics_folder, directory)
        for song in os.listdir(relative_dir_path):
            lyrics_path = os.path.join(relative_dir_path, song)
            with open(lyrics_path, encoding='utf8') as file:
                text = file.read()
            song_tokens = tokenize_uk.tokenize_uk.tokenize_words(text)
            valid_tokens = [token for token in song_tokens if is_valid_token(token)]
            artist_tokens[directory].extend(valid_tokens)
    if writeToFiles:
        write_tokens_to_file(artist_tokens)
    return artist_tokens
