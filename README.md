# Analise Visual e Anonimizacao de Imagens no Azure

o projeto foi reposicionado para um laboratorio seguro de deteccao de rostos, extracao de metadados da imagem e anonimizacao com blur.

## O que o projeto entrega

- API REST para analise de imagem
- deteccao local de rostos
- anonimizacao de rostos com blur
- metadados visuais como dimensoes, brilho medio e cores dominantes
- exemplos de uso com `curl`
- testes automatizados
- Dockerfile para execucao local

## Por que mudei o foco

O titulo original apontava para reconhecimento facial, mas esse caminho cruza riscos importantes de privacidade e biometria. Para deixar o repositorio mais forte, util e responsavel, foquei em um caso de uso seguro:

- transformar imagens em dados nao sensiveis
- proteger rostos em vez de identificar pessoas
- mostrar pipeline de visao computacional aplicavel a moderacao, LGPD e pre-processamento

## Endpoints

### `GET /health`

Retorna o status da API.

### `POST /api/images/analyze`

Recebe uma imagem e retorna:

- dimensoes
- brilho medio
- cores dominantes
- quantidade de rostos detectados
- bounding boxes

### `POST /api/images/anonymize`

Recebe uma imagem, aplica blur nos rostos detectados e devolve um PNG anonimizado.

## Como executar localmente

### Com Python

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Com Docker

```bash
docker build -t safe-vision-analysis .
docker run -p 8000:8000 safe-vision-analysis
```

## Exemplos

Veja:

- [curl-analyze.txt](examples/curl-analyze.txt)
- [curl-anonymize.txt](examples/curl-anonymize.txt)

## Estrutura do projeto

- `app/main.py`: endpoints da API
- `app/vision_service.py`: deteccao de rostos, analise visual e anonimizacao
- `app/models.py`: contratos de resposta
- `tests/test_vision_api.py`: testes do fluxo principal
- `docs/responsible-ai.md`: escopo seguro e limites do projeto

## Relacao com Azure

O nome do repositorio menciona Azure ML, mas para esse tipo de fluxo o ecossistema mais natural hoje fica em torno de servicos de visao do Azure. Este MVP local serve como base de portfolio para:

- pre-processamento antes de pipelines de ML
- moderacao e privacidade de imagens
- enriquecimento visual antes de armazenamento ou busca
- integracao futura com servicos gerenciados do Azure

## Referencias oficiais

Usei como base documentacao oficial da Microsoft sobre Azure AI Vision e Azure Face:

- [Azure AI Vision documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)
- [Image Analysis overview](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis)
- [Azure Face service overview](https://learn.microsoft.com/en-us/azure/ai-services/face/overview-identity)

Observacao: a documentacao oficial destaca que o Azure Face tem acesso limitado baseado em criterios de elegibilidade e uso. Por isso, este projeto deliberadamente fica no campo de deteccao e anonimizacao, sem identificacao de pessoas.

## Validacao

```bash
pytest
```

Os testes cobrem:

- analise de imagem com rosto detectado
- retorno de PNG anonimizado
- analise sem rostos

## Proximos passos

- adicionar upload em lote
- salvar relatorio JSON por imagem
- incluir redacao de texto visivel em documentos
- criar interface web simples para preview antes/depois
