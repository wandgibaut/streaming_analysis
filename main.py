from streamings import StreamingAnalyzer


if __name__ == '__main__':
    analyzer = StreamingAnalyzer(base_url=None)

    all_streamings = ['netflix', 'amazon', 'hulu', 'disney_plus']

    for streaming in all_streamings:
        raw_data = analyzer.get_streaming_data_filtered(streaming, f'title,country,date_added,release_year,duration,listed_in,type')

        # persiste os dados vindos da api
        analyzer.persist_data_json(raw_data, f'data/filtered_in_{streaming}')
        analyzer.persist_data_csv(raw_data, f'data/filtered_in_{streaming}')

        # persiste os dados agrupados 
        analyzer.persist_data_json(raw_data.groupby('release_year').count(), f'data/counted_filtered_in_{streaming}')
        analyzer.persist_data_csv(raw_data.groupby('release_year').count(), f'data/counted_filtered_in_{streaming}')

        # persiste as imagens
        analyzer.create_histogram_release_year(raw_data, f'number of movies and series per release year in {streaming}', streaming)
        analyzer.create_boxplot_release_year(raw_data, f'number of movies and series per release year in {streaming}', streaming)
        