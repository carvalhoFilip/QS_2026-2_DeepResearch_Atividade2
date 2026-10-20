#!/usr/bin/env python3
"""
Validador de Saída Estruturada e Verificação de Fontes
Atividade 2 - Qualidade de Software 2026.2 - Equipe 06 (DeepResearch)
Responsável: Daniel José Silva Trindade
"""

import json
import re
import sys
import urllib.request
import urllib.error
from jsonschema import validate, ValidationError

# Definição formal do JSON Schema adotado para o DeepResearch
SCHEMA_SAIDA_ESTRUTURADA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "DeepResearchStructuredOutput",
    "description": "Contrato de saída estruturada para agente de pesquisa com rastreabilidade de fontes.",
    "type": "object",
    "required": [
        "resposta_resumo",
        "evidencia_suficiente",
        "conflito_detectado",
        "afirmacoes",
        "fontes_consultadas"
    ],
    "properties": {
        "resposta_resumo": {
            "type": "string",
            "minLength": 10,
            "description": "Síntese textual consolidada da resposta."
        },
        "evidencia_suficiente": {
            "type": "boolean",
            "description": "Flag indicando se as evidências foram suficientes para responder sem incerteza."
        },
        "conflito_detectado": {
            "type": "boolean",
            "description": "Flag indicando se houve contradição entre fontes recuperadas."
        },
        "fontes_consultadas": {
            "type": "array",
            "items": {"type": "string", "format": "uri"},
            "minItems": 1,
            "description": "Lista de URLs consultadas durante o processo de pesquisa."
        },
        "afirmacoes": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "texto", "fonte_url", "trecho_apoio"],
                "properties": {
                    "id": {"type": "string", "pattern": "^AF-[0-9]{2,}$"},
                    "texto": {"type": "string", "minLength": 5},
                    "fonte_url": {"type": "string", "format": "uri"},
                    "trecho_apoio": {"type": "string", "minLength": 5},
                    "grau_certeza": {
                        "type": "string",
                        "enum": ["alto", "medio", "baixo"]
                    }
                }
            }
        }
    }
}

def validar_sintaxe_json(conteudo_texto):
    """Verifica se a entrada é um JSON sintaticamente válido."""
    try:
        dados = json.loads(conteudo_texto)
        return True, dados, "JSON sintaticamente válido."
    except json.JSONDecodeError as e:
        return False, None, f"Erro de sintaxe JSON: {e.msg} (linha {e.lineno}, coluna {e.colno})"

def validar_esquema(dados):
    """Verifica se os dados obedecem ao JSON Schema."""
    try:
        validate(instance=dados, schema=SCHEMA_SAIDA_ESTRUTURADA)
        return True, "Estrutura e campos em conformidade com o esquema."
    except ValidationError as e:
        campo = ".".join([str(p) for p in e.absolute_path]) or "raiz"
        return False, f"Falha de validação de esquema no campo '{campo}': {e.message}"

def verificar_url(url, timeout=5):
    """Verifica se a URL possui formato válido e é acessível via HTTP/HTTPS."""
    url_regex = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}))'
        r'(:[0-9]{1,5})?'
        r'(/.*)?$', re.IGNORECASE
    )
    if not url_regex.match(url):
        return False, f"URL com formato inválido: {url}"
    
    # Testa conectividade com User-Agent padrão
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) DeepResearchValidator/1.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status in [200, 301, 302]:
                return True, f"URL acessível (HTTP {response.status})"
            return False, f"URL retornou status HTTP {response.status}"
    except urllib.error.HTTPError as e:
        return False, f"Erro HTTP ao acessar URL: {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return False, f"Falha de conexão / host não resolvido: {e.reason}"
    except Exception as e:
        return False, f"Erro genérico na validação de URL: {str(e)}"

def verificar_sustentacao(afirmacao, mock_conteudo_fonte=None):
    """
    Verifica se a fonte sustenta a afirmação conferindo a presença do trecho de apoio.
    Se mock_conteudo_fonte for fornecido, compara diretamente com ele.
    """
    url = afirmacao.get("fonte_url")
    trecho = afirmacao.get("trecho_apoio", "").strip()
    texto_afirmacao = afirmacao.get("texto", "").strip()
    
    if not trecho:
        return "não sustentada", "Ausência de trecho de apoio na afirmação."
    
    if mock_conteudo_fonte is not None:
        conteudo = mock_conteudo_fonte
    else:
        # Tenta obter o conteúdo da URL
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 DeepResearchValidator/1.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                conteudo = response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return "não sustentada", f"Não foi possível recuperar a página para checagem: {str(e)}"

    # Checa se o trecho de apoio exato ou suas palavras-chave constam no documento
    trecho_normalizado = " ".join(trecho.lower().split())
    conteudo_normalizado = " ".join(conteudo.lower().split())
    
    if trecho_normalizado in conteudo_normalizado:
        return "sustentada", f"Trecho de apoio verificado no texto da fonte '{url}'."
    else:
        # Checagem de correspondência parcial
        palavras_trecho = set(trecho_normalizado.split())
        palavras_presentes = [p for p in palavras_trecho if p in conteudo_normalizado]
        if len(palavras_presentes) / max(1, len(palavras_trecho)) > 0.7:
            return "parcialmente sustentada", "Trecho não coincide exatamente, mas maior parte das palavras-chave foi localizada."
        return "não sustentada", f"Trecho de apoio '{trecho}' NÃO foi encontrado no conteúdo da fonte."

def pipeline_validacao_completa(conteudo_texto, mock_conteudo=None):
    """Executa o pipeline completo de validação."""
    relatorio = {
        "sintaxe_json": False,
        "esquema_valido": False,
        "urls_validas": True,
        "sustentacao": [],
        "veredito_geral": "REJEITADO",
        "detalhes": []
    }
    
    # 1. Checagem sintática
    ok_sintaxe, dados, msg_sintaxe = validar_sintaxe_json(conteudo_texto)
    relatorio["detalhes"].append(msg_sintaxe)
    if not ok_sintaxe:
        return relatorio
    relatorio["sintaxe_json"] = True
    
    # 2. Checagem de esquema
    ok_esquema, msg_esquema = validar_esquema(dados)
    relatorio["detalhes"].append(msg_esquema)
    if not ok_esquema:
        return relatorio
    relatorio["esquema_valido"] = True
    
    # 3. Checagem de URLs e Sustentação das afirmações
    todas_urls_ok = True
    todas_sustentadas = True
    
    for af in dados.get("afirmacoes", []):
        url = af.get("fonte_url")
        # Se for teste com URL falsa específica para teste offline, checamos regex/resolução
        ok_url, msg_url = verificar_url(url)
        relatorio["detalhes"].append(f"[{af.get('id')}] URL '{url}': {msg_url}")
        if not ok_url:
            todas_urls_ok = False
            
        veredito, msg_sust = verificar_sustentacao(af, mock_conteudo_fonte=mock_conteudo)
        relatorio["sustentacao"].append({
            "id": af.get("id"),
            "veredito": veredito,
            "motivo": msg_sust
        })
        if veredito != "sustentada":
            todas_sustentadas = False
            
    relatorio["urls_validas"] = todas_urls_ok
    
    if relatorio["sintaxe_json"] and relatorio["esquema_valido"] and relatorio["urls_validas"] and todas_sustentadas:
        relatorio["veredito_geral"] = "APROVADO"
    elif not relatorio["urls_validas"]:
        relatorio["veredito_geral"] = "REJEITADO_URL_INVALIDA"
    elif not todas_sustentadas:
        relatorio["veredito_geral"] = "ALERTA_SUSTENTACAO_FALHA"
    else:
        relatorio["veredito_geral"] = "REJEITADO_ESQUEMA"
        
    return relatorio

if __name__ == "__main__":
    print("Módulo de validação de saída estruturada carregado com sucesso.")
