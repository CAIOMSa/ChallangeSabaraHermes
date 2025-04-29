from services import DiagnosticosService
import pandas as pd
import numpy as np
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

base = DiagnosticosService.coleta_base_ML()

df = pd.DataFrame(base)
def extrair_pressao(valor):
    if isinstance(valor, str):
        match = re.match(r"(\d+)[xX/](\d+)", valor)
        if match:
            return int(match.group(1)), int(match.group(2))
    return None, None

df['pressao_sistolica'], df['pressao_diastolica'] = zip(*df['pressao'].map(extrair_pressao))

def limpar_valor(val):
    if isinstance(val, str):
        val = val.replace('%', '').replace('°C', '').replace(',', '.')
        try:
            return float(val)
        except:
            return np.nan
    return val

df['saturacaosangue'] = df['saturacaosangue'].map(limpar_valor)
df['temperatura'] = df['temperatura'].map(limpar_valor)

campos_numericos = ['peso', 'saturacaosangue', 'temperatura', 'pressao_sistolica', 'pressao_diastolica']
df[campos_numericos] = df[campos_numericos].astype(float).fillna(0)

def tratar_cdi(valor):
    if isinstance(valor, list):
        return valor
    return []

df['cdi'] = df['idcdi'].apply(tratar_cdi)

def compor_texto(row):
    return (
        (row['relatoriopessoal'] or "") * 3 + " " +
        (row['observacoesmedicas'] or "") * 3 + " " +
        (row['obsmedica'] or "") * 2 + " " +
        (row['condicoesmedpreexistentes'] or "") + " " +
        (row['historicomedfamiliar'] or "") + " " +
        (row['medicacoesemuso'] or "") + " " +
        (row['restricoes'] or "") + " " +
        (row['examesrealizados'] or "")
    )

df['texto'] = df.apply(compor_texto, axis=1)

tfidf = TfidfVectorizer(max_features=1000)
X_text = tfidf.fit_transform(df['texto'])

X_cdi = np.array(df['cdi'].tolist())
if X_cdi.shape[1] == 0:
    X_cdi = np.zeros((len(df), 1))

scaler = StandardScaler()
X_num = scaler.fit_transform(df[campos_numericos])

X = np.hstack((X_num, X_text.toarray(), X_cdi))
y = df['doenca']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

text_matrix = tfidf.transform(df['texto'])

def prever_doenca(json_input, idcdi_val=None):
    pressao_s, pressao_d = extrair_pressao(json_input.get('pressao', '0x0'))
    saturacao = limpar_valor(json_input.get('saturacaosangue', '0'))
    temperatura = limpar_valor(json_input.get('temperatura', '0'))

    dados_numericos = np.array([[
        json_input.get('peso', 0),
        saturacao,
        temperatura,
        pressao_s or 0,
        pressao_d or 0
    ]])
    dados_numericos = scaler.transform(dados_numericos)

    texto = (
        json_input.get('relatoriopessoal', '') * 3 + " " +
        json_input.get('observacoesmedicas', '') * 3 + " " +
        json_input.get('obsmedica', '') * 2 + " " +
        json_input.get('condicoesmedpreexistentes', '') + " " +
        json_input.get('historicomedfamiliar', '') + " " +
        json_input.get('medicacoesemuso', '') + " " +
        json_input.get('restricoes', '') + " " +
        json_input.get('examesrealizados', '')
    )

    texto_tfidf = tfidf.transform([texto])

    cdi_input = np.array(idcdi_val or [0]).reshape(1, -1)
    if cdi_input.shape[1] != X_cdi.shape[1]:
        cdi_input = np.zeros((1, X_cdi.shape[1]))  # normalizar forma

    vetor_input = np.hstack((dados_numericos, texto_tfidf.toarray(), cdi_input))

    probs = clf.predict_proba(vetor_input)[0]
    classes = clf.classes_
    top3 = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]

    similaridade = cosine_similarity(texto_tfidf, text_matrix).flatten()
    indices_similares = similaridade.argsort()[-3:][::-1]
    similares = df.iloc[indices_similares][['doenca', 'medicacao', 'examesrealizados']].to_dict(orient='records')

    return {
        "previsoes": [{"doenca": d, "probabilidade": round(p, 4)} for d, p in top3],
        "explicacao": f"O modelo encontrou padrões fortemente associados às doenças no topo da lista. Foram analisados sintomas, medicamentos em uso e relatórios clínicos.",
        "casos_similares": similares
    }