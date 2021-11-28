import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class StreamingAnalyzer:
    def __init__(self, base_url : str = None):
        self.base_url = 'https://data-api-zeta.vercel.app'
        if base_url:
            self.base_url = base_url

    def get_streaming_data_by_genre(self, streaming: str, genre: str):
        return self._get_streaming_data_by_filter(streaming, 'genre', genre)

    def get_streaming_data_by_year(self, streaming: str, year: str):
        return self._get_streaming_data_by_filter(streaming, 'year', year)
    
    def get_streaming_data_by_actor(self, streaming: str, actor: str):
        return self._get_streaming_data_by_filter(streaming, 'actor', actor)

    def get_streaming_data_by_director(self, streaming: str, director: str):
        return self._get_streaming_data_by_filter(streaming, 'director', director)

    def get_streaming_data_by_country(self, streaming: str, country: str):
        return self._get_streaming_data_by_filter(streaming, 'country', country)

    def get_streaming_data_by_duration(self, streaming: str, duration: str):
        return self._get_streaming_data_by_filter(streaming, 'duration', duration)

    def _get_streaming_data_by_filter(self, streaming: str, filter: str, value: str):
        return pd.read_json(requests.get(f'{self.base_url}/{streaming}/{filter}/{value}').json())

    def get_streaming_data_filtered(self, streaming: str, filter: str):
        return pd.read_json(requests.get(f'{self.base_url}/{streaming}/filter/{filter}').json())

    def get_all_streaming_data(self, streaming: str):
        return pd.read_json(requests.get(f'{self.base_url}/{streaming}').json())

    

    def count_streaming_by_director(self, director: str):
        return self._count_by('director', director)

    def count_streaming_by_year(self, year: str):
        return self._count_by('year', year)

    def count_streaming_by_genre(self, genre: str):
        return self._count_by('genre', genre)

    def count_streaming_by_actor(self, actor: str):
        return self._count_by('actor', actor)
    
    def count_streaming_by_duration(self, duration: str):
        return self._count_by('duration', duration)
    
    def count_streaming_by_country(self, country: str):
        return self._count_by('country', country)

    def _count_by(self, filter: str, value: str):
        return requests.get(f'{self.base_url}/streaming/{filter}/count/{value}').json()



    def persist_data_json(self, data: pd.DataFrame, filename: str):
        data.to_json(f'{filename}.json')
    
    def persist_data_csv(self, data: pd.DataFrame, filename: str):
        data.to_csv(f'{filename}.csv')


    def create_histogram_release_year(self, raw_data, title, streaming):
        plt.clf()
        hist = sns.histplot(data=raw_data, x='release_year', hue='type').set_title(title)
        fig = hist.get_figure()
        fig.savefig(f'image/hist_number_titles_release_year_in_{streaming}.png')

    def create_boxplot_release_year(self, raw_data, title, streaming):
        plt.clf()
        box = sns.boxplot(data=raw_data, x='release_year', y='type').set_title(title)
        fig = box.get_figure()
        fig.savefig(f'image/boxplot_number_titles_release_year_in_{streaming}.png')

    def prepare_data_for_duration_movie(self, raw_data: pd.DataFrame):
        answer = raw_data[raw_data['type'] == 'Movie']
        answer['duration'] = answer['duration'].dropna().str.replace(' min', '').astype(int)

        return answer.groupby('duration').count()

    def show_grouped_graph(self, data, x_label, y_label):
        plt.figure(figsize=(10,5))
        plt.plot(data.index, data.title)
        plt.xlabel(f'{x_label}')
        plt.ylabel('number of movies')
        plt.title(f'Number of {y_label} per {x_label}')
    
        plt.show()

    