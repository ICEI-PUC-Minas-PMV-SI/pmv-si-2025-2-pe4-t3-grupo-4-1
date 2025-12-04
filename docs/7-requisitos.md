# REQUISITOS

## Requisitos funcionais
* RF01: O sistema deve permitir o cadastro, consulta, edição e exclusão dos usuários administradores e voluntários.
* RF02: O sistema deve permitir o cadastro, consulta, edição e exclusão das campanhas pelos usuários do sistema.
* RF03: O sistema deve permitir o cadastro, consulta, edição e exclusão das ações pelos usuários do sistema
* RF04: O sistema deve permitir o cadastro, consulta, edição e exclusão das doações pelos usuários do sistema.
* RF05: O sistema deverá coletar e processar os dados relacionados às campanhas e ações cadastradas, gerando métricas quantitativas e qualitativas que auxiliem na análise de resultados e na tomada de decisão:
  * Métricas de Campanhas:
    * Número total de doações: Soma de todas as doações associadas à campanha.
      * Fórmula: Total de Doações = Σ(doações vinculadas à campanha)
    * Valor arrecadado: Soma do valor monetário total das doações recebidas.
      * Fórmula: Valor Arrecadado = Σ(valor de cada doação)
    * Meta atingida (%): Porcentagem do valor arrecadado em relação à meta definida.
      * Fórmula: Meta Atingida (%) = (Valor Arrecadado / Meta da Campanha) × 100.

  * Métricas de Ações (eventos, atividades, mutirões, etc.):
    * Proporção de Ações Bem-Sucedidas:
      * Percentual de ações que atingiram seus objetivos em relação ao total de ações realizadas.
        * Fórmula: Ações Bem-Sucedidas (%) = (Ações que atingiram os objetivos / Total de Ações) × 100
    * Distribuição de Ações por Categoria:
      * Percentual de ações realizadas em cada categoria (animais, meio ambiente, crianças, idosos, etc.) em relação ao total.
        * Fórmula: Distribuição por Categoria (%) = (Ações da Categoria / Total de Ações) × 100
  Média de Voluntários Participantes por Ação: Número médio de voluntários que participam das ações realizadas pela ONG.
  Fórmula: Média de Voluntários = Total de Participações de Voluntários / Total de Ações
* RF06: O sistema deve restringir o acesso às funcionalidades conforme o perfil do usuário.
* RF07: O sistema deve disponibilizar uma interface pública de visualização de resultados, acessível sem autenticação, contendo apenas dados consolidados e anonimizados sobre as campanhas e ações, em conformidade com a LGPD (Lei nº 13.709/2018).

## Requisitos não funcionais
* RNF01: A interface deve ser responsiva e acessível em computadores, com layout adaptável a diferentes tamanhos de tela.
* RNF02: O sistema deve implementar autenticação segura, utilizando padrões como OAuth2, JWT ou similar.
* RNF03: O sistema deve ser compatível com os principais navegadores modernos (Chrome, Firefox, Edge, Safari).
* RNF04: O sistema deve garantir que dados pessoais sejam armazenados de forma criptografada, em conformidade com a LGPD.
* RNF05: O sistema deve ter um tempo de resposta menor que 500 ms para garantir performance adequada.
* RNF06: O sistema deve garantir uma disponibilidade mínima de 99%, exceto em períodos programados de manutenção.