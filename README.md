# Service Update

Automatiza o download, extração e inferência de modelos YOLO em AWS S3, além de reenvio dos resultados.

## Sumário
- [Visão Geral](#visão-geral)  
- [Funcionalidades](#funcionalidades)  
- [Pré-requisitos](#pré-requisitos)  
- [Instalação](#instalação)  
- [Uso](#uso)  
- [Roadmap](#roadmap)  

## Visão Geral
O `service_update.py` é um utilitário em Python que:
1. Baixa artefatos (ZIP/TAR) de um bucket S3.  
2. Extrai os arquivos localmente.  
3. Executa inferência em lote com um modelo YOLO.  
4. Compacta e envia os resultados de volta para o S3.  

## Funcionalidades
- Suporte a formatos ZIP, TAR e TAR.GZ.  
- Logging detalhado (nível INFO).  
- Tratamento de erros de credenciais AWS via `botocore.exceptions`.  
- PyInstaller-ready (instruções inclusas nos comentários).  

## Pré-requisitos
- Python 
- Dependências: `boto3`, `ultralytics`, `opencv-python`, `pyyaml`

## Instalação
```bash
git clone https://github.com/samirzera/Service-Update.git
cd repositorio clonado
