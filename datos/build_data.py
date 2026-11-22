# Genera datos.js a partir de datos/hoja.py.  Uso: python3 datos/build_data.py
import json, os, sys
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import hoja as H
G = {'male': 'Hombre', 'female': 'Mujer', 'unknown': 'Desconocido'}
R = {'Región Autónoma del Atlántico Norte': 'RACCN', 'Región Autónoma del Atlántico Sur': 'RACCS', 'Unknown': 'Desconocido'}
reg = lambda x: R.get(x, x.replace(' Department', ''))
PLAT = {'facebook': 'Facebook', 'instagram': 'Instagram', 'whatsapp': 'WhatsApp', 'threads': 'Threads'}
out = dict(marcas=[])
for nombre, m in H.MARCAS.items():
    diario = [dict(fecha=f, alcance=int(a), impresiones=int(i), interacciones=int(e), costo=float(c), clics=int(k)) for f, a, i, e, c, k in (l.split() for l in m['diario'].strip().split('\n'))]
    cre = []
    for line in m['cre'].strip().split('\n'):
        f, rest = line.split('|')
        for it in rest.split(';'):
            n, p, a, i, e = it.split(); cre.append(dict(fecha=f, anuncio=n, plataforma=PLAT[p], alcance=int(a), impresiones=int(i), interacciones=int(e)))
    aud = [dict(dimension='Género', segmento=G[k], valor=v) for k, v in m['gen']] + [dict(dimension='Edad', segmento=k, valor=v) for k, v in m['edad']] + [dict(dimension='Región', segmento=reg(k), valor=v) for k, v in m['reg']]
    out['marcas'].append(dict(marca=nombre, campana=m['campana'], alcance=m['alcance'], frecuencia=m['frecuencia'], cpm=m['cpm'], diario=diario, creativos=cre, audiencia=aud))
out['actualizado'] = max(d['fecha'] for m in out['marcas'] for d in m['diario'])
open(os.path.join(D0, '..', 'datos.js'), 'w', encoding='utf-8').write('window.DG_DATA = ' + json.dumps(out, ensure_ascii=False) + ';\n')
print({m['marca']: (len(m['diario']), len(m['creativos'])) for m in out['marcas']})
