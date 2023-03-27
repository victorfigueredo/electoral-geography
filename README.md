# Electoral-Geography
Electoral-Geography is a repository for analyzing electoral data, focusing on vote distribution across municipalities. It calculates the Gini concentration index and dominance metrics to study vote patterns and candidate performance within each municipality, offering valuable insights for researchers and political analysts.

## Obtaining CSV Data from TSE Website

To obtain the necessary CSV data from the Tribunal Superior Eleitoral (TSE) website, follow the steps below:
1. Visit the TSE Election Results page: [Resultado da Eleição ](https://sig.tse.jus.br/ords/dwapr/seai/r/sig-eleicao-resultados/resultado-da-elei%C3%A7%C3%A3o?p0_sit_totalizacao=Eleito&session=6493818457117)
2. Select the appropriate filters based on the desired dataset. For the given filename votacao_candidato-municipio_deputado_federal_2018_sp_eleito, some relevant filters are:
-- `Ano da Eleição`: Choose the election year (e.g., 2018).
-- `Cargo`: Select the political office (e.g., Deputado Federal).
-- `UF`: Choose the state (e.g., São Paulo).
-- `Situação totalização`: Select the situation (e.g., Eleito).
3. Click on the "Consultar" button.
4. Once the results are displayed, click on the "Exportar Dados" button and choose "CSV" as the format.
5. Download the generated CSV file and save it to your local machine.

## Usage
After obtaining the CSV data, update the relevant file paths and filters in the provided code to match the downloaded data, and execute the script to calculate the Gini concentration index and dominance metrics for each municipality.
