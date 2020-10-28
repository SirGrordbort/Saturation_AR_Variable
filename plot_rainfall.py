import iris

iwv = iris.load('single_lvl_data.nc', 'tcwv')[0]
u_ivt = iris.load('single_lvl_data.nc', 'p71.162')[0]  # Eastward IVT
v_ivt = iris.load('single_lvl_data.nc', 'p72.162')[0]  # Northward IVT
norm_ivt = iris.load('mycube.nc')
rainfall = iris.load('single_lvl_data.nc', 'tp')[0]

extracted_iwv = iwv.extract(iris.Constraint(latitude=lambda cell: 0 < cell < 100))
extracted_norm_ivt = norm_ivt.extract(iris.Constraint(latitude=lambda cell: 41.49 < cell < 45.1, longitude=lambda cell: 172.24 < cell < 172.26))
extracted_rainfall = rainfall.extract(iris.Constraint(latitude=lambda cell: 41.49 < cell < 45.1, longitude=lambda cell: 172.24 < cell < 172.26))
print("loaded data")