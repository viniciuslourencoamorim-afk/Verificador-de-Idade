# Verificador de Idade

Projeto com aplicativo desktop em Python/CustomTkinter e uma versao web estatica.

## Aplicativo desktop

```powershell
python -m pip install -r requirements.txt
python main.py
```

O aplicativo desktop salva os cadastros em `dados_salvos.json`, ao lado do script. O arquivo e ignorado pelo Git para proteger dados pessoais.

## Pagina web

Os arquivos do site ficam em `site/`. O GitHub Actions publica automaticamente a pagina quando ha alteracoes em `site/` na branch `main`.

URL: https://viniciuslourencoamorim-afk.github.io/Verificador-de-Idade/

Na versao web, os cadastros ficam no `localStorage` do navegador atual. Eles nao sao compartilhados entre dispositivos nem enviados ao GitHub.

Repositorio: https://github.com/viniciuslourencoamorim-afk/Verificador-de-Idade
