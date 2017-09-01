# RFM-analysis

RFM analysis is a simple python script (and IPython notebook) to perform RFM analysis from customer purchase history data. 
[Please read the blog post on RFM analysis](https://joaocorreia.io/blog/rfm-analysis-increase-sales-by-segmenting-your-customers.html), it includes instructions on how to make RFM analysis actionable and a ready to use Tableau dashboard.

## Usage:

```bash
$ python RFM-analysis.py -i sample-orders.csv -o rfm-segments.csv -d "2014-04-01"
```

- orders file (-i sample-orders.csv)
- output file with the RFM segmentation (-o rfm-segmenta.csv)
- maximum date of your orders table (-d “YYYY-mm-dd”).
