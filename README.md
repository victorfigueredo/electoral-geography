# Electoral-Geography

Electoral-Geography is a repository for analyzing electoral data, focusing on vote distribution across municipalities. It calculates the Gini concentration index and dominance metrics to study vote patterns and candidate performance within each municipality, offering valuable insights for researchers and political analysts.

## Authors and Acknowledgement

This code was developed in 2023 as part of the research required for a graduate degree in Political Science at the University of Brasília, under the guidance of Assistant Professor Arnaldo Mauerberg Jr., PhD.

**Developer/Researcher:**
- Victor Figueredo ([150047479@aluno.unb.br](mailto:150047479@aluno.unb.br))

**Supervisor:**
- Arnaldo Mauerberg Jr., PhD ([arnaldo.mauerberg@unb.br](mailto:arnaldo.mauerberg@unb.br))

## Obtaining CSV Data from TSE Website

To obtain the necessary CSV data from the Tribunal Superior Eleitoral (TSE) website, follow the steps below:

1. Visit the TSE Election Results page: [Resultado da Eleição ](https://sig.tse.jus.br/ords/dwapr/r/seai/sig-eleicao-resultados/resultado-da-elei%C3%A7%C3%A3o?p0_sit_totalizacao=&session=9722158968605).
2. Select the appropriate filters based on the desired dataset. For the given filename votacao_candidato-municipio_deputado_federal_2018_sp_eleito, some relevant filters are:
    - `Ano da Eleição`: Choose the election year (e.g., 2018).
    - `Cargo`: Select the political office (e.g., Deputado Federal).
    - `UF`: Choose the state (e.g., São Paulo).
    - `Situação totalização`: Select the situation (e.g., Eleito).
    - `Abrangência`: Select the scope (e.g., Município).
3. Click on the "Consultar" button.
4. Once the results are displayed, click on the "Exportar Dados" button and choose "CSV" as the format.
5. Download the generated CSV file and save it to your local machine.


# Installation

Follow these steps to set up the project:

1. Clone the repository:

    ```
    git clone https://github.com/victorfigueredo/electoral-geography.git
    cd electoral-geography
    ```

2. Create a virtual environment (optional but recommended):

    For Unix or MacOS, run:

    ```
    python3 -m venv env
    ```

    For Windows, run:

    ```
    py -m venv env
    ```

3. Activate the virtual environment:

    For Unix or MacOS, run:

    ```
    source env/bin/activate
    ```

    For Windows, run:

    ```
    .\env\Scripts\activate
    ```

4. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```


## Usage

After obtaining the CSV data, execute the following command:

```shell
python main.py votacao_candidato-municipio_deputado_federal_2022_sp.csv
```

Replace votacao_candidato-municipio_deputado_federal_2022_sp.csv with the path to your downloaded CSV file. The file name should match the TSE output format.

This script will calculate the Gini concentration index and dominance metrics for each municipality, based on the provided CSV data, and will identify city mentions in the Twitter data. Ensure that the Twitter data for the relevant year and federal unit is placed in the appropriate directory, as mentioned in the script.