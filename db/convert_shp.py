import shapefile
import pygeoif
import pandas as pd

if __name__ == '__main__':
	r = shapefile.Reader("../../hex/hex")

	x = []

	for s in r.shapes():
		g=[]
		
		g.append(pygeoif.geometry.as_shape(s)) 

		x.append(pygeoif.MultiPolygon(g))

	df = pd.DataFrame([m.wkt for m in x], columns=['geo'])
	df.index += 1
	df.to_csv('hex.csv', header=True, index_label='id')