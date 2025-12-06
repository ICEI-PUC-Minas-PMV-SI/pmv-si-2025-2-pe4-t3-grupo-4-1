# Metodologia

## Encontros

Junto à ONG, os encontros são realizados de maneira remota, com a representante direta da instituição, Mariana, com uma frequência mínima de 15 em 15 dias. Para poder ser entendido as necessidades da Voluntários da Alegria. A partir desses encontros, é possível tomar decisões de maneira mais assertiva de como funcionará o sistema para que atenda as necessidades da melhor maneira possível.
<img width="568" height="319" alt="figura-2" src="https://github.com/user-attachments/assets/61d02060-7ba8-4cff-8a29-8aaee0a1f30b" />

## Recursos tecnológicos da ONG

A ONG Voluntários da Alegria não faz uso de nenhum recurso tecnológico próprio, eles não têm uma rede centralizada e os voluntários usam recursos tecnológicos pessoais para realizar as atividades na ONG.

## Arquitetura Organizacional

Conforme o levantamento realizado junto à ONG, a organização não possui uma infraestrutura de hardware própria ou centralizada, e as atividades são realizadas com os recursos tecnológicos pessoais dos voluntários. Quanto aos softwares, a ONG utiliza um conjunto de ferramentas baseadas em nuvem para gerenciar suas operações e dados. A arquitetura de software atual é composta pelas seguintes soluções:
* Planilhas Google: Utilizado como ferramenta para o controle financeiro interno. As planilhas do Google são empregadas para registrar e detalhar as movimentações financeiras, permitindo uma melhor análise entre os membros da equipe.
* Notion: Funciona como a plataforma de transparência pública da organização. Nele, os dados financeiros, já consolidados a partir do Google Planilhas, são apresentados de forma acessível para a comunidade, doadores e apoiadores.
* Google Drive: Empregado como repositório para o armazenamento de diversos tipos de arquivos. A plataforma é utilizada para guardar documentos, como termos de voluntariado e de direito de imagem, além de registros históricos, incluindo planilhas financeiras antigas e fotos das ações.
* Google Forms: É a ferramenta utilizada para a captação de dados. Seus usos incluem o mapeamento de adesão para ações específicas, inscrições de novos voluntários, pedido de camiseta da ONG.

## Arquitetura do Sistema Proposto
ARQUITETURA DO SISTEMA
A arquitetura do sistema tem como objetivo centralizar a gestão de informações da ONG Voluntários da Alegria, unificando dados de campanhas, ações, voluntários e doações em uma plataforma web e integrada ao Power BI.
1. Camada de Entrada de Dados (Frontend)
Desenvolvida em Django Template (HTML, CSS, JS);
Interface web responsiva e intuitiva;
Funcionalidades: cadastro, consulta, edição e exclusão de campanhas, ações, voluntários e doações;
2. Camada de Processamento e Integração (Backend/API)
Implementada em Python com o framework Django (Django REST Framework).
Utiliza API RESTful para comunicação entre o frontend, o banco de dados e o Power BI.
Autenticação JWT (JSON Web Token) para controle de acesso e segurança.
Endpoints CRUD e endpoints específicos para relatórios consolidados, consumidos pelo Power BI.
Respostas em formato JSON, seguindo padrão REST e comunicação via HTTPS.
3. Camada de Persistência de Dados (Banco de Dados)
Utiliza o SQLite como Sistema Gerenciador de Banco de Dados (SGBD).
Estrutura relacional com tabelas de campanhas, ações, voluntários, doações e usuários.
Garantia de integridade, consistência e segurança das informações.
4. Camada Analítica (Power BI)
O Power BI consome os dados da API via token de serviço autenticado.
Exibe dashboards com métricas consolidadas (valor arrecadado, taxa de adesão, engajamento etc.).
Atualização automática a partir dos dados reais do sistema.
5. Camada de Acesso e Segurança
Perfis de acesso: Administrador e Voluntário.
Criptografia de dados sensíveis e conformidade com a LGPD.
Controle de permissões e autenticação baseada em JWT.
6. Benefícios da Arquitetura Proposta
Centralização e integridade dos dados.
Transparência nas ações e campanhas.
Integração direta com o Power BI.
Segurança e escalabilidade para futuras expansões.




# INTEGRAÇÃO DE DADOS E PROCESSO DE ETL
Nesta etapa foi implementado o processo de integração de dados entre o sistema web desenvolvido em Django e a camada analítica construída no Power BI, responsável por consolidar as informações operacionais da ONG Voluntários da Alegria.
O objetivo central foi garantir que os dados cadastrados no sistema — como campanhas, ações, doações, despesas e beneficiários — fossem automaticamente coletados, transformados e disponibilizados em formato padronizado, servindo como base para a análise gerencial e a tomada de decisão estratégica da instituição.
O processo de ETL (Extração, Transformação e Carga) foi planejado para atuar de forma automatizada, permitindo que as informações sejam extraídas periodicamente do banco de dados SQLite, tratadas para garantir anonimização e consistência, e armazenadas em um formato pronto para consumo pelo Power BI.
Dessa forma, a ONG passa a dispor de uma fonte única de verdade (Single Source of Truth), unindo dados financeiros e operacionais em uma visão consolidada.

## PROCESSO DE ETL
### Extração
A extração dos dados é realizada diretamente do banco SQLite, utilizado pelo sistema Django. Foram definidas queries específicas para cada entidade principal do sistema:
Campanhas (Campaign): nome, categoria, valor-meta, valor arrecadado e datas.


Ações (Action): título, categoria, participantes e período de realização.
Doações (Donation): valor, método de pagamento e campanha relacionada.
Despesas (Expense): valor, data de pagamento e campanha relacionada.
Beneficiários (Beneficiary): nome da entidade e tipo de grupo atendido.
A extração é feita através de um job automático, configurado com o pacote django-crontab, que executa a função export_data_to_csv no intervalo definido (atualmente a cada 30 segundos em ambiente de teste).

### Transformação
Durante o processo de transformação, os dados passam por tratamento e anonimização antes de serem gravados. As principais transformações aplicadas incluem:
Anonimização de dados sensíveis: remoção ou substituição de nomes, e-mails e identificadores diretos de usuários e doadores.
Normalização de campos: padronização de datas, categorias e formatos monetários.
Cálculo de indicadores derivados, como:
Progresso de arrecadação (% da meta atingida);
Total de participantes por ação;
Valor total de doações e despesas por campanha;
Quantidade de beneficiários atendidos.
Essas transformações garantem integridade, consistência e conformidade com a LGPD (Lei nº 13.709/2018).


### Carga
Após o tratamento, os dados consolidados são salvos em um único arquivo CSV unificado, gerado automaticamente no diretório do projeto. O arquivo contém todas as informações integradas, organizadas em colunas padronizadas e prontas para importação no Power BI. Cada execução do job substitui o arquivo anterior, garantindo que o Power BI sempre acesse os dados mais recentes.


### Plataformas do sistema
Aqui disponibilizamos o acesso às plataformas do Power BI e o sistema que a ONG utilizará no seu dia a dia.

[Power BI](https://app.powerbi.com/view?r=eyJrIjoiYjdlYjJmMjQtZWU3Yi00NWIyLTg2MjktYzViODA5ZWE0OGIzIiwidCI6IjE0Y2JkNWE3LWVjOTQtNDZiYS1iMzE0LWNjMGZjOTcyYTE2MSIsImMiOjh9)
[Site institucional](https://voluntarios.darvinlabs.com/)
[Painel administrativo](https://voluntarios.darvinlabs.com/admin/login/?next=/admin/)
