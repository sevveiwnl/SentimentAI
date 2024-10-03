from flask import Blueprint, render_template, request, jsonify, current_app
from app.genius_api import search_song, get_lyrics
from app.sentiment_analysis import analyze_sentiment

main = Blueprint('main', __name__)

#render homepage 
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        song_title = data.get('song_title')
        artist_name = data.get('artist_name')

        # Search for the song
        song = search_song(song_title, artist_name)
        if not song:
            return jsonify({'error': 'Song not found'}), 404

        # Get lyrics
        lyrics = get_lyrics(song['url'])
        if not lyrics:
            return jsonify({'error': 'Lyrics not found'}), 404

        # Analyze sentiment
        analysis_result = analyze_sentiment(lyrics)

        return jsonify({
            'song_title': song.get('title', 'Unknown Title'),
            'artist_name': song.get('artist', {}).get('name', 'Unknown Artist'),
            'lyrics': lyrics,
            'sentiments': analysis_result['sentiments'],
            'scores': analysis_result['scores'],
            'overall_sentiment': analysis_result['overall_sentiment'],
            'sentiment_distribution': analysis_result['sentiment_distribution']
        })

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
