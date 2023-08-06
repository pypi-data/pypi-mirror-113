import pandas as pd

class HPrice:
    #inpot data for making an instance is a pandas dataframe with columns:date, open, high,low,clos,volume,
    # and n represents number of candles colliding to two price, one high and one low
    def __init__(self, data, n):
        self.data = data
        self.n = n

    def HPrice(self):
        """ what are we doing here?
        like cash data in other repository, we make neowave cashdata form OHLC data, but in cash data, frames are static and we forced to find
        a high and a low price in a frame(e.g. n=4 candles) but here we shift our data and make cashdata n time and after we finished
        (e.g. we make n=4 complete cash data) we compare all cash data 's and store those are stayed in all cash data 's
        after that we have to remove those points that are not extremom """

        date_list = []
        price_list = []
        volume_list = []
        for j in range(self.n):
            date = []
            price = []
            volume = []

            for i in range(self.data.shape[0] % self.n +j, self.data.shape[0], self.n):
                sub_df = self.data[i: i+self.n]
                max_index = sub_df['high'].idxmax()
                min_index = sub_df['low'].idxmin()
                if max_index < min_index:
                    date.append(sub_df['date'][max_index])
                    date.append(sub_df['date'][min_index])

                    price.append(sub_df['high'][max_index])
                    price.append(sub_df['low'][min_index])

                    volume.append(sub_df['volume'][max_index])
                    volume.append(sub_df['volume'][min_index])

                elif max_index > min_index:
                    date.append(sub_df['date'][min_index])
                    date.append(sub_df['date'][max_index])

                    price.append(sub_df['low'][min_index])
                    price.append(sub_df['high'][max_index])

                    volume.append(sub_df['volume'][min_index])
                    volume.append(sub_df['volume'][max_index])

                else:
                    if sub_df['close'][max_index] > sub_df['open'][max_index]:
                        date.append(sub_df['date'][min_index])
                        date.append(sub_df['date'][max_index])

                        price.append(sub_df['low'][min_index])
                        price.append(sub_df['high'][max_index])

                        volume.append(sub_df['volume'][min_index])
                        volume.append(sub_df['volume'][max_index])

                    else:
                        date.append(sub_df['date'][max_index])
                        date.append(sub_df['date'][min_index])

                        price.append(sub_df['high'][max_index])
                        price.append(sub_df['low'][min_index])

                        volume.append(sub_df['volume'][max_index])
                        volume.append(sub_df['volume'][min_index])

            date_list.append(date)
            price_list.append(price)
            volume_list.append(volume)
        H_date = []
        H_price = []
        H_volume = []
        for i in range(len(date_list[0])):
            is_there = True
            for j in date_list:
                if date_list[0][i] not in j:
                    is_there = False
            if is_there:
                H_date.append(date_list[0][i])
                H_price.append(price_list[0][i])
                H_volume.append(volume_list[0][i])

        result = pd.DataFrame(list(zip(H_date, H_price, H_volume)), columns=['date', 'price', 'volume'])
        return result

    #TODo find best way te clear dots that is not very effective in data
    def clear_HPrice(self):
        """what did i do?
            i just iterate prices from HPrice function and to find out whether the point i is extremum or not,
             i check if (i - (i-1) * ((i+1) -i)
             if it was negative, then it was an extremum."""
        data = self.HPrice()
        result = [data.iloc[0]]
        for i in range(1, data.shape[0]-1):
            if (data['price'][i] - data['price'][i-1]) * (data['price'][i+1] - data['price'][i]) < 0:
                result.append(data.iloc[i])
        result.append(data.iloc[-1])

        return pd.DataFrame(result, columns = ['date' , 'price', 'volume']).reset_index().drop(['index'], axis=1)