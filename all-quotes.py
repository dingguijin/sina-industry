import efinance as ef

x = ef.stock.get_realtime_quotes()
x.to_csv("quotes.csv")
