import sys
import efinance as ef

def _download_one_stock(beg, end, stock):
    return ef.stock.get_quote_history(stock[0], beg=beg, end=end)

def _download_and_save(beg, end, stocks):
    for stock in stocks:
        print(stock)
        x = _download_one_stock(beg, end, stock)
        x.to_csv(stock[1] + ".csv")
        print(x)
    return

def _get_all_stocks():
    x = ef.stock.get_realtime_quotes()
    return x[x.columns[:2]].to_numpy().tolist()

def _main(beg, end, stock):
    if stock == None:
        stock = _get_all_stocks()
    else:
        stock = [(stock, stock)]

    _download_and_save(beg, end, stock)
    return


if __name__ == "__main__":

    _beg = "20170101"
    _end = "20300101"
    _stock = None

    if len(sys.argv) == 2:
        _beg = sys.argv[1]

    if len(sys.argv) == 3:
        _beg = sys.argv[1]
        _end = sys.argv[2]

    if len(sys.argv) == 4:
        _beg = sys.argv[1]
        _end = sys.argv[2]
        _stock = sys.argv[3]

    _main(_beg, _end, _stock)
