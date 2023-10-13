import folium
from folium import plugins

with open('airport.json', 'r', encoding='utf8') as f:
    null = None
    airport_dict = f.read()
    
    # airport_dict = f.readlines()
    airport_dict = eval(airport_dict)
    # print(
# print(airport_dict)
lat, lon = 37.504811111562, 127.025492036104
# 줌 크기
zoom_size = 12
# 구글 지도 타일 설정
tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
attr = "Google"

m = folium.Map(
    location=[lat, lon],
    zoom_start=zoom_size,
    tiles=tiles,
    attr=attr,
    overlay=True,
    disable_3d=True
)
points = []
print(airport_dict['trail'])
for i in airport_dict['trail']:
    points.append([i['lat'], i['lng']])

# folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(m)
plugins.AntPath(
    locations=points, reverse="True", dash_array=[20, 30]
).add_to(m)
m.save('mmt.html')
