# Metodologia

## Encontros

Junto à ONG, os encontros são realizados de maneira remota, com a representante direta da instituição, Mariana, com uma frequência mínima de 15 em 15 dias. Para poder ser entendido as necessidades da Voluntários da Alegria. A partir desses encontros, é possível tomar decisões de maneira mais assertiva de como funcionará o sistema para que atenda as necessidades da melhor maneira possível.

## Recursos tecnológicos da ONG

A ONG Voluntários da Alegria não faz uso de nenhum recurso tecnológico próprio, eles não têm uma rede centralizada e os voluntários usam recursos tecnológicos pessoais para realizar as atividades na ONG.

## Arquitetura Organizacional

Conforme o levantamento realizado junto à ONG, a organização não possui uma infraestrutura de hardware própria ou centralizada, e as atividades são realizadas com os recursos tecnológicos pessoais dos voluntários. Quanto aos softwares, a ONG utiliza um conjunto de ferramentas baseadas em nuvem para gerenciar suas operações e dados. A arquitetura de software atual é composta pelas seguintes soluções:
* Planilhas Google: Utilizado como ferramenta para o controle financeiro interno. As planilhas do Google são empregadas para registrar e detalhar as movimentações financeiras, permitindo uma melhor análise entre os membros da equipe.
* Notion: Funciona como a plataforma de transparência pública da organização. Nele, os dados financeiros, já consolidados a partir do Google Planilhas, são apresentados de forma acessível para a comunidade, doadores e apoiadores.
* Google Drive: Empregado como repositório para o armazenamento de diversos tipos de arquivos. A plataforma é utilizada para guardar documentos, como termos de voluntariado e de direito de imagem, além de registros históricos, incluindo planilhas financeiras antigas e fotos das ações.
* Google Forms: É a ferramenta utilizada para a captação de dados. Seus usos incluem o mapeamento de adesão para ações específicas, inscrições de novos voluntários, pedido de camiseta da ONG.

## Arquitetura do Sistema Proposto
A arquitetura proposta tem como objetivo centralizar a gestão de informações da ONG Voluntários da Alegria em um sistema web próprio, que servirá como base confiável para a alimentação de dados sobre ações, campanhas, voluntários e doações. Esse sistema funcionará como fonte única de verdade (Single Source of Truth), permitindo a integração com o Power BI, que consumirá essas informações para gerar relatórios e dashboards interativos.

### 1. Camada de Entrada de Dados (Sistema Web da ONG)
A aplicação será responsável por:
* Cadastro, edição, consulta e exclusão de campanhas, ações, voluntários e colaboradores.
* Registro de doações financeiras e materiais.
* Disponibilização de formulários públicos para inscrição de voluntários e recebimento de doações (com QR Code ou chave Pix).
* Geração de logs de atividades para auditoria e maior transparência.
O sistema será desenvolvido como uma aplicação web responsiva, acessível a partir de computadores e dispositivos móveis, garantindo facilidade de uso para gestores e voluntários.

### 2. Camada de Persistência de Dados (Banco de Dados Relacional)
Todas as informações do sistema serão armazenadas em um banco de dados relacional, estruturado em tabelas que representarão as entidades principais:
* Campanhas (objetivo, período, valores arrecadados, taxa de sucesso).
* Ações (tipo, participantes, impacto).
* Voluntários (dados cadastrais, histórico de participação).
* Doações (financeiras e materiais, vinculadas a campanhas/ações).
Essa camada garante integridade, consistência e segurança dos dados, além de possibilitar integrações futuras.

### 3. Camada de Processamento e Integração
O sistema web disponibilizará uma API REST que permitirá:
* Consumo dos dados pelo Power BI para geração de dashboards.
* Gerenciamento de informações através de cadastro, leitura, atualização e remoção (CRUD).
* Criação de endpoints específicos para relatórios consolidados, facilitando a análise no Power BI sem necessidade de transformação manual.

### 4. Camada Analítica (Power BI)
O Power BI será conectado diretamente à API do sistema, garantindo que os dados utilizados para relatórios estejam sempre atualizados. Entre as principais funcionalidades:
* Dashboards para análise de arrecadações e comparação entre frentes de atuação.
* Indicadores de desempenho de campanhas e ações (taxa de adesão, popularidade, arrecadação recorrente).
* Segmentações por período, causa e tipo de doação.
* Exportação e compartilhamento de relatórios para gestores, voluntários e apoiadores.

### 5. Camada de Acesso e Segurança
A arquitetura prevê diferentes níveis de acesso:
* Administradores: acesso completo a cadastros, relatórios e configurações.
* Membros voluntários: acesso restrito a campanhas/ações em que atuam.
* Público externo: acesso apenas a relatórios de transparência e páginas públicas de inscrição/doação.
A segurança será garantida por:
* Autenticação com JWT.
* Criptografia de dados sensíveis, em conformidade com a LGPD.
* Controle de permissões por perfil.

### 6. Benefícios da Arquitetura Proposta
* Centralização: todos os dados da ONG ficam em um único sistema.
* Facilidade no cadastro de dados, posto que mais voluntários terão acesso ao registro de informações relevantes para a atuação da ONG.
* Integração nativa com Power BI, garantindo dashboards dinâmicos e confiáveis.
* Maior transparência: dados abertos ao público, fortalecendo a credibilidade.
* Escalabilidade: possibilidade de expansão para novas métricas, módulos ou integrações.
* Segurança e conformidade: proteção de dados sensíveis e aderência à LGPD.

## Métricas

As métricas do sistema são cálculos feitos a partir dos dados disponibilizados do sistema, para o melhor acompanhamento das atividades, campanhas e ações, realizadas pela ONG, durante um período de tempo. Essas métricas serão disponibilizadas no painel de amostragem de dados no sistema.

* ### LISTAGEM DAS MÉTRICAS
* Número total de doações por campanha
* Número total de doadores das campanhas
* Valor total arrecadado pelas campanhas, num período de tempo
* Número total de objetos doados e seu valor total estimado
* Valor total de dinheiro arrecadado por campanha
* Valor total de dinheiro arrecadado nas campanhas durante um período de tempo
* Valor total do dinheiro gasto por campanha
* Valor total do dinheiro gasto por ação
* Valor total do dinheiro gasto com as atividades num período de tempo
* Valor total do dinheiro gasto por frente, animal, meio ambiente, crianças e idosos
* Valor total arrecadado por frente, animal, meio ambiente, crianças e idosos, nas campanhas
* Quantidade de atividades realizadas por frente, animal, meio ambiente, crianças e idosos, categorizada por campanha e ações
* Quantidade total de campanhas que não atenderam a meta de doações a serem atingidas
* Quantidade total de campanhas que tiveram as metas bem sucedidas
* Quantidade total de pessoas impactadas pelas ações no sistema
* Quantidade total de grupo beneficiado no sistema
* Quantidade total de voluntários que marcaram presença nas açòes
* Quantidade total de voluntários inscritos nas atividades, ações e campanhas, no sistema



## Projeto do Data Warehouse/ Data Mart
TODO

## Integração de Fontes de Dados
TODO
